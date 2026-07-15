import pandas as pd

from config import ABA_DADOS, PLANILHA_ID, PLANILHA_ID_2, ABA_DADOS_2
from gsheets_conector import abrir_planilha


def carregar_dados_brutos() -> pd.DataFrame:
    """Carrega os dados da aba configurada no Google Sheets."""
    spreadsheet = abrir_planilha(PLANILHA_ID)
    worksheet = spreadsheet.worksheet(ABA_DADOS)
    return pd.DataFrame(worksheet.get_all_records())

def carregar_dados_brutos_2() -> pd.DataFrame:
    """Carrega os dados da aba configurada no Google Sheets."""
    spreadsheet = abrir_planilha(PLANILHA_ID_2)
    worksheet = spreadsheet.worksheet(ABA_DADOS_2)
    return pd.DataFrame(worksheet.get_all_records())


def carregar_dados_preparados() -> pd.DataFrame:
    """Carrega e aplica limpezas básicas estáveis para análise."""
    df = carregar_dados_brutos()

    df.columns = df.columns.str.strip()
    df = df.dropna(how="all")
    df = df.replace("", pd.NA)

    return df


def carregar_dados_preparados_2() -> pd.DataFrame:
    """Carrega e aplica limpezas básicas estáveis para análise."""
    df = carregar_dados_brutos_2()

    df.columns = df.columns.str.strip()
    df = df.dropna(how="all")
    df = df.replace("", pd.NA)

    return df
