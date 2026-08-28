#!/usr/bin/env python3
"""Sincroniza a carga util da skill stack-ai-init com a raiz do repositorio de origem.

Subcomandos:
  verificar        compara assets/stack e assets/estrutura.json com a origem
  aplicar          reescreve a carga a partir da origem
  aceitar-manuais  registra o hash de origem dos arquivos mantidos a mao

Os arquivos listados em MANUAIS nunca sao sobrescritos: a carga leva uma variante
propria deles. Quando a origem muda, o script reporta revisar-manualmente ate que
alguem revise a variante e rode aceitar-manuais.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import shutil
import stat
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
CARGA = SKILL / "assets" / "stack"
ESTRUTURA = SKILL / "assets" / "estrutura.json"

# Caminhos, relativos a raiz de origem, que nao entram na carga.
EXCLUIDOS = (
    ".git",
    "specs",
    ".claude/settings.local.json",
    ".opencode/node_modules",
    ".opencode/package.json",
    ".opencode/package-lock.json",
    ".agents/skills/stack-ai-init",
    ".agents/skills/stack-ai-creator",
)

# Nomes de diretorio ou arquivo descartados em qualquer nivel.
NOMES_EXCLUIDOS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".DS_Store"}

# Arquivos cuja variante na carga e mantida a mao, nao copiada da origem.
MANUAIS = (".vscode/settings.json", ".agents/skills/README.md", "README.md")


def caminho_na_carga(rel: str) -> str:
    """.claude/skills -> dot-claude/skills"""
    partes = [("dot-" + p[1:]) if p.startswith(".") else p for p in rel.split("/")]
    return "/".join(partes)


def caminho_no_destino(rel: str) -> str:
    """dot-claude/skills -> .claude/skills"""
    partes = [("." + p[4:]) if p.startswith("dot-") else p for p in rel.split("/")]
    return "/".join(partes)


def excluido(rel: str, nome: str) -> bool:
    if nome in NOMES_EXCLUIDOS:
        return True
    return any(rel == e or rel.startswith(e + "/") for e in EXCLUIDOS)


def symlink_distribuivel(caminho: str, alvo: str) -> bool:
    """Symlink so entra na carga se apontar para algo que a carga leva junto.

    O symlink de descoberta de uma skill excluida (.claude/skills/stack-ai-init)
    chegaria quebrado no destino, porque a skill em si nao e distribuida.
    """
    if posixpath.isabs(alvo):
        return False
    destino = posixpath.normpath(posixpath.join(posixpath.dirname(caminho), alvo))
    if destino.startswith(".."):
        return False
    return not excluido(destino, posixpath.basename(destino))


def hash_arquivo(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def modo(caminho: Path) -> int:
    return stat.S_IMODE(caminho.lstat().st_mode)


def varrer_origem(raiz: Path) -> dict:
    """Arquivos, diretorios vazios e symlinks da origem, ja filtrados."""
    arquivos: dict[str, Path] = {}
    vazios: list[str] = []
    symlinks: list[dict] = []

    for atual, dirs, nomes in os.walk(raiz):
        atual_p = Path(atual)
        rel_dir = atual_p.relative_to(raiz).as_posix()
        rel_dir = "" if rel_dir == "." else rel_dir

        mantidos = []
        for d in sorted(dirs):
            rel = f"{rel_dir}/{d}" if rel_dir else d
            if excluido(rel, d):
                continue
            if (atual_p / d).is_symlink():
                alvo = os.readlink(atual_p / d)
                if symlink_distribuivel(rel, alvo):
                    symlinks.append({"caminho": rel, "alvo": alvo})
                continue
            mantidos.append(d)
        dirs[:] = mantidos

        for n in sorted(nomes):
            rel = f"{rel_dir}/{n}" if rel_dir else n
            if excluido(rel, n):
                continue
            p = atual_p / n
            if p.is_symlink():
                alvo = os.readlink(p)
                if symlink_distribuivel(rel, alvo):
                    symlinks.append({"caminho": rel, "alvo": alvo})
                continue
            arquivos[rel] = p

        if rel_dir and not any(atual_p.iterdir()):
            vazios.append(rel_dir)

    return {
        "arquivos": arquivos,
        "vazios": sorted(vazios),
        "symlinks": sorted(symlinks, key=lambda s: s["caminho"]),
    }


def varrer_carga() -> dict[str, Path]:
    """Arquivos ja presentes na carga, com caminho traduzido para o destino."""
    if not CARGA.is_dir():
        return {}
    achados: dict[str, Path] = {}
    for atual, dirs, nomes in os.walk(CARGA):
        dirs[:] = [d for d in sorted(dirs) if d not in NOMES_EXCLUIDOS]
        for n in sorted(nomes):
            if n in NOMES_EXCLUIDOS:
                continue
            p = Path(atual) / n
            rel_carga = p.relative_to(CARGA).as_posix()
            achados[caminho_no_destino(rel_carga)] = p
    return achados


def carregar_estrutura() -> dict:
    if not ESTRUTURA.is_file():
        return {"diretorios_vazios": [], "symlinks": [], "manuais": {}}
    dados = json.loads(ESTRUTURA.read_text(encoding="utf-8"))
    dados.setdefault("diretorios_vazios", [])
    dados.setdefault("symlinks", [])
    dados.setdefault("manuais", {})
    return dados


def comparar(raiz: Path) -> list[dict]:
    """Deriva entre origem e carga. Cada item tem caminho, situacao e detalhe."""
    origem = varrer_origem(raiz)
    na_carga = varrer_carga()
    estrutura = carregar_estrutura()
    itens: list[dict] = []

    for rel, fonte in sorted(origem["arquivos"].items()):
        alvo = na_carga.get(rel)
        if rel in MANUAIS:
            if alvo is None:
                itens.append({"caminho": rel, "situacao": "faltando-na-carga", "detalhe": "variante manual ausente"})
            elif estrutura["manuais"].get(rel) != hash_arquivo(fonte):
                itens.append({"caminho": rel, "situacao": "revisar-manualmente", "detalhe": "origem mudou desde a ultima revisao"})
            continue
        if alvo is None:
            itens.append({"caminho": rel, "situacao": "faltando-na-carga", "detalhe": ""})
        elif hash_arquivo(alvo) != hash_arquivo(fonte):
            itens.append({"caminho": rel, "situacao": "conteudo-diferente", "detalhe": ""})
        elif modo(alvo) != modo(fonte):
            itens.append({"caminho": rel, "situacao": "modo-diferente", "detalhe": f"{modo(alvo):o} na carga, {modo(fonte):o} na origem"})

    for rel in sorted(set(na_carga) - set(origem["arquivos"])):
        itens.append({"caminho": rel, "situacao": "sobrando-na-carga", "detalhe": ""})

    if estrutura["diretorios_vazios"] != origem["vazios"]:
        itens.append({"caminho": "assets/estrutura.json", "situacao": "estrutura-diferente", "detalhe": "diretorios_vazios"})
    if estrutura["symlinks"] != origem["symlinks"]:
        itens.append({"caminho": "assets/estrutura.json", "situacao": "estrutura-diferente", "detalhe": "symlinks"})

    return itens


def aplicar(raiz: Path) -> list[dict]:
    origem = varrer_origem(raiz)
    na_carga = varrer_carga()
    estrutura = carregar_estrutura()
    acoes: list[dict] = []

    for rel, fonte in sorted(origem["arquivos"].items()):
        if rel in MANUAIS:
            continue
        alvo = CARGA / caminho_na_carga(rel)
        igual = alvo.is_file() and hash_arquivo(alvo) == hash_arquivo(fonte) and modo(alvo) == modo(fonte)
        if igual:
            continue
        alvo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fonte, alvo)
        acoes.append({"caminho": rel, "situacao": "atualizado" if rel in na_carga else "adicionado", "detalhe": ""})

    for rel in sorted(set(na_carga) - set(origem["arquivos"])):
        na_carga[rel].unlink()
        acoes.append({"caminho": rel, "situacao": "removido", "detalhe": ""})

    for atual, dirs, nomes in os.walk(CARGA, topdown=False):
        p = Path(atual)
        if p != CARGA and not any(p.iterdir()):
            p.rmdir()

    manuais = {rel: estrutura["manuais"].get(rel, "") for rel in MANUAIS}
    nova = {
        "diretorios_vazios": origem["vazios"],
        "symlinks": origem["symlinks"],
        "manuais": manuais,
    }
    if nova != estrutura:
        ESTRUTURA.parent.mkdir(parents=True, exist_ok=True)
        ESTRUTURA.write_text(json.dumps(nova, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        acoes.append({"caminho": "assets/estrutura.json", "situacao": "atualizado", "detalhe": ""})

    return acoes


def aceitar_manuais(raiz: Path) -> list[dict]:
    estrutura = carregar_estrutura()
    acoes: list[dict] = []
    for rel in MANUAIS:
        fonte = raiz / rel
        if not fonte.is_file():
            acoes.append({"caminho": rel, "situacao": "erro", "detalhe": "ausente na origem"})
            continue
        atual = hash_arquivo(fonte)
        if estrutura["manuais"].get(rel) == atual:
            continue
        estrutura["manuais"][rel] = atual
        acoes.append({"caminho": rel, "situacao": "registrado", "detalhe": atual[:12]})
    if acoes:
        ESTRUTURA.write_text(json.dumps(estrutura, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return acoes


def imprimir(itens: list[dict], vazio: str) -> None:
    if not itens:
        print(vazio)
        return
    largura = max(len(i["situacao"]) for i in itens)
    for i in itens:
        detalhe = f"  ({i['detalhe']})" if i["detalhe"] else ""
        print(f"{i['situacao']:<{largura}}  {i['caminho']}{detalhe}")
    print(f"\n{len(itens)} item(ns)")


def raiz_padrao() -> Path:
    return SKILL.parents[2]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("comando", choices=("verificar", "aplicar", "aceitar-manuais"))
    parser.add_argument("--origem", default=None, help="raiz do repositorio que serve de molde")
    parser.add_argument("--json", action="store_true", help="saida em JSON")
    args = parser.parse_args(argv)

    raiz = Path(args.origem).resolve() if args.origem else raiz_padrao()
    if not (raiz / "AGENTS.md").is_file() or not (raiz / ".agents" / "skills").is_dir():
        print(f"origem nao parece a raiz da stack: {raiz}", file=sys.stderr)
        return 2

    if args.comando == "verificar":
        itens = comparar(raiz)
        if args.json:
            print(json.dumps(itens, indent=2, ensure_ascii=False))
        else:
            imprimir(itens, "Carga em dia com a origem.")
        return 1 if itens else 0

    if args.comando == "aplicar":
        acoes = aplicar(raiz)
        pendentes = [i for i in comparar(raiz) if i["situacao"] == "revisar-manualmente"]
        if args.json:
            print(json.dumps(acoes + pendentes, indent=2, ensure_ascii=False))
        else:
            imprimir(acoes, "Nada a aplicar.")
            if pendentes:
                print()
                imprimir(pendentes, "")
        return 1 if pendentes else 0

    acoes = aceitar_manuais(raiz)
    if args.json:
        print(json.dumps(acoes, indent=2, ensure_ascii=False))
    else:
        imprimir(acoes, "Hashes manuais ja registrados.")
    return 2 if any(a["situacao"] == "erro" for a in acoes) else 0


if __name__ == "__main__":
    sys.exit(main())
