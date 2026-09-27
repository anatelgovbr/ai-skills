#!/usr/bin/env python3
"""Testes do gate de cobertura: formatos, limites, linha de base e saida."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import verificar_cobertura as vc

COBERTURA = b"""<?xml version="1.0" ?>
<coverage line-rate="0.75" branch-rate="0.5">
  <packages><package name="app"><classes>
    <class name="a" filename="app/a.py"><lines>
      <line number="1" hits="1"/>
      <line number="2" hits="3" branch="true" condition-coverage="50% (1/2)"/>
      <line number="3" hits="0"/>
      <line number="4" hits="2"/>
    </lines></class>
  </classes></package></packages>
</coverage>
"""

COBERTURA_SEM_RAMOS = b"""<coverage><packages><package><classes>
<class filename="x.php"><lines><line number="1" hits="1"/></lines></class>
</classes></package></packages></coverage>"""

LCOV = b"""TN:
SF:src/a.js
DA:1,1
DA:2,0
BRDA:2,0,0,1
BRDA:2,0,1,-
BRDA:2,0,2,0
LF:2
LH:1
end_of_record
SF:src/b.js
DA:1,5
end_of_record
"""

JACOCO = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE report PUBLIC "-//JACOCO//DTD Report 1.1//EN" "report.dtd">
<report name="exemplo">
  <package name="br/gov/exemplo">
    <sourcefile name="Servico.java">
      <counter type="INSTRUCTION" missed="3" covered="30"/>
      <counter type="BRANCH" missed="1" covered="3"/>
      <counter type="LINE" missed="1" covered="9"/>
    </sourcefile>
  </package>
</report>
"""


class Base(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)

    def gravar(self, nome: str, dados: bytes) -> Path:
        caminho = Path(self.dir.name) / nome
        caminho.write_bytes(dados)
        return caminho

    def rodar(self, *args):
        saida, erro = io.StringIO(), io.StringIO()
        with redirect_stdout(saida), redirect_stderr(erro):
            codigo = vc.principal(list(args))
        return codigo, saida.getvalue(), erro.getvalue()


class TesteFormatos(Base):
    def test_cobertura_soma_linhas_e_condicoes(self):
        m = vc.medir(self.gravar("c.xml", COBERTURA))
        a = m.arquivos["app/a.py"]
        self.assertEqual((a.linhas_total, a.linhas_cobertas), (4, 3))
        self.assertEqual((a.ramos_total, a.ramos_cobertos), (2, 1))
        self.assertEqual(vc.resumo(m), {"formato": "cobertura", "arquivos": 1,
                                        "linhas": 75.0, "ramos": 50.0})

    def test_lcov_trata_traco_e_zero_como_ramo_nao_coberto(self):
        m = vc.medir(self.gravar("lcov.info", LCOV))
        a = m.arquivos["src/a.js"]
        self.assertEqual((a.linhas_total, a.linhas_cobertas), (2, 1))
        self.assertEqual((a.ramos_total, a.ramos_cobertos), (3, 1))
        self.assertEqual(m.arquivos["src/b.js"].linhas_cobertas, 1)
        self.assertEqual(vc.resumo(m)["linhas"], 66.67)

    def test_lcov_ignora_registro_fora_de_arquivo(self):
        m = vc.medir(self.gravar("l.info", b"TN:\nDA:1,1\nSF:x\nDA:1,1\nend_of_record\nDA:9,9\n"))
        self.assertEqual(m.arquivos["x"].linhas_total, 1)

    def test_jacoco_usa_contadores_de_linha_e_ramo_com_doctype(self):
        m = vc.medir(self.gravar("jacoco.xml", JACOCO))
        a = m.arquivos["br/gov/exemplo/Servico.java"]
        self.assertEqual((a.linhas_total, a.linhas_cobertas), (10, 9))
        self.assertEqual((a.ramos_total, a.ramos_cobertos), (4, 3))

    def test_formato_explicito_prevalece(self):
        self.assertEqual(vc.medir(self.gravar("r.txt", LCOV), "lcov").formato, "lcov")


class TesteEntradaInvalida(Base):
    def test_arquivo_inexistente(self):
        with self.assertRaisesRegex(vc.ErroDeEntrada, "nao encontrado"):
            vc.medir(Path(self.dir.name) / "nada.xml")

    def test_relatorio_grande_demais(self):
        caminho = self.gravar("c.xml", COBERTURA)
        original = vc.MAIOR_RELATORIO
        vc.MAIOR_RELATORIO = 10
        self.addCleanup(setattr, vc, "MAIOR_RELATORIO", original)
        with self.assertRaisesRegex(vc.ErroDeEntrada, "maior que"):
            vc.medir(caminho)

    def test_recusa_xml_com_entidade(self):
        bomba = b'<?xml version="1.0"?><!DOCTYPE c [<!ENTITY a "aaaa">]><coverage>&a;</coverage>'
        with self.assertRaisesRegex(vc.ErroDeEntrada, "entidade"):
            vc.medir(self.gravar("b.xml", bomba))

    def test_xml_quebrado(self):
        with self.assertRaisesRegex(vc.ErroDeEntrada, "XML invalido"):
            vc.medir(self.gravar("q.xml", b"<coverage><class>"))

    def test_raiz_desconhecida(self):
        with self.assertRaisesRegex(vc.ErroDeEntrada, "raiz desconhecida"):
            vc.medir(self.gravar("r.xml", b"<outra/>"))

    def test_texto_nao_reconhecido(self):
        with self.assertRaisesRegex(vc.ErroDeEntrada, "nao reconhecido"):
            vc.medir(self.gravar("r.txt", b"qualquer coisa"))

    def test_relatorio_vazio_e_erro_e_nao_aprovacao(self):
        with self.assertRaisesRegex(vc.ErroDeEntrada, "sem nenhuma linha"):
            vc.medir(self.gravar("v.xml", b"<coverage/>"))

    def test_lcov_malformado(self):
        with self.assertRaisesRegex(vc.ErroDeEntrada, "malformado"):
            vc.medir(self.gravar("m.info", b"SF:a\nDA:1\nend_of_record\n"))


