# Azul Flight Scraper - Pontos para Punta Cana 🛫

🔍 **Scraper automatizado** para monitorar passagens em pontos da **Azul Airlines** para **Punta Cana** em **Classe Executiva**.

## 📋 O que faz

Este script monitora automaticamente passagens aéreas em pontos da Azul (programa TudoAzul) para voos de **São Paulo (GRU/VCP)** para **Punta Cana (PUJ)** em **classe executiva**.

### Funcionalidades

- ✅ **Monitoramento contínuo**: Executa buscas a cada 10 minutos
- ✅ **Multi-origem**: Busca voos saindo de **GRU** (Guarulhos) e **VCP** (Viracopos)
- ✅ **Alertas inteligentes**: Notifica por **Email** e **Pushover** quando encontrar pontos abaixo do threshold
- ✅ **Banco de dados**: Rastreia os menores valores encontrados
- ✅ **Critical Alerts**: Pushover com Priority 2 toca mesmo em modo Sono/Focus (iOS/Android)
- ✅ **Histórico**: Mantém registro dos melhores valores encontrados por data

## 🚀 Como funciona

1. **Busca automática**: A cada 10 minutos, o scraper consulta 14 rotas (7 datas × 2 origens)
2. **Comparação de valores**: Compara com o banco de dados local
3. **Alertas**: Se encontrar valor menor que o threshold configurado, envia notificação
4. **Atualização**: Salva o novo menor valor no banco de dados

## 📦 Instalação

### Pré-requisitos

- Python 3.10+
- Google Chrome (ou Chromium)
- Linux (testado no Ubuntu)

### Passos

1. **Clone o repositório**:

```bash
git clone git@github.com:rafaeldbernardes/Azul-Scraper-.git
cd Azul-Scraper-
```

2. **Instale as dependências**:

```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**:

```bash
cp .env.example .env
nano .env
```

Edite o arquivo `.env` com suas credenciais:

```env
# Email
EMAIL_ENABLED=True
EMAIL_FROM=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app
EMAIL_TO=seu_email@gmail.com

# Pushover
PUSHOVER_ENABLED=True
PUSHOVER_USER_KEY=seu_user_key
PUSHOVER_API_TOKEN=seu_api_token
```

### Configurar Pushover (Opcional)

Para receber alertas no celular:

1. Crie uma conta em [pushover.net](https://pushover.net)
2. Crie uma aplicação para pegar o API Token
3. No app Pushover (iOS/Android):
   - **Android**: Ative "Sobrepor ao modo Não Perturbe"
   - **iOS**: Ative "Critical Alerts" nas permissões do app

## ⚙️ Configuração

Edite `main.py` para personalizar:

```python
# Threshold de pontos para alerta
POINTS_THRESHOLD = 300000  # Alerta se encontrar < 300.000 pontos

# Datas para monitorar (YYYY-MM-DD)
dates = [
    '2026-04-26',
    '2026-04-27',
    '2026-04-28',
    '2026-04-29',
    '2026-04-30',
    '2026-05-01',
    '2026-05-02'
]

# Aeroportos de origem
origins = ['GRU', 'VCP']  # Guarulhos e Viracopos
```

## 🎯 Uso

### Executar o scraper

```bash
python main.py
```

O script irá:
1. Inicializar o Chrome em modo headless
2. Buscar voos para cada data e origem configurada
3. Comparar com o banco de dados
4. Enviar alertas se encontrar novos valores mais baixos
5. Aguardar 10 minutos e repetir

### Testar alertas

```bash
python test_pushover.py
```

Envia 3 notificações de teste com diferentes sons para verificar a configuração.

## 📊 Banco de Dados

O script mantém um arquivo `best_points.json` com os menores valores encontrados:

```json
{
  "GRU-2026-04-26": {
    "points": "285.000",
    "points_value": 285000,
    "last_updated": "2025-01-29T10:30:00"
  },
  "VCP-2026-04-26": {
    "points": "295.000",
    "points_value": 295000,
    "last_updated": "2025-01-29T10:35:00"
  }
}
```

## 🔧 Troubleshooting

### Chrome não inicia

Certifique-se de que o Chrome está instalado:
```bash
google-chrome --version
```

### Timeout errors

O timeout padrão é de 20 segundos. Se sua internet for lenta, aumente em `classes/Scraper.py`:
```python
delay = 30  # aumente de 20 para 30
```

### Alertas não chegam

1. **Email**: Verifique se允许 less secure apps ou use App Password do Gmail
2. **Pushover**:
   - Verifique se `PUSHOVER_ENABLED = True`
   - No iOS: configure "Critical Alerts" nas permissões do app
   - No Android: configure para "Sobrepor ao modo Não Perturbe"

## 📈 Estrutura do Projeto

```
Azul-Scraper-/
├── main.py                 # Script principal
├── classes/
│   └── Scraper.py         # Web scraper com Selenium
├── test_pushover.py       # Teste de alertas
├── requirements.txt       # Dependências Python
├── .env.example          # Template de configuração
├── best_points.json      # Banco de dados local
└── README.md            # Este arquivo
```

## ⚠️ Disclaimer

Este script é destinado apenas para fins educacionais e uso pessoal. Respeite os termos de serviço da Azul Airlines. O uso excessivo de scraping pode resultar em bloqueio de IP.

## 📄 Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

**Desenvolvido para monitorar passagens em pontos para viagens em família** ✈️👨‍👩‍👧‍👦
