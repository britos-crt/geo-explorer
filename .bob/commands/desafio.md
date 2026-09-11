---
description: Gera um desafio de programação aleatório baseado em tecnologia e nível de dificuldade
argument-hint: <tecnologia> <nivel: iniciante|intermediario|avancado>
---

O usuário quer um desafio de programação para a tecnologia **$1** no nível **$2**.

Siga os passos abaixo rigorosamente:

1. **Valide os parâmetros:**
   - Se `$1` não foi informado, exiba:
     ```
     ❌ Informe a tecnologia. Uso correto: `/desafio <tecnologia> <nivel>`
     Exemplo: `/desafio Python iniciante`
     ```
   - Se `$2` não foi informado, exiba:
     ```
     ❌ Informe o nível de dificuldade. Uso correto: `/desafio <tecnologia> <nivel>`
     Níveis válidos: iniciante | intermediário | avançado
     Exemplo: `/desafio Python iniciante`
     ```
   - Se `$2` não for um dos valores válidos (`iniciante`, `intermediário`, `intermediario`, `avançado`, `avancado`), exiba:
     ```
     ❌ Nível inválido: "$2"
     Níveis válidos: iniciante | intermediário | avançado
     ```

2. **Se os parâmetros forem válidos**, gere um desafio de programação criativo, coerente e educativo para a tecnologia **$1** no nível **$2**, formatado exatamente assim:

```
# 🧩 Desafio de $1

**Nível:** $2

---

## 📋 Descrição

<Descreva o desafio de forma clara e objetiva em 2 a 4 linhas.>

## ✅ Requisitos

- <Requisito 1>
- <Requisito 2>
- <Requisito 3>
- <Requisito 4 (se aplicável)>

## 💡 Exemplo

**Entrada:**
<Mostre um exemplo de entrada no formato de código compatível com $1>

**Saída esperada:**
<Mostre a saída esperada no formato de código>

## 🎯 Objetivo de aprendizado

<Explique em 1 ou 2 frases o que o aluno vai praticar com este desafio.>

## 💬 Dica

<Ofereça uma dica opcional que não entregue a solução, mas ajude o aluno a pensar no caminho certo.>

---
*Desafio gerado pelo Geo-Explorer para a tecnologia $1 — nível $2.*
```

3. O desafio deve ser **variado**: cada vez que o comando for executado com os mesmos parâmetros, gere um desafio diferente. Use criatividade para variar os temas: algoritmos, estruturas de dados, manipulação de strings, lógica, APIs, banco de dados, etc.

4. O nível de complexidade deve respeitar o nível informado:
   - **Iniciante:** conceitos básicos, sintaxe, estruturas simples
   - **Intermediário:** funções, estruturas de dados, manipulação de arquivos, APIs
   - **Avançado:** padrões de projeto, concorrência, otimização, arquitetura
