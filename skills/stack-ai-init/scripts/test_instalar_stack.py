#!/usr/bin/env python3
"""Testes de instalar_stack.py."""

import contextlib
import io
import json
import os
import shutil
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import instalar_stack as inst  # noqa: E402

SETTINGS_CARGA = {
    "chat.useAgentsMdFile": True,
    "chat.useNestedAgentsMdFiles": False,
    "chat.agentSkillsLocations": {".agents/skills": True, ".claude/skills": False},
    "chat.promptFilesRecommendations": {"speckit.plan": True},
}

# O destino de teste chama-se "destino", entao o nome derivado e este.
MARKETPLACE = "stack-ai-destino"
PLACEHOLDER = inst.PLACEHOLDER_MARKETPLACE

CLAUDE_SETTINGS_CARGA = {
    "extraKnownMarketplaces": {PLACEHOLDER: {"source": {"source": "directory", "path": "."}}},
    "enabledPlugins": {f"stack-ai@{PLACEHOLDER}": True},
}

CLAUDE_SETTINGS_RENDERIZADO = {
    "extraKnownMarketplaces": {MARKETPLACE: {"source": {"source": "directory", "path": "."}}},
    "enabledPlugins": {f"stack-ai@{MARKETPLACE}": True},
}

MARKETPLACE_CARGA = {
    "name": PLACEHOLDER,
    "owner": {"name": "Equipe do repositorio"},
    "plugins": [{"name": "stack-ai", "source": "./.agents", "version": "1.0.0"}],
}

MARKETPLACE_RENDERIZADO = dict(MARKETPLACE_CARGA, name=MARKETPLACE)

GITIGNORE_CARGA = "# Claude Code\n.claude/settings.local.json\n\n.specify/feature.json\n/specs\n"


def escrever(caminho: Path, conteudo: str = "conteudo\n") -> Path:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho


class Base(unittest.TestCase):
    """Carga util sintetica, para nao depender do tamanho da carga real."""

    def setUp(self):
        raiz = Path(tempfile.mkdtemp(prefix="stack-init-teste-"))
        self.addCleanup(shutil.rmtree, raiz, ignore_errors=True)
        self.destino = raiz / "destino"
        self.destino.mkdir()

        self.carga = raiz / "assets" / "stack"
        self.estrutura = raiz / "assets" / "estrutura.json"
        escrever(self.carga / "AGENTS.md", "# Regras\n")
        escrever(self.carga / "CLAUDE.md", "@AGENTS.md\n")
        escrever(self.carga / "README.md", "# Stack\n")
        escrever(self.carga / "dot-gitignore", GITIGNORE_CARGA)
        escrever(self.carga / "dot-agents" / "skills" / "README.md", "# Catalogo\n")
        escrever(self.carga / "dot-agents" / "skills" / "skill-creator" / "SKILL.md", "# skill-creator\n")
        escrever(self.carga / "dot-claude" / "skills" / "speckit-plan" / "SKILL.md", "# plan\n")
        escrever(self.carga / "dot-vscode" / "settings.json", json.dumps(SETTINGS_CARGA, indent=4) + "\n")
        escrever(self.carga / "dot-claude" / "settings.json", json.dumps(CLAUDE_SETTINGS_CARGA, indent=4) + "\n")
        escrever(self.carga / "dot-claude-plugin" / "marketplace.json", json.dumps(MARKETPLACE_CARGA, indent=4) + "\n")
        script = escrever(self.carga / "dot-specify" / "scripts" / "bash" / "common.sh", "#!/bin/sh\n")
        script.chmod(0o755)
        self.estrutura.write_text(json.dumps({
            "diretorios_vazios": [".claude/commands", ".specify/references"],
            "symlinks": [{"caminho": ".claude/skills/skill-creator", "alvo": "../../.agents/skills/skill-creator"}],
        }), encoding="utf-8")

        for nome, valor in (("CARGA", self.carga), ("ESTRUTURA", self.estrutura)):
            remendo = mock.patch.object(inst, nome, valor)
            remendo.start()
            self.addCleanup(remendo.stop)

    def instalar(self, sobrescrever=False):
        return inst.instalar(self.destino, sobrescrever, aplicar=True)

    def acao_de(self, acoes, caminho):
        return next(a["acao"] for a in acoes if a["caminho"] == caminho)


