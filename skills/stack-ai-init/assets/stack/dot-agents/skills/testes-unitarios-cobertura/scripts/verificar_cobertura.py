#!/usr/bin/env python3
"""Gate de cobertura de testes: le o relatorio e reprova abaixo do minimo.

Formatos aceitos: Cobertura XML (pytest-cov, PHPUnit, Jest, Vitest, coverlet),
LCOV (Jest, Vitest, c8, gcov2lcov) e JaCoCo XML (Java, Kotlin).

Codigos de saida: 0 aprovado, 1 reprovado, 2 erro de entrada.
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

MINIMO_PADRAO = 90.0
MAIOR_RELATORIO = 200 * 1024 * 1024
CONDICAO = re.compile(r"\((\d+)/(\d+)\)")


class ErroDeEntrada(Exception):
    """Relatorio ausente, ilegivel ou em formato desconhecido."""


@dataclass
class Arquivo:
    nome: str
    linhas_total: int = 0
    linhas_cobertas: int = 0
    ramos_total: int = 0
    ramos_cobertos: int = 0


@dataclass
class Medicao:
    formato: str
    arquivos: dict = field(default_factory=dict)

    def arquivo(self, nome: str) -> Arquivo:
        return self.arquivos.setdefault(nome, Arquivo(nome))

    def soma(self, campo: str) -> int:
        return sum(getattr(a, campo) for a in self.arquivos.values())


def percentual(cobertos: int, total: int):
    if total == 0:
        return None
    return round(100.0 * cobertos / total, 2)


def ler_bytes(caminho: Path) -> bytes:
    if not caminho.is_file():
        raise ErroDeEntrada(f"relatorio nao encontrado: {caminho}")
    if caminho.stat().st_size > MAIOR_RELATORIO:
        raise ErroDeEntrada(f"relatorio maior que {MAIOR_RELATORIO} bytes: {caminho}")
    return caminho.read_bytes()


def xml_seguro(dados: bytes) -> ET.Element:
    # Relatorio de cobertura nunca precisa declarar entidade; recusar fecha XXE e expansao.
    if b"<!ENTITY" in dados:
        raise ErroDeEntrada("relatorio XML declara entidade; recusado por seguranca")
    try:
        return ET.fromstring(dados)
    except ET.ParseError as erro:
        raise ErroDeEntrada(f"XML invalido: {erro}") from erro


def detectar_formato(dados: bytes) -> str:
    inicio = dados.lstrip()[:200]
    if inicio.startswith((b"TN:", b"SF:")):
        return "lcov"
    if inicio.startswith(b"<"):
        raiz = xml_seguro(dados).tag
        if raiz == "coverage":
            return "cobertura"
        if raiz == "report":
            return "jacoco"
        raise ErroDeEntrada(f"XML com raiz desconhecida: <{raiz}>")
    raise ErroDeEntrada("formato nao reconhecido; informe --formato")


def ler_cobertura(dados: bytes) -> Medicao:
    medicao = Medicao("cobertura")
    for classe in xml_seguro(dados).iter("class"):
        arquivo = medicao.arquivo(classe.get("filename", "?"))
        for linha in classe.iter("line"):
            arquivo.linhas_total += 1
            if int(linha.get("hits", "0")) > 0:
                arquivo.linhas_cobertas += 1
            achado = CONDICAO.search(linha.get("condition-coverage", ""))
            if linha.get("branch") == "true" and achado:
                arquivo.ramos_cobertos += int(achado.group(1))
                arquivo.ramos_total += int(achado.group(2))
    return medicao


def ler_lcov(dados: bytes) -> Medicao:
    medicao = Medicao("lcov")
    atual = None
    for bruta in dados.decode("utf-8", errors="replace").splitlines():
        chave, _, valor = bruta.strip().partition(":")
        if chave == "SF":
            atual = medicao.arquivo(valor)
        elif atual is None:
            continue
        elif chave == "DA":
            atual.linhas_total += 1
            if int(valor.split(",")[1]) > 0:
                atual.linhas_cobertas += 1
        elif chave == "BRDA":
            atual.ramos_total += 1
            if valor.split(",")[3] not in ("-", "0"):
                atual.ramos_cobertos += 1
        elif chave == "end_of_record":
            atual = None
    return medicao


def ler_jacoco(dados: bytes) -> Medicao:
    medicao = Medicao("jacoco")
    for pacote in xml_seguro(dados).iter("package"):
        for fonte in pacote.findall("sourcefile"):
            arquivo = medicao.arquivo(f"{pacote.get('name', '')}/{fonte.get('name', '?')}")
            for contador in fonte.findall("counter"):
                perdidos = int(contador.get("missed", "0"))
                cobertos = int(contador.get("covered", "0"))
                if contador.get("type") == "LINE":
                    arquivo.linhas_total += perdidos + cobertos
                    arquivo.linhas_cobertas += cobertos
                elif contador.get("type") == "BRANCH":
                    arquivo.ramos_total += perdidos + cobertos
                    arquivo.ramos_cobertos += cobertos
    return medicao


LEITORES = {"cobertura": ler_cobertura, "lcov": ler_lcov, "jacoco": ler_jacoco}


def medir(caminho: Path, formato: str = "auto") -> Medicao:
    dados = ler_bytes(caminho)
    if formato == "auto":
        formato = detectar_formato(dados)
    try:
        medicao = LEITORES[formato](dados)
    except (ValueError, IndexError) as erro:
        raise ErroDeEntrada(f"relatorio {formato} malformado: {erro}") from erro
    if not medicao.arquivos or medicao.soma("linhas_total") == 0:
        raise ErroDeEntrada("relatorio sem nenhuma linha medida; os testes rodaram com cobertura?")
    return medicao


def resumo(medicao: Medicao) -> dict:
    return {
        "formato": medicao.formato,
        "arquivos": len(medicao.arquivos),
        "linhas": percentual(medicao.soma("linhas_cobertas"), medicao.soma("linhas_total")),
        "ramos": percentual(medicao.soma("ramos_cobertos"), medicao.soma("ramos_total")),
    }


def avaliar(medicao: Medicao, minimo_linhas: float, minimo_ramos: float,
            minimo_arquivo: float = 0.0, linha_base: dict = None) -> dict:
    total = resumo(medicao)
    falhas = []
    if total["linhas"] < minimo_linhas:
        falhas.append(f"linhas {total['linhas']}% abaixo do minimo {minimo_linhas}%")
    if minimo_ramos > 0:
        if total["ramos"] is None:
            falhas.append("relatorio sem medicao de ramos; habilite a cobertura de ramos na ferramenta de teste")
        elif total["ramos"] < minimo_ramos:
            falhas.append(f"ramos {total['ramos']}% abaixo do minimo {minimo_ramos}%")
    abaixo = []
    for arquivo in sorted(medicao.arquivos.values(), key=lambda a: a.nome):
        taxa = percentual(arquivo.linhas_cobertas, arquivo.linhas_total)
        if taxa is not None and taxa < minimo_arquivo:
            abaixo.append({"arquivo": arquivo.nome, "linhas": taxa})
    if abaixo:
        falhas.append(f"{len(abaixo)} arquivo(s) abaixo do minimo por arquivo {minimo_arquivo}%")
    if linha_base:
        for metrica in ("linhas", "ramos"):
            anterior, atual = linha_base.get(metrica), total[metrica]
            if anterior is not None and atual is not None and atual < anterior:
                falhas.append(f"{metrica} cairam de {anterior}% para {atual}% em relacao a linha de base")
    return {**total, "minimos": {"linhas": minimo_linhas, "ramos": minimo_ramos,
                                 "arquivo": minimo_arquivo},
            "arquivos_abaixo": abaixo, "falhas": falhas, "aprovado": not falhas}


def formatar_texto(resultado: dict) -> str:
    ramos = "nao medido" if resultado["ramos"] is None else f"{resultado['ramos']}%"
    saida = [
        f"Formato: {resultado['formato']} | arquivos medidos: {resultado['arquivos']}",
        f"Linhas: {resultado['linhas']}% (minimo {resultado['minimos']['linhas']}%)",
        f"Ramos: {ramos} (minimo {resultado['minimos']['ramos']}%)",
    ]
    for item in resultado["arquivos_abaixo"]:
        saida.append(f"  abaixo do minimo por arquivo: {item['arquivo']} {item['linhas']}%")
    saida.extend(f"FALHA: {falha}" for falha in resultado["falhas"])
    saida.append("APROVADO" if resultado["aprovado"] else "REPROVADO")
    return "\n".join(saida)


def ler_linha_base(caminho: Path) -> dict:
    try:
        return json.loads(ler_bytes(caminho))
    except json.JSONDecodeError as erro:
        raise ErroDeEntrada(f"linha de base nao e JSON valido: {erro}") from erro


def principal(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--relatorio", required=True, type=Path)
    parser.add_argument("--formato", choices=["auto", *LEITORES], default="auto")
    parser.add_argument("--minimo-linhas", type=float, default=MINIMO_PADRAO)
    parser.add_argument("--minimo-ramos", type=float, default=MINIMO_PADRAO)
    parser.add_argument("--minimo-arquivo", type=float, default=0.0)
    parser.add_argument("--linha-base", type=Path,
                        help="JSON de uma execucao anterior com --json; reprova se a cobertura cair")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        linha_base = ler_linha_base(args.linha_base) if args.linha_base else None
        resultado = avaliar(medir(args.relatorio, args.formato), args.minimo_linhas,
                            args.minimo_ramos, args.minimo_arquivo, linha_base)
    except ErroDeEntrada as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        return 2
    print(json.dumps(resultado, ensure_ascii=False, indent=2) if args.json
          else formatar_texto(resultado))
    return 0 if resultado["aprovado"] else 1


if __name__ == "__main__":
    sys.exit(principal())
