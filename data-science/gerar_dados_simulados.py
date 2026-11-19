# -*- coding: utf-8 -*-
"""
Água em Casa - gera a base simulada de leituras dos sensores.

Saídas (pasta dados/):
  casas_simuladas.csv              1 linha por casa
  leituras_sensor_simuladas.csv    1 linha por leitura (a cada 15 min, das 22h às 6h)

Valores usados:
  - 20 casas em 5 bairros (A a E); bairros altos não recebem água na redução
  - caixas de 500 L (58 cm de água) ou 1000 L (80 cm)
  - consumo por pessoa maior às 22h e menor de madrugada
  - outubro/2026: noites 1 a 15 sem aviso, 16 a 30 com aviso
  - depois do aviso a família gasta 40% menos
  - alguns erros de leitura (vazias, fora do alcance e duplicadas)
"""
import numpy as np
import pandas as pd
from pathlib import Path

SEMENTE = 2026
rng = np.random.default_rng(SEMENTE)
PASTA = Path(__file__).parent / "dados"
PASTA.mkdir(exist_ok=True)

# --------------------------------------------------------------------------
# 1. Casas
# --------------------------------------------------------------------------
BAIRROS = {  # bairro: (altitude, entrada de água durante a redução em L/h)
    "Bairro A": ("alta", 0.0),
    "Bairro B": ("alta", 0.0),
    "Bairro C": ("média", 15.0),
    "Bairro D": ("média", 15.0),
    "Bairro E": ("baixa", 40.0),
}
ALTURA_CAIXA = {500: 58.0, 1000: 80.0}   # cm de água útil em cada modelo

casas = []
n = 1
for bairro, (altitude, _) in BAIRROS.items():
    for _ in range(4):
        capacidade = int(rng.choice([500, 1000], p=[0.4, 0.6]))
        casas.append({
            "casa_id": "C%02d" % n,
            "bairro": bairro,
            "altitude": altitude,
            "capacidade_litros": capacidade,
            "altura_caixa_cm": ALTURA_CAIXA[capacidade],
            "moradores": int(rng.choice([1, 2, 3, 4, 5, 6],
                                        p=[0.10, 0.20, 0.30, 0.22, 0.12, 0.06])),
        })
        n += 1
casas = pd.DataFrame(casas)

# --------------------------------------------------------------------------
# 2. Leituras: 30 noites x 20 casas x 33 leituras (22:00 a 06:00, a cada 15 min)
# --------------------------------------------------------------------------
CONSUMO_PESSOA_HORA = {22: 30, 23: 18, 0: 7, 1: 3, 2: 2, 3: 2, 4: 3, 5: 12, 6: 15}  # L/h
REDUCAO_COM_AVISO = 0.40
OFFSET_SENSOR_CM = 3.0     # o sensor fica 3 cm acima do nível máximo da água
PASSO_H = 0.25             # 15 minutos

linhas = []
noites = pd.date_range("2026-10-01", "2026-10-30", freq="D")
for numero_noite, noite in enumerate(noites, start=1):
    aviso_ativo = int(numero_noite >= 16)
    for casa in casas.itertuples():
        altitude, entrada = BAIRROS[casa.bairro]
        ini = {"alta": (0.45, 0.90), "média": (0.55, 0.95), "baixa": (0.75, 1.00)}[altitude]
        litros = rng.uniform(*ini) * casa.capacidade_litros
        fator_casa = rng.uniform(0.85, 1.20)
        fator_noite = rng.lognormal(0, 0.25)
        avisada = False
        historico = []
        for k in range(33):
            data_hora = noite + pd.Timedelta(hours=22) + pd.Timedelta(minutes=15 * k)
            # leitura do sensor neste instante
            nivel = litros / casa.capacidade_litros
            distancia = casa.altura_caixa_cm * (1 - nivel) + OFFSET_SENSOR_CM
            distancia += rng.normal(0, 0.4)
            historico.append(litros)

            # o sistema calcula as horas restantes com o consumo da última hora
            alerta = 0
            if aviso_ativo and k >= 4:
                gasto_1h = max(historico[-5] - litros, 1e-6)
                horas_restantes = litros / gasto_1h
                horas_ate_6h = (33 - 1 - k) * PASSO_H
                if horas_restantes < horas_ate_6h:
                    alerta = 1
                    avisada = True

            linhas.append({
                "casa_id": casa.casa_id,
                "data_hora": data_hora,
                "distancia_cm": round(distancia, 1),
                "aviso_ativo": aviso_ativo,
                "alerta_enviado": alerta,
            })

            # água que sai (consumo) e que entra (pressão reduzida) nos próximos 15 min
            consumo = (CONSUMO_PESSOA_HORA[data_hora.hour] * casa.moradores
                       * fator_casa * fator_noite * rng.uniform(0.7, 1.3))
            if avisada:
                consumo *= (1 - REDUCAO_COM_AVISO)
            litros = litros + (entrada - consumo) * PASSO_H
            litros = float(np.clip(litros, 0, casa.capacidade_litros))

leituras = pd.DataFrame(linhas)

# --------------------------------------------------------------------------
# 3. Erros típicos de sensor (para a etapa de preparação dos dados)
# --------------------------------------------------------------------------
idx = leituras.sample(frac=0.008, random_state=1).index
leituras.loc[idx, "distancia_cm"] = np.nan                    # leitura vazia
idx = leituras.drop(idx).sample(frac=0.004, random_state=2).index
leituras.loc[idx, "distancia_cm"] = 400.0                     # fora do alcance
duplicadas = leituras.sample(frac=0.003, random_state=3)
leituras = pd.concat([leituras, duplicadas]).sort_values(["casa_id", "data_hora"])
leituras.insert(0, "leitura_id", range(1, len(leituras) + 1))
leituras["data_hora"] = leituras["data_hora"].dt.strftime("%Y-%m-%d %H:%M")

casas.to_csv(PASTA / "casas_simuladas.csv", index=False)
leituras.to_csv(PASTA / "leituras_sensor_simuladas.csv", index=False)
print("casas:", len(casas), "| leituras:", len(leituras))