class TesteMapeamentoDeNome(unittest.TestCase):
    def test_ida_e_volta(self):
        for rel in (".claude/skills/x/SKILL.md", ".gitignore", ".opencode/.gitignore", "AGENTS.md"):
            self.assertEqual(inst.caminho_no_destino(inst.caminho_na_carga(rel)), rel)

    def test_apenas_o_ponto_inicial_do_componente(self):
        self.assertEqual(inst.caminho_na_carga(".opencode/.gitignore"), "dot-opencode/dot-gitignore")
        self.assertEqual(inst.caminho_na_carga(".specify/memory/.constitution-template.json"),
                         "dot-specify/memory/dot-constitution-template.json")
        self.assertEqual(inst.caminho_na_carga("speckit.plan.md"), "speckit.plan.md")


class TesteInstalacaoLimpa(Base):
    def test_todos_os_arquivos_da_carga_chegam_iguais(self):
        """Byte a byte, exceto os dois que recebem o nome do marketplace."""
        acoes = self.instalar()
        for rel, fonte in inst.arquivos_da_carga().items():
            alvo = self.destino / rel
            self.assertTrue(alvo.is_file(), rel)
            rendido = inst.texto_da_carga(rel, fonte, inst.nome_do_marketplace(self.destino))
            self.assertEqual(inst.hash_arquivo(alvo), inst.hash_da_carga(fonte, rendido), rel)
        self.assertFalse([a for a in acoes if a["acao"] == "erro"])

    def test_so_os_arquivos_declarados_sofrem_substituicao(self):
        for rel, fonte in inst.arquivos_da_carga().items():
            rendido = inst.texto_da_carga(rel, fonte, inst.nome_do_marketplace(self.destino))
            if rel in inst.SUBSTITUIVEIS:
                self.assertIsNotNone(rendido, rel)
            else:
                self.assertIsNone(rendido, rel)

    def test_preserva_bit_de_execucao(self):
        self.instalar()
        modo = stat.S_IMODE((self.destino / ".specify/scripts/bash/common.sh").stat().st_mode)
        self.assertEqual(modo, 0o755)

    def test_cria_diretorios_vazios_declarados(self):
        self.instalar()
        self.assertTrue((self.destino / ".claude/commands").is_dir())
        self.assertTrue((self.destino / ".specify/references").is_dir())

    def test_cria_symlink_com_alvo_relativo_que_resolve(self):
        self.instalar()
        link = self.destino / ".claude/skills/skill-creator"
        self.assertTrue(link.is_symlink())
        self.assertEqual(os.readlink(link), "../../.agents/skills/skill-creator")
        self.assertTrue((link / "SKILL.md").is_file())

    def test_simular_nao_escreve(self):
        inst.instalar(self.destino, False, aplicar=False)
        self.assertEqual(list(self.destino.iterdir()), [])

    def test_simular_e_instalar_planejam_o_mesmo(self):
        simulado = [(a["caminho"], a["acao"]) for a in inst.instalar(self.destino, False, aplicar=False)]
        aplicado = [(a["caminho"], a["acao"]) for a in self.instalar()]
        self.assertEqual(simulado, aplicado)

    def test_segunda_rodada_nao_tem_pendencia(self):
        self.instalar()
        acoes = self.instalar()
        self.assertFalse([a for a in acoes if a["acao"] not in inst.LIMPAS])


