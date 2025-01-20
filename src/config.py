# Чтобы добавить новую крипту вам нужно добавить ссылку на вебсокет соединение с сайта ниже
# Найти связки можно тут:
# https://docs.gemini.com/websocket-api/?utm_source=otiebis-zaebal#all-supported-symbols
tickers = [
    # ("TITLE", "wss://link"),
    ("BTC", "wss://api.gemini.com/v1/marketdata/btcusd"),
    ("ETH", "wss://api.gemini.com/v1/marketdata/ethusd"),
    ("LTC", "wss://api.gemini.com/v1/marketdata/ltcusd"),
    ("DOGE", "wss://api.gemini.com/v1/marketdata/dogeusd"),
]

# Constants
BLINK_KAOMOJI: str = "┻━┻︵ヽ(`Д´)ﾉ︵┻━┻"
TEMP_PID_PATH = "/tmp/polybar-ticker.pid"

SERVER_PORT: int = 14888
UPDATE_TIME: float | int = 0.64
BLINK_KAOMOJI_REPEAT_TIME: float | int = 0.05
RETRY_CONNECT_TIMEOUT: float | int = 4

# TODO:
#  добавить класс соединения для работы с tradingview по апи ключу
#  Добавить соединение использующее aiohttp вместо curl_cffi
#  добавить тесты
