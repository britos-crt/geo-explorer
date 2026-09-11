"""
commands_logic.py
Lógica de negócio dos slash commands do projeto Geo-Explorer.
Separa a regra de negócio da camada de apresentação (slash commands).
"""

import json
import os
from datetime import date
from typing import Optional

# Caminho padrão do arquivo de trilhas (relativo à raiz do projeto)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRILHAS_JSON_PATH = os.path.join(_PROJECT_ROOT, "data", "trilhas_geo.json")

NIVEIS_VALIDOS = {"iniciante", "intermediário", "intermediario", "avançado", "avancado"}

# ---------------------------------------------------------------------------
# Utilitários internos
# ---------------------------------------------------------------------------

def _normalizar(texto: str) -> str:
    """Converte para minúsculas e remove acentos simples para comparação."""
    substituicoes = str.maketrans("áàãâéêíóôõúüç", "aaaaeeiooouuc")
    return texto.lower().translate(substituicoes)


def _carregar_trilhas(caminho: str = TRILHAS_JSON_PATH) -> dict:
    """Carrega e retorna o JSON de trilhas. Lança FileNotFoundError ou ValueError."""
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()
    if not conteudo:
        raise ValueError("O arquivo JSON está vazio.")
    try:
        return json.loads(conteudo)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido: {exc}") from exc


def _buscar_trilha(tecnologia: str, dados: dict) -> Optional[dict]:
    """Busca uma trilha pelo campo tecnologia ou nome (case-insensitive)."""
    termo = _normalizar(tecnologia)
    for trilha in dados.get("trilhas", []):
        if termo in _normalizar(trilha.get("tecnologia", "")):
            return trilha
        if termo in _normalizar(trilha.get("nome", "")):
            return trilha
    return None


# ---------------------------------------------------------------------------
# /trilhas <tecnologia>
# ---------------------------------------------------------------------------

class ResultadoTrilha:
    """Resultado da consulta de trilha."""
    def __init__(self, encontrada: bool, trilha: Optional[dict] = None,
                 tecnologias_disponiveis: Optional[list] = None,
                 erro: Optional[str] = None):
        self.encontrada = encontrada
        self.trilha = trilha
        self.tecnologias_disponiveis = tecnologias_disponiveis or []
        self.erro = erro


def consultar_trilha(tecnologia: str, caminho_json: str = TRILHAS_JSON_PATH) -> ResultadoTrilha:
    """
    Consulta a trilha correspondente à tecnologia informada.
    Retorna um ResultadoTrilha com os dados encontrados ou mensagem de erro.
    """
    if not tecnologia or not tecnologia.strip():
        return ResultadoTrilha(
            encontrada=False,
            erro="Informe a tecnologia. Uso: /trilhas <tecnologia>"
        )

    try:
        dados = _carregar_trilhas(caminho_json)
    except (FileNotFoundError, ValueError) as exc:
        return ResultadoTrilha(encontrada=False, erro=str(exc))

    trilha = _buscar_trilha(tecnologia, dados)

    if trilha:
        return ResultadoTrilha(encontrada=True, trilha=trilha)

    tecnologias = [t.get("tecnologia", "") for t in dados.get("trilhas", [])]
    return ResultadoTrilha(
        encontrada=False,
        tecnologias_disponiveis=tecnologias,
        erro=f"Trilha para '{tecnologia}' não encontrada."
    )


# ---------------------------------------------------------------------------
# /desafio <tecnologia> <nivel>
# ---------------------------------------------------------------------------

class ResultadoDesafio:
    """Resultado da geração de desafio."""
    def __init__(self, valido: bool, tecnologia: str = "", nivel: str = "",
                 erro: Optional[str] = None):
        self.valido = valido
        self.tecnologia = tecnologia
        self.nivel = nivel
        self.erro = erro


def validar_desafio(tecnologia: str, nivel: str) -> ResultadoDesafio:
    """
    Valida os parâmetros do comando /desafio.
    Retorna ResultadoDesafio indicando se os parâmetros são válidos.
    """
    if not tecnologia or not tecnologia.strip():
        return ResultadoDesafio(
            valido=False,
            erro="Informe a tecnologia. Uso: /desafio <tecnologia> <nivel>"
        )

    if not nivel or not nivel.strip():
        return ResultadoDesafio(
            valido=False,
            erro="Informe o nível. Uso: /desafio <tecnologia> <nivel>\n"
                 "Níveis válidos: iniciante | intermediário | avançado"
        )

    if _normalizar(nivel) not in NIVEIS_VALIDOS:
        return ResultadoDesafio(
            valido=False,
            erro=f"Nível inválido: '{nivel}'\nNíveis válidos: iniciante | intermediário | avançado"
        )

    return ResultadoDesafio(valido=True, tecnologia=tecnologia.strip(), nivel=nivel.strip())


# ---------------------------------------------------------------------------
# /certificado <nome> <tecnologia>
# ---------------------------------------------------------------------------

class ResultadoCertificado:
    """Resultado da geração de certificado."""
    def __init__(self, valido: bool, nome: str = "", tecnologia: str = "",
                 trilha_dados: Optional[dict] = None, data_emissao: str = "",
                 erro: Optional[str] = None):
        self.valido = valido
        self.nome = nome
        self.tecnologia = tecnologia
        self.trilha_dados = trilha_dados
        self.data_emissao = data_emissao
        self.erro = erro


def gerar_certificado(nome: str, tecnologia: str,
                      caminho_json: str = TRILHAS_JSON_PATH) -> ResultadoCertificado:
    """
    Valida os parâmetros e busca dados da trilha para compor o certificado.
    Retorna ResultadoCertificado com todos os dados necessários para a renderização.
    """
    if not nome or not nome.strip():
        return ResultadoCertificado(
            valido=False,
            erro="Informe seu nome. Uso: /certificado <nome> <tecnologia>"
        )

    if not tecnologia or not tecnologia.strip():
        return ResultadoCertificado(
            valido=False,
            erro="Informe a trilha/tecnologia. Uso: /certificado <nome> <tecnologia>"
        )

    data_hoje = date.today().strftime("%d/%m/%Y")
    trilha_dados = None

    try:
        dados = _carregar_trilhas(caminho_json)
        trilha_dados = _buscar_trilha(tecnologia, dados)
    except (FileNotFoundError, ValueError):
        # Certificado genérico: arquivo ausente não impede a geração
        pass

    return ResultadoCertificado(
        valido=True,
        nome=nome.strip(),
        tecnologia=tecnologia.strip(),
        trilha_dados=trilha_dados,
        data_emissao=data_hoje
    )
