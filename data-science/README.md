# Água em Casa: Data Science & Statistical Computing

**FIAP · Global Solution 2026.2 · CitizenTech · Engenharia de Software (2º ano)**

| Integrante | RM |
|---|---|
| Bruno Santos Castilho | 566799 |

## O que é
Análise descritiva dos dados da **Água em Casa**: um sensor na caixa d'água que avisa a família antes de a água acabar durante a redução noturna de pressão da Sabesp (22h às 6h).

O notebook responde a 5 perguntas:
1. Os reservatórios de São Paulo passam por períodos de falta?
2. Em que horário as famílias mais gastam água?
3. Sem o sistema, em quantas noites a caixa secaria?
4. Com o aviso, as famílias chegam às 6h com mais água?
5. O número de moradores e o tamanho da caixa influenciam o risco?

## Arquivos

```
data-science/
├── analise_agua_em_casa.ipynb       notebook executado (preparação, análise, gráficos, conclusões)
├── gerar_dados_simulados.py         script que gera a base simulada (semente fixa 2026)
├── README.md
└── dados/
    ├── mananciais_sabesp_2000_2024.csv    base PÚBLICA
    ├── casas_simuladas.csv                base SIMULADA (20 casas)
    └── leituras_sensor_simuladas.csv      base SIMULADA (19.859 leituras)
```

## Fontes dos dados
| Arquivo | Fonte |
|---|---|
| `mananciais_sabesp_2000_2024.csv` | **Pública.** Volume diário dos sistemas que abastecem a Grande SP (01/01/2000 a 16/10/2024). Dados do Portal dos Mananciais da Sabesp, organizados por Beatriz Milz no pacote *mananciais* (licença CC BY 4.0): https://github.com/beatrizmilz/mananciais · DOI 10.5281/zenodo.4733056 |
| `casas_simuladas.csv` e `leituras_sensor_simuladas.csv` | Simuladas pelo `gerar_dados_simulados.py` (valores explicados na seção 1 do notebook). Sem dados pessoais. |

Contexto da redução de pressão (22h às 6h): Diário do Grande ABC (31/07/2026) e Correio da Manhã (out/2026), a partir de decisões da Arsesp e da Sabesp.

## Como executar
1. Instale o Python 3.10 ou mais novo e as bibliotecas:
   ```
   pip install pandas numpy matplotlib jupyter
   ```
2. Deixe a pasta `dados/` ao lado do notebook.
3. Abra o notebook:
   ```
   jupyter notebook analise_agua_em_casa.ipynb
   ```
   Depois clique em *Run All*. Também funciona no VS Code e no Google Colab; no Colab, envie a pasta `dados/` antes.
4. Para gerar a base simulada de novo, rode `python gerar_dados_simulados.py`. A semente é fixa, então o resultado sai sempre igual.

## Principais resultados
- O Cantareira ficou abaixo de 30% em 19% dos dias entre 2000 e 2024, e abaixo de zero (reserva técnica) por 536 dias em 2014 e 2015.
- 61% da água da noite sai entre 22h e 0h.
- Sem aviso, a caixa secou antes das 6h em 8,3% das noites, e em 16,7% nos bairros altos.
- Com o aviso, as noites em que a caixa secou caíram para 2,3%.
- O número de moradores tem correlação forte com o gasto noturno (0,71).
