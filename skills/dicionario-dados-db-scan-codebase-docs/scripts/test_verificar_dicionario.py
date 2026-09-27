import contextlib
import io
import json
import os
import runpy
import sys
import tempfile
import unittest
from pathlib import Path

import verificar_dicionario as v


DICIONARIO_COLUNAS = """# Dicionário de Dados de Teste - release-2026-A

## Índice de Tabelas

- [schema.tabela-a](#schematabela-a)
- [tabela_á](#tabela_á)

## schema.tabela-a

Armazena algo.

| Tabela | Coluna | Descrição |
|---|---|---|
| schema.tabela-a | chave-principal | Número que identifica o registro. |
| schema.tabela-a | nome.exibicao | Nome exibido. |

## tabela_á

Armazena outra coisa, um domínio composto por:<ul><li>a: primeiro valor</li><li>b: segundo valor</li></ul>

| Tabela | Coluna | Descrição |
|---|---|---|
| tabela_á | id:tabela | Número que identifica a tabela. |
"""

DICIONARIO_TABELAS = """# Dicionário de Dados de Teste - release-2026-A

| Tabela | Descrição |
|---|---|
| schema.tabela-a | Armazena algo. |
| tabela_á | Armazena outra coisa, um domínio composto por:<ul><li>a: primeiro valor</li><li>b: segundo valor</li></ul> |
"""

CHANGELOG_ISOLADO = """# Histórico Estrutural de Teste

## [release-B]

### Adicionado

- **Tabela `tabela_nova`**
"""


def rodar(argv):
    saida = io.StringIO()
    erro = io.StringIO()
    original = sys.argv
    sys.argv = ["verificar_dicionario.py"] + argv
    try:
        with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(erro):
            try:
                v.main()
            except SystemExit as e:
                return e.code, saida.getvalue() + erro.getvalue()
    finally:
        sys.argv = original
    return 0, saida.getvalue() + erro.getvalue()


