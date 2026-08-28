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

GITIGNORE_CARGA = "# Claude Code\n.claude/settings.local.json\n\n.specify/feature.json\n"


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
        acoes = self.instalar()
        for rel, fonte in inst.arquivos_da_carga().items():
            alvo = self.destino / rel
            self.assertTrue(alvo.is_file(), rel)
            self.assertEqual(inst.hash_arquivo(alvo), inst.hash_arquivo(fonte), rel)
        self.assertFalse([a for a in acoes if a["acao"] == "erro"])

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

    def test_recusa_a_propria_raiz_da_skill(self):
        self.assertEqual(self.rodar(["instalar", "--destino", str(inst.SKILL.parents[2])]), 2)

    def test_codigo_zero_em_instalacao_limpa(self):
        self.assertEqual(self.rodar(["instalar", "--destino", str(self.destino)]), 0)

    def test_codigo_um_com_pendencia(self):
        escrever(self.destino / ".claude/skills/speckit-plan/SKILL.md", "editado\n")
        self.assertEqual(self.rodar(["instalar", "--destino", str(self.destino)]), 1)


if __name__ == "__main__":
    unittest.main()
