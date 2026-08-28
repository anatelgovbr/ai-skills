#!/usr/bin/env python3
"""Testes de sincronizar_payload.py."""

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

import sincronizar_payload as sinc  # noqa: E402


def escrever(caminho: Path, conteudo: str = "conteudo\n") -> Path:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho


class Base(unittest.TestCase):
    """Origem sintetica com a mesma forma da raiz real da stack."""

    def setUp(self):
        base = Path(tempfile.mkdtemp(prefix="stack-sinc-teste-"))
        self.addCleanup(shutil.rmtree, base, ignore_errors=True)
        self.origem = base / "origem"
        self.carga = base / "assets" / "stack"
        self.estrutura = base / "assets" / "estrutura.json"

        escrever(self.origem / "AGENTS.md", "# Regras\n")
        escrever(self.origem / "CLAUDE.md", "@AGENTS.md\n")
        escrever(self.origem / "README.md", "# Stack\n")
        escrever(self.origem / ".gitignore", "vendor/\n")
        escrever(self.origem / ".agents" / "skills" / "README.md", "# Catalogo\n")
        escrever(self.origem / ".agents" / "skills" / "skill-creator" / "SKILL.md", "# skill-creator\n")
        escrever(self.origem / ".claude" / "skills" / "speckit-plan" / "SKILL.md", "# plan\n")
        escrever(self.origem / ".vscode" / "settings.json", '{"chat.useAgentsMdFile": true}\n')
        escrever(self.origem / ".opencode" / ".gitignore", "node_modules\n")
        script = escrever(self.origem / ".specify" / "scripts" / "bash" / "common.sh", "#!/bin/sh\n")
        script.chmod(0o755)

        # Itens que nunca podem entrar na carga.
        escrever(self.origem / ".git" / "config", "[core]\n")
        escrever(self.origem / "specs" / "rascunho.md", "rascunho\n")
        escrever(self.origem / ".claude" / "settings.local.json", "{}\n")
        escrever(self.origem / ".opencode" / "package.json", "{}\n")
        escrever(self.origem / ".opencode" / "node_modules" / "x" / "index.js", "0\n")
        escrever(self.origem / ".agents" / "skills" / "stack-ai-creator" / "SKILL.md", "# outra\n")
        escrever(self.origem / ".agents" / "skills" / "skill-creator" / "scripts" / "__pycache__" / "x.pyc", "\n")

        # Diretorio vazio e symlink, que so existem em assets/estrutura.json.
        (self.origem / ".claude" / "commands").mkdir(parents=True)
        os.symlink("../../.agents/skills/skill-creator", self.origem / ".claude" / "skills" / "skill-creator")

        for nome, valor in (("CARGA", self.carga), ("ESTRUTURA", self.estrutura)):
            remendo = mock.patch.object(sinc, nome, valor)
            remendo.start()
            self.addCleanup(remendo.stop)

    def rodar(self, argv):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return sinc.main(argv + ["--origem", str(self.origem)])

    def situacoes(self):
        return {i["caminho"]: i["situacao"] for i in sinc.comparar(self.origem)}

    def variantes_manuais(self):
        escrever(self.carga / "dot-vscode" / "settings.json", '{"variante": true}\n')
        escrever(self.carga / "dot-agents" / "skills" / "README.md", "# Catalogo sem a interna\n")
        escrever(self.carga / "README.md", "# Stack instalada\n")
        sinc.aceitar_manuais(self.origem)


class TesteVarredura(Base):
    def test_carga_recebe_os_arquivos_com_nome_dot(self):
        sinc.aplicar(self.origem)
        for rel in ("AGENTS.md", "dot-gitignore", "dot-claude/skills/speckit-plan/SKILL.md",
                    "dot-opencode/dot-gitignore", "dot-agents/skills/skill-creator/SKILL.md"):
            self.assertTrue((self.carga / rel).is_file(), rel)

    def test_exclusoes_nao_entram(self):
        sinc.aplicar(self.origem)
        na_carga = {p.relative_to(self.carga).as_posix() for p in self.carga.rglob("*") if p.is_file()}
        for proibido in ("dot-git/config", "specs/rascunho.md", "dot-claude/settings.local.json",
                         "dot-opencode/package.json", "dot-opencode/node_modules/x/index.js",
                         "dot-agents/skills/stack-ai-creator/SKILL.md",
                         "dot-agents/skills/skill-creator/scripts/__pycache__/x.pyc"):
            self.assertNotIn(proibido, na_carga)

    def test_preserva_bit_de_execucao(self):
        sinc.aplicar(self.origem)
        modo = stat.S_IMODE((self.carga / "dot-specify/scripts/bash/common.sh").stat().st_mode)
        self.assertEqual(modo, 0o755)

    def test_estrutura_registra_vazios_e_symlinks(self):
        sinc.aplicar(self.origem)
        dados = json.loads(self.estrutura.read_text(encoding="utf-8"))
        self.assertEqual(dados["diretorios_vazios"], [".claude/commands"])
        self.assertEqual(dados["symlinks"], [{"caminho": ".claude/skills/skill-creator",
                                              "alvo": "../../.agents/skills/skill-creator"}])

    def test_symlink_nao_vira_arquivo_na_carga(self):
        sinc.aplicar(self.origem)
        self.assertFalse((self.carga / "dot-claude/skills/skill-creator").exists())

    def test_symlink_para_skill_excluida_nao_entra(self):
        """Chegaria quebrado no destino, porque a skill em si nao e distribuida."""
        os.symlink("../../.agents/skills/stack-ai-creator", self.origem / ".claude" / "skills" / "stack-ai-creator")
        sinc.aplicar(self.origem)
        caminhos = {s["caminho"] for s in json.loads(self.estrutura.read_text(encoding="utf-8"))["symlinks"]}
        self.assertEqual(caminhos, {".claude/skills/skill-creator"})

    def test_symlink_para_fora_do_repositorio_nao_entra(self):
        os.symlink("/etc", self.origem / ".claude" / "absoluto")
        os.symlink("../../fora", self.origem / ".claude" / "relativo-para-fora")
        sinc.aplicar(self.origem)
        caminhos = {s["caminho"] for s in json.loads(self.estrutura.read_text(encoding="utf-8"))["symlinks"]}
        self.assertEqual(caminhos, {".claude/skills/skill-creator"})


