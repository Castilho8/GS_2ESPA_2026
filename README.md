# 💧 Água em Casa

**Um sensor na caixa d'água que avisa a família antes de a água acabar durante a redução noturna de pressão.**
FIAP · Global Solution 2026.2 · CitizenTech · Engenharia de Software, 2º ano

**Integrante:** Bruno Santos Castilho · RM 566799

## Ficha da CitizenTech

| Campo | |
|---|---|
| **Nome** | Água em Casa |
| **Cidade** | São Paulo |
| **Cidadão beneficiado** | Famílias de São Paulo, principalmente em bairros altos e casas com caixa d'água pequena, que ficam sem água de madrugada.  |
| **Problema em uma frase** | Desde agosto de 2025 a Sabesp reduz a pressão da água à noite (hoje das 22h às 6h), e a família não sabe se a caixa d'água vai durar até a pressão voltar: só descobre quando a torneira seca. |
| **Como funciona** | Um sensor na tampa da caixa mede o nível. O sistema calcula quanto a família gastou na última hora e quantas horas a água ainda dura. Se ela não dura até as 6h, o celular avisa a família, em linguagem simples, para economizar a tempo. |
| **O que cada parte faz** | **Sensor** (ESP32 + HC-SR04): mede a distância até a água e acende um LED verde, amarelo ou vermelho. **Python:** calcula o nível, o gasto por hora, as horas restantes e o aviso. **Página web:** mostra o aviso para a família, com cor e texto. **Banco de dados:** guarda o histórico de leituras e alertas. |
| **Link do repositório** | https://github.com/Castilho8/GS_2ESPA_2026 |
| **Indicador de impacto** | **Aviso a tempo:** em 3 de cada 4 noites em que a água quase acabou (74%), a família foi avisada pelo menos 1 hora antes. **Menos noites sem água:** a caixa ficou vazia antes das 6h em 1 de cada 12 noites sem o sistema (8,3%) e em só 1 de cada 43 com o aviso (2,3%). (dados simulados) |
| **ODS conectados** | **11, 10 e 13** (explicação abaixo) |

### ODS: como o projeto contribui
- **ODS 11 (Cidades e comunidades sustentáveis):** a meta 11.1 fala de acesso a serviços básicos adequados. O projeto ajuda a família a manter o abastecimento durante a redução de pressão.
- **ODS 10 (Redução das desigualdades):** a falta de água pesa mais em bairros altos e em casas com caixa pequena. A solução é barata e dá a essas famílias uma informação que hoje elas não têm.
- **ODS 13 (Ação contra a mudança do clima):** a redução existe por causa da estiagem. O aviso ajuda as famílias a se adaptarem (meta 13.1, resiliência) e a economizar água nos períodos críticos.