class TesteColisao(Base):
    def test_arquivo_diferente_e_preservado_por_padrao(self):
        alvo = escrever(self.destino / ".claude/skills/speckit-plan/SKILL.md", "editado pelo time\n")
        acoes = self.instalar()
        self.assertEqual(alvo.read_text(encoding="utf-8"), "editado pelo time\n")
        self.assertEqual(self.acao_de(acoes, ".claude/skills/speckit-plan/SKILL.md"), "ignorado-existe")

    def test_sobrescrever_atualiza_arquivo_da_stack(self):
        alvo = escrever(self.destino / ".claude/skills/speckit-plan/SKILL.md", "versao antiga\n")
        acoes = self.instalar(sobrescrever=True)
        self.assertEqual(alvo.read_text(encoding="utf-8"), "# plan\n")
        self.assertEqual(self.acao_de(acoes, ".claude/skills/speckit-plan/SKILL.md"), "substituido")

    def test_arquivo_identico_nao_conta_como_pendencia(self):
        self.instalar()
        acoes = self.instalar()
        self.assertEqual(self.acao_de(acoes, ".claude/skills/speckit-plan/SKILL.md"), "ignorado-igual")


class TesteArquivosProtegidos(Base):
    def test_instalados_quando_ausentes(self):
        acoes = self.instalar()
        for rel in inst.PROTEGIDOS:
            self.assertEqual(self.acao_de(acoes, rel), "criado")

    def test_nunca_substituidos_nem_com_sobrescrever(self):
        escrever(self.destino / "AGENTS.md", "# Regras do time\n")
        escrever(self.destino / "README.md", "# Projeto\n")
        acoes = self.instalar(sobrescrever=True)
        self.assertEqual((self.destino / "AGENTS.md").read_text(encoding="utf-8"), "# Regras do time\n")
        self.assertEqual((self.destino / "README.md").read_text(encoding="utf-8"), "# Projeto\n")
        self.assertEqual(self.acao_de(acoes, "AGENTS.md"), "ignorado-protegido")

    def test_iguais_a_carga_nao_viram_pendencia(self):
        self.instalar()
        acoes = self.instalar()
        self.assertEqual(self.acao_de(acoes, "AGENTS.md"), "ignorado-igual")


