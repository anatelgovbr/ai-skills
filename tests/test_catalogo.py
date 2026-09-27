"""Testes de integridade estrutural do catalogo de skills."""

import json
import pathlib
import unittest

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DIR_SKILLS = RAIZ / "skills"

SKILLS_ANATEL = {
    "ciclo-design",
    "conformidade-de-escrita-normativa",
    "dicionario-dados-db-scan-codebase-docs",
    "escrita-em-linguagem-simples-pt-br",
    "gauntlet-loop-forge",
    "recapitulacao-resumo-ata-relato-reuniao",
    "stack-ai-build-project-context",
    "stack-ai-init",
    "testes-unitarios-cobertura",
}

DIVIDA_EVALS = {
    "ciclo-design",
    "conformidade-de-escrita-normativa",
    "dicionario-dados-db-scan-codebase-docs",
    "escrita-em-linguagem-simples-pt-br",
    "gauntlet-loop-forge",
    "recapitulacao-resumo-ata-relato-reuniao",
    "stack-ai-build-project-context",
    "stack-ai-init",
}


def _listar_skills():
    if not DIR_SKILLS.is_dir():
        return []
    return sorted(
        d.name for d in DIR_SKILLS.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    )


def _extrair_evals(dados):
    if isinstance(dados, list):
        return dados
    if isinstance(dados, dict) and "evals" in dados:
        return dados["evals"]
    return None


class TestEstruturaSkill(unittest.TestCase):

    def test_toda_skill_tem_skill_md(self):
        for nome in _listar_skills():
            caminho = DIR_SKILLS / nome / "SKILL.md"
            self.assertTrue(
                caminho.exists(),
                f"{nome} nao tem SKILL.md",
            )

    def test_skill_md_nao_esta_vazio(self):
        for nome in _listar_skills():
            caminho = DIR_SKILLS / nome / "SKILL.md"
            self.assertGreater(
                caminho.stat().st_size, 0,
                f"{nome}/SKILL.md esta vazio",
            )


class TestScriptsTemTestes(unittest.TestCase):

    def test_scripts_anatel_tem_test(self):
        for nome in sorted(SKILLS_ANATEL):
            scripts = DIR_SKILLS / nome / "scripts"
            if not scripts.is_dir():
                continue
            producao = [
                f for f in scripts.iterdir()
                if f.suffix == ".py"
                and f.is_file()
                and not f.name.startswith("test_")
            ]
            for script in producao:
                teste = scripts / f"test_{script.name}"
                self.assertTrue(
                    teste.exists(),
                    f"{nome}/scripts/{script.name} nao tem "
                    f"test_{script.name}",
                )


class TestEvalsAnatel(unittest.TestCase):

    def test_anatel_nova_tem_evals(self):
        obrigatorias = SKILLS_ANATEL - DIVIDA_EVALS
        for nome in sorted(obrigatorias):
            caminho = DIR_SKILLS / nome / "evals" / "evals.json"
            self.assertTrue(
                caminho.exists(),
                f"{nome} nao tem evals/evals.json",
            )

    def test_evals_json_valido(self):
        for nome in sorted(SKILLS_ANATEL):
            caminho = DIR_SKILLS / nome / "evals" / "evals.json"
            if not caminho.exists():
                continue
            try:
                dados = json.loads(caminho.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                self.fail(f"{nome}/evals/evals.json invalido: {exc}")
            lista = _extrair_evals(dados)
            self.assertIsNotNone(
                lista,
                f"{nome}/evals/evals.json: formato nao reconhecido",
            )
            self.assertIsInstance(lista, list)
            self.assertGreater(
                len(lista), 0,
                f"{nome}/evals/evals.json nao tem casos",
            )

    def test_divida_so_diminui(self):
        for nome in sorted(DIVIDA_EVALS):
            caminho = DIR_SKILLS / nome / "evals" / "evals.json"
            if caminho.exists():
                self.fail(
                    f"{nome} ja tem evals/evals.json: "
                    f"remova de DIVIDA_EVALS em test_catalogo.py"
                )


class TestCatalogoReadme(unittest.TestCase):

    def test_skills_presentes_no_readme(self):
        readme = (RAIZ / "README.md").read_text(encoding="utf-8")
        for nome in _listar_skills():
            self.assertIn(
                f"`{nome}`",
                readme,
                f"skill {nome} ausente do README.md",
            )


if __name__ == "__main__":
    unittest.main()
