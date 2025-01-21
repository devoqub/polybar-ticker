Русский | [English](https://github.com/devoqub/polybar-ticker/blob/main/README.md) | [Japanese](https://github.com/devoqub/polybar-ticker/blob/main/README%20JP.md)

# Polybar Ticker

Модуль для Polybar — криптотрекер, интегрирующий данные о криптовалютах непосредственно в панель. Обеспечивает быстрый
доступ, удобство использования и простоту настройки.
Поддерживает вывод в нескольких вариантах \[Обычный, Упрощенный(только цена), Отображение всех валют, Скрыто] так же
можно сделать свой.

Пример:

![photo_2025-01-19_18-45-12](https://github.com/user-attachments/assets/059d1725-7c7d-46f7-af14-c85d818bab66)
<video src="https://github.com/user-attachments/assets/7306b5c1-7203-43a7-974c-3bbda063e987"> </video>

## Краткая инструкция

Левый клик по тикеру - переключить на следующую крипту
Клик колёсиком мышки - изменить визуальное отображение тикера
Правый клик - переключить на предыдущую крипту

## Установка

При разработке использовался Python 3.12

Перед установкой перейдите в дерикторию где которой будет храниться проект (рекомендуется по пути где лежит polybar,
обычно `~/.config/polybar/`)
Клонируйте репозиторий:

```bash
git clone https://github.com/devoqub/polybar-ticker/ &&
cd polybar-ticker
```

После этого создайте виртуальное окружение и установите зависимости.

```bash
python -m venv venv && 
source venv/bin/activate && 
pip install -r requirements.txt
```

Вставьте это в конфиг polybar:

```ini
[module/ticker]
type = custom/script

exec = /path/to/polybar/venv/bin/python /path/to/folder/src/main.py
tail = true

click-left = echo "next" | nc 127.0.0.1 14888
click-middle = echo "change-handler" | nc 127.0.0.1 14888
click-right = echo "prev" | nc 127.0.0.1 14888
```

На этом готово, программа должна начать работать в виртуальном окружении! :)

## Добавление своих криптовалют

Добавление производится через конфиг config.py, необходимо добавить кортеж где первый элемент является названием
криптовалюты (то, как она будет отображатся в polybar), и ссылку на связку.

Связки можно найти тут: https://docs.gemini.com/websocket-api/#all-supported-symbols

Ну или методом перебора :)

Пример:

```python
# Чтобы добавить новую крипту вам нужно добавить ссылку на вебсокет соединение с сайта ниже
# Найти связки можно тут:
# https://docs.gemini.com/websocket-api/?utm_source=otiebis-zaebal#all-supported-symbols
tickers = [
    # ("TITLE", "wss://link"),
    ("BTC", "wss://api.gemini.com/v1/marketdata/btcusd"),
    ("ETH", "wss://api.gemini.com/v1/marketdata/ethusd"),
    ("LTC", "wss://api.gemini.com/v1/marketdata/ltcusd"),
]
```

## Changelog

...


