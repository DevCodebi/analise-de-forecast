# Análise de Forecast

Projeto de análise exploratória de dados de forecast logístico, com carga automatizada a partir do **Google Sheets** e análise em **Jupyter Notebooks**.

---

## Visão geral

O projeto segue uma separação clara de responsabilidades:

```text
Google Sheets
      ↓
gsheets_conector.py   → conexão e autenticação
      ↓
config.py             → constantes (planilha, aba)
      ↓
data_load.py          → carga e preparo dos dados
      ↓
notebooks/            → exploração, gráficos e análises
```

---

## Estrutura do projeto

```text
analise_de_forecast/
├── config.py                 # Configurações centralizadas
├── gsheets_conector.py       # Conexão com Google Sheets
├── data_load.py              # Carga e limpeza dos dados
├── requirements.txt          # Dependências Python
├── .gitignore                # Arquivos ignorados pelo Git
├── credentials/              # Credenciais Google (não versionado)
│   └── chave_api_google.json
├── env_analise_forecast/     # Ambiente virtual (não versionado)
└── notebooks/
    └── 01_exploracao.ipynb   # Análise exploratória
```

---

## Módulos

### `config.py`

**Função:** centralizar as configurações fixas do projeto em um único lugar.

| Variável      | Descrição                                      |
|---------------|------------------------------------------------|
| `PLANILHA_ID` | ID da planilha no Google Sheets (pela URL)     |
| `ABA_DADOS`   | Nome da aba a ser lida (`Forecast_Semana_1_V2`) |

**Por que existe:** evita espalhar IDs e nomes de abas pelo código. Ao adicionar novas versões de forecast, basta atualizar este arquivo.

---

### `gsheets_conector.py`

**Função:** gerenciar a conexão com a API do Google Sheets.

| Função             | Descrição                                                                 |
|--------------------|---------------------------------------------------------------------------|
| `conectar_sheets()` | Autentica via Service Account e retorna o cliente `gspread`               |
| `abrir_planilha()`  | Abre uma planilha pelo nome ou pelo ID                                   |

**Detalhes técnicos:**
- Usa o arquivo `credentials/chave_api_google.json` para autenticação
- Escopos: `spreadsheets` e `drive`
- Tenta abrir pelo nome; se não encontrar, tenta pelo ID

**Testar conexão:**

```powershell
python gsheets_conector.py
```

---

### `data_load.py`

**Função:** carregar dados do Google Sheets e aplicar limpezas básicas para análise.

| Função                      | Descrição                                              |
|-----------------------------|--------------------------------------------------------|
| `carregar_dados_brutos()`   | Lê a aba configurada e retorna um `DataFrame` bruto    |
| `carregar_dados_preparados()` | Aplica limpezas estáveis antes da análise            |

**Limpezas aplicadas em `carregar_dados_preparados()`:**
- Remove espaços extras dos nomes das colunas
- Remove linhas completamente vazias
- Converte strings vazias em `NA`

**Colunas esperadas na planilha:**

| Coluna              | Tipo     | Descrição                    |
|---------------------|----------|------------------------------|
| `data`              | data     | Data do forecast             |
| `Origem`            | texto    | CD de origem                 |
| `Destino`           | texto    | Loja de destino              |
| `volume_forecast`   | numérico | Volume previsto              |
| `timestamp_geracao` | datetime | Quando o forecast foi gerado |

**Testar carga:**

```powershell
python data_load.py
```

---

### `notebooks/01_exploracao.ipynb`

**Função:** análise exploratória dos dados (EDA).

**O que faz:**
1. Importa `carregar_dados_preparados()` do `data_load.py`
2. Carrega o `DataFrame` com os dados da planilha
3. Exibe visão geral: `head()`, `info()`, `describe()`
4. Agrupa volume por data
5. Gera gráfico de linha do volume ao longo do tempo

**Regra:** o notebook **não** contém lógica de conexão ou carga — apenas análise e visualização.

---

### `requirements.txt`

**Função:** listar todas as dependências Python do projeto.

| Pacote         | Uso                                      |
|----------------|------------------------------------------|
| `gspread`      | Integração com Google Sheets             |
| `google-auth`  | Autenticação com Service Account         |
| `pandas`       | Manipulação e análise de dados           |
| `jupyter`      | Ambiente de notebooks                    |
| `ipykernel`    | Kernel Jupyter para o ambiente virtual   |
| `matplotlib`   | Gráficos                                 |
| `seaborn`      | Visualizações estatísticas (futuro)      |

---

### `.gitignore`

**Função:** impedir que arquivos sensíveis ou desnecessários sejam enviados ao GitHub.

**Ignora:**
- `env_analise_forecast/` — ambiente virtual
- `credentials/` — credenciais Google
- `*.json` — arquivos JSON (inclui chaves de API)
- `.ipynb_checkpoints/` — checkpoints do Jupyter
- `data/` — cache local de dados (futuro)

---

### `credentials/chave_api_google.json`

**Função:** arquivo de credenciais da Service Account do Google Cloud.

> **Atenção:** este arquivo **nunca** deve ser commitado no Git. Cada desenvolvedor precisa do seu próprio arquivo, baixado no [Google Cloud Console](https://console.cloud.google.com/).

**Configuração necessária no Google Cloud:**
1. Criar projeto no Google Cloud
2. Ativar a **Google Sheets API**
3. Criar uma **Service Account** e baixar a chave JSON
4. Compartilhar a planilha com o e-mail da Service Account (`client_email` do JSON)

---

## Configuração do ambiente

### 1. Criar e ativar o ambiente virtual

```powershell
cd analise_de_forecast
python -m venv env_analise_forecast
.\env_analise_forecast\Scripts\Activate.ps1
```

### 2. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 3. Registrar kernel Jupyter (opcional)

```powershell
python -m ipykernel install --user --name=env_analise_forecast --display-name="Análise Forecast"
```

### 4. Configurar credenciais

Coloque o arquivo `chave_api_google.json` em `credentials/`.

---

## Como usar

### Rodar carga de dados

```powershell
python data_load.py
```

### Abrir notebook de exploração

1. Abra `notebooks/01_exploracao.ipynb` no Cursor
2. Selecione o kernel **Análise Forecast** (ou `env_analise_forecast`)
3. Execute as células de cima para baixo

---

## Fluxo para novas versões de forecast

Quando uma nova aba/planilha de forecast for publicada:

1. Atualize `config.py` com o novo `ABA_DADOS` ou `PLANILHA_ID`
2. Rode `python data_load.py` para validar a carga
3. Explore no notebook ou crie `02_comparacoes.ipynb`

---

## Versionamento (Git)

```powershell
git add .
git status          # confira que credentials/ NÃO aparece
git commit -m "Descrição da mudança"
git push
```

Repositório: [github.com/DevCodebi/analise-de-forecast](https://github.com/DevCodebi/analise-de-forecast)

---

## Roadmap

| Etapa | Arquivo | Status |
|-------|---------|--------|
| Conexão Google Sheets | `gsheets_conector.py` | Concluído |
| Carga de dados | `data_load.py` | Concluído |
| Exploração | `01_exploracao.ipynb` | Em andamento |
| Comparação entre forecasts | `02_comparacoes.ipynb` | Planejado |
| Modelagem / previsão | `03_forecast.ipynb` | Planejado |
