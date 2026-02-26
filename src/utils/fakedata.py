"""Módulo para gerar dados simulados de roaming móvel."""

import os
import random
from datetime import timedelta

import numpy as np
import pandas as pd
from faker import Faker

# Configuração inicial
fake = Faker()
Faker.seed(42)  # Para reprodutibilidade
np.random.seed(42)  # Para reprodutibilidade


def generate_roaming_data(num_rows: int = 1000):
    """Gera um DataFrame simulado de dados de roaming móvel.

    Args:
        num_rows (int, optional): Número de linhas no DataFrame. Padrão é 1000.

    Returns:
        pd.DataFrame: DataFrame contendo os dados simulados.
    """
    data: list[dict[str, object]] = []

    # Listas de domínio para dar realismo
    tadig_codes = [
        "BRAV1",
        "NLDLT",
        "FRAF1",
        "ESPTE",
    ]  # Exemplo: Country + Operator
    call_types = ["MOC", "MTC", "SMS", "GPRS"]  # MOC=Voice Out, MTC=Voice In, GPRS=Data
    apns = ["internet", "ims", "corporate.apn", "mms"]

    for _ in range(num_rows):
        # 1. Datas (Lógica: Processamento ocorre 1 a 5 dias após a chamada)
        call_date = fake.date_time_between(start_date="-30d", end_date="now")
        processing_lag = random.randint(1, 5)
        tap_date = call_date + timedelta(days=processing_lag)

        # 2. Identificadores
        # IMSI geralmente tem 15 dígitos (MCC+MNC+MSIN)
        imsi = fake.numerify(text="72411%%%%%%%%%%")  # 724 é Brasil 11 é Vivo
        # MSISDN (Phone Number)
        msisdn = fake.numerify(text="55119########")
        # TAC (Type Allocation Code - primeiros 8 digitos do IMEI)
        device_tac = fake.numerify(text="########")

        # 3. Definição do Tipo de Chamada e Métricas
        call_type = random.choice(call_types)
        tadig = random.choice(tadig_codes)

        charged_events = 0
        charged_minutes = 0.0
        charged_mb = 0.0
        apn_network = ""
        gross_charge = 0.0

        # Lógica de cobrança baseada no tipo
        if call_type == "GPRS":  # Dados
            charged_mb = round(random.uniform(0.001, 10000.0), 9)
            apn_network = random.choice(apns)
            number_of_events = random.randint(1, 100)  # Sessões de dados
            charged_events = number_of_events
            gross_charge = charged_mb * 0.0005

        elif call_type == "SMS":
            number_of_events = random.randint(1, 5)
            charged_events = number_of_events
            gross_charge = number_of_events * 0.01

        else:  # MOC ou MTC (Voz)
            charged_minutes = round(random.uniform(0.5, 600.0), 9)
            number_of_events = 1
            charged_events = 1
            gross_charge = charged_minutes * 0.05

        # Adicionar ruído/variações no custo (simulando acordos diferentes)
        gross_charge = round(gross_charge * random.uniform(0.9, 1.1), 9)

        row: dict[str, object] = {
            "TAP File (Current) Processing Date": tap_date.strftime("%Y-%m-%d"),
            "Date (Call)": call_date.strftime("%Y-%m-%d %H:%M:%S"),
            "PMN (Settlement) TADIG Code": tadig,
            "Call Type": call_type,
            "IMSI": imsi,
            "MSISDN": msisdn,
            "APN Network": apn_network,
            "Device TAC": device_tac,
            "Number of Events": number_of_events,
            "Charged Events": charged_events,
            "Charged Minutes": charged_minutes,
            "Charged MB": charged_mb,
            "Settlement Gross Charge - USD": gross_charge,
        }
        data.append(row)

    return pd.DataFrame(data)


if __name__ == "__main__":
    # Gerar e Salvar
    df_fake = generate_roaming_data(5000)  # Gerar 5000 linhas

    os.makedirs("./data", exist_ok=True)
    df_fake.to_csv(
        "./data/roaming_traffic_dummy.csv",
        index=False,
        sep=";",
        decimal=",",
        header=True,
    )

    print("Arquivo gerado com sucesso!")
    print(df_fake.head(5))
