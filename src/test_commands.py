"""
test_commands.py
Testes unitários dos slash commands do projeto Geo-Explorer.
Cobre /trilhas, /desafio e /certificado com foco em ≥70% de aprovação.
Execute com: python -m pytest src/test_commands.py -v
             ou: python src/test_commands.py
"""

import json
import os
import sys
import tempfile
import unittest
from datetime import date

# Garante que o diretório src está no path para importação
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from commands_logic import (
    consultar_trilha,
    validar_desafio,
    gerar_certificado,
    NIVEIS_VALIDOS,
    _normalizar,
    _buscar_trilha,
    _carregar_trilhas,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

TRILHAS_FIXTURE = {
    "trilhas": [
        {
            "id": 2,
            "nome": "Java do Zero ao Profissional",
            "tecnologia": "Java",
            "nivel": "Iniciante",
            "modulos": 12,
            "xp_total": 4800,
            "badges": ["Java Starter", "OOP Expert", "Java Pro"],
            "promocao": {"ativa": False, "desconto_percent": 0, "validade": None},
            "vitalicio": True,
            "live_ao_vivo": {"disponivel": True, "frequencia": "Quinzenal", "dia_semana": "Terça-feira"}
        },
        {
            "id": 1,
            "nome": "Fundamentos de Python para Dados",
            "tecnologia": "Python",
            "nivel": "Iniciante",
            "modulos": 8,
            "xp_total": 3200,
            "badges": ["Python Starter", "Data Novice", "Script Master"],
            "promocao": {"ativa": True, "desconto_percent": 30, "validade": "2025-08-31"},
            "vitalicio": True,
            "live_ao_vivo": {"disponivel": True, "frequencia": "Semanal", "dia_semana": "Quarta-feira"}
        },
    ],
    "total_trilhas": 2
}


def _criar_json_temp(conteudo: dict) -> str:
    """Cria um arquivo JSON temporário e retorna seu caminho."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    )
    json.dump(conteudo, tmp, ensure_ascii=False)
    tmp.close()
    return tmp.name


def _criar_arquivo_temp_vazio() -> str:
    """Cria um arquivo temporário vazio e retorna seu caminho."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    )
    tmp.write("")
    tmp.close()
    return tmp.name


def _criar_arquivo_temp_invalido() -> str:
    """Cria um arquivo temporário com JSON inválido e retorna seu caminho."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    )
    tmp.write("{invalid json content")
    tmp.close()
    return tmp.name


# ---------------------------------------------------------------------------
# Testes — utilidades internas
# ---------------------------------------------------------------------------

class TestNormalizacao(unittest.TestCase):
    """Testa a função _normalizar."""

    def test_minusculas(self):
        self.assertEqual(_normalizar("JAVA"), "java")

    def test_acento_a(self):
        self.assertEqual(_normalizar("Avançado"), "avancado")

    def test_acento_e(self):
        self.assertEqual(_normalizar("Intermediário"), "intermediario")

    def test_sem_alteracao(self):
        self.assertEqual(_normalizar("python"), "python")

    def test_string_vazia(self):
        self.assertEqual(_normalizar(""), "")


# ---------------------------------------------------------------------------
# Testes — _carregar_trilhas
# ---------------------------------------------------------------------------

class TestCarregarTrilhas(unittest.TestCase):
    """Testa o carregamento do JSON de trilhas."""

    def setUp(self):
        self.caminho_valido = _criar_json_temp(TRILHAS_FIXTURE)
        self.caminho_vazio = _criar_arquivo_temp_vazio()
        self.caminho_invalido = _criar_arquivo_temp_invalido()

    def tearDown(self):
        for f in [self.caminho_valido, self.caminho_vazio, self.caminho_invalido]:
            if os.path.exists(f):
                os.unlink(f)

    def test_carrega_json_valido(self):
        dados = _carregar_trilhas(self.caminho_valido)
        self.assertIn("trilhas", dados)
        self.assertEqual(len(dados["trilhas"]), 2)

    def test_arquivo_nao_encontrado(self):
        with self.assertRaises(FileNotFoundError):
            _carregar_trilhas("/caminho/que/nao/existe.json")

    def test_arquivo_vazio(self):
        with self.assertRaises(ValueError):
            _carregar_trilhas(self.caminho_vazio)

    def test_json_invalido(self):
        with self.assertRaises(ValueError):
            _carregar_trilhas(self.caminho_invalido)


# ---------------------------------------------------------------------------
# Testes — _buscar_trilha
# ---------------------------------------------------------------------------

class TestBuscarTrilha(unittest.TestCase):
    """Testa a busca de trilha por tecnologia."""

    def test_busca_java_exato(self):
        resultado = _buscar_trilha("Java", TRILHAS_FIXTURE)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["tecnologia"], "Java")

    def test_busca_java_minusculo(self):
        resultado = _buscar_trilha("java", TRILHAS_FIXTURE)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["tecnologia"], "Java")

    def test_busca_java_maiusculo(self):
        resultado = _buscar_trilha("JAVA", TRILHAS_FIXTURE)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["tecnologia"], "Java")

    def test_busca_python(self):
        resultado = _buscar_trilha("Python", TRILHAS_FIXTURE)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["tecnologia"], "Python")

    def test_busca_por_nome_parcial(self):
        resultado = _buscar_trilha("Profissional", TRILHAS_FIXTURE)
        self.assertIsNotNone(resultado)

    def test_busca_tecnologia_inexistente(self):
        resultado = _buscar_trilha("Rust", TRILHAS_FIXTURE)
        self.assertIsNone(resultado)

    def test_busca_lista_vazia(self):
        resultado = _buscar_trilha("Java", {"trilhas": []})
        self.assertIsNone(resultado)


# ---------------------------------------------------------------------------
# Testes — /trilhas (consultar_trilha)
# ---------------------------------------------------------------------------

class TestConsultarTrilha(unittest.TestCase):
    """Testa o comando /trilhas com foco na trilha de Java."""

    def setUp(self):
        self.caminho = _criar_json_temp(TRILHAS_FIXTURE)

    def tearDown(self):
        if os.path.exists(self.caminho):
            os.unlink(self.caminho)

    # --- Cenários de sucesso ---

    def test_trilha_java_encontrada(self):
        resultado = consultar_trilha("Java", self.caminho)
        self.assertTrue(resultado.encontrada)
        self.assertIsNotNone(resultado.trilha)
        self.assertEqual(resultado.trilha["tecnologia"], "Java")

    def test_trilha_java_nome_completo(self):
        resultado = consultar_trilha("Java", self.caminho)
        self.assertEqual(resultado.trilha["nome"], "Java do Zero ao Profissional")

    def test_trilha_java_modulos(self):
        resultado = consultar_trilha("Java", self.caminho)
        self.assertEqual(resultado.trilha["modulos"], 12)

    def test_trilha_java_xp(self):
        resultado = consultar_trilha("Java", self.caminho)
        self.assertEqual(resultado.trilha["xp_total"], 4800)

    def test_trilha_java_badges(self):
        resultado = consultar_trilha("Java", self.caminho)
        self.assertIn("Java Starter", resultado.trilha["badges"])
        self.assertIn("OOP Expert", resultado.trilha["badges"])
        self.assertIn("Java Pro", resultado.trilha["badges"])

    def test_trilha_java_nivel(self):
        resultado = consultar_trilha("Java", self.caminho)
        self.assertEqual(resultado.trilha["nivel"], "Iniciante")

    def test_trilha_java_vitalicio(self):
        resultado = consultar_trilha("Java", self.caminho)
        self.assertTrue(resultado.trilha["vitalicio"])

    def test_trilha_java_live_disponivel(self):
        resultado = consultar_trilha("Java", self.caminho)
        self.assertTrue(resultado.trilha["live_ao_vivo"]["disponivel"])

    def test_trilha_java_sem_promocao(self):
        resultado = consultar_trilha("Java", self.caminho)
        self.assertFalse(resultado.trilha["promocao"]["ativa"])

    def test_trilha_java_case_insensitive(self):
        resultado = consultar_trilha("java", self.caminho)
        self.assertTrue(resultado.encontrada)

    def test_trilha_python_encontrada(self):
        resultado = consultar_trilha("Python", self.caminho)
        self.assertTrue(resultado.encontrada)
        self.assertEqual(resultado.trilha["tecnologia"], "Python")

    # --- Cenários de erro ---

    def test_tecnologia_vazia(self):
        resultado = consultar_trilha("", self.caminho)
        self.assertFalse(resultado.encontrada)
        self.assertIsNotNone(resultado.erro)

    def test_tecnologia_espacos(self):
        resultado = consultar_trilha("   ", self.caminho)
        self.assertFalse(resultado.encontrada)

    def test_tecnologia_inexistente(self):
        resultado = consultar_trilha("Cobol", self.caminho)
        self.assertFalse(resultado.encontrada)
        self.assertGreater(len(resultado.tecnologias_disponiveis), 0)

    def test_tecnologias_disponiveis_na_falha(self):
        resultado = consultar_trilha("Haskell", self.caminho)
        self.assertIn("Java", resultado.tecnologias_disponiveis)
        self.assertIn("Python", resultado.tecnologias_disponiveis)

    def test_arquivo_inexistente(self):
        resultado = consultar_trilha("Java", "/nao/existe.json")
        self.assertFalse(resultado.encontrada)
        self.assertIsNotNone(resultado.erro)

    def test_json_invalido(self):
        caminho = _criar_arquivo_temp_invalido()
        try:
            resultado = consultar_trilha("Java", caminho)
            self.assertFalse(resultado.encontrada)
            self.assertIsNotNone(resultado.erro)
        finally:
            os.unlink(caminho)


# ---------------------------------------------------------------------------
# Testes — /desafio (validar_desafio)
# ---------------------------------------------------------------------------

class TestValidarDesafio(unittest.TestCase):
    """Testa o comando /desafio — geração de desafio para o aluno."""

    # --- Parâmetros válidos ---

    def test_valido_java_iniciante(self):
        resultado = validar_desafio("Java", "iniciante")
        self.assertTrue(resultado.valido)
        self.assertEqual(resultado.tecnologia, "Java")
        self.assertEqual(resultado.nivel, "iniciante")

    def test_valido_python_intermediario(self):
        resultado = validar_desafio("Python", "intermediário")
        self.assertTrue(resultado.valido)

    def test_valido_react_avancado(self):
        resultado = validar_desafio("React", "avançado")
        self.assertTrue(resultado.valido)

    def test_valido_sem_acento_intermediario(self):
        resultado = validar_desafio("Java", "intermediario")
        self.assertTrue(resultado.valido)

    def test_valido_sem_acento_avancado(self):
        resultado = validar_desafio("Java", "avancado")
        self.assertTrue(resultado.valido)

    def test_preserva_tecnologia_original(self):
        resultado = validar_desafio("  Java  ", "iniciante")
        self.assertEqual(resultado.tecnologia, "Java")

    # --- Parâmetros inválidos ---

    def test_tecnologia_vazia(self):
        resultado = validar_desafio("", "iniciante")
        self.assertFalse(resultado.valido)
        self.assertIsNotNone(resultado.erro)

    def test_nivel_vazio(self):
        resultado = validar_desafio("Java", "")
        self.assertFalse(resultado.valido)
        self.assertIsNotNone(resultado.erro)

    def test_nivel_invalido(self):
        resultado = validar_desafio("Java", "fácil")
        self.assertFalse(resultado.valido)
        self.assertIn("inválido", resultado.erro.lower())

    def test_nivel_invalido_expert(self):
        resultado = validar_desafio("Java", "expert")
        self.assertFalse(resultado.valido)

    def test_tecnologia_none_like(self):
        resultado = validar_desafio("   ", "iniciante")
        self.assertFalse(resultado.valido)

    def test_nivel_none_like(self):
        resultado = validar_desafio("Java", "   ")
        self.assertFalse(resultado.valido)


# ---------------------------------------------------------------------------
# Testes — /certificado (gerar_certificado)
# ---------------------------------------------------------------------------

class TestGerarCertificado(unittest.TestCase):
    """Testa o comando /certificado — geração de certificado para o aluno."""

    def setUp(self):
        self.caminho = _criar_json_temp(TRILHAS_FIXTURE)

    def tearDown(self):
        if os.path.exists(self.caminho):
            os.unlink(self.caminho)

    # --- Cenários de sucesso com trilha encontrada ---

    def test_certificado_java_valido(self):
        resultado = gerar_certificado("Alexandre", "Java", self.caminho)
        self.assertTrue(resultado.valido)
        self.assertEqual(resultado.nome, "Alexandre")
        self.assertEqual(resultado.tecnologia, "Java")

    def test_certificado_contem_dados_trilha(self):
        resultado = gerar_certificado("Alexandre", "Java", self.caminho)
        self.assertIsNotNone(resultado.trilha_dados)
        self.assertEqual(resultado.trilha_dados["tecnologia"], "Java")

    def test_certificado_data_emissao_formato(self):
        resultado = gerar_certificado("Alexandre", "Java", self.caminho)
        partes = resultado.data_emissao.split("/")
        self.assertEqual(len(partes), 3)
        self.assertEqual(len(partes[2]), 4)  # ano com 4 dígitos

    def test_certificado_data_emissao_hoje(self):
        resultado = gerar_certificado("Alexandre", "Java", self.caminho)
        esperado = date.today().strftime("%d/%m/%Y")
        self.assertEqual(resultado.data_emissao, esperado)

    def test_certificado_badges_disponiveis(self):
        resultado = gerar_certificado("Alexandre", "Java", self.caminho)
        self.assertIn("Java Starter", resultado.trilha_dados["badges"])

    def test_certificado_xp_correto(self):
        resultado = gerar_certificado("Alexandre", "Java", self.caminho)
        self.assertEqual(resultado.trilha_dados["xp_total"], 4800)

    def test_certificado_nome_com_espacos(self):
        resultado = gerar_certificado("  Alexandre  ", "Java", self.caminho)
        self.assertEqual(resultado.nome, "Alexandre")

    # --- Certificado genérico (trilha não encontrada no JSON) ---

    def test_certificado_trilha_inexistente_ainda_valido(self):
        resultado = gerar_certificado("Alexandre", "COBOL", self.caminho)
        self.assertTrue(resultado.valido)
        self.assertIsNone(resultado.trilha_dados)
        self.assertEqual(resultado.nome, "Alexandre")

    def test_certificado_sem_json_ainda_valido(self):
        resultado = gerar_certificado("Alexandre", "Java", "/nao/existe.json")
        self.assertTrue(resultado.valido)
        self.assertIsNone(resultado.trilha_dados)

    def test_certificado_json_invalido_ainda_valido(self):
        caminho = _criar_arquivo_temp_invalido()
        try:
            resultado = gerar_certificado("Alexandre", "Java", caminho)
            self.assertTrue(resultado.valido)
        finally:
            os.unlink(caminho)

    # --- Cenários de erro de validação ---

    def test_nome_vazio(self):
        resultado = gerar_certificado("", "Java", self.caminho)
        self.assertFalse(resultado.valido)
        self.assertIsNotNone(resultado.erro)

    def test_nome_espacos(self):
        resultado = gerar_certificado("   ", "Java", self.caminho)
        self.assertFalse(resultado.valido)

    def test_tecnologia_vazia(self):
        resultado = gerar_certificado("Alexandre", "", self.caminho)
        self.assertFalse(resultado.valido)
        self.assertIsNotNone(resultado.erro)

    def test_tecnologia_espacos(self):
        resultado = gerar_certificado("Alexandre", "   ", self.caminho)
        self.assertFalse(resultado.valido)


# ---------------------------------------------------------------------------
# Runner principal — executa e grava resultados em TXT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import io

    suite = unittest.TestLoader().loadTestsFromModule(
        sys.modules[__name__]
    )

    buffer = io.StringIO()
    runner = unittest.TextTestRunner(
        stream=buffer,
        verbosity=2,
        descriptions=True
    )
    resultado = runner.run(suite)

    saida = buffer.getvalue()

    total = resultado.testsRun
    falhas = len(resultado.failures)
    erros = len(resultado.errors)
    aprovados = total - falhas - erros
    taxa = (aprovados / total * 100) if total > 0 else 0

    relatorio = f"""
================================================================================
  RELATÓRIO DE TESTES — GEO-EXPLORER SLASH COMMANDS
  Gerado em: {date.today().strftime("%d/%m/%Y")}
================================================================================

COBERTURA DE TESTES POR COMANDO:
  /trilhas     — consultar_trilha()   — cenários: Java encontrado, erros, edge cases
  /desafio     — validar_desafio()    — cenários: parâmetros válidos e inválidos
  /certificado — gerar_certificado()  — cenários: com/sem JSON, erros de validação

--------------------------------------------------------------------------------
RESULTADO DETALHADO:
--------------------------------------------------------------------------------
{saida}
--------------------------------------------------------------------------------
SUMÁRIO FINAL:
  Total de testes executados : {total}
  ✅ Aprovados                : {aprovados}
  ❌ Falhas                   : {falhas}
  💥 Erros                    : {erros}
  📊 Taxa de aprovação        : {taxa:.1f}%
  🎯 Meta mínima              : 70.0%
  {'✅ META ATINGIDA' if taxa >= 70 else '❌ META NÃO ATINGIDA'}
================================================================================
"""

    print(relatorio)

    # Grava o relatório no arquivo TXT
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "docs",
        "resultado_testes.txt"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(relatorio)

    print(f"Relatório salvo em: {output_path}")
    sys.exit(0 if taxa >= 70 else 1)