class TesteAvaliacao(Base):
    def medicao(self, dados=COBERTURA):
        return vc.medir(self.gravar("c.xml", dados))

    def test_aprova_quando_atinge_os_minimos(self):
        r = vc.avaliar(self.medicao(), 75, 50)
        self.assertTrue(r["aprovado"])
        self.assertEqual(r["falhas"], [])

    def test_reprova_linhas_e_ramos_abaixo(self):
        r = vc.avaliar(self.medicao(), 90, 90)
        self.assertFalse(r["aprovado"])
        self.assertEqual(len(r["falhas"]), 2)
        self.assertIn("linhas 75.0%", r["falhas"][0])
        self.assertIn("ramos 50.0%", r["falhas"][1])

    def test_ramos_nao_medidos_reprovam_quando_exigidos(self):
        r = vc.avaliar(self.medicao(COBERTURA_SEM_RAMOS), 90, 90)
        self.assertIsNone(r["ramos"])
        self.assertIn("sem medicao de ramos", r["falhas"][0])

    def test_minimo_de_ramos_zero_dispensa_medicao(self):
        self.assertTrue(vc.avaliar(self.medicao(COBERTURA_SEM_RAMOS), 90, 0)["aprovado"])

    def test_minimo_por_arquivo(self):
        m = vc.medir(self.gravar("l.info", LCOV))
        r = vc.avaliar(m, 0, 0, minimo_arquivo=80)
        self.assertEqual(r["arquivos_abaixo"], [{"arquivo": "src/a.js", "linhas": 50.0}])
        self.assertFalse(r["aprovado"])

    def test_queda_em_relacao_a_linha_base_reprova(self):
        r = vc.avaliar(self.medicao(), 0, 0, linha_base={"linhas": 80.0, "ramos": 40.0})
        self.assertEqual(r["falhas"], ["linhas cairam de 80.0% para 75.0% em relacao a linha de base"])

    def test_linha_base_sem_metrica_nao_compara(self):
        r = vc.avaliar(self.medicao(COBERTURA_SEM_RAMOS), 0, 0,
                       linha_base={"linhas": None, "ramos": 99.0})
        self.assertTrue(r["aprovado"])


class TesteLinhaDeComando(Base):
    def test_aprovado_sai_zero_com_texto(self):
        codigo, saida, _ = self.rodar("--relatorio", str(self.gravar("c.xml", COBERTURA)),
                                      "--minimo-linhas", "70", "--minimo-ramos", "50")
        self.assertEqual(codigo, 0)
        self.assertIn("Linhas: 75.0% (minimo 70.0%)", saida)
        self.assertTrue(saida.rstrip().endswith("APROVADO"))

    def test_padrao_e_noventa_e_reprova_com_um(self):
        codigo, saida, _ = self.rodar("--relatorio", str(self.gravar("c.xml", COBERTURA)))
        self.assertEqual(codigo, 1)
        self.assertIn("minimo 90.0%", saida)
        self.assertIn("FALHA: linhas", saida)
        self.assertTrue(saida.rstrip().endswith("REPROVADO"))

    def test_texto_lista_arquivo_abaixo_e_ramo_nao_medido(self):
        _, saida, _ = self.rodar("--relatorio", str(self.gravar("c.xml", COBERTURA_SEM_RAMOS)),
                                 "--minimo-ramos", "0", "--minimo-arquivo", "100")
        self.assertIn("Ramos: nao medido", saida)
        self.assertNotIn("abaixo do minimo por arquivo:", saida)
        codigo, saida, _ = self.rodar("--relatorio", str(self.gravar("l.info", LCOV)),
                                      "--minimo-linhas", "0", "--minimo-ramos", "0",
                                      "--minimo-arquivo", "80")
        self.assertEqual(codigo, 1)
        self.assertIn("abaixo do minimo por arquivo: src/a.js 50.0%", saida)

    def test_json_serve_de_linha_base_da_proxima_execucao(self):
        relatorio = str(self.gravar("c.xml", COBERTURA))
        codigo, saida, _ = self.rodar("--relatorio", relatorio, "--minimo-linhas", "0",
                                      "--minimo-ramos", "0", "--json")
        self.assertEqual(codigo, 0)
        base = self.gravar("base.json", saida.encode("utf-8"))
        self.assertEqual(json.loads(saida)["linhas"], 75.0)
        codigo, _, _ = self.rodar("--relatorio", str(self.gravar("l.info", LCOV)),
                                  "--minimo-linhas", "0", "--minimo-ramos", "0",
                                  "--linha-base", str(base))
        self.assertEqual(codigo, 1)

    def test_linha_base_invalida_sai_dois(self):
        codigo, _, erro = self.rodar("--relatorio", str(self.gravar("c.xml", COBERTURA)),
                                     "--linha-base", str(self.gravar("b.json", b"{nao")))
        self.assertEqual(codigo, 2)
        self.assertIn("linha de base", erro)

    def test_erro_de_entrada_sai_dois(self):
        codigo, saida, erro = self.rodar("--relatorio", str(Path(self.dir.name) / "x.xml"))
        self.assertEqual((codigo, saida), (2, ""))
        self.assertIn("ERRO: relatorio nao encontrado", erro)


if __name__ == "__main__":
    unittest.main()
