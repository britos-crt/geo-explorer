---
description: Gera um certificado fictício de conclusão de trilha para o usuário
argument-hint: <nome-do-usuario> <tecnologia>
---

O usuário quer gerar um certificado fictício de conclusão. Nome do usuário: **$1**. Trilha/tecnologia: **$2**.

Siga os passos abaixo rigorosamente:

1. **Valide os parâmetros:**
   - Se `$1` não foi informado, exiba:
     ```
     ❌ Informe seu nome. Uso correto: `/certificado <seu-nome> <tecnologia>`
     Exemplo: `/certificado Alexandre Python`
     ```
   - Se `$2` não foi informado, exiba:
     ```
     ❌ Informe a trilha/tecnologia. Uso correto: `/certificado <seu-nome> <tecnologia>`
     Exemplo: `/certificado Alexandre Python`
     ```

2. **Leia o arquivo `data/trilhas_geo.json`** e procure uma trilha cujo campo `tecnologia` ou `nome` contenha **$2** (sem distinção de maiúsculas/minúsculas).

3. **Se a trilha for encontrada no JSON**, gere o certificado com os dados reais da trilha:

```
---

# 🏆 CERTIFICADO DE CONCLUSÃO

---

## Certificamos que

# $1

concluiu com êxito a trilha de estudos:

## <nome completo da trilha encontrada no JSON>

---

**Tecnologia:** <tecnologia>
**Nível:** <nivel>
**Módulos concluídos:** <modulos>
**XP conquistado:** <xp_total> XP
**Badges conquistados:**
<liste cada badge em uma linha com ✦>

---

> Este certificado reconhece o esforço, dedicação e aprendizado de **$1**
> na trilha **<nome da trilha> — Geo Explorer**.

**Data de emissão:** <data atual no formato DD/MM/AAAA>

---

*⚠️ Certificado fictício e demonstrativo gerado pelo projeto Geo-Explorer.*
*Não possui validade oficial.*

---
```

4. **Se a trilha NÃO for encontrada no JSON**, gere um certificado genérico utilizando apenas os dados informados pelo usuário:

```
---

# 🏆 CERTIFICADO DE CONCLUSÃO

---

## Certificamos que

# $1

concluiu com êxito a trilha de estudos:

## $2 — Geo Explorer

---

> Este certificado reconhece o esforço, dedicação e aprendizado de **$1**
> na trilha de **$2**.

**Data de emissão:** <data atual no formato DD/MM/AAAA>

---

*⚠️ Certificado fictício e demonstrativo gerado pelo projeto Geo-Explorer.*
*Não possui validade oficial.*

---
```

5. **Se o arquivo `data/trilhas_geo.json` não existir ou o JSON for inválido**, gere o certificado genérico do passo 4 mesmo assim, sem interromper o fluxo.

6. O certificado deve ser exibido **integralmente no chat**, formatado em Markdown, de forma solene e profissional.
