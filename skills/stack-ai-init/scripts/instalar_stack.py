#!/usr/bin/env python3
"""Instala a stack minima de IA em um repositorio de destino.

Subcomandos:
  simular    calcula o que seria feito, sem escrever nada
  instalar   aplica a carga util no destino
  verificar  compara uma instalacao existente com a carga, sem escrever nada

O script nao le a codebase de destino e nao decide nada sobre ela: copia os
artefatos da carga, cria os diretorios e symlinks declarados em
assets/estrutura.json e mescla os dois arquivos que pertencem ao destino
(.gitignore e .vscode/settings.json). Arquivo que ja existe e preservado.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
CARGA = SKILL / "assets" / "stack"
ESTRUTURA = SKILL / "assets" / "estrutura.json"

# Arquivos que o destino preenche com conteudo proprio: instalados so quando
# ausentes, jamais substituidos, nem com --sobrescrever.
PROTEGIDOS = ("README.md", "AGENTS.md", "CLAUDE.md")

# Arquivo do destino que recebe acrescimo linha a linha.
MESCLA_LINHAS = ".gitignore"
CABECALHO_GITIGNORE = "# Stack de IA"

# Arquivo do destino que recebe acrescimo de chaves.
MESCLA_JSON = ".vscode/settings.json"
# Chaves cujo valor e objeto e cujas subchaves ausentes tambem sao acrescentadas.
CHAVES_OBJETO = ("chat.agentSkillsLocations", "chat.promptFilesRecommendations")

NOMES_IGNORADOS = {"__pycache__", ".DS_Store"}

LIMPAS = {"criado", "ignorado-igual", "mesclado", "symlink", "igual", "proprio-do-destino", "substituido"}


def caminho_na_carga(rel: str) -> str:
    return "/".join([("dot-" + p[1:]) if p.startswith(".") else p for p in rel.split("/")])


def caminho_no_destino(rel: str) -> str:
    return "/".join([("." + p[4:]) if p.startswith("dot-") else p for p in rel.split("/")])


def hash_arquivo(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def arquivos_da_carga() -> dict[str, Path]:
    """Caminho no destino -> arquivo correspondente na carga."""
    achados: dict[str, Path] = {}
    for atual, dirs, nomes in os.walk(CARGA):
        dirs[:] = [d for d in sorted(dirs) if d not in NOMES_IGNORADOS]
        for n in sorted(nomes):
            if n in NOMES_IGNORADOS:
                continue
            p = Path(atual) / n
            achados[caminho_no_destino(p.relative_to(CARGA).as_posix())] = p
    return dict(sorted(achados.items()))


def carregar_estrutura() -> dict:
    dados = json.loads(ESTRUTURA.read_text(encoding="utf-8"))
    return {
        "diretorios_vazios": dados.get("diretorios_vazios", []),
        "symlinks": dados.get("symlinks", []),
    }


def mesclar_linhas(atual: str, carga: str) -> tuple[str, list[str]]:
    """Acrescenta ao final as linhas da carga que faltam. Idempotente."""
    presentes = {l.strip() for l in atual.splitlines() if l.strip()}
    faltando = []
    for linha in carga.splitlines():
        if linha.strip() and linha.strip() not in presentes and linha.strip() not in {f.strip() for f in faltando}:
            faltando.append(linha)
    if not faltando:
        return atual, []
    bloco = []
    if atual and not atual.endswith("\n"):
        bloco.append("")
    bloco.append("")
    if CABECALHO_GITIGNORE not in presentes:
        bloco.append(CABECALHO_GITIGNORE)
    bloco.extend(faltando)
    return atual + "\n".join(bloco) + "\n", faltando


def mesclar_json(atual: str, carga: str) -> tuple[str | None, list[str], str]:
    """Acrescenta chaves ausentes. Devolve (conteudo, chaves acrescentadas, erro)."""
    try:
        dados = json.loads(atual)
    except json.JSONDecodeError as e:
        return None, [], f"JSON nao estrito ({e.msg}, linha {e.lineno})"
    if not isinstance(dados, dict):
        return None, [], "raiz do JSON nao e um objeto"
    novo = json.loads(carga)
    acrescentadas: list[str] = []
    for chave, valor in novo.items():
        if chave not in dados:
            dados[chave] = valor
            acrescentadas.append(chave)
        elif chave in CHAVES_OBJETO and isinstance(valor, dict) and isinstance(dados[chave], dict):
            for sub, subvalor in valor.items():
                if sub not in dados[chave]:
                    dados[chave][sub] = subvalor
                    acrescentadas.append(f"{chave} > {sub}")
    if not acrescentadas:
        return atual, [], ""
    return json.dumps(dados, indent=4, ensure_ascii=False) + "\n", acrescentadas, ""


def alvo_do_symlink(caminho: str, alvo: str) -> str:
    """Caminho, relativo a raiz do destino, para onde o symlink aponta."""
    return posixpath.normpath(posixpath.join(posixpath.dirname(caminho), alvo))


def instalar(destino: Path, sobrescrever: bool, aplicar: bool) -> list[dict]:
    carga = arquivos_da_carga()
    estrutura = carregar_estrutura()
    acoes: list[dict] = []

    def registrar(caminho, tipo, acao, detalhe=""):
        acoes.append({"caminho": caminho, "tipo": tipo, "acao": acao, "detalhe": detalhe})

    for rel in estrutura["diretorios_vazios"]:
        p = destino / rel
        if p.is_dir():
            registrar(rel, "diretorio", "ignorado-igual")
        elif p.exists():
            registrar(rel, "diretorio", "erro", "existe e nao e diretorio")
        else:
            if aplicar:
                p.mkdir(parents=True, exist_ok=True)
            registrar(rel, "diretorio", "criado")

    for rel, fonte in carga.items():
        p = destino / rel
        existe = p.exists()

        if rel == MESCLA_LINHAS:
            if not existe:
                if aplicar:
                    p.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(fonte, p)
                registrar(rel, "arquivo", "criado")
                continue
            conteudo, faltando = mesclar_linhas(p.read_text(encoding="utf-8"), fonte.read_text(encoding="utf-8"))
            if not faltando:
                registrar(rel, "arquivo", "ignorado-igual", "todas as linhas ja presentes")
            else:
                if aplicar:
                    p.write_text(conteudo, encoding="utf-8")
                registrar(rel, "arquivo", "mesclado", f"{len(faltando)} linha(s) acrescentada(s)")
            continue

        if rel == MESCLA_JSON:
            if not existe:
                if aplicar:
                    p.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(fonte, p)
                registrar(rel, "arquivo", "criado")
                continue
            conteudo, chaves, erro = mesclar_json(p.read_text(encoding="utf-8"), fonte.read_text(encoding="utf-8"))
            if erro:
                registrar(rel, "arquivo", "manual", f"{erro}; acrescente a mao: {', '.join(json.loads(fonte.read_text(encoding='utf-8')))}")
            elif not chaves:
                registrar(rel, "arquivo", "ignorado-igual", "todas as chaves ja presentes")
            else:
                if aplicar:
                    p.write_text(conteudo, encoding="utf-8")
                resumo = ", ".join(chaves[:4]) + (f" e mais {len(chaves) - 4}" if len(chaves) > 4 else "")
                registrar(rel, "arquivo", "mesclado", f"{len(chaves)} chave(s): {resumo}")
            continue

        if rel in PROTEGIDOS:
            if not existe:
                if aplicar:
                    shutil.copy2(fonte, p)
                registrar(rel, "arquivo", "criado")
            elif hash_arquivo(p) == hash_arquivo(fonte):
                registrar(rel, "arquivo", "ignorado-igual")
            else:
                registrar(rel, "arquivo", "ignorado-protegido", "conteudo do destino, nunca substituido")
            continue

        if existe and hash_arquivo(p) == hash_arquivo(fonte):
            registrar(rel, "arquivo", "ignorado-igual")
        elif existe and not sobrescrever:
            registrar(rel, "arquivo", "ignorado-existe", "difere da carga; use --sobrescrever para atualizar")
        else:
            if aplicar:
                p.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(fonte, p)
            registrar(rel, "arquivo", "substituido" if existe else "criado")

    for link in estrutura["symlinks"]:
        rel, alvo = link["caminho"], link["alvo"]
        p = destino / rel
        if p.is_symlink():
            atual = os.readlink(p)
            if atual == alvo:
                registrar(rel, "symlink", "ignorado-igual")
            else:
                registrar(rel, "symlink", "ignorado-existe", f"aponta para {atual}")
            continue
        if p.exists():
            registrar(rel, "symlink", "ignorado-existe", "ja existe como diretorio real")
            continue
        if not aplicar:
            registrar(rel, "symlink", "symlink", f"-> {alvo}")
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.symlink(alvo, p)
            registrar(rel, "symlink", "symlink", f"-> {alvo}")
        except OSError as e:
            fonte_dir = CARGA / caminho_na_carga(alvo_do_symlink(rel, alvo))
            if not fonte_dir.is_dir():
                registrar(rel, "symlink", "erro", f"symlink falhou ({e.strerror}) e {alvo} nao esta na carga")
                continue
            shutil.copytree(fonte_dir, p, dirs_exist_ok=True)
            registrar(rel, "symlink", "symlink-degradado", f"symlink falhou ({e.strerror}); copia real no lugar")

    if aplicar:
        for acao in acoes:
            if acao["tipo"] == "arquivo" and acao["acao"] in ("criado", "substituido"):
                p, fonte = destino / acao["caminho"], carga[acao["caminho"]]
                if not p.is_file() or hash_arquivo(p) != hash_arquivo(fonte):
                    acao["acao"], acao["detalhe"] = "erro", "conteudo nao confere apos a copia"

    return acoes


def verificar(destino: Path) -> list[dict]:
    carga = arquivos_da_carga()
    estrutura = carregar_estrutura()
    itens: list[dict] = []

    def registrar(caminho, tipo, acao, detalhe=""):
        itens.append({"caminho": caminho, "tipo": tipo, "acao": acao, "detalhe": detalhe})

    for rel in estrutura["diretorios_vazios"]:
        registrar(rel, "diretorio", "igual" if (destino / rel).is_dir() else "ausente")

    for rel, fonte in carga.items():
        p = destino / rel
        if not p.exists():
            registrar(rel, "arquivo", "ausente")
            continue
        if rel in PROTEGIDOS:
            registrar(rel, "arquivo", "proprio-do-destino")
        elif rel == MESCLA_LINHAS:
            _, faltando = mesclar_linhas(p.read_text(encoding="utf-8"), fonte.read_text(encoding="utf-8"))
            registrar(rel, "arquivo", "igual" if not faltando else "divergente", f"{len(faltando)} linha(s) da carga faltando" if faltando else "")
        elif rel == MESCLA_JSON:
            _, chaves, erro = mesclar_json(p.read_text(encoding="utf-8"), fonte.read_text(encoding="utf-8"))
            if erro:
                registrar(rel, "arquivo", "manual", erro)
            else:
                registrar(rel, "arquivo", "igual" if not chaves else "divergente", ", ".join(chaves))
        elif hash_arquivo(p) == hash_arquivo(fonte):
            registrar(rel, "arquivo", "igual")
        else:
            registrar(rel, "arquivo", "divergente")

    for link in estrutura["symlinks"]:
        rel, alvo = link["caminho"], link["alvo"]
        p = destino / rel
        if p.is_symlink():
            registrar(rel, "symlink", "igual" if os.readlink(p) == alvo else "divergente", os.readlink(p))
        elif p.is_dir():
            registrar(rel, "symlink", "divergente", "diretorio real no lugar do symlink")
        else:
            registrar(rel, "symlink", "ausente")

    return itens


def imprimir(itens: list[dict], detalhado: bool) -> None:
    if not itens:
        print("Nada a fazer.")
        return
    grupos: dict[str, list[dict]] = {}
    for i in itens:
        grupos.setdefault(i["acao"], []).append(i)
    for acao in sorted(grupos):
        linhas = grupos[acao]
        print(f"\n{acao} ({len(linhas)})")
        mostrados = linhas if detalhado or len(linhas) <= 12 else linhas[:12]
        for i in mostrados:
            detalhe = f"  ({i['detalhe']})" if i["detalhe"] else ""
            print(f"  {i['caminho']}{detalhe}")
        if len(mostrados) < len(linhas):
            print(f"  ... e mais {len(linhas) - len(mostrados)}; use --detalhado")
    pendentes = [i for i in itens if i["acao"] not in LIMPAS]
    print(f"\n{len(itens)} item(ns), {len(pendentes)} pendente(s)")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("comando", choices=("simular", "instalar", "verificar"))
    parser.add_argument("--destino", required=True, help="raiz do repositorio que recebe a stack")
    parser.add_argument("--sobrescrever", action="store_true", help="atualiza arquivo da stack que ja existe e difere")
    parser.add_argument("--detalhado", action="store_true", help="lista todos os itens de cada grupo")
    parser.add_argument("--json", action="store_true", help="saida em JSON")
    args = parser.parse_args(argv)

    if not CARGA.is_dir() or not ESTRUTURA.is_file():
        print(f"carga util ausente em {CARGA}", file=sys.stderr)
        return 2

    destino = Path(args.destino).resolve()
    if not destino.is_dir():
        print(f"destino inexistente: {destino}", file=sys.stderr)
        return 2
    if destino == SKILL.parents[2]:
        print("destino e a propria raiz que hospeda a skill; informe outro repositorio", file=sys.stderr)
        return 2

    if args.comando == "verificar":
        itens = verificar(destino)
    else:
        itens = instalar(destino, args.sobrescrever, aplicar=args.comando == "instalar")

    if args.json:
        print(json.dumps(itens, indent=2, ensure_ascii=False))
    else:
        if not (destino / ".git").exists():
            print(f"aviso: {destino} nao e um repositorio git")
        imprimir(itens, args.detalhado)

    if any(i["acao"] == "erro" for i in itens):
        return 2
    return 1 if any(i["acao"] not in LIMPAS for i in itens) else 0


if __name__ == "__main__":
    sys.exit(main())
