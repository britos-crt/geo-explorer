# 📘 GEO-EXPLORER — Documentação Completa do Projeto

> **Projeto:** geo-explorer  
> **Repositório:** https://github.com/britos-crt/geo-explorer  
> **Plataforma de referência:** [DIO — Digital Innovation One](https://www.dio.me/)  
> **Assistente utilizado:** IBM Bob (AI Assistant)  
> **Última atualização:** Junho de 2025

---

## Índice

1. [Visão Geral](#1-visão-geral)
2. [Tecnologias e Dependências](#2-tecnologias-e-dependências)
3. [Estrutura de Diretórios](#3-estrutura-de-diretórios)
4. [Configuração Inicial do Ambiente](#4-configuração-inicial-do-ambiente)
5. [Dados — trilhas_geo.json](#5-dados--trilhas_geojson)
6. [Slash Commands do IBM Bob](#6-slash-commands-do-ibm-bob)
7. [Lógica de Negócio — commands_logic.py](#7-lógica-de-negócio--commands_logicpy)
8. [Testes Unitários](#8-testes-unitários)
9. [Servidor MCP](#9-servidor-mcp)
10. [Registro no IBM Bob — mcp.json](#10-registro-no-ibm-bob--mcpjson)
11. [Prompts Utilizados na Construção](#11-prompts-utilizados-na-construção)
12. [Modos de Uso](#12-modos-de-uso)
13. [Dicas de Uso](#13-dicas-de-uso)
14. [Insights e Decisões de Arquitetura](#14-insights-e-decisões-de-arquitetura)
15. [Expansão Futura](#15-expansão-futura)
16. [Referências](#16-referências)

---

## 1. Visão Geral

O **Geo-Explorer** é um projeto educacional construído inteiramente com auxílio do IBM Bob, que demonstra como integrar:

- **Slash commands locais** do IBM Bob para automação de fluxos educacionais
- **Lógica de negócio em Python** separada da camada de apresentação
- **Testes unitários** com cobertura de 100% dos cenários críticos
- **Servidor MCP** (Model Context Protocol) para expor as funcionalidades via API, HTTP ou SSE

O projeto simula um sistema de trilhas de aprendizado inspirado na plataforma DIO, permitindo que usuários consultem trilhas, gerem desafios de programação e emitam certificados fictícios — tudo diretamente pelo chat do IBM Bob ou via API.

### Principais funcionalidades

| Funcionalidade | Como acessar |
|---|---|
| Consultar trilha de estudo | Slash command `/trilhas` ou ferramenta MCP `consultar_trilha_tool` |
| Gerar desafio de programação | Slash command `/desafio` ou ferramenta MCP `gerar_desafio_tool` |
| Emitir certificado fictício | Slash command `/certificado` ou ferramenta MCP `gerar_certificado_tool` |
| Listar todas as trilhas | Ferramenta MCP `listar_trilhas_tool` |

---

## 2. Tecnologias e Dependências

### Linguagem principal
- **Python 3.14+**

### Dependências do servidor MCP
```
mcp[cli]>=1.0.0      # SDK MCP v2 (MCPServer)
starlette>=0.40.0    # Framework ASGI para modo HTTP/SSE
uvicorn>=0.30.0      # Servidor ASGI para modo HTTP/SSE
```

Instalação:
```bash
pip install -r mcp/requirements.txt
```

### Ferramentas do projeto
- **IBM Bob** — assistente de IA para geração de código e slash commands
- **Git + GitHub** — controle de versão com `credential.helper store`
- **unittest** — framework de testes nativo do Python
- **MCP SDK v2** — Model Context Protocol para exposição via API

---

## 3. Estrutura de Diretórios

```
geo-explorer/
│
├── .bob/                          # Configurações locais do IBM Bob
│   ├── commands/                  # Slash commands locais do projeto
│   │   ├── trilhas.md             # /trilhas <tecnologia>
│   │   ├── desafio.md             # /desafio <tecnologia> <nivel>
│   │   └── certificado.md         # /certificado <nome> <tecnologia>
│   └── mcp.json                   # Registro do servidor MCP no IBM Bob
│
├── commands/                      # Diretório reservado para futuras extensões
│
├── data/
│   └── trilhas_geo.json           # Base de dados com 32 trilhas fictícias
│
├── docs/
│   ├── resultado_testes.txt       # Relatório de execução dos testes unitários
│   └── GEO_EXPLORER_DOCS.md      # Este arquivo de documentação
│
├── mcp/
│   ├── server.py                  # Servidor MCP principal (stdio + SSE + HTTP)
│   └── requirements.txt           # Dependências Python do servidor MCP
│
├── src/
│   ├── commands_logic.py          # Lógica de negócio dos slash commands
│   └── test_commands.py           # 59 testes unitários (100% de aprovação)
│
├── .bobignore                     # Arquivos/diretórios ignorados pelo IBM Bob
└── CONECTIONTESTE.md              # Arquivo de teste de conectividade Git
```

---

## 4. Configuração Inicial do Ambiente

### 4.1 Configurar credenciais Git globalmente

```bash
git config --global credential.helper store
```

Verifica se foi aplicado:
```bash
git config --global --get credential.helper
# Saída esperada: store
```

> **O que faz:** salva as credenciais Git em `~/.git-credentials` após o primeiro login,
> de forma persistente e sem precisar redigitar em cada operação.

### 4.2 Clonar o repositório

```bash
mkdir -p ~/Documents/Exercicios/Dio
git clone https://github.com/britos-crt/geo-explorer.git \
  ~/Documents/Exercicios/Dio/geo-explorer
```

### 4.3 Instalar dependências do MCP server

```bash
cd ~/Documents/Exercicios/Dio/geo-explorer
pip install -r mcp/requirements.txt
```

### 4.4 Abrir o projeto no IBM Bob

Abra o diretório `~/Documents/Exercicios/Dio/geo-explorer` no IBM Bob.
Os slash commands e o servidor MCP serão carregados automaticamente.

---

## 5. Dados — trilhas_geo.json

**Caminho:** `data/trilhas_geo.json`

Contém **32 trilhas fictícias** inspiradas na plataforma DIO, cada uma com a seguinte estrutura:

```json
{
  "id": 2,
  "nome": "Java do Zero ao Profissional",
  "tecnologia": "Java",
  "nivel": "Iniciante",
  "modulos": 12,
  "xp_total": 4800,
  "badges": ["Java Starter", "OOP Expert", "Java Pro"],
  "promocao": {
    "ativa": false,
    "desconto_percent": 0,
    "validade": null
  },
  "vitalicio": true,
  "live_ao_vivo": {
    "disponivel": true,
    "frequencia": "Quinzenal",
    "dia_semana": "Terça-feira"
  }
}
```

### Campos disponíveis

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | inteiro | Identificador único da trilha |
| `nome` | string | Nome completo da trilha |
| `tecnologia` | string | Tecnologia principal (usada na busca) |
| `nivel` | string | Iniciante / Intermediário / Avançado |
| `modulos` | inteiro | Quantidade de módulos da trilha |
| `xp_total` | inteiro | Total de XP conquistado ao concluir |
| `badges` | array | Lista de 3 badges progressivos |
| `promocao.ativa` | booleano | Se há promoção ativa |
| `promocao.desconto_percent` | inteiro | Percentual de desconto |
| `promocao.validade` | string/null | Data de validade da promoção |
| `vitalicio` | booleano | Se o acesso é vitalício |
| `live_ao_vivo.disponivel` | booleano | Se há lives ao vivo |
| `live_ao_vivo.frequencia` | string/null | Semanal / Quinzenal / Mensal |
| `live_ao_vivo.dia_semana` | string/null | Dia da semana da live |

### Tecnologias disponíveis na base de dados

Python, Java, React, Scikit-Learn, AWS, Docker/Kubernetes, SQL/MongoDB,
CyberSecurity/Kali Linux, Flutter/Dart, TensorFlow, Git/GitHub, TypeScript/Node.js,
Pandas/NumPy, Spring Boot, Selenium, Angular/RxJS, Solidity/Ethereum, Terraform,
Vue.js, Node.js/Express, Apache Spark, C#/.NET, Figma, Power BI/DAX, Go/gRPC,
Rust, R/ggplot2, Next.js/Prisma, OpenAI/LangChain, Kotlin/Jetpack Compose,
MLflow/Kubeflow, Unity/C#

---

## 6. Slash Commands do IBM Bob

Os slash commands ficam em `.bob/commands/` e são **exclusivos do projeto geo-explorer**.
São carregados automaticamente quando o projeto está aberto no IBM Bob.

### 6.1 `/trilhas <tecnologia>`

**Arquivo:** `.bob/commands/trilhas.md`

**O que faz:**
1. Lê o arquivo `data/trilhas_geo.json`
2. Busca a trilha da tecnologia informada (case-insensitive, por `tecnologia` ou `nome`)
3. Exibe plano de estudos completo em Markdown com módulos, XP, badges, promoção e live

**Exemplo de uso:**
```
/trilhas Java
/trilhas Python
/trilhas React
```

**Resposta esperada:**
```markdown
# Trilha de Java do Zero ao Profissional

**Tecnologia:** Java
**Nível:** Iniciante
**Módulos:** 12
**XP Total:** 4800 XP
**Vitalício:** Sim

## Badges disponíveis
- Java Starter
- OOP Expert
- Java Pro

## Promoção
❌ Sem promoção ativa no momento.

## Live ao Vivo
📡 Disponível — Quinzenal, toda Terça-feira

## Plano de Estudos sugerido
...
```

**Tratamento de erros:**
- Tecnologia não informada → mensagem de ajuda
- Tecnologia inexistente → lista todas as disponíveis
- Arquivo JSON ausente ou inválido → mensagem de aviso

---

### 6.2 `/desafio <tecnologia> <nivel>`

**Arquivo:** `.bob/commands/desafio.md`

**O que faz:**
1. Valida tecnologia e nível informados
2. Gera um desafio de programação criativo e educativo
3. Varia o desafio a cada execução (mesmo com os mesmos parâmetros)

**Níveis válidos:** `iniciante` | `intermediário` | `intermediario` | `avançado` | `avancado`

**Exemplo de uso:**
```
/desafio Python iniciante
/desafio Java intermediário
/desafio React avancado
```

**Estrutura da resposta:**
```markdown
# 🧩 Desafio de Python

**Nível:** iniciante

---

## 📋 Descrição
...

## ✅ Requisitos
- ...

## 💡 Exemplo
Entrada: ...
Saída esperada: ...

## 🎯 Objetivo de aprendizado
...

## 💬 Dica
...
```

**Tratamento de erros:**
- Tecnologia não informada → mensagem de ajuda com exemplo
- Nível não informado → mostra níveis válidos
- Nível inválido → indica o valor inválido e sugere os corretos

---

### 6.3 `/certificado <nome> <tecnologia>`

**Arquivo:** `.bob/commands/certificado.md`

**O que faz:**
1. Valida nome e tecnologia informados
2. Busca dados reais da trilha no `trilhas_geo.json`
3. Gera certificado completo com badges e XP (se trilha encontrada)
4. Gera certificado genérico se a trilha não existir no JSON

**Exemplo de uso:**
```
/certificado Alexandre Java
/certificado Maria Python
/certificado João React
```

**Resposta esperada:**
```markdown
---

# 🏆 CERTIFICADO DE CONCLUSÃO

---

## Certificamos que

# Alexandre

concluiu com êxito a trilha de estudos:

## Java do Zero ao Profissional

---

**Tecnologia:** Java
**Nível:** Iniciante
**Módulos concluídos:** 12
**XP conquistado:** 4800 XP

**Badges conquistados:**
✦ Java Starter
✦ OOP Expert
✦ Java Pro

---

> Este certificado reconhece o esforço e dedicação de **Alexandre**
> na trilha **Java do Zero ao Profissional — Geo Explorer**.

**Data de emissão:** DD/MM/AAAA

---

*⚠️ Certificado fictício e demonstrativo gerado pelo projeto Geo-Explorer.*
*Não possui validade oficial.*
```

---

## 7. Lógica de Negócio — commands_logic.py

**Arquivo:** `src/commands_logic.py`

Este módulo separa completamente a lógica de negócio da camada de apresentação
(slash commands e MCP), tornando o código reutilizável e testável.

### Funções públicas

#### `consultar_trilha(tecnologia, caminho_json)`
Busca uma trilha pela tecnologia informada.

```python
from src.commands_logic import consultar_trilha

resultado = consultar_trilha("Java")

if resultado.encontrada:
    print(resultado.trilha["nome"])       # "Java do Zero ao Profissional"
    print(resultado.trilha["xp_total"])   # 4800
else:
    print(resultado.erro)
    print(resultado.tecnologias_disponiveis)
```

#### `validar_desafio(tecnologia, nivel)`
Valida os parâmetros para geração de desafio.

```python
from src.commands_logic import validar_desafio

resultado = validar_desafio("Python", "iniciante")

if resultado.valido:
    print(resultado.tecnologia)  # "Python"
    print(resultado.nivel)       # "iniciante"
else:
    print(resultado.erro)
```

#### `gerar_certificado(nome, tecnologia, caminho_json)`
Gera os dados do certificado, com fallback gracioso para JSON ausente.

```python
from src.commands_logic import gerar_certificado

resultado = gerar_certificado("Alexandre", "Java")

if resultado.valido:
    print(resultado.nome)           # "Alexandre"
    print(resultado.data_emissao)   # "DD/MM/AAAA"
    print(resultado.trilha_dados)   # dict com dados da trilha ou None
```

### Classes de resultado

| Classe | Campos principais |
|---|---|
| `ResultadoTrilha` | `encontrada`, `trilha`, `tecnologias_disponiveis`, `erro` |
| `ResultadoDesafio` | `valido`, `tecnologia`, `nivel`, `erro` |
| `ResultadoCertificado` | `valido`, `nome`, `tecnologia`, `trilha_dados`, `data_emissao`, `erro` |

### Funções utilitárias internas

| Função | Descrição |
|---|---|
| `_normalizar(texto)` | Remove acentos e converte para minúsculas para comparação |
| `_carregar_trilhas(caminho)` | Carrega o JSON; lança `FileNotFoundError` ou `ValueError` |
| `_buscar_trilha(tecnologia, dados)` | Busca trilha por `tecnologia` ou `nome` (case-insensitive) |

---

## 8. Testes Unitários

**Arquivo:** `src/test_commands.py`

### Execução

```bash
cd ~/Documents/Exercicios/Dio/geo-explorer
python3 src/test_commands.py
```

O relatório é salvo automaticamente em `docs/resultado_testes.txt`.

### Resultado atual

```
Total de testes executados : 59
✅ Aprovados                : 59
❌ Falhas                   : 0
💥 Erros                    : 0
📊 Taxa de aprovação        : 100.0%
🎯 Meta mínima              : 70.0%
✅ META ATINGIDA
```

### Suítes de teste

| Suíte | Testes | Cenários cobertos |
|---|---|---|
| `TestNormalizacao` | 5 | Acentos, maiúsculas, string vazia |
| `TestCarregarTrilhas` | 4 | JSON válido, arquivo ausente, vazio, inválido |
| `TestBuscarTrilha` | 7 | Java exato, minúsculas, maiúsculas, Python, nome parcial, inexistente, lista vazia |
| `TestConsultarTrilha` | 18 | Java com todos os campos, case-insensitive, erros, edge cases |
| `TestValidarDesafio` | 12 | Todos os níveis válidos (com/sem acento), parâmetros inválidos e vazios |
| `TestGerarCertificado` | 13 | Com trilha real, sem JSON, JSON inválido, trilha inexistente, erros de validação |

### Fixtures de teste

Os testes usam um JSON mínimo (`TRILHAS_FIXTURE`) com apenas 2 trilhas (Java e Python),
criado em arquivo temporário para isolamento total dos testes de sistema de arquivos.

---

## 9. Servidor MCP

**Arquivo:** `mcp/server.py`

O servidor expõe as ferramentas do Geo-Explorer via **Model Context Protocol v2**,
permitindo acesso local pelo IBM Bob e acesso remoto via HTTPS, SSE ou API.

### Ferramentas expostas

| Ferramenta | Parâmetros | Retorna |
|---|---|---|
| `consultar_trilha_tool` | `tecnologia: str` | Dados da trilha em Markdown |
| `gerar_desafio_tool` | `tecnologia: str`, `nivel: str` | Metadados e instruções do desafio |
| `gerar_certificado_tool` | `nome: str`, `tecnologia: str` | Certificado completo em Markdown |
| `listar_trilhas_tool` | _(nenhum)_ | Lista de todas as 32 trilhas |

### Modos de transporte

#### Modo stdio — IBM Bob local (padrão)
```bash
python3 mcp/server.py
# ou explicitamente:
python3 mcp/server.py --transport stdio
```

#### Modo SSE — acesso remoto via HTTPS/API (legado, amplo suporte)
```bash
python3 mcp/server.py --transport sse --host 0.0.0.0 --port 8000
# Endpoint SSE: http://host:8000/sse
```

#### Modo Streamable HTTP — padrão MCP v2 moderno
```bash
python3 mcp/server.py --transport http --host 0.0.0.0 --port 8000
# Endpoint MCP: http://host:8000/mcp
```

### Para expor via HTTPS

Configure um reverse proxy (nginx, Caddy ou Traefik) na frente da porta exposta.
Exemplo básico com Caddy:

```
geo-explorer.seu-dominio.com {
    reverse_proxy localhost:8000
}
```

### Para integração via API externa

Qualquer cliente compatível com MCP pode se conectar via SSE ou Streamable HTTP.
Exemplos de clientes compatíveis: Claude Desktop, Cursor, Windsurf, IBM Bob (remoto).

Configuração no cliente MCP:
```json
{
  "mcpServers": {
    "geo-explorer": {
      "url": "https://geo-explorer.seu-dominio.com/sse"
    }
  }
}
```

---

## 10. Registro no IBM Bob — mcp.json

**Arquivo:** `.bob/mcp.json`

```json
{
  "mcpServers": {
    "geo-explorer": {
      "command": "/usr/bin/python3",
      "args": [
        "/home/britos/Documents/Exercicios/Dio/geo-explorer/mcp/server.py"
      ],
      "env": {}
    }
  }
}
```

> **Importante:** o arquivo `.bob/mcp.json` registra o servidor **apenas para este projeto**.
> Outros projetos abertos no IBM Bob não terão acesso a este servidor.
> Para um registro global, use `~/.bob/mcp.json`.

---

## 11. Prompts Utilizados na Construção

Esta seção documenta todos os prompts usados na sessão de desenvolvimento com o IBM Bob,
como referência para profissionais que queiram replicar ou adaptar o projeto.

---

### Prompt 1 — Configuração do Git
```
Bob, configure para mim o Git globalmente para usar a credencial.help store,
garantindo que as credenciais fiquem salvas de forma persistente no ambiente
local do usuário, e não em nenhum arquivo de projeto.
```
**Resultado:** `git config --global credential.helper store`

---

### Prompt 2 — Clone do repositório
```
Bob, clone o seguinte repositório dentro de ~/Documents/Exercicios/Dio/:
https://github.com/britos-crt/geo-explorer.git
```
**Resultado:** Clone realizado em `~/Documents/Exercicios/Dio/geo-explorer`

---

### Prompt 3 — Arquivo de teste de conexão
```
Bob, crie dentro do repositório clonado um arquivo .md com o nome de
CONECTIONTESTE, que em seu conteúdo contenha essa frase: "Hello World!"
```
**Resultado:** `CONECTIONTESTE.md` criado com conteúdo `Hello World!`

---

### Prompt 4 — Estrutura de diretórios
```
Bob, crie dentro do repositório clonado uma estrutura de projeto "geo-explorer"
e dentro dessa estrutura os diretórios: src, data, commands, mcp e docs.
```
**Resultado:** Criação dos 5 diretórios na raiz do projeto

---

### Prompt 5 — Criação do arquivo de dados
```
Bob, dentro do diretório "data", crie para mim um arquivo com o nome de
"trilhas_geo" com a extensão .json
```
**Resultado:** `data/trilhas_geo.json` criado com conteúdo `{}`

---

### Prompt 6 — Populando as trilhas
```
Bob, agora dentro do arquivo trilhas_geo.json, crie uma lista extensa e bem
detalhada de pelo menos 30 trilhas fictícias, utilizando como referência a DIO,
contendo nomes, tecnologia, nível, número de módulos, XP total, badges
disponíveis, promoções, vitalício, e live ao vivo.
```
**Resultado:** 32 trilhas ficticias com schema completo

---

### Prompt 7 — Arquivo .bobignore
```
Bob, crie um arquivo .bobignore na raiz do projeto. Dentro desse arquivo
ignore as seguintes palavras e diretórios: /node_modules, arquivos com a
extensão ".env", /data/cache-progresso, certificados gerados
/docs/certificados-emitidos e qualquer outro arquivo com a extensão ".temp".
```
**Resultado:** `.bobignore` com 5 regras de exclusão

---

### Prompt 8 — Slash commands
```
Bob, implemente três slash commands locais, exclusivos deste projeto:
/trilhas, /desafio e /certificado. [especificação detalhada de cada comando
com tratamento de erros, integração com o JSON, formatação Markdown, etc.]
```
**Resultado:** 3 arquivos em `.bob/commands/` com frontmatter e lógica completa

---

### Prompt 9 — Testes unitários
```
Bob, crie arquivos de testes unitários e teste esse fluxo para atingir uma
cobertura de 70% de aprovação. Teste os comandos /trilhas para consultar
trilhas de Java, gere um desafio para o aluno e um certificado para o mesmo.
Grave os resultados em um arquivo TXT para acompanhamento.
```
**Resultado:** `src/commands_logic.py` + `src/test_commands.py` (59 testes, 100% aprovação)
+ `docs/resultado_testes.txt`

---

### Prompt 10 — Servidor MCP
```
Bob, crie um MCP server do projeto geo-explorer, para que futuramente pessoas
possam vir acessá-lo por meio de um servidor HTTPS ou SSO ou via API.
Use a pasta MCP do projeto para isso.
```
**Resultado:** `mcp/server.py` (MCPServer v2, 3 transportes), `mcp/requirements.txt`,
`.bob/mcp.json`

---

### Prompt 11 — Documentação
```
Bob, crie um arquivo de documentação de todo o projeto feito até o momento,
com todos os prompts usados, modos de uso, dicas de uso, insights, para futuros
profissionais que irão consultar ou aprender ou até mesmo implementar o projeto.
```
**Resultado:** Este arquivo — `docs/GEO_EXPLORER_DOCS.md`

---

## 12. Modos de Uso

### Modo 1 — Uso via chat do IBM Bob (slash commands)

Abra o projeto no IBM Bob e use diretamente no chat:

```
/trilhas Python
/desafio Java iniciante
/certificado Alexandre React
```

Os comandos aparecem automaticamente no menu ao digitar `/`.

---

### Modo 2 — Uso via ferramentas MCP no IBM Bob

Com o projeto aberto e o servidor MCP registrado em `.bob/mcp.json`,
o IBM Bob pode chamar as ferramentas diretamente ao processar suas mensagens.
Basta perguntar naturalmente:

```
"Me mostre a trilha de Docker"
"Gere um desafio avançado de Python para mim"
"Quero meu certificado de conclusão de Java"
"Liste todas as trilhas disponíveis"
```

---

### Modo 3 — Uso via linha de comando (Python)

```python
import sys
sys.path.insert(0, 'src')
from commands_logic import consultar_trilha, validar_desafio, gerar_certificado

# Consultar trilha
r = consultar_trilha("Java")
print(r.trilha["nome"])

# Validar desafio
r = validar_desafio("Python", "iniciante")
print(r.valido, r.tecnologia, r.nivel)

# Gerar certificado
r = gerar_certificado("Alexandre", "Java")
print(r.nome, r.data_emissao)
```

---

### Modo 4 — Uso via API/HTTPS (remoto)

Inicie o servidor em modo SSE:
```bash
python3 mcp/server.py --transport sse --host 0.0.0.0 --port 8000
```

Qualquer cliente MCP pode se conectar ao endpoint `http://host:8000/sse`
e chamar as ferramentas via protocolo MCP.

---

### Modo 5 — Execução dos testes

```bash
cd ~/Documents/Exercicios/Dio/geo-explorer
python3 src/test_commands.py
```

---

## 13. Dicas de Uso

### Para desenvolvedores

1. **Adicionar novas trilhas:** edite apenas `data/trilhas_geo.json`. Nenhum código
   precisa ser alterado — toda a lógica de busca é dinâmica.

2. **Adicionar novo slash command:** crie um arquivo `.md` em `.bob/commands/`
   com frontmatter `description` e `argument-hint`. Use `$1`, `$2`... para os argumentos.

3. **Adicionar nova ferramenta MCP:** em `mcp/server.py`, use o decorator `@mcp.tool()`
   com uma função Python pura. Nenhuma reinicialização manual é necessária — o Bob
   recarrega automaticamente.

4. **Reutilizar a lógica de negócio:** `src/commands_logic.py` é independente de
   framework — pode ser importado tanto pelo MCP server quanto por scripts externos,
   CLIs ou APIs REST futuras.

5. **Busca é tolerante:** a busca por tecnologia aceita maiúsculas, minúsculas,
   acentos e correspondência parcial por nome. `"java"`, `"JAVA"` e `"Java"` retornam
   o mesmo resultado.

---

### Para estudantes

1. **Explore o código em camadas:** comece por `data/trilhas_geo.json` (dados),
   depois `src/commands_logic.py` (regras), depois `mcp/server.py` (exposição).

2. **Use os testes como documentação viva:** `src/test_commands.py` demonstra como
   cada função se comporta em todos os cenários — é uma excelente referência.

3. **Experimente os comandos:** com o projeto aberto no IBM Bob, teste cada comando
   com diferentes tecnologias e observe o comportamento de erro intencional.

4. **Estude a estrutura MCP:** o `mcp/server.py` é um exemplo real e funcional de
   como expor uma API via Model Context Protocol — uma tecnologia emergente em 2025.

---

### Para profissionais que vão implementar o projeto

1. **Credenciais Git:** configure sempre `credential.helper` antes de trabalhar
   com repositórios privados. O `store` salva em texto plano; para ambientes
   corporativos, prefira `libsecret` (Linux) ou `osxkeychain` (macOS).

2. **Segurança de tokens:** nunca exponha Personal Access Tokens em chats.
   Use variáveis de ambiente ou gestores de segredos (Vault, AWS Secrets Manager).

3. **Para produção:** substitua o `store` do Git por autenticação via SSH key ou
   OIDC. Coloque o servidor MCP atrás de um reverse proxy com TLS.

4. **Escalonamento:** para múltiplos usuários simultâneos no modo HTTP, considere
   múltiplas instâncias com um load balancer na frente.

5. **Persistência de dados:** substitua o `trilhas_geo.json` por um banco de dados
   (PostgreSQL, MongoDB) para ambientes com muita escrita. A camada
   `commands_logic.py` precisa de alteração mínima para isso.

---

## 14. Insights e Decisões de Arquitetura

### Separação em camadas
A decisão de separar `commands_logic.py` dos slash commands e do servidor MCP foi
fundamental. Isso permite:
- Testar a lógica de forma isolada (sem depender do IBM Bob ou do MCP)
- Reutilizar o mesmo código em múltiplos contextos (slash commands, MCP, CLI, API REST)
- Substituir partes do sistema sem refatoração em cascata

### Slash commands como prompts de IA
Os arquivos `.md` em `.bob/commands/` não são scripts tradicionais — são **instruções
para a IA** do Bob. Isso significa que o "processamento" é feito pelo modelo de
linguagem, não por código executado localmente. Consequência importante: o mesmo
comando pode gerar respostas ligeiramente diferentes a cada execução, o que é
proposital para o `/desafio` (variedade) mas deve ser levado em conta para o
`/trilhas` (consistência esperada).

### MCP SDK v2 com MCPServer
A versão instalada era o MCP SDK v2, que renomeou `FastMCP` para `MCPServer`
(de `mcp.server.mcpserver`). O decorator `@mcp.tool()` e os métodos
`run_stdio_async()`, `run_sse_async()`, `run_streamable_http_async()` são o
padrão v2. Qualquer código escrito para MCP v1 com `FastMCP` requer ajuste.

### Busca tolerante a acentos e maiúsculas
A função `_normalizar()` usa `str.maketrans` para remover acentos antes da
comparação. Isso garante que `"intermediário"`, `"intermediario"` e `"INTERMEDIARIO"`
sejam tratados como equivalentes — essencial para uma boa experiência de usuário
em português.

### Certificado gracioso em caso de falha
O `/certificado` nunca falha por ausência do JSON — gera um certificado genérico.
Isso é intencional: a experiência do usuário de receber seu certificado nunca
deve ser bloqueada por um problema de infraestrutura.

### .bobignore
Assim como `.gitignore` instrui o Git, o `.bobignore` instrui o IBM Bob a não
indexar certos arquivos no contexto das conversas. Isso é importante para:
- Segurança: evitar que arquivos `.env` com credenciais sejam lidos pelo modelo
- Performance: evitar indexar caches e arquivos temporários desnecessários
- Privacidade: evitar que certificados emitidos apareçam em contexto

---

## 15. Expansão Futura

### Funcionalidades sugeridas

| Funcionalidade | Complexidade | Onde implementar |
|---|---|---|
| Banco de dados real (PostgreSQL/MongoDB) | Média | `src/commands_logic.py` |
| Autenticação JWT para API remota | Alta | `mcp/server.py` + middleware |
| Dashboard de progresso do aluno | Alta | Novo módulo `src/progresso.py` |
| Suporte a múltiplos idiomas (i18n) | Média | `data/` + `src/` |
| Geração de PDF do certificado | Média | Nova ferramenta MCP + `reportlab` |
| Integração real com API da DIO | Alta | Nova ferramenta MCP + OAuth |
| Busca semântica de trilhas (embeddings) | Alta | Nova ferramenta MCP + `sentence-transformers` |
| Cache Redis para consultas frequentes | Média | `src/commands_logic.py` |
| Webhook para notificação de promoções | Média | Novo endpoint em `mcp/server.py` |
| /progresso para acompanhar trilha atual | Baixa | `.bob/commands/progresso.md` |

### Novos slash commands sugeridos

```
/progresso <tecnologia>   — acompanha progresso em uma trilha
/comparar <tec1> <tec2>   — compara duas trilhas lado a lado
/recomendar <nivel>        — recomenda trilhas por nível
/ranking                   — exibe trilhas com maior XP
```

---

## 16. Referências

- [IBM Bob Documentation](https://bob.ibm.com/docs) — Documentação oficial do IBM Bob
- [MCP SDK Python v2 — Migration Guide](https://py.sdk.modelcontextprotocol.io/v2/migration/) — Guia de migração MCPServer
- [Model Context Protocol Specification](https://modelcontextprotocol.io/) — Especificação oficial do protocolo MCP
- [DIO — Digital Innovation One](https://www.dio.me/) — Plataforma de referência para as trilhas fictícias
- [Python unittest](https://docs.python.org/3/library/unittest.html) — Documentação do framework de testes
- [Git credential.helper](https://git-scm.com/docs/git-credential-store) — Documentação do armazenamento de credenciais Git

---

*Documentação gerada com auxílio do IBM Bob — Junho de 2025*  
*Projeto: geo-explorer | Repositório: https://github.com/britos-crt/geo-explorer*
