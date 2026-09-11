#!/usr/bin/env python3
"""
mcp/server.py — Geo-Explorer MCP Server (MCP SDK v2)
======================================================
Expõe as ferramentas do projeto Geo-Explorer via Model Context Protocol (MCP).

Modos de transporte disponíveis:
  1. stdio  (padrão) — usado localmente pelo IBM Bob
  2. sse    — HTTP/SSE para acesso remoto via HTTPS ou API (legado)
  3. http   — Streamable HTTP para acesso remoto moderno

Uso:
  # Modo stdio (IBM Bob local):
  python3 mcp/server.py

  # Modo SSE para acesso remoto / HTTPS (porta padrão 8000):
  python3 mcp/server.py --transport sse --host 0.0.0.0 --port 8000

  # Modo Streamable HTTP (MCP v2 moderno):
  python3 mcp/server.py --transport http --host 0.0.0.0 --port 8000

Ferramentas expostas:
  - consultar_trilha    → consulta trilha por tecnologia em data/trilhas_geo.json
  - gerar_desafio       → valida parâmetros para geração de desafio de programação
  - gerar_certificado   → gera certificado fictício de conclusão de trilha
  - listar_trilhas      → lista todas as trilhas disponíveis
"""

import argparse
import os
import sys

# ---------------------------------------------------------------------------
# Ajusta sys.path para importar commands_logic.py de src/
# ---------------------------------------------------------------------------
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "src"))

from commands_logic import (
    consultar_trilha,
    validar_desafio,
    gerar_certificado,
    _carregar_trilhas,
    TRILHAS_JSON_PATH,
)

from mcp.server.mcpserver import MCPServer

# ---------------------------------------------------------------------------
# Instância do servidor MCP v2
# ---------------------------------------------------------------------------
mcp = MCPServer(
    name="geo-explorer",
    version="1.0.0",
    description=(
        "Servidor MCP do projeto Geo-Explorer. "
        "Fornece ferramentas para consulta de trilhas de estudo, "
        "geração de desafios de programação e emissão de certificados fictícios."
    ),
)

# ---------------------------------------------------------------------------
# Ferramenta: consultar_trilha
# ---------------------------------------------------------------------------

@mcp.tool(
    description=(
        "Consulta o arquivo data/trilhas_geo.json e retorna os dados completos da trilha "
        "de estudos correspondente à tecnologia informada. "
        "Retorna: nome, tecnologia, nível, módulos, XP total, badges, promoção e live ao vivo."
    )
)
def consultar_trilha_tool(tecnologia: str) -> str:
    """
    Consulta uma trilha de estudos pelo nome da tecnologia.

    Args:
        tecnologia: Nome da tecnologia ou trilha (ex: 'Java', 'Python', 'React')
    """
    resultado = consultar_trilha(tecnologia)

    if not resultado.encontrada:
        if resultado.tecnologias_disponiveis:
            lista = "\n".join(f"  • {t}" for t in resultado.tecnologias_disponiveis)
            return (
                f"❌ {resultado.erro}\n\n"
                f"**Tecnologias disponíveis:**\n{lista}\n\n"
                f"Dica: tente com uma das tecnologias listadas acima."
            )
        return f"❌ {resultado.erro}"

    t = resultado.trilha
    promo = t["promocao"]
    live = t["live_ao_vivo"]

    promo_txt = (
        f"✅ Desconto de {promo['desconto_percent']}% — válido até {promo['validade']}"
        if promo["ativa"]
        else "❌ Sem promoção ativa no momento."
    )
    live_txt = (
        f"📡 Disponível — {live['frequencia']}, toda {live['dia_semana']}"
        if live["disponivel"]
        else "📵 Não há lives ao vivo para esta trilha."
    )
    badges = "\n".join(f"  ✦ {b}" for b in t["badges"])

    return (
        f"# Trilha: {t['nome']}\n\n"
        f"**Tecnologia:** {t['tecnologia']}\n"
        f"**Nível:** {t['nivel']}\n"
        f"**Módulos:** {t['modulos']}\n"
        f"**XP Total:** {t['xp_total']} XP\n"
        f"**Vitalício:** {'Sim' if t['vitalicio'] else 'Não'}\n\n"
        f"## Badges disponíveis\n{badges}\n\n"
        f"## Promoção\n{promo_txt}\n\n"
        f"## Live ao Vivo\n{live_txt}\n"
    )


