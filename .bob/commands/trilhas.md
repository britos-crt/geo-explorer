---
description: Consulta o arquivo data/trilhas_geo.json e exibe o plano de estudos de uma tecnologia
argument-hint: <tecnologia>
---

O usuário quer ver o plano de estudos da trilha de **$1**.

Siga os passos abaixo rigorosamente:

1. Leia o arquivo `data/trilhas_geo.json` localizado na raiz deste projeto.
2. Procure na lista `trilhas` um item cujo campo `tecnologia` contenha o termo **$1** (faça a busca sem distinção de maiúsculas/minúsculas). Se não encontrar por `tecnologia`, tente também pelo campo `nome`.
3. **Se a trilha for encontrada**, apresente no chat um plano de estudos formatado em Markdown com as seguintes seções:

```
# Trilha de <nome da trilha>

**Tecnologia:** <tecnologia>
**Nível:** <nivel>
**Módulos:** <modulos>
**XP Total:** <xp_total> XP
**Vitalício:** Sim / Não

## Badges disponíveis
- <badge 1>
- <badge 2>
- <badge 3>

## Promoção
<Se ativa: "✅ Desconto de X% — válido até <validade>">
<Se inativa: "❌ Sem promoção ativa no momento.">

## Live ao Vivo
<Se disponível: "📡 Disponível — <frequencia>, toda <dia_semana>">
<Se indisponível: "📵 Não há lives ao vivo para esta trilha.">

## Plano de Estudos sugerido

Com base nos <modulos> módulos desta trilha de <tecnologia> no nível <nivel>, apresente um plano de estudos detalhado, dividido em módulos numerados sequencialmente. Cada módulo deve ter:
- Um título temático coerente com a tecnologia e o nível
- De 3 a 5 tópicos/subtópicos relevantes ao conteúdo esperado

---
*Plano gerado com base nos dados do projeto Geo-Explorer.*
```

4. **Se a trilha NÃO for encontrada**, exiba:

```
❌ Trilha para "$1" não encontrada no arquivo `data/trilhas_geo.json`.

**Tecnologias disponíveis:**
<liste todos os valores do campo `tecnologia` de cada item da lista `trilhas`>

Dica: tente `/trilhas <uma das tecnologias acima>`.
```

5. **Se o arquivo não existir ou o JSON for inválido**, exiba:
```
⚠️ Não foi possível ler o arquivo `data/trilhas_geo.json`. Verifique se o arquivo existe e se o JSON é válido.
```
