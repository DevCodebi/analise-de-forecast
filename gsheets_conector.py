from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

# Escopos necessários
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Caminho do JSON (relativo ao arquivo)
CREDENTIALS_PATH = Path(__file__).parent / "credentials" / "chave_api_google.json"


def conectar_sheets():
    creds = Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
    )
    client = gspread.authorize(creds)
    return client


def abrir_planilha(nome_ou_id: str):
    client = conectar_sheets()
    try:
        # Tenta abrir pelo nome
        return client.open(nome_ou_id)
    except gspread.SpreadsheetNotFound:
        # Se não achar pelo nome, tenta pelo ID da URL
        return client.open_by_key(nome_ou_id)


if __name__ == "__main__":
    from config import ABA_DADOS, PLANILHA_ID

    spreadsheet = abrir_planilha(PLANILHA_ID)
    worksheet = spreadsheet.worksheet(ABA_DADOS)

    print("Conectado com sucesso!")
    print("Planilha:", spreadsheet.title)
    print("Aba:", worksheet.title)
    print("Primeira célula (A1):", worksheet.acell("A1").value)