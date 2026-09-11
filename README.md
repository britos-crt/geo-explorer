# 🌍 Geo-Explorer

> Projeto educacional construído com auxílio do **IBM Bob** (AI Assistant), inspirado na plataforma [DIO — Digital Innovation One](https://www.dio.me/).

O Geo-Explorer simula um sistema de trilhas de aprendizado com slash commands nativos do IBM Bob, lógica de negócio em Python, testes unitários e um servidor MCP (Model Context Protocol) para exposição via API ou HTTPS.

---

## ✨ Funcionalidades

| Funcionalidade | Slash Command | Ferramenta MCP |
|---|---|---|
| Consultar trilha de estudo | `/trilhas <tecnologia>` | `consultar_trilha_tool` |
| Gerar desafio de programação | `/desafio <tecnologia> <nivel>` | `gerar_desafio_tool` |
| Emitir certificado fictício | `/certificado <nome> <tecnologia>` | `gerar_certificado_tool` |
| Listar todas as trilhas | — | `listar_trilhas_tool` |

---

## 📁 Estrutura do Projeto

```
geo-explorer/
├── .bob/
│   ├── commands/
│   │   ├── trilhas.md        # /trilhas <tecnologia>
│   │   ├── desafio.md        # /desafio <tecnologia> <nivel>
│   │   └── certificado.md    # /certificado <nome> <tecnologia>
│   └── mcp.json              # Registro do servidor MCP no IBM Bob
├── data/
│   └── trilhas_geo.json      # 32 trilhas fictícias com tecnologia, XP, badges, promoções e lives
├── docs/
│   ├── GEO_EXPLORER_DOCS.md  # Documentação completa do projeto
│   └── resultado_testes.txt  # Relatório de execução dos testes unitários
├── mcp/
│   ├── server.py             # Servidor MCP v2 (stdio + SSE + Streamable HTTP)
│   └── requirements.txt      # Dependências Python
├── src/
│   ├── commands_logic.py     # Lógica de negócio (consultar, desafio, certificado)
│   └── test_commands.py      # 59 testes unitários — 100% de aprovação
├── .bobignore                # Exclusões do IBM Bob
├── .gitignore                # Exclusões do Git
└── README.md                 # Este arquivo
```

---

## 🚀 Como Usar

### Pré-requisitos

- Python 3.11+
- IBM Bob instalado
- Git configurado

### 1. Clone o repositório

```bash
git clone https://github.com/britos-crt/geo-explorer.git
cd geo-explorer
```

### 2. Instale as dependências

```bash
pip install -r mcp/requirements.txt
```

### 3. Abra no IBM Bob

Abra o diretório do projeto no IBM Bob. Os slash commands e o servidor MCP serão carregados automaticamente.

---

## 💬 Slash Commands

Use diretamente no chat do IBM Bob (digite `/` para ver o menu):

### `/trilhas <tecnologia>`
Consulta a trilha de estudos de uma tecnologia e exibe plano completo com módulos, XP, badges, promoção e live ao vivo.

```
/trilhas Java
/trilhas Python
/trilhas React
```

### `/desafio <tecnologia> <nivel>`
Gera um desafio de programação criativo para a tecnologia e nível informados.

Níveis válidos: `iniciante` | `intermediário` | `avançado`

```
/desafio Python iniciante
/desafio Java intermediário
/desafio React avançado
```

### `/certificado <nome> <tecnologia>`
Emite um certificado fictício de conclusão de trilha com dados reais do JSON.

```
/certificado Alexandre Java
/certificado Maria Python
```

---

## 🔌 Servidor MCP

O projeto expõe suas ferramentas via **Model Context Protocol v2**, permitindo integração com qualquer cliente MCP compatível.

### Modo local — IBM Bob (stdio)
Configurado automaticamente via `.bob/mcp.json`. Nenhuma ação necessária.

### Modo remoto — HTTP/SSE

```bash
# HTTP/SSE (amplo suporte)
python3 mcp/server.py --transport sse --host 0.0.0.0 --port 8000

# Streamable HTTP (MCP v2 moderno)
python3 mcp/server.py --transport http --host 0.0.0.0 --port 8000
```

Para HTTPS, coloque um reverse proxy (nginx, Caddy) na frente da porta exposta.

---

## 🧪 Testes

```bash
python3 src/test_commands.py
```

```
Total de testes : 59
✅ Aprovados    : 59
📊 Aprovação   : 100%
```

O relatório é salvo automaticamente em `docs/resultado_testes.txt`.

---

## 📊 Base de Dados

O arquivo `data/trilhas_geo.json` contém **32 trilhas fictícias** com:

- Nome e tecnologia
- Nível (Iniciante / Intermediário / Avançado)
- Módulos e XP total
- Badges progressivos (3 por trilha)
- Promoções com desconto e validade
- Acesso vitalício
- Lives ao vivo com frequência e dia da semana

Tecnologias disponíveis: Python, Java, React, AWS, Docker, Kubernetes, Flutter, TensorFlow, TypeScript, Angular, Vue.js, Go, Rust, Kotlin, Next.js, Spring Boot, Terraform, Blockchain/Solidity, Power BI, Unity e mais.

---

## 📚 Documentação Completa

Consulte [`docs/GEO_EXPLORER_DOCS.md`](docs/GEO_EXPLORER_DOCS.md) para:

- Todos os prompts usados na construção do projeto
- Decisões de arquitetura e insights
- Guia de expansão futura
- Referências e tecnologias utilizadas

---

## 🛠️ Tecnologias

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-v2-6366f1?style=flat)
![IBM Bob](https://img.shields.io/badge/IBM%20Bob-AI%20Assistant-0f62fe?style=flat)
![DIO](https://img.shields.io/badge/DIO-Referência-E8272A?style=flat)

---

## 📄 Licença

Projeto educacional e demonstrativo. Sem licença comercial.

---

*Desenvolvido com 🤖 IBM Bob — Junho de 2025*
