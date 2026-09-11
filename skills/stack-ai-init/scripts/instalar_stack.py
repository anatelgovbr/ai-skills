#!/usr/bin/env python3
"""Instala a stack minima de IA em um repositorio de destino.

Subcomandos:
  simular    calcula o que seria feito, sem escrever nada
  instalar   aplica a carga util no destino
  verificar  compara uma instalacao existente com a carga, sem escrever nada

O script nao le a codebase de destino e nao decide nada sobre ela: copia os
artefatos da carga, cria os diretorios e symlinks declarados em
assets/estrutura.json e mescla os tres arquivos que pertencem ao destino
(.gitignore, .vscode/settings.json e .claude/settings.json). Arquivo que ja
existe e preservado.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
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
# Linha que so entra quando o destino ainda nao tem `specs/`. A stack e spec
# first e trata a spec como descartavel, entao o destino novo nasce ignorando a
# pasta. Destino que ja tem `specs/` fica como esta: se ja ignorava, continua
# ignorando; se versionava, a stack nao muda isso por ele.
LINHA_CONDICIONAL_SPECS = "/specs"

# Arquivos do destino que recebem acrescimo de chaves.
MESCLA_JSON = (".vscode/settings.json", ".claude/settings.json")
# Chaves cujo valor e objeto e cujas subchaves ausentes tambem sao acrescentadas.
CHAVES_OBJETO = (
    "chat.agentSkillsLocations",
    "chat.promptFilesRecommendations",
    "extraKnownMarketplaces",
    "enabledPlugins",
)

# Nome do marketplace: precisa ser unico entre repositorios, porque o Claude Code
# guarda um caminho so por nome no registro da maquina. Vale o nome que o destino
# ja declara; a derivacao do diretorio e so o padrao de criacao. Os arquivos abaixo
# trazem o placeholder no lugar do nome.
PLUGIN = "stack-ai"
PREFIXO_MARKETPLACE = "stack-ai-"
PLACEHOLDER_MARKETPLACE = "{{MARKETPLACE}}"
SUBSTITUIVEIS = (".claude-plugin/marketplace.json", ".claude/settings.json")

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


def hash_texto(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def nome_derivado(destino: Path) -> str:
    """stack-ai-<diretorio de destino>, reduzido a [a-z0-9-]."""
    sigla = re.sub(r"[^a-z0-9]+", "-", destino.name.lower()).strip("-")
    return PREFIXO_MARKETPLACE + (sigla or "repo")


def json_do_destino(p: Path) -> dict | None:
    """Objeto JSON do arquivo, ou None quando ele falta ou nao e um objeto."""
    try:
        dados = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return dados if isinstance(dados, dict) else None


def nome_ja_declarado(destino: Path) -> str | None:
    """Nome do marketplace que o destino ja declara, ou None quando nao ha nenhum.

    A fonte e o `marketplace.json`, que e quem declara. O `settings.json` entra so
    como reserva, e por `enabledPlugins`: a chave e `<plugin>@<marketplace>`, entao
    ela diz de qual marketplace o plugin da stack esta ligado. Marketplace de outro
    plugin, que o time tenha declarado, nao e adotado.
    """
    dados = json_do_destino(destino / ".claude-plugin" / "marketplace.json")
    if dados:
        nome = dados.get("name")
        if isinstance(nome, str) and nome and nome != PLACEHOLDER_MARKETPLACE:
            return nome

    dados = json_do_destino(destino / ".claude" / "settings.json")
    if dados and isinstance(dados.get("enabledPlugins"), dict):
        for chave in dados["enabledPlugins"]:
            plugin, arroba, marketplace = str(chave).partition("@")
            if arroba and plugin == PLUGIN and marketplace:
                return marketplace
    return None


def nome_do_marketplace(destino: Path) -> str:
    """O nome que o destino ja declara, ou o derivado quando ainda nao ha nenhum.

    O nome so precisa ser unico entre repositorios, e uma instalacao que ja tem o
    seu funciona. Renomear nao traz ganho, quebraria a chave `<plugin>@<marketplace>`
    ja ligada e deixaria uma entrada orfa no registro da maquina. Entao a carga adota
    o nome do destino, e nada e acrescentado ao lado do que ja esta la.
    """
    return nome_ja_declarado(destino) or nome_derivado(destino)


def texto_da_carga(rel: str, fonte: Path, marketplace: str) -> str | None:
    """Conteudo com o nome do marketplace resolvido, ou None quando o arquivo
    nao depende do destino e pode ser copiado byte a byte."""
    if rel not in SUBSTITUIVEIS:
        return None
    bruto = fonte.read_text(encoding="utf-8")
    return bruto.replace(PLACEHOLDER_MARKETPLACE, marketplace)


def hash_da_carga(fonte: Path, rendido: str | None) -> str:
    return hash_arquivo(fonte) if rendido is None else hash_texto(rendido)


def escrever_da_carga(p: Path, fonte: Path, rendido: str | None) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    if rendido is None:
        shutil.copy2(fonte, p)
    else:
        p.write_text(rendido, encoding="utf-8")


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


def mesclar_linhas(atual: str, carga: str, tem_specs: bool = False) -> tuple[str, list[str]]:
    """Acrescenta ao final as linhas da carga que faltam. Idempotente.

    Com `tem_specs`, a linha que ignora `specs/` fica de fora. Quem ja tem a
    pasta decide sozinho se a versiona: se ela ja estava no `.gitignore`,
    continua; se nao estava, a stack nao coloca.
    """
    presentes = {l.strip() for l in atual.splitlines() if l.strip()}
    faltando = []
    for linha in carga.splitlines():
        if tem_specs and linha.strip() == LINHA_CONDICIONAL_SPECS:
            continue
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
    # Resolvido antes da primeira escrita, para que marketplace.json e settings.json
    # recebam o mesmo nome mesmo quando o primeiro e criado durante esta execucao.
    marketplace = nome_do_marketplace(destino)
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
        rendido = texto_da_carga(rel, fonte, marketplace)

        if rel == MESCLA_LINHAS:
            if not existe:
                if aplicar:
                    p.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(fonte, p)
                registrar(rel, "arquivo", "criado")
                continue
            conteudo, faltando = mesclar_linhas(p.read_text(encoding="utf-8"), fonte.read_text(encoding="utf-8"), (destino / "specs").is_dir())
            if not faltando:
                registrar(rel, "arquivo", "ignorado-igual", "todas as linhas ja presentes")
            else:
                if aplicar:
                    p.write_text(conteudo, encoding="utf-8")
                registrar(rel, "arquivo", "mesclado", f"{len(faltando)} linha(s) acrescentada(s)")
            continue

        if rel in MESCLA_JSON:
            carga_texto = rendido if rendido is not None else fonte.read_text(encoding="utf-8")
            if not existe:
                if aplicar:
                    escrever_da_carga(p, fonte, rendido)
                registrar(rel, "arquivo", "criado")
                continue
            conteudo, chaves, erro = mesclar_json(p.read_text(encoding="utf-8"), carga_texto)
            if erro:
                registrar(rel, "arquivo", "manual", f"{erro}; acrescente a mao: {', '.join(json.loads(carga_texto))}")
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

        if existe and hash_arquivo(p) == hash_da_carga(fonte, rendido):
            registrar(rel, "arquivo", "ignorado-igual")
        elif existe and not sobrescrever:
            registrar(rel, "arquivo", "ignorado-existe", "difere da carga; use --sobrescrever para atualizar")
        else:
            if aplicar:
                escrever_da_carga(p, fonte, rendido)
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
                rendido = texto_da_carga(acao["caminho"], fonte, marketplace)
                if not p.is_file() or hash_arquivo(p) != hash_da_carga(fonte, rendido):
                    acao["acao"], acao["detalhe"] = "erro", "conteudo nao confere apos a copia"

    return acoes


def verificar(destino: Path) -> list[dict]:
    carga = arquivos_da_carga()
    estrutura = carregar_estrutura()
    marketplace = nome_do_marketplace(destino)
    itens: list[dict] = []

    def registrar(caminho, tipo, acao, detalhe=""):
        itens.append({"caminho": caminho, "tipo": tipo, "acao": acao, "detalhe": detalhe})

    for rel in estrutura["diretorios_vazios"]:
        registrar(rel, "diretorio", "igual" if (destino / rel).is_dir() else "ausente")

    for rel, fonte in carga.items():
        p = destino / rel
        rendido = texto_da_carga(rel, fonte, marketplace)
        if not p.exists():
            registrar(rel, "arquivo", "ausente")
            continue
        if rel in PROTEGIDOS:
            registrar(rel, "arquivo", "proprio-do-destino")
        elif rel == MESCLA_LINHAS:
            _, faltando = mesclar_linhas(p.read_text(encoding="utf-8"), fonte.read_text(encoding="utf-8"), (destino / "specs").is_dir())
            registrar(rel, "arquivo", "igual" if not faltando else "divergente", f"{len(faltando)} linha(s) da carga faltando" if faltando else "")
        elif rel in MESCLA_JSON:
            carga_texto = rendido if rendido is not None else fonte.read_text(encoding="utf-8")
            _, chaves, erro = mesclar_json(p.read_text(encoding="utf-8"), carga_texto)
            if erro:
                registrar(rel, "arquivo", "manual", erro)
            else:
                registrar(rel, "arquivo", "igual" if not chaves else "divergente", ", ".join(chaves))
        elif hash_arquivo(p) == hash_da_carga(fonte, rendido):
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
    if destino == SKILL or destino in SKILL.parents:
        print("destino hospeda a propria skill; informe outro repositorio", file=sys.stderr)
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
