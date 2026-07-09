import pandas as pd

from config import ABA_DADOS, PLANILHA_ID
from gsheets_conector import abrir_planilha


def carregar_dados_brutos() -> pd.DataFrame:
    """Carrega os dados da aba configurada no Google Sheets."""
    spreadsheet = abrir_planilha(PLANILHA_ID)
    worksheet = spreadsheet.worksheet(ABA_DADOS)
    return pd.DataFrame(worksheet.get_all_records())


def carregar_dados_preparados() -> pd.DataFrame:
    """Carrega e aplica limpezas básicas estáveis para análise."""
    df = carregar_dados_brutos()

    df.columns = df.columns.str.strip()
    df = df.dropna(how="all")
    df = df.replace("", pd.NA)

    return df


if __name__ == "__main__":
    df = carregar_dados_preparados()
    print(f"Planilha carregada: {ABA_DADOS}")
    print(f"Linhas: {len(df)} | Colunas: {len(df.columns)}")
    print(df.head())