class TesteDeriva(Base):
    def setUp(self):
        super().setUp()
        sinc.aplicar(self.origem)
        self.variantes_manuais()

    def test_carga_em_dia(self):
        self.assertEqual(sinc.comparar(self.origem), [])

    def test_arquivo_novo_na_origem(self):
        escrever(self.origem / ".claude" / "skills" / "speckit-tasks" / "SKILL.md", "# tasks\n")
        self.assertEqual(self.situacoes()[".claude/skills/speckit-tasks/SKILL.md"], "faltando-na-carga")

    def test_arquivo_removido_da_origem_sobra_na_carga(self):
        (self.origem / ".claude" / "skills" / "speckit-plan" / "SKILL.md").unlink()
        self.assertEqual(self.situacoes()[".claude/skills/speckit-plan/SKILL.md"], "sobrando-na-carga")
        sinc.aplicar(self.origem)
        self.assertFalse((self.carga / "dot-claude/skills/speckit-plan/SKILL.md").exists())

    def test_conteudo_diferente(self):
        escrever(self.origem / "CLAUDE.md", "@OUTRO.md\n")
        self.assertEqual(self.situacoes()["CLAUDE.md"], "conteudo-diferente")
        sinc.aplicar(self.origem)
        self.assertEqual(sinc.comparar(self.origem), [])

    def test_modo_diferente(self):
        (self.origem / ".specify" / "scripts" / "bash" / "common.sh").chmod(0o644)
        self.assertEqual(self.situacoes()[".specify/scripts/bash/common.sh"], "modo-diferente")

    def test_diretorio_vazio_novo(self):
        (self.origem / ".github" / "prompts").mkdir(parents=True)
        self.assertEqual(self.situacoes()["assets/estrutura.json"], "estrutura-diferente")
        sinc.aplicar(self.origem)
        dados = json.loads(self.estrutura.read_text(encoding="utf-8"))
        self.assertIn(".github/prompts", dados["diretorios_vazios"])


class TesteArquivosManuais(Base):
    def test_variante_ausente_e_reportada(self):
        sinc.aplicar(self.origem)
        self.assertEqual(self.situacoes()[".vscode/settings.json"], "faltando-na-carga")

    def test_aplicar_nunca_sobrescreve_a_variante(self):
        sinc.aplicar(self.origem)
        self.variantes_manuais()
        sinc.aplicar(self.origem)
        self.assertEqual((self.carga / "dot-vscode/settings.json").read_text(encoding="utf-8"), '{"variante": true}\n')

    def test_mudanca_na_origem_pede_revisao(self):
        sinc.aplicar(self.origem)
        self.variantes_manuais()
        escrever(self.origem / ".vscode" / "settings.json", '{"chat.useAgentsMdFile": true, "novo": 1}\n')
        self.assertEqual(self.situacoes()[".vscode/settings.json"], "revisar-manualmente")
        self.assertEqual(self.rodar(["aplicar"]), 1)
        sinc.aceitar_manuais(self.origem)
        self.assertEqual(sinc.comparar(self.origem), [])


class TesteLinhaDeComando(Base):
    def test_origem_invalida(self):
        vazio = self.origem.parent / "vazio"
        vazio.mkdir()
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(sinc.main(["verificar", "--origem", str(vazio)]), 2)

    def test_verificar_sinaliza_deriva_e_fica_limpo_depois(self):
        self.assertEqual(self.rodar(["verificar"]), 1)
        self.rodar(["aplicar"])
        self.variantes_manuais()
        self.assertEqual(self.rodar(["verificar"]), 0)


if __name__ == "__main__":
    unittest.main()