class TesteMesclagemDeGitignore(Base):
    def test_criado_quando_ausente(self):
        self.instalar()
        self.assertEqual((self.destino / ".gitignore").read_text(encoding="utf-8"), GITIGNORE_CARGA)

    def test_acrescenta_so_o_que_falta_e_preserva_o_destino(self):
        escrever(self.destino / ".gitignore", "vendor/\n.specify/feature.json\n")
        acoes = self.instalar()
        texto = (self.destino / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("vendor/", texto)
        self.assertEqual(texto.count(".specify/feature.json"), 1)
        self.assertIn(".claude/settings.local.json", texto)
        self.assertIn(inst.CABECALHO_GITIGNORE, texto)
        self.assertEqual(self.acao_de(acoes, ".gitignore"), "mesclado")

    def test_idempotente(self):
        escrever(self.destino / ".gitignore", "vendor/\n")
        self.instalar()
        primeiro = (self.destino / ".gitignore").read_text(encoding="utf-8")
        acoes = self.instalar()
        self.assertEqual((self.destino / ".gitignore").read_text(encoding="utf-8"), primeiro)
        self.assertEqual(self.acao_de(acoes, ".gitignore"), "ignorado-igual")


class TesteRegraDeSpecs(Base):
    """A stack nao decide sozinha ignorar `specs/` de quem ja versiona a pasta."""

    def ler(self):
        return (self.destino / ".gitignore").read_text(encoding="utf-8")

    def test_destino_sem_specs_recebe_a_linha(self):
        escrever(self.destino / ".gitignore", "vendor/\n")
        self.instalar()
        self.assertIn("/specs", self.ler())

    def test_destino_com_specs_nao_recebe_a_linha(self):
        escrever(self.destino / ".gitignore", "vendor/\n")
        (self.destino / "specs").mkdir()
        self.instalar()
        self.assertNotIn("/specs", self.ler())

    def test_o_resto_da_carga_entra_mesmo_com_specs(self):
        escrever(self.destino / ".gitignore", "vendor/\n")
        (self.destino / "specs").mkdir()
        self.instalar()
        self.assertIn(".claude/settings.local.json", self.ler())
        self.assertIn(".specify/feature.json", self.ler())


class TesteMesclagemDeSettings(Base):
    def ler(self):
        return json.loads((self.destino / ".vscode/settings.json").read_text(encoding="utf-8"))

    def test_criado_quando_ausente(self):
        self.instalar()
        self.assertEqual(self.ler(), SETTINGS_CARGA)

    def test_preserva_valor_ja_definido_e_acrescenta_o_resto(self):
        escrever(self.destino / ".vscode/settings.json", json.dumps({
            "editor.tabSize": 2,
            "chat.useAgentsMdFile": False,
            "chat.agentSkillsLocations": {".github/skills": True},
        }, indent=4))
        acoes = self.instalar()
        dados = self.ler()
        self.assertEqual(dados["editor.tabSize"], 2)
        self.assertFalse(dados["chat.useAgentsMdFile"])
        self.assertTrue(dados["chat.agentSkillsLocations"][".github/skills"])
        self.assertTrue(dados["chat.agentSkillsLocations"][".agents/skills"])
        self.assertIn("chat.promptFilesRecommendations", dados)
        self.assertEqual(self.acao_de(acoes, ".vscode/settings.json"), "mesclado")

    def test_json_nao_estrito_nao_e_tocado(self):
        bruto = '{\n    // comentario do time\n    "editor.tabSize": 2,\n}\n'
        escrever(self.destino / ".vscode/settings.json", bruto)
        acoes = self.instalar()
        self.assertEqual((self.destino / ".vscode/settings.json").read_text(encoding="utf-8"), bruto)
        self.assertEqual(self.acao_de(acoes, ".vscode/settings.json"), "manual")

    def test_idempotente(self):
        escrever(self.destino / ".vscode/settings.json", json.dumps({"editor.tabSize": 2}, indent=4))
        self.instalar()
        primeiro = (self.destino / ".vscode/settings.json").read_text(encoding="utf-8")
        acoes = self.instalar()
        self.assertEqual((self.destino / ".vscode/settings.json").read_text(encoding="utf-8"), primeiro)
        self.assertEqual(self.acao_de(acoes, ".vscode/settings.json"), "ignorado-igual")


class TesteMesclagemDeSettingsDoClaude(Base):
    def ler(self):
        return json.loads((self.destino / ".claude/settings.json").read_text(encoding="utf-8"))

    def test_criado_quando_ausente(self):
        self.instalar()
        self.assertEqual(self.ler(), CLAUDE_SETTINGS_RENDERIZADO)

    def test_marketplace_recebe_o_nome_derivado_do_destino(self):
        self.instalar()
        bruto = (self.destino / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
        self.assertNotIn(PLACEHOLDER, bruto)
        self.assertEqual(json.loads(bruto), MARKETPLACE_RENDERIZADO)

    def test_settings_nao_deixa_placeholder(self):
        self.instalar()
        bruto = (self.destino / ".claude/settings.json").read_text(encoding="utf-8")
        self.assertNotIn(PLACEHOLDER, bruto)

    def test_arquivos_substituidos_sao_idempotentes(self):
        self.instalar()
        acoes = self.instalar()
        self.assertEqual(self.acao_de(acoes, ".claude-plugin/marketplace.json"), "ignorado-igual")
        self.assertEqual(self.acao_de(acoes, ".claude/settings.json"), "ignorado-igual")

    def test_verificar_nao_acusa_divergencia_no_marketplace(self):
        self.instalar()
        itens = inst.verificar(self.destino)
        por_caminho = {i["caminho"]: i["acao"] for i in itens}
        self.assertEqual(por_caminho[".claude-plugin/marketplace.json"], "igual")
        self.assertEqual(por_caminho[".claude/settings.json"], "igual")

    def test_preserva_o_do_time_e_acrescenta_o_da_stack(self):
        escrever(self.destino / ".claude/settings.json", json.dumps({
            "extraKnownMarketplaces": {"outro": {"source": {"source": "directory", "path": "./outro"}}},
            "enabledPlugins": {"outro@outro": True},
        }, indent=4))
        acoes = self.instalar()
        dados = self.ler()
        self.assertIn("outro", dados["extraKnownMarketplaces"])
        self.assertIn(MARKETPLACE, dados["extraKnownMarketplaces"])
        self.assertTrue(dados["enabledPlugins"]["outro@outro"])
        self.assertTrue(dados["enabledPlugins"][f"stack-ai@{MARKETPLACE}"])
        self.assertEqual(self.acao_de(acoes, ".claude/settings.json"), "mesclado")

    def test_valor_ja_definido_pelo_time_nao_muda(self):
        escrever(self.destino / ".claude/settings.json", json.dumps({
            "enabledPlugins": {f"stack-ai@{MARKETPLACE}": False},
        }, indent=4))
        self.instalar()
        self.assertFalse(self.ler()["enabledPlugins"][f"stack-ai@{MARKETPLACE}"])

    def test_idempotente(self):
        escrever(self.destino / ".claude/settings.json", json.dumps({"permissions": {"allow": []}}, indent=4))
        self.instalar()
        primeiro = (self.destino / ".claude/settings.json").read_text(encoding="utf-8")
        acoes = self.instalar()
        self.assertEqual((self.destino / ".claude/settings.json").read_text(encoding="utf-8"), primeiro)
        self.assertEqual(self.acao_de(acoes, ".claude/settings.json"), "ignorado-igual")


class TesteNomeDoMarketplace(unittest.TestCase):
    def test_deriva_do_nome_do_diretorio(self):
        self.assertEqual(inst.nome_do_marketplace(Path("/x/sei-sdd")), "stack-ai-sei-sdd")
        self.assertEqual(inst.nome_do_marketplace(Path("/x/sdta")), "stack-ai-sdta")

    def test_reduz_caracteres_fora_de_a_z0_9(self):
        self.assertEqual(inst.nome_do_marketplace(Path("/x/Meu Repo!")), "stack-ai-meu-repo")
        self.assertEqual(inst.nome_do_marketplace(Path("/x/.oculto")), "stack-ai-oculto")

    def test_sem_nome_utilizavel_cai_no_padrao(self):
        self.assertEqual(inst.nome_do_marketplace(Path("/")), "stack-ai-repo")


class TesteNomeJaDeclaradoPeloDestino(unittest.TestCase):
    """O nome derivado e so o padrao de criacao: destino que ja tem o seu mantem."""

    def setUp(self):
        raiz = Path(tempfile.mkdtemp(prefix="stack-init-nome-"))
        self.addCleanup(shutil.rmtree, raiz, ignore_errors=True)
        self.destino = raiz / "destino"
        self.destino.mkdir()

    def test_sem_declaracao_nenhuma_usa_o_derivado(self):
        self.assertIsNone(inst.nome_ja_declarado(self.destino))
        self.assertEqual(inst.nome_do_marketplace(self.destino), "stack-ai-destino")

    def test_marketplace_json_manda(self):
        escrever(self.destino / ".claude-plugin/marketplace.json",
                 json.dumps(dict(MARKETPLACE_CARGA, name="stack-ai-outro-nome")))
        self.assertEqual(inst.nome_do_marketplace(self.destino), "stack-ai-outro-nome")

    def test_settings_entra_como_reserva(self):
        escrever(self.destino / ".claude/settings.json",
                 json.dumps({"enabledPlugins": {"stack-ai@stack-ai-legado": True}}))
        self.assertEqual(inst.nome_do_marketplace(self.destino), "stack-ai-legado")

    def test_marketplace_de_outro_plugin_nao_e_adotado(self):
        escrever(self.destino / ".claude/settings.json", json.dumps({
            "extraKnownMarketplaces": {"outro": {"source": {"source": "directory", "path": "./outro"}}},
            "enabledPlugins": {"outro@outro": True},
        }))
        self.assertIsNone(inst.nome_ja_declarado(self.destino))
        self.assertEqual(inst.nome_do_marketplace(self.destino), "stack-ai-destino")

    def test_placeholder_cru_nao_e_adotado(self):
        escrever(self.destino / ".claude-plugin/marketplace.json",
                 json.dumps(dict(MARKETPLACE_CARGA, name=PLACEHOLDER)))
        self.assertEqual(inst.nome_do_marketplace(self.destino), "stack-ai-destino")

    def test_json_quebrado_nao_derruba_a_resolucao(self):
        escrever(self.destino / ".claude-plugin/marketplace.json", "{ nao e json,")
        self.assertEqual(inst.nome_do_marketplace(self.destino), "stack-ai-destino")


class TesteInstalacaoComNomeJaDeclarado(Base):
    """Destino com nome proprio nao ganha um segundo marketplace ao lado."""

    OUTRO = "stack-ai-nome-da-pasta-de-trabalho"

    def declarar(self):
        escrever(self.destino / ".claude-plugin/marketplace.json",
                 json.dumps(dict(MARKETPLACE_CARGA, name=self.OUTRO), indent=4) + "\n")
        escrever(self.destino / ".claude/settings.json", json.dumps({
            "extraKnownMarketplaces": {self.OUTRO: {"source": {"source": "directory", "path": "."}}},
            "enabledPlugins": {f"stack-ai@{self.OUTRO}": True},
        }, indent=4) + "\n")

    def test_settings_nao_ganha_chave_duplicada(self):
        self.declarar()
        acoes = self.instalar()
        dados = json.loads((self.destino / ".claude/settings.json").read_text(encoding="utf-8"))
        self.assertEqual(list(dados["extraKnownMarketplaces"]), [self.OUTRO])
        self.assertEqual(list(dados["enabledPlugins"]), [f"stack-ai@{self.OUTRO}"])
        self.assertEqual(self.acao_de(acoes, ".claude/settings.json"), "ignorado-igual")

    def test_marketplace_json_do_destino_nao_e_divergencia(self):
        self.declarar()
        acoes = self.instalar()
        self.assertEqual(self.acao_de(acoes, ".claude-plugin/marketplace.json"), "ignorado-igual")
        self.assertEqual(
            json.loads((self.destino / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))["name"],
            self.OUTRO)

    def test_verificar_sai_limpo(self):
        self.declarar()
        self.instalar()
        por_caminho = {i["caminho"]: i["acao"] for i in inst.verificar(self.destino)}
        self.assertEqual(por_caminho[".claude-plugin/marketplace.json"], "igual")
        self.assertEqual(por_caminho[".claude/settings.json"], "igual")

    def test_so_o_marketplace_json_ja_basta(self):
        """settings.json ausente recebe o nome que o marketplace.json declara."""
        escrever(self.destino / ".claude-plugin/marketplace.json",
                 json.dumps(dict(MARKETPLACE_CARGA, name=self.OUTRO), indent=4) + "\n")
        self.instalar()
        dados = json.loads((self.destino / ".claude/settings.json").read_text(encoding="utf-8"))
        self.assertEqual(list(dados["extraKnownMarketplaces"]), [self.OUTRO])
        self.assertEqual(list(dados["enabledPlugins"]), [f"stack-ai@{self.OUTRO}"])


class TesteSymlink(Base):
    def test_alvo_diferente_nao_e_tocado(self):
        link = self.destino / ".claude/skills/skill-creator"
        link.parent.mkdir(parents=True)
        os.symlink("../outro-lugar", link)
        acoes = self.instalar()
        self.assertEqual(os.readlink(link), "../outro-lugar")
        self.assertEqual(self.acao_de(acoes, ".claude/skills/skill-creator"), "ignorado-existe")

    def test_diretorio_real_no_lugar_nao_e_tocado(self):
        escrever(self.destino / ".claude/skills/skill-creator/SKILL.md", "copia local\n")
        acoes = self.instalar()
        self.assertEqual(self.acao_de(acoes, ".claude/skills/skill-creator"), "ignorado-existe")
        self.assertFalse((self.destino / ".claude/skills/skill-creator").is_symlink())

    def test_fallback_para_copia_quando_symlink_falha(self):
        with mock.patch.object(inst.os, "symlink", side_effect=OSError(1, "sem privilegio")):
            acoes = self.instalar()
        alvo = self.destino / ".claude/skills/skill-creator"
        self.assertFalse(alvo.is_symlink())
        self.assertTrue((alvo / "SKILL.md").is_file())
        self.assertEqual(self.acao_de(acoes, ".claude/skills/skill-creator"), "symlink-degradado")


class TesteVerificar(Base):
    def test_instalacao_recem_feita_esta_igual(self):
        self.instalar()
        itens = inst.verificar(self.destino)
        self.assertFalse([i for i in itens if i["acao"] not in inst.LIMPAS])

    def test_detecta_arquivo_alterado_e_ausente(self):
        self.instalar()
        escrever(self.destino / ".claude/skills/speckit-plan/SKILL.md", "mexeram aqui\n")
        (self.destino / ".agents/skills/skill-creator/SKILL.md").unlink()
        itens = {i["caminho"]: i["acao"] for i in inst.verificar(self.destino)}
        self.assertEqual(itens[".claude/skills/speckit-plan/SKILL.md"], "divergente")
        self.assertEqual(itens[".agents/skills/skill-creator/SKILL.md"], "ausente")

    def test_arquivo_protegido_diferente_nao_e_divergencia(self):
        self.instalar()
        escrever(self.destino / "AGENTS.md", "# Regras do time\n")
        itens = {i["caminho"]: i["acao"] for i in inst.verificar(self.destino)}
        self.assertEqual(itens["AGENTS.md"], "proprio-do-destino")

    def test_nao_escreve_nada(self):
        self.instalar()
        antes = sorted(p.relative_to(self.destino).as_posix() for p in self.destino.rglob("*"))
        inst.verificar(self.destino)
        self.assertEqual(sorted(p.relative_to(self.destino).as_posix() for p in self.destino.rglob("*")), antes)


class TesteLinhaDeComando(Base):
    def rodar(self, argv):
        """Executa main sem despejar o relatorio na saida dos testes."""
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return inst.main(argv)

    def test_destino_inexistente(self):
        self.assertEqual(self.rodar(["instalar", "--destino", str(self.destino / "nao-existe")]), 2)

    def test_recusa_destino_que_hospeda_a_skill(self):
        for destino in (inst.SKILL, inst.SKILL.parents[0], inst.SKILL.parents[1]):
            with self.subTest(destino=str(destino)):
                self.assertEqual(self.rodar(["instalar", "--destino", str(destino)]), 2)

    def test_codigo_zero_em_instalacao_limpa(self):
        self.assertEqual(self.rodar(["instalar", "--destino", str(self.destino)]), 0)

    def test_codigo_um_com_pendencia(self):
        escrever(self.destino / ".claude/skills/speckit-plan/SKILL.md", "editado\n")
        self.assertEqual(self.rodar(["instalar", "--destino", str(self.destino)]), 1)


if __name__ == "__main__":
    unittest.main()