# ---------------------------------------------------------------------------
# Ferramenta: gerar_desafio
# ---------------------------------------------------------------------------

@mcp.tool(
    description=(
        "Valida os parâmetros e retorna metadados estruturados para geração de um desafio de "
        "programação aleatório. Use os dados retornados para criar o desafio completo. "
        "Níveis aceitos: iniciante, intermediário (ou intermediario), avançado (ou avancado)."
    )
)
def gerar_desafio_tool(tecnologia: str, nivel: str) -> str:
    """
    Valida e prepara os parâmetros para um desafio de programação.

    Args:
        tecnologia: Tecnologia alvo do desafio (ex: 'Python', 'Java', 'React')
        nivel: Nível de dificuldade — iniciante | intermediário | avançado
    """
    resultado = validar_desafio(tecnologia, nivel)

    if not resultado.valido:
        return f"❌ {resultado.erro}"

    return (
        f"# 🧩 Desafio de {resultado.tecnologia}\n\n"
        f"**Nível:** {resultado.nivel}\n\n"
        f"---\n\n"
        f"✅ Parâmetros validados com sucesso.\n\n"
        f"**Tecnologia:** `{resultado.tecnologia}`  \n"
        f"**Nível:** `{resultado.nivel}`\n\n"
        f"Gere agora um desafio de programação criativo e educativo para a tecnologia "
        f"**{resultado.tecnologia}** no nível **{resultado.nivel}**.\n\n"
        f"Estruture o desafio com:\n"
        f"- 📋 Descrição do problema\n"
        f"- ✅ Requisitos técnicos\n"
        f"- 💡 Exemplo de entrada e saída\n"
        f"- 🎯 Objetivo de aprendizado\n"
        f"- 💬 Dica (sem entregar a solução)\n"
    )


# ---------------------------------------------------------------------------
# Ferramenta: gerar_certificado
# ---------------------------------------------------------------------------

@mcp.tool(
    description=(
        "Gera os dados completos para um certificado fictício de conclusão de trilha. "
        "Busca os detalhes da trilha em data/trilhas_geo.json. "
        "Se a trilha não for encontrada no arquivo, gera um certificado genérico com os dados informados. "
        "O certificado é demonstrativo e não possui validade oficial."
    )
)
def gerar_certificado_tool(nome: str, tecnologia: str) -> str:
    """
    Gera um certificado fictício de conclusão de trilha.

    Args:
        nome: Nome completo do aluno a ser certificado
        tecnologia: Nome da tecnologia ou trilha concluída (ex: 'Java', 'Python')
    """
    resultado = gerar_certificado(nome, tecnologia)

    if not resultado.valido:
        return f"❌ {resultado.erro}"

    if resultado.trilha_dados:
        t = resultado.trilha_dados
        badges = "\n".join(f"✦ {b}" for b in t["badges"])
        return (
            f"---\n\n"
            f"# 🏆 CERTIFICADO DE CONCLUSÃO\n\n"
            f"---\n\n"
            f"## Certificamos que\n\n"
            f"# {resultado.nome}\n\n"
            f"concluiu com êxito a trilha de estudos:\n\n"
            f"## {t['nome']}\n\n"
            f"---\n\n"
            f"**Tecnologia:** {t['tecnologia']}  \n"
            f"**Nível:** {t['nivel']}  \n"
            f"**Módulos concluídos:** {t['modulos']}  \n"
            f"**XP conquistado:** {t['xp_total']} XP  \n\n"
            f"**Badges conquistados:**  \n{badges}\n\n"
            f"---\n\n"
            f"> Este certificado reconhece o esforço e dedicação de **{resultado.nome}** "
            f"na trilha **{t['nome']} — Geo Explorer**.\n\n"
            f"**Data de emissão:** {resultado.data_emissao}\n\n"
            f"---\n\n"
            f"*⚠️ Certificado fictício e demonstrativo gerado pelo Geo-Explorer MCP Server.*  \n"
            f"*Não possui validade oficial.*\n\n"
            f"---\n"
        )

    return (
        f"---\n\n"
        f"# 🏆 CERTIFICADO DE CONCLUSÃO\n\n"
        f"---\n\n"
        f"## Certificamos que\n\n"
        f"# {resultado.nome}\n\n"
        f"concluiu com êxito a trilha de estudos:\n\n"
        f"## {resultado.tecnologia} — Geo Explorer\n\n"
        f"---\n\n"
        f"> Este certificado reconhece o esforço e dedicação de **{resultado.nome}** "
        f"na trilha de **{resultado.tecnologia}**.\n\n"
        f"**Data de emissão:** {resultado.data_emissao}\n\n"
        f"---\n\n"
        f"*⚠️ Certificado fictício e demonstrativo gerado pelo Geo-Explorer MCP Server.*  \n"
        f"*Não possui validade oficial.*\n\n"
        f"---\n"
    )