class FormatoTest(unittest.TestCase):
    def executar(self, texto, nome="dicionario_colunas.md", extra=None):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = Path(tmp, nome)
            caminho.write_text(texto, encoding="utf-8")
            return rodar(["formato", str(caminho)] + (extra or []))

    def test_dicionario_colunas_atual_integro(self):
        codigo, saida = self.executar(DICIONARIO_COLUNAS)
        self.assertEqual(codigo, 0, saida)

    def test_dicionario_tabelas_atual_integro(self):
        codigo, saida = self.executar(DICIONARIO_TABELAS, "dicionario_tabelas.md")
        self.assertEqual(codigo, 0, saida)

    def test_versao_nao_semver_e_aceita(self):
        codigo, saida = self.executar(
            DICIONARIO_TABELAS,
            "dicionario_tabelas.md",
            ["--padrao-versao", r"release-\d{4}-[A-Z]"],
        )
        self.assertEqual(codigo, 0, saida)

    def test_titulo_ausente(self):
        texto = DICIONARIO_COLUNAS.split("\n", 1)[1]
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("titulo", saida)

    def test_versao_ausente_no_titulo(self):
        texto = DICIONARIO_COLUNAS.replace(" - release-2026-A", " - ")
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("versao nao vazia", saida)

    def test_cabecalho_de_colunas_deve_ser_exato(self):
        texto = DICIONARIO_COLUNAS.replace(
            "| Tabela | Coluna | Descrição |", "| Tabela | Campo | Descrição |", 1
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("cabecalho exato", saida)

    def test_cabecalho_de_tabelas_deve_ser_exato(self):
        texto = DICIONARIO_TABELAS.replace("| Tabela | Descrição |", "| Nome | Descrição |")
        codigo, saida = self.executar(texto, "dicionario_tabelas.md")
        self.assertEqual(codigo, 1)
        self.assertIn("cabecalho exato", saida)

    def test_indice_ausente(self):
        texto = DICIONARIO_COLUNAS.replace("## Índice de Tabelas", "## Sumário")
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("indice", saida)

    def test_ancora_incorreta(self):
        texto = DICIONARIO_COLUNAS.replace("#schematabela-a", "#schema.tabela-a")
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("ancora incorreta", saida)

    def test_colisao_de_ancoras_recebe_sufixo(self):
        texto = """# Dicionário de Dados de Teste - R1

## Índice de Tabelas

- [a.b](#ab)
- [ab](#ab-1)

## a.b

Armazena o primeiro conceito.

| Tabela | Coluna | Descrição |
|---|---|---|
| a.b | id-a | Identificador. |

## ab

Armazena o segundo conceito.

| Tabela | Coluna | Descrição |
|---|---|---|
| ab | id-b | Identificador. |
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 0, saida)

    def test_indice_deve_corresponder_as_secoes(self):
        texto = DICIONARIO_COLUNAS.replace("[tabela_á]", "[tabela_errada]")
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("corresponder 1:1", saida)

    def test_descricao_de_secao_vazia(self):
        texto = DICIONARIO_COLUNAS.replace("Armazena algo.", " ", 1)
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("descricao ausente", saida)

    def test_descricao_de_secao_deve_ocupar_uma_linha(self):
        texto = DICIONARIO_COLUNAS.replace(
            "Armazena algo.", "Armazena algo.\nOutra linha.", 1
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("linha em branco obrigatoria depois da descricao", saida)

    def test_descricao_de_coluna_vazia(self):
        texto = DICIONARIO_COLUNAS.replace("| schema.tabela-a | nome.exibicao | Nome exibido. |", "| schema.tabela-a | nome.exibicao | |")
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("descricao vazia", saida)

    def test_descricao_de_tabela_vazia(self):
        texto = DICIONARIO_TABELAS.replace("| schema.tabela-a | Armazena algo. |", "| schema.tabela-a | |")
        codigo, saida = self.executar(texto, "dicionario_tabelas.md")
        self.assertEqual(codigo, 1)
        self.assertIn("descricao vazia", saida)

    def test_coluna_tabela_deve_repetir_identificador_exato(self):
        texto = DICIONARIO_COLUNAS.replace(
            "| tabela_á | id:tabela |", "| tabela_errada | id:tabela |"
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("diverge do cabecalho", saida)

    def test_secoes_fora_de_ordem(self):
        primeiro = DICIONARIO_COLUNAS.index("## schema.tabela-a")
        segundo = DICIONARIO_COLUNAS.index("## tabela_á")
        prefixo = DICIONARIO_COLUNAS[:primeiro]
        bloco_a = DICIONARIO_COLUNAS[primeiro:segundo]
        bloco_b = DICIONARIO_COLUNAS[segundo:]
        texto = prefixo + bloco_b + "\n" + bloco_a
        texto = texto.replace(
            "- [schema.tabela-a](#schematabela-a)\n- [tabela_á](#tabela_á)",
            "- [tabela_á](#tabela_á)\n- [schema.tabela-a](#schematabela-a)",
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("fora de ordem", saida)

    def test_linhas_de_tabelas_fora_de_ordem(self):
        texto = DICIONARIO_TABELAS.replace(
            "| schema.tabela-a | Armazena algo. |\n| tabela_á |",
            "| tabela_á | Armazena outra coisa, um domínio composto por:<ul><li>a: primeiro valor</li><li>b: segundo valor</li></ul> |\n| schema.tabela-a |",
        ).replace(
            "| schema.tabela-a | Armazena outra coisa, um domínio composto por:<ul><li>a: primeiro valor</li><li>b: segundo valor</li></ul> |",
            "| schema.tabela-a | Armazena algo. |",
        )
        codigo, saida = self.executar(texto, "dicionario_tabelas.md")
        self.assertEqual(codigo, 1)
        self.assertIn("fora de ordem", saida)

    def test_identificadores_genericos_sao_aceitos(self):
        self.assertIn("schema.tabela-a", DICIONARIO_COLUNAS)
        codigo, saida = self.executar(DICIONARIO_COLUNAS)
        self.assertEqual(codigo, 0, saida)

    def test_entidade_html_nao_substitui_escape_de_pipe(self):
        modelo = """# Dicionário de Dados de Teste - R1

## Índice de Tabelas

- [tabela&#124;particao](#tabela124particao)

## tabela&#124;particao

Armazena partições.

| Tabela | Coluna | Descrição |
|---|---|---|
| tabela&#124;particao | chave&#124;natural | Identificador. |
"""
        for entidade in ("&#124;", "&#x7c;", "&vert;", "&verbar;", "&VerticalLine;"):
            with self.subTest(entidade=entidade):
                codigo, saida = self.executar(modelo.replace("&#124;", entidade))
                self.assertEqual(codigo, 1, saida)
                self.assertIn("linha", saida)

    def test_duas_barras_nao_substituem_escape_unico_de_pipe(self):
        texto = r"""# Dicionário de Dados de Teste - R1

## Índice de Tabelas

- [tabela\\|particao](#tabelaparticao)

## tabela\\|particao

Armazena partições.

| Tabela | Coluna | Descrição |
|---|---|---|
| tabela\\|particao | chave\\|natural | Identificador. |
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("linha", saida)

    def test_pipe_escapado_com_barra_e_aceito(self):
        texto = r"""# Dicionário de Dados de Teste - R1

## Índice de Tabelas

- [tabela\|particao](#tabelaparticao)

## tabela\|particao

Armazena partições.

| Tabela | Coluna | Descrição |
|---|---|---|
| tabela\|particao | chave\|natural | Identificador. |
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 0, saida)

    def test_pk_declarada_deve_vir_primeiro(self):
        texto = DICIONARIO_COLUNAS.replace(
            "| schema.tabela-a | chave-principal | Número que identifica o registro. |\n"
            "| schema.tabela-a | nome.exibicao | Nome exibido. |",
            "| schema.tabela-a | nome.exibicao | Nome exibido. |\n"
            "| schema.tabela-a | chave-principal | Número que identifica o registro. |",
        )
        codigo, saida = self.executar(
            texto,
            extra=["--checar-ordem", "--padrao-pk", "chave-principal"],
        )
        self.assertEqual(codigo, 1)
        self.assertIn("ORDEM", saida)

    def test_pk_declarada_e_primeira_e_aceita(self):
        codigo, saida = self.executar(
            DICIONARIO_COLUNAS,
            extra=["--checar-ordem", "--padrao-pk", "chave-principal"],
        )
        self.assertEqual(codigo, 0, saida)

    def test_colunas_fora_de_ordem_sem_padrao_pk_avisa_e_reprova(self):
        texto = DICIONARIO_COLUNAS.replace(
            "| schema.tabela-a | chave-principal | Número que identifica o registro. |\n"
            "| schema.tabela-a | nome.exibicao | Nome exibido. |",
            "| schema.tabela-a | nome.exibicao | Nome exibido. |\n"
            "| schema.tabela-a | chave-principal | Número que identifica o registro. |",
        )
        codigo, saida = self.executar(texto, extra=["--checar-ordem"])
        self.assertEqual(codigo, 1)
        self.assertIn("fora de ordem alfabetica", saida)
        self.assertIn("--padrao-pk nao informado", saida)

    def test_regex_invalida_em_padrao_versao_e_rejeitada(self):
        codigo, saida = rodar(
            ["formato", "qualquer.md", "--padrao-versao", "(("]
        )
        self.assertEqual(codigo, 2, saida)
        self.assertIn("regex invalida", saida)

    def test_versao_nao_confere_com_padrao_versao(self):
        codigo, saida = self.executar(
            DICIONARIO_TABELAS,
            "dicionario_tabelas.md",
            ["--padrao-versao", r"^\d+\.\d+\.\d+$"],
        )
        self.assertEqual(codigo, 1)
        self.assertIn("nao corresponde a --padrao-versao", saida)

    def test_titulo_completamente_ausente_em_arquivo_vazio(self):
        codigo, saida = self.executar("", "dicionario_tabelas.md")
        self.assertEqual(codigo, 1)
        self.assertIn("titulo ausente", saida)
        self.assertIn("linha em branco obrigatoria entre titulo e tabela", saida)

    def test_linhas_em_branco_finais_sao_descartadas(self):
        codigo, saida = self.executar(DICIONARIO_TABELAS + "\n\n", "dicionario_tabelas.md")
        self.assertEqual(codigo, 0, saida)

    def test_separador_de_tabelas_deve_ser_exato(self):
        texto = DICIONARIO_TABELAS.replace("|---|---|", "|:--|:--|")
        codigo, saida = self.executar(texto, "dicionario_tabelas.md")
        self.assertEqual(codigo, 1)
        self.assertIn("separador exato obrigatorio", saida)

    def test_linha_em_branco_inesperada_na_tabela_de_tabelas(self):
        texto = DICIONARIO_TABELAS.replace(
            "| schema.tabela-a | Armazena algo. |\n",
            "| schema.tabela-a | Armazena algo. |\n\n",
        )
        codigo, saida = self.executar(texto, "dicionario_tabelas.md")
        self.assertEqual(codigo, 1)
        self.assertIn("linha em branco inesperada na tabela de tabelas", saida)

    def test_linha_com_quantidade_de_celulas_invalida_na_tabela_de_tabelas(self):
        texto = DICIONARIO_TABELAS.replace(
            "| schema.tabela-a | Armazena algo. |",
            "| schema.tabela-a | Armazena algo. | extra |",
        )
        codigo, saida = self.executar(texto, "dicionario_tabelas.md")
        self.assertEqual(codigo, 1)
        self.assertIn("invalida na tabela de tabelas", saida)

    def test_identificador_de_tabela_vazio_na_tabela_de_tabelas(self):
        texto = DICIONARIO_TABELAS.replace(
            "| schema.tabela-a | Armazena algo. |", "|  | Armazena algo. |"
        )
        codigo, saida = self.executar(texto, "dicionario_tabelas.md")
        self.assertEqual(codigo, 1)
        self.assertIn("identificador de tabela vazio", saida)

    def test_tabela_duplicada_na_tabela_de_tabelas(self):
        texto = """# T - v1

| Tabela | Descrição |
|---|---|
| a | Primeira vez. |
| a | Segunda vez. |
"""
        codigo, saida = self.executar(texto, "dicionario_tabelas.md")
        self.assertEqual(codigo, 1)
        self.assertIn("tabela duplicada: a", saida)

    def test_linha_sem_pipes_e_invalida_na_tabela_de_tabelas(self):
        texto = DICIONARIO_TABELAS.replace(
            "| schema.tabela-a | Armazena algo. |\n",
            "| schema.tabela-a | Armazena algo. |\nnota solta sem pipes\n",
        )
        codigo, saida = self.executar(texto, "dicionario_tabelas.md")
        self.assertEqual(codigo, 1)
        self.assertIn("invalida na tabela de tabelas", saida)

    def test_cabecalho_de_secao_sem_nome_e_invalido(self):
        texto = DICIONARIO_COLUNAS + "\n##    \n"
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("cabecalho de secao invalido", saida)

    def test_nenhuma_tabela_encontrada(self):
        texto = """# T - v1

| Tabela | Descrição |
|---|---|
"""
        codigo, saida = self.executar(texto, "dicionario_tabelas.md")
        self.assertEqual(codigo, 1)
        self.assertIn("nenhuma tabela encontrada", saida)

    def test_indice_sem_linha_em_branco_apos_titulo_do_indice(self):
        texto = """# T - v1

## Índice de Tabelas
- [a](#a)

## a

Desc.

| Tabela | Coluna | Descrição |
|---|---|---|
| a | c | d |
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("linha em branco obrigatoria depois do titulo do indice", saida)

    def test_indice_sem_linha_em_branco_antes_da_primeira_secao(self):
        texto = """# T - v1

## Índice de Tabelas

- [a](#a)
## a

Desc.

| Tabela | Coluna | Descrição |
|---|---|---|
| a | c | d |
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("linha em branco obrigatoria entre indice e primeira secao", saida)

    def test_indice_vazio_e_sem_secoes_de_tabela(self):
        texto = "# T - v1\n\n## Índice de Tabelas\n"
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("indice de tabelas vazio", saida)
        self.assertIn("nenhuma secao de tabela encontrada", saida)

    def test_linha_em_branco_inesperada_no_indice(self):
        texto = """# T - v1

## Índice de Tabelas

- [a](#a)

- [b](#b)

## a

Desc.

| Tabela | Coluna | Descrição |
|---|---|---|
| a | c | d |

## b

Desc.

| Tabela | Coluna | Descrição |
|---|---|---|
| b | c | d |
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("linha em branco inesperada no indice", saida)

    def test_entrada_invalida_no_indice_por_formato(self):
        texto = """# T - v1

## Índice de Tabelas

- a(a)

## a

Desc.

| Tabela | Coluna | Descrição |
|---|---|---|
| a | c | d |
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("entrada invalida no indice", saida)

    def test_entrada_invalida_no_indice_por_nome_vazio(self):
        texto = """# T - v1

## Índice de Tabelas

- [ ](#a)

## a

Desc.

| Tabela | Coluna | Descrição |
|---|---|---|
| a | c | d |
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("entrada invalida no indice", saida)

    def test_indice_duplicado_e_tratado_como_secao_ignorada(self):
        texto = """# T - v1

## Índice de Tabelas

- [a](#a)

## Índice de Tabelas

## a

Desc.

| Tabela | Coluna | Descrição |
|---|---|---|
| a | c | d |
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("indice de tabelas obrigatorio e unico", saida)

    def test_secao_duplicada_e_entrada_duplicada_no_indice(self):
        texto = """# T - v1

## Índice de Tabelas

- [a](#a)
- [a](#a-1)

## a

Desc.

| Tabela | Coluna | Descrição |
|---|---|---|
| a | c | d |

## a

Desc.

| Tabela | Coluna | Descrição |
|---|---|---|
| a | c | d |
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("secao duplicada: a", saida)
        self.assertIn("entrada duplicada no indice: a", saida)

    def test_destino_duplicado_no_indice(self):
        texto = """# T - v1

## Índice de Tabelas

- [a](#x)
- [b](#x)

## a

Desc.

| Tabela | Coluna | Descrição |
|---|---|---|
| a | c | d |

## b

Desc.

| Tabela | Coluna | Descrição |
|---|---|---|
| b | c | d |
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("destino duplicado no indice: #x", saida)

    def test_secao_sem_linha_em_branco_apos_cabecalho(self):
        texto = DICIONARIO_COLUNAS.replace(
            "## schema.tabela-a\n\nArmazena algo.",
            "## schema.tabela-a\nArmazena algo.",
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("linha em branco obrigatoria depois do cabecalho da secao", saida)

    def test_linha_em_branco_inesperada_na_secao_de_colunas(self):
        texto = DICIONARIO_COLUNAS.replace(
            "| schema.tabela-a | chave-principal | Número que identifica o registro. |\n",
            "| schema.tabela-a | chave-principal | Número que identifica o registro. |\n\n",
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("invalida na secao schema.tabela-a", saida)

    def test_identificador_de_coluna_vazio(self):
        texto = DICIONARIO_COLUNAS.replace(
            "| schema.tabela-a | nome.exibicao | Nome exibido. |",
            "| schema.tabela-a |  | Nome exibido. |",
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("identificador de coluna vazio", saida)

    def test_coluna_duplicada_na_secao(self):
        texto = DICIONARIO_COLUNAS.replace(
            "| schema.tabela-a | nome.exibicao | Nome exibido. |",
            "| schema.tabela-a | chave-principal | Duplicada. |",
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("coluna duplicada em schema.tabela-a: chave-principal", saida)

    def test_arquivo_de_outro_nome_e_rejeitado(self):
        codigo, saida = self.executar(DICIONARIO_COLUNAS, "outro.md")
        self.assertEqual(codigo, 2, saida)
        self.assertIn("ERRO", saida)


class TabelasColunasTest(unittest.TestCase):
    def executar(self, tabelas=DICIONARIO_TABELAS, colunas=DICIONARIO_COLUNAS):
        with tempfile.TemporaryDirectory() as tmp:
            caminho_tabelas = Path(tmp, "dicionario_tabelas.md")
            caminho_colunas = Path(tmp, "dicionario_colunas.md")
            caminho_tabelas.write_text(tabelas, encoding="utf-8")
            caminho_colunas.write_text(colunas, encoding="utf-8")
            return rodar([
                "tabelas-colunas",
                "--tabelas", str(caminho_tabelas),
                "--colunas", str(caminho_colunas),
            ])

    def test_conjuntos_e_descricoes_consistentes(self):
        codigo, saida = self.executar()
        self.assertEqual(codigo, 0, saida)

    def test_tabela_ausente_e_reportada(self):
        tabelas = DICIONARIO_TABELAS.replace(
            "| tabela_á | Armazena outra coisa, um domínio composto por:<ul><li>a: primeiro valor</li><li>b: segundo valor</li></ul> |\n", ""
        )
        codigo, saida = self.executar(tabelas=tabelas)
        self.assertEqual(codigo, 1)
        self.assertIn("tabela_á", saida)

    def test_descricoes_de_tabela_divergentes_sao_reportadas(self):
        tabelas = DICIONARIO_TABELAS.replace("Armazena algo.", "Armazena algo diferente.")
        codigo, saida = self.executar(tabelas=tabelas)
        self.assertEqual(codigo, 1)
        self.assertIn("Descricoes de tabela divergentes", saida)
        self.assertIn("schema.tabela-a", saida)

    def test_qualquer_divergencia_de_marcacao_e_reportada(self):
        tabelas = DICIONARIO_TABELAS.replace("Armazena algo.", "Armazena algo.<ul><li>nota</li></ul>")
        codigo, saida = self.executar(tabelas=tabelas)
        self.assertEqual(codigo, 1)
        self.assertIn("schema.tabela-a", saida)

    def test_versoes_divergentes_sao_reportadas(self):
        tabelas = DICIONARIO_TABELAS.replace("release-2026-A", "release-2026-B")
        codigo, saida = self.executar(tabelas=tabelas)
        self.assertEqual(codigo, 1)
        self.assertIn("Titulo ou versao diverge", saida)

    def test_nomes_de_arquivo_invalidos_sao_rejeitados(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho_errado = Path(tmp, "tabelas.md")
            caminho_colunas = Path(tmp, "dicionario_colunas.md")
            caminho_errado.write_text(DICIONARIO_TABELAS, encoding="utf-8")
            caminho_colunas.write_text(DICIONARIO_COLUNAS, encoding="utf-8")
            codigo, saida = rodar([
                "tabelas-colunas",
                "--tabelas", str(caminho_errado),
                "--colunas", str(caminho_colunas),
            ])
        self.assertEqual(codigo, 2, saida)
        self.assertIn("aceita somente dicionario_tabelas.md", saida)

    def test_erros_de_formato_sao_reportados_no_cruzamento(self):
        tabelas = DICIONARIO_TABELAS.replace("| Tabela | Descrição |", "| Nome | Descrição |")
        codigo, saida = self.executar(tabelas=tabelas)
        self.assertEqual(codigo, 2, saida)
        self.assertIn("ERRO de formato em dicionario_tabelas.md", saida)


class ChangelogTest(unittest.TestCase):
    def executar(self, changelog, dicionario=None, extra=None, arquivo=False):
        with tempfile.TemporaryDirectory() as tmp:
            caminho_changelog = Path(tmp, "CHANGELOG.md")
            caminho_changelog.write_text(changelog, encoding="utf-8")
            if dicionario is not None:
                Path(tmp, "dicionario_colunas.md").write_text(dicionario, encoding="utf-8")
            alvo = caminho_changelog if arquivo else tmp
            return rodar(["changelog", str(alvo)] + (extra or []))

    def test_changelog_valido_via_pasta(self):
        codigo, saida = self.executar(CHANGELOG_ISOLADO)
        self.assertEqual(codigo, 0, saida)

    def test_changelog_valido_via_arquivo_direto(self):
        codigo, saida = self.executar(CHANGELOG_ISOLADO, arquivo=True)
        self.assertEqual(codigo, 0, saida)

    def test_titulo_invalido(self):
        texto = CHANGELOG_ISOLADO.replace("# Histórico Estrutural de Teste", "Histórico Estrutural de Teste")
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("titulo", saida)

    def test_titulo_duplicado(self):
        texto = CHANGELOG_ISOLADO.replace(
            "# Histórico Estrutural de Teste",
            "# Histórico Estrutural de Teste\n# Outro título",
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("exatamente um titulo H1", saida)

    def test_versao_vazia(self):
        texto = CHANGELOG_ISOLADO.replace("## [release-B]", "## []")
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("versao vazio", saida)

    def test_cabecalho_de_versao_malformado(self):
        texto = CHANGELOG_ISOLADO.replace("## [release-B]", "## release-B")
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("cabecalho de versao invalido", saida)

    def test_categoria_nao_permitida(self):
        texto = CHANGELOG_ISOLADO.replace("### Adicionado", "### Modificado")
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("nao permitida", saida)

    def test_categoria_duplicada(self):
        texto = CHANGELOG_ISOLADO + """
### Adicionado

- **Tabela `outra_tabela`**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("categoria duplicada", saida)

    def test_categorias_fora_de_ordem(self):
        texto = """# Changelog de Teste

## [2]

### Excluído

- **Tabela `antiga`**

### Alterado

- **Tabela `atual`**
  - **Colunas**
    - **Nova `campo`**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("categorias fora de ordem", saida)

    def test_bullet_malformado(self):
        texto = CHANGELOG_ISOLADO.replace("- **Tabela", "* **Tabela")
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("conteudo inesperado", saida)

    def test_indices_exige_marcador_masculino(self):
        texto = """# Changelog de Teste

## [2]

### Alterado

- **Tabela `atual`**
  - **Índices**
    - **Nova `indice`**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("tipo 'Nova' invalido", saida)

    def test_alteracao_de_coluna_exige_gramatica(self):
        texto = """# Changelog de Teste

## [2]

### Alterado

- **Tabela `atual`**
  - **Colunas**
    - **Alterada `campo`**: mudou o tipo.
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("gramatica de alteracao", saida)

    def test_duplicidade_de_objeto(self):
        texto = """# Changelog de Teste

## [2]

### Alterado

- **Tabela `atual`**
  - **Colunas**
    - **Nova `campo`**
    - **Nova `campo`**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("objeto duplicado", saida)

    def test_duplicidade_de_versao(self):
        texto = CHANGELOG_ISOLADO + CHANGELOG_ISOLADO.split("\n", 1)[1]
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("versao duplicada", saida)

    def test_detalhe_fisico_e_permitido_em_objeto_novo(self):
        texto = """# Histórico Estrutural de Teste

## [2]

### Alterado

- **Tabela `atual`**
  - **Colunas**
    - **Nova `campo`**: tipo: nenhum para varchar(10).
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 0, saida)

    def test_detalhe_incompleto_em_objeto_novo_e_rejeitado(self):
        texto = """# Histórico Estrutural de Teste

## [2]

### Alterado

- **Tabela `atual`**
  - **Colunas**
    - **Nova `campo`**: tipo informado sem pontuação
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("gramatica de detalhe", saida)

    def test_tabela_pode_aparecer_em_categorias_distintas(self):
        texto = """# Histórico Estrutural de Teste

## [2]

### Alterado

- **Tabela `atual`**
  - **Colunas**
    - **Nova `campo`**

### Excluído

- **Tabela `atual`**
  - **Índices**
    - **Excluído `indice_antigo`**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 0, saida)

    def test_topicos_atuais_e_detalhes_validos(self):
        texto = """# Histórico Estrutural de Teste

## [2]

### Alterado

- **Tabela `atual`**
  - **Chaves primárias**
    - **Alterada `pk_atual`**: composição: id_antigo para id_atual.
  - **Chaves estrangeiras**
    - **Nova `fk_atual`**
  - **Restrições**
    - **Alterada `ck_atual`**: expressão: valor > 0 para valor >= 0.
  - **Propriedades da tabela**
    - **Alterada `particionamento`**: estratégia: lista para faixa.
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 0, saida)

    def test_versoes_numericas_fora_de_ordem(self):
        texto = """# Changelog de Teste

## [1.9]

### Adicionado

- **Tabela `a`**

## [1.10]

### Adicionado

- **Tabela `b`**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("ordem decrescente", saida)

    def test_ordem_fornecida_e_respeitada(self):
        texto = CHANGELOG_ISOLADO + """

## [release-A]

### Adicionado

- **Tabela `outra_tabela`**
"""
        codigo, saida = self.executar(
            texto, extra=["--ordem-versoes", "release-B,release-A"]
        )
        self.assertEqual(codigo, 0, saida)

    def test_padrao_de_versao_opcional(self):
        codigo, saida = self.executar(
            CHANGELOG_ISOLADO,
            extra=["--padrao-versao", r"release-[A-Z]"],
        )
        self.assertEqual(codigo, 0, saida)

    def test_versao_fora_da_ordem_fornecida_e_rejeitada(self):
        texto = CHANGELOG_ISOLADO.replace("release-B", "release-A") + """

## [release-B]

### Adicionado

- **Tabela `outra_tabela`**
"""
        codigo, saida = self.executar(
            texto, extra=["--ordem-versoes", "release-B,release-A"]
        )
        self.assertEqual(codigo, 1)
        self.assertIn("ordem fornecida", saida)

    def test_cruzamento_e_adicional_quando_dicionario_existe(self):
        texto = """# Changelog de Teste

## [release-B]

### Alterado

- **Tabela `schema.tabela-a`**
  - **Colunas**
    - **Nova `campo-ausente`**
"""
        codigo, saida = self.executar(texto, DICIONARIO_COLUNAS)
        self.assertEqual(codigo, 1)
        self.assertIn("schema.tabela-a.campo-ausente", saida)

    def test_tabela_excluida_presente_e_reportada(self):
        texto = """# Changelog de Teste

## [release-B]

### Excluído

- **Tabela `schema.tabela-a`**
"""
        codigo, saida = self.executar(texto, DICIONARIO_COLUNAS)
        self.assertEqual(codigo, 1)
        self.assertIn("schema.tabela-a", saida)

    def test_ordem_versoes_com_item_vazio_e_rejeitada_pelo_argparse(self):
        codigo, saida = self.executar(
            CHANGELOG_ISOLADO, extra=["--ordem-versoes", "release-B,,release-A"]
        )
        self.assertEqual(codigo, 2, saida)
        self.assertIn("vazias", saida)

    def test_ordem_versoes_com_duplicidade_e_rejeitada_pelo_argparse(self):
        codigo, saida = self.executar(
            CHANGELOG_ISOLADO, extra=["--ordem-versoes", "release-B,release-B"]
        )
        self.assertEqual(codigo, 2, saida)
        self.assertIn("duplicidades", saida)

    def test_ordem_fornecida_sem_uma_das_versoes_do_changelog(self):
        texto = CHANGELOG_ISOLADO + """
## [release-C]

### Adicionado

- **Tabela `outra_tabela`**
"""
        codigo, saida = self.executar(
            texto, extra=["--ordem-versoes", "release-B"]
        )
        self.assertEqual(codigo, 1)
        self.assertIn("versoes ausentes de --ordem-versoes", saida)
        self.assertIn("release-C", saida)

    def test_versao_do_changelog_nao_confere_com_padrao(self):
        codigo, saida = self.executar(
            CHANGELOG_ISOLADO, extra=["--padrao-versao", r"^\d+$"]
        )
        self.assertEqual(codigo, 1)
        self.assertIn("nao corresponde a --padrao-versao", saida)

    def test_categoria_vazia_e_invalida(self):
        texto = """# Changelog de Teste

## [2]

###

- **Tabela `a`**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("categoria invalida", saida)

    def test_bullet_de_tabela_sem_formatacao_e_malformado(self):
        texto = """# Changelog de Teste

## [2]

### Adicionado

- Tabela sem negrito
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("bullet de tabela malformado", saida)

    def test_identificador_de_tabela_vazio_no_bullet(self):
        texto = """# Changelog de Teste

## [2]

### Adicionado

- **Tabela ` `**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("identificador de tabela vazio", saida)

    def test_topico_fora_de_categoria_permitida(self):
        texto = """# Changelog de Teste

## [2]

### Adicionado

- **Tabela `a`**
  - **Colunas**
    - **Nova `c`**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("topico fora de tabela alterada/excluida", saida)
        self.assertIn("bullet de objeto fora de topico", saida)

    def test_topico_duplicado_na_mesma_tabela(self):
        texto = """# Changelog de Teste

## [2]

### Alterado

- **Tabela `a`**
  - **Colunas**
    - **Nova `c`**
  - **Colunas**
    - **Nova `d`**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("topico duplicado em a: Colunas", saida)

    def test_topico_malformado(self):
        texto = """# Changelog de Teste

## [2]

### Alterado

- **Tabela `a`**
  - **Coisa Invalida**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("topico malformado", saida)

    def test_objeto_identificador_vazio(self):
        texto = """# Changelog de Teste

## [2]

### Alterado

- **Tabela `a`**
  - **Colunas**
    - **Nova ` `**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("identificador de objeto vazio", saida)

    def test_alteracao_sem_detalhe(self):
        texto = """# Changelog de Teste

## [2]

### Alterado

- **Tabela `a`**
  - **Colunas**
    - **Alterada `c`**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("alteracao sem detalhe", saida)

    def test_bullet_de_objeto_sem_formatacao_e_malformado(self):
        texto = """# Changelog de Teste

## [2]

### Alterado

- **Tabela `a`**
  - **Colunas**
    - Nova campo sem negrito
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("bullet de objeto malformado", saida)

    def test_tabela_alterada_sem_topico(self):
        texto = """# Changelog de Teste

## [2]

### Alterado

- **Tabela `a`**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("tabela alterada sem topico: a", saida)

    def test_topico_vazio_sem_objetos(self):
        texto = """# Changelog de Teste

## [2]

### Alterado

- **Tabela `a`**
  - **Colunas**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1)
        self.assertIn("topico vazio em a: Colunas", saida)

    def test_renomeacao_de_coluna_reflete_no_cruzamento(self):
        texto = """# Changelog de Teste

## [release-B]

### Alterado

- **Tabela `schema.tabela-a`**
  - **Colunas**
    - **Alterada `novo_nome`**: renomeada de `nome.exibicao`.
"""
        codigo, saida = self.executar(texto, DICIONARIO_COLUNAS)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("schema.tabela-a.novo_nome", saida)
        self.assertIn("schema.tabela-a.nome.exibicao", saida)

    def test_coluna_excluida_ainda_presente_e_reportada(self):
        texto = """# Changelog de Teste

## [release-B]

### Excluído

- **Tabela `schema.tabela-a`**
  - **Colunas**
    - **Excluída `nome.exibicao`**
"""
        codigo, saida = self.executar(texto, DICIONARIO_COLUNAS)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("colunas excluidas ou renomeadas ainda presentes", saida)
        self.assertIn("schema.tabela-a.nome.exibicao", saida)

    def test_tabela_renomeada_ainda_presente_no_dicionario(self):
        texto = """# Changelog de Teste

## [release-B]

### Adicionado

- **Tabela `tabela_nova`** (renomeada de `schema.tabela-a`)
"""
        codigo, saida = self.executar(texto, DICIONARIO_COLUNAS)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("tabelas renomeadas ainda presentes no dicionario", saida)
        self.assertIn("schema.tabela-a", saida)

    def test_colunas_de_tabela_renomeada_nao_sao_cruzadas_novamente(self):
        texto = """# Changelog de Teste

## [release-B]

### Adicionado

- **Tabela `tabela_nova`** (renomeada de `schema.tabela-a`)

### Excluído

- **Tabela `schema.tabela-a`**
  - **Colunas**
    - **Excluída `nome.exibicao`**
"""
        codigo, saida = self.executar(texto, DICIONARIO_COLUNAS)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("tabelas renomeadas ainda presentes no dicionario", saida)
        self.assertNotIn("schema.tabela-a.nome.exibicao", saida)

    def test_dicionario_malformado_e_entrada_invalida(self):
        texto = """# Changelog de Teste

## [release-B]

### Adicionado

- **Tabela `tabela_nova`**
"""
        dicionario = DICIONARIO_COLUNAS.replace("## Índice de Tabelas", "## Sumário")
        codigo, saida = self.executar(texto, dicionario)
        self.assertEqual(codigo, 2, saida)
        self.assertIn("ERRO de formato em", saida)

    def test_tipo_invalido_em_colunas_nao_gera_estado_de_coluna(self):
        """Um tipo fora do vocabulario feminino de Colunas e reportado e ignorado no cruzamento."""
        texto = """# Changelog de Teste

## [2]

### Alterado

- **Tabela `a`**
  - **Colunas**
    - **Novo `c`**
"""
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("tipo 'Novo' invalido em Alterado/Colunas", saida)

    def test_alteracao_de_coluna_existente_nao_gera_divergencia(self):
        texto = """# Changelog de Teste

## [release-B]

### Alterado

- **Tabela `schema.tabela-a`**
  - **Colunas**
    - **Alterada `chave-principal`**: tipo: int para bigint.
"""
        codigo, saida = self.executar(texto, DICIONARIO_COLUNAS)
        self.assertEqual(codigo, 0, saida)
        self.assertIn("OK", saida)

    def test_arquivo_isolado_com_nome_diferente_de_changelog(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = Path(tmp, "outro.md")
            caminho.write_text(CHANGELOG_ISOLADO, encoding="utf-8")
            codigo, saida = rodar(["changelog", str(caminho)])
        self.assertEqual(codigo, 2, saida)
        self.assertIn("arquivo isolado deve se chamar CHANGELOG.md", saida)


class DiffTest(unittest.TestCase):
    def executar(self, antigo, novo, extra=None):
        with tempfile.TemporaryDirectory() as tmp:
            pasta_antigo = Path(tmp, "antes")
            pasta_novo = Path(tmp, "depois")
            pasta_antigo.mkdir()
            pasta_novo.mkdir()
            caminho_antigo = pasta_antigo / "dicionario_colunas.md"
            caminho_novo = pasta_novo / "dicionario_colunas.md"
            caminho_antigo.write_text(antigo, encoding="utf-8")
            caminho_novo.write_text(novo, encoding="utf-8")
            return rodar([
                "diff", "--antigo", str(caminho_antigo), "--novo", str(caminho_novo)
            ] + (extra or []))

    def test_sem_diferenca(self):
        codigo, saida = self.executar(DICIONARIO_COLUNAS, DICIONARIO_COLUNAS)
        self.assertEqual(codigo, 0, saida)

    def test_mesmo_arquivo_e_entrada_invalida(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = Path(tmp, "dicionario_colunas.md")
            caminho.write_text(DICIONARIO_COLUNAS, encoding="utf-8")
            codigo, saida = rodar([
                "diff", "--antigo", str(caminho), "--novo", str(caminho)
            ])
        self.assertEqual(codigo, 2, saida)
        self.assertIn("arquivos distintos", saida)

    def test_hard_link_e_entrada_invalida(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho_antigo = Path(tmp, "dicionario_colunas.md")
            caminho_antigo.write_text(DICIONARIO_COLUNAS, encoding="utf-8")
            pasta_novo = Path(tmp, "novo")
            pasta_novo.mkdir()
            caminho_novo = pasta_novo / "dicionario_colunas.md"
            os.link(caminho_antigo, caminho_novo)
            codigo, saida = rodar([
                "diff", "--antigo", str(caminho_antigo), "--novo", str(caminho_novo)
            ])
        self.assertEqual(codigo, 2, saida)
        self.assertIn("arquivos distintos", saida)

    def test_coluna_adicionada_aparece_na_contagem(self):
        novo = DICIONARIO_COLUNAS.replace(
            "| tabela_á | id:tabela | Número que identifica a tabela. |",
            "| tabela_á | id:tabela | Número que identifica a tabela. |\n"
            "| tabela_á | nova-coluna | Nova descrição. |",
        )
        codigo, saida = self.executar(DICIONARIO_COLUNAS, novo, ["--json"])
        self.assertEqual(codigo, 1)
        dados = json.loads(saida)
        self.assertEqual(dados["contagem_alteracoes"]["colunas_adicionadas"], 1)

    def test_descricao_de_tabela_alterada_e_detectada(self):
        novo = DICIONARIO_COLUNAS.replace("Armazena algo.", "Armazena algo diferente.")
        codigo, saida = self.executar(DICIONARIO_COLUNAS, novo, ["--json"])
        self.assertEqual(codigo, 1)
        dados = json.loads(saida)
        self.assertEqual(dados["contagem_alteracoes"]["descricoes_tabela_alteradas"], 1)

    def test_nomes_de_arquivo_invalidos_sao_rejeitados(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho_errado = Path(tmp, "colunas.md")
            caminho_novo = Path(tmp, "dicionario_colunas.md")
            caminho_errado.write_text(DICIONARIO_COLUNAS, encoding="utf-8")
            caminho_novo.write_text(DICIONARIO_COLUNAS, encoding="utf-8")
            codigo, saida = rodar([
                "diff", "--antigo", str(caminho_errado), "--novo", str(caminho_novo)
            ])
        self.assertEqual(codigo, 2, saida)
        self.assertIn("diff aceita somente arquivos dicionario_colunas.md", saida)

    def test_arquivo_antigo_inexistente_e_entrada_invalida(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho_antigo = Path(tmp, "nao-existe", "dicionario_colunas.md")
            caminho_novo = Path(tmp, "dicionario_colunas.md")
            caminho_novo.write_text(DICIONARIO_COLUNAS, encoding="utf-8")
            codigo, saida = rodar([
                "diff", "--antigo", str(caminho_antigo), "--novo", str(caminho_novo)
            ])
        self.assertEqual(codigo, 2, saida)
        self.assertIn("ERRO", saida)

    def test_arquivo_malformado_e_reportado_no_diff(self):
        antigo = DICIONARIO_COLUNAS.replace("## Índice de Tabelas", "## Sumário")
        codigo, saida = self.executar(antigo, DICIONARIO_COLUNAS)
        self.assertEqual(codigo, 2, saida)
        self.assertIn("ERRO de formato em antigo", saida)

    def test_saida_textual_lista_adicionadas_removidas_e_alteradas(self):
        antigo = """# T - v1

## Índice de Tabelas

- [a](#a)
- [b](#b)

## a

Desc A.

| Tabela | Coluna | Descrição |
|---|---|---|
| a | c1 | d1 |

## b

Desc B.

| Tabela | Coluna | Descrição |
|---|---|---|
| b | c1 | d1 |
"""
        novo = """# T - v1

## Índice de Tabelas

- [a](#a)
- [d](#d)

## a

Desc A alterada.

| Tabela | Coluna | Descrição |
|---|---|---|
| a | c1 | d1 |

## d

Desc D.

| Tabela | Coluna | Descrição |
|---|---|---|
| d | c1 | d1 |
"""
        codigo, saida = self.executar(antigo, novo)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("Tabelas adicionadas (1):", saida)
        self.assertIn("- d:", saida)
        self.assertIn("Tabelas removidas (1):", saida)
        self.assertIn("- b", saida)
        self.assertIn("Tabelas alteradas (1):", saida)
        self.assertIn("descricao_tabela=True", saida)


class EntradaInvalidaTest(unittest.TestCase):
    def test_formato_arquivo_ausente(self):
        codigo, saida = rodar(["formato", "/nao/existe/dicionario_colunas.md"])
        self.assertEqual(codigo, 2, saida)
        self.assertIn("ERRO", saida)

    def test_tabelas_colunas_arquivo_ausente(self):
        codigo, saida = rodar([
            "tabelas-colunas",
            "--tabelas", "/nao/existe/dicionario_tabelas.md",
            "--colunas", "/nao/existe/dicionario_colunas.md",
        ])
        self.assertEqual(codigo, 2, saida)
        self.assertIn("ERRO", saida)

    def test_changelog_ausente(self):
        with tempfile.TemporaryDirectory() as tmp:
            codigo, saida = rodar(["changelog", tmp])
        self.assertEqual(codigo, 2, saida)
        self.assertIn("ausente", saida)

    def test_encoding_invalido(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = Path(tmp, "dicionario_colunas.md")
            caminho.write_bytes(b"\xff\xfe binario")
            codigo, saida = rodar(["formato", str(caminho)])
        self.assertEqual(codigo, 2, saida)
        self.assertIn("ERRO", saida)


class LacunasTest(unittest.TestCase):
    def executar(self, texto, nome="dicionario_colunas.md", extra=None):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = Path(tmp, nome)
            caminho.write_text(texto, encoding="utf-8")
            return rodar(["lacunas", str(caminho)] + (extra or []))

    def test_sem_marcador_retorna_zero(self):
        codigo, saida = self.executar(DICIONARIO_COLUNAS)
        self.assertEqual(codigo, 0, saida)
        self.assertIn("sem marcadores de lacuna", saida)

    def test_conta_marcador_na_forma_canonica(self):
        texto = DICIONARIO_COLUNAS.replace(
            "| schema.tabela-a | nome.exibicao | Nome exibido. |",
            "| schema.tabela-a | nome.exibicao | Nome exibido, correspondente a "
            "TODO: significado e critério - nenhum escritor localizado. |",
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("1 marcadores em 1 objetos", saida)
        self.assertIn("significado e criterio", saida)

    def test_tolera_sufixo_que_torna_a_frase_gramatical(self):
        texto = DICIONARIO_COLUNAS.replace(
            "Nome exibido.",
            "Nome exibido, correspondente a TODO: significado e critério não confirmados "
            "- sem escritor.",
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("significado e criterio", saida)
        self.assertNotIn("fora do vocabulario", saida)

    def test_marcador_sem_motivo_avisa(self):
        texto = DICIONARIO_COLUNAS.replace(
            "Nome exibido.", "Nome exibido de TODO: entidade ou evento."
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("sem motivo depois do separador", saida)

    def test_termo_fora_do_vocabulario_avisa(self):
        texto = DICIONARIO_COLUNAS.replace(
            "Nome exibido.", "Nome exibido de TODO: coisa inventada - nada encontrado."
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("fora do vocabulario", saida)

    def test_marcadores_adjacentes_sem_pontuacao_entre_eles(self):
        """Motivo de um marcador nao pode engolir o marcador seguinte."""
        texto = DICIONARIO_COLUNAS.replace(
            "Nome exibido.",
            "TODO: propriedade ou conceito - sem definicao de "
            "TODO: entidade ou evento - sem definicao, correspondente a "
            "TODO: significado e critério - sem decodificador.",
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("3 marcadores em 1 objetos", saida)

    def test_dois_marcadores_na_mesma_descricao(self):
        texto = DICIONARIO_COLUNAS.replace(
            "Nome exibido.",
            "TODO: propriedade ou conceito - sem fonte. É utilizado para "
            "TODO: função - sem consumidor localizado.",
        )
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("2 marcadores em 1 objetos", saida)

    def test_marcador_em_descricao_de_tabela(self):
        texto = DICIONARIO_TABELAS.replace(
            "| tabela_á | Armazena outra coisa",
            "| tabela_á | Representa TODO: granularidade - sem evidência. Armazena outra coisa",
        )
        codigo, saida = self.executar(texto, nome="dicionario_tabelas.md")
        self.assertEqual(codigo, 1, saida)
        self.assertIn("granularidade", saida)

    def test_json_traz_agregados_e_itens(self):
        texto = DICIONARIO_COLUNAS.replace(
            "Nome exibido.", "Nome exibido de TODO: entidade ou evento - sem escritor."
        )
        codigo, saida = self.executar(texto, extra=["--json"])
        self.assertEqual(codigo, 1, saida)
        dados = json.loads(saida)
        self.assertEqual(dados["marcadores"], 1)
        self.assertEqual(dados["objetos_afetados"], 1)
        self.assertEqual(dados["itens"][0]["coluna"], "nome.exibicao")
        self.assertEqual(dados["itens"][0]["motivo"], "sem escritor")

    def test_arquivo_de_outro_nome_e_entrada_invalida(self):
        codigo, saida = self.executar(DICIONARIO_COLUNAS, nome="outro.md")
        self.assertEqual(codigo, 2, saida)
        self.assertIn("ERRO", saida)

    def test_dicionario_malformado_e_entrada_invalida(self):
        texto = DICIONARIO_COLUNAS.replace("## Índice de Tabelas", "## Sumário")
        codigo, saida = self.executar(texto)
        self.assertEqual(codigo, 2, saida)


class PontoDeEntradaTest(unittest.TestCase):
    def test_execucao_como_script_invoca_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = Path(tmp, "dicionario_tabelas.md")
            caminho.write_text(DICIONARIO_TABELAS, encoding="utf-8")
            saida = io.StringIO()
            original = sys.argv
            sys.argv = ["verificar_dicionario.py", "formato", str(caminho)]
            try:
                with contextlib.redirect_stdout(saida):
                    with self.assertRaises(SystemExit) as contexto:
                        runpy.run_path(v.__file__, run_name="__main__")
            finally:
                sys.argv = original
        self.assertEqual(contexto.exception.code, 0)
        self.assertIn("OK", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