# ---------------------------------------------------------------------------
# Ferramenta: listar_trilhas
# ---------------------------------------------------------------------------

@mcp.tool(
    description=(
        "Lista todas as trilhas de estudo disponíveis no arquivo data/trilhas_geo.json, "
        "mostrando id, nome, tecnologia, nível e XP total de cada uma."
    )
)
def listar_trilhas_tool() -> str:
    """Lista todas as trilhas disponíveis no Geo-Explorer."""
    try:
        dados = _carregar_trilhas()
    except (FileNotFoundError, ValueError) as exc:
        return f"⚠️ Não foi possível carregar as trilhas: {exc}"

    trilhas = dados.get("trilhas", [])
    if not trilhas:
        return "⚠️ Nenhuma trilha encontrada no arquivo data/trilhas_geo.json."

    linhas = ["# Trilhas disponíveis no Geo-Explorer\n"]
    for t in trilhas:
        linhas.append(
            f"**{t['id']:02d}.** {t['nome']}  \n"
            f"    🛠 {t['tecnologia']} | 📊 {t['nivel']} | ⭐ {t['xp_total']} XP\n"
        )
    linhas.append(
        f"\n_Total: {dados.get('total_trilhas', len(trilhas))} trilhas disponíveis_"
    )
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import asyncio

    parser = argparse.ArgumentParser(
        description="Geo-Explorer MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemplos:\n"
            "  python3 mcp/server.py                              # stdio (IBM Bob local)\n"
            "  python3 mcp/server.py --transport sse              # HTTP/SSE remoto\n"
            "  python3 mcp/server.py --transport http             # Streamable HTTP (MCP v2)\n"
            "  python3 mcp/server.py --transport sse --host 0.0.0.0 --port 8080\n"
        ),
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "http"],
        default="stdio",
        help="Transporte MCP (padrão: stdio)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host para modos SSE/HTTP (padrão: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Porta para modos SSE/HTTP (padrão: 8000)",
    )
    args = parser.parse_args()

    if args.transport == "stdio":
        print("[geo-explorer MCP] Iniciando no modo stdio...", file=sys.stderr)
        asyncio.run(mcp.run_stdio_async())

    elif args.transport == "sse":
        print(
            f"[geo-explorer MCP] Iniciando no modo SSE em http://{args.host}:{args.port}\n"
            f"  SSE endpoint   : http://{args.host}:{args.port}/sse\n"
            f"  Para HTTPS     : use um reverse proxy (nginx/caddy) na frente desta porta.",
            file=sys.stderr,
        )
        asyncio.run(mcp.run_sse_async(host=args.host, port=args.port))

    elif args.transport == "http":
        print(
            f"[geo-explorer MCP] Iniciando no modo Streamable HTTP em http://{args.host}:{args.port}\n"
            f"  MCP endpoint   : http://{args.host}:{args.port}/mcp\n"
            f"  Para HTTPS     : use um reverse proxy (nginx/caddy) na frente desta porta.",
            file=sys.stderr,
        )
        asyncio.run(mcp.run_streamable_http_async(host=args.host, port=args.port))
