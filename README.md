[Русский](https://github.com/devoqub/polybar-ticker/blob/main/README%20RU.md) | English | [Japanese](https://github.com/devoqub/polybar-ticker/blob/main/README%20JP.md)

# Polybar Ticker

A really simple module for [Polybar](https://github.com/polybar/polybar) — a cryptocurrency tracker that integrates cryptocurrency data directly into the panel. It provides
quick access, ease of use, and simple configuration.
Supports output in several formats [Regular, Simplified (only price), Display all currencies, Hidden]. You can also create your own.

Examples

![photo_2025-01-19_18-45-12](https://github.com/user-attachments/assets/059d1725-7c7d-46f7-af14-c85d818bab66)
<video src="https://github.com/user-attachments/assets/7306b5c1-7203-43a7-974c-3bbda063e987"> </video>



## Quick guide
Left click - next crypto

Middle click - change rendering style

Right click - prev crypto


## Installation
Dependencies:
- curl_cffi
- psutil

Python 3.12 was used during development.

Before installation, navigate to the directory where the project will be stored, then clone the repository:

```bash
git clone https://github.com/devoqub/polybar-ticker/
```

Next, install the dependencies (Note that dependencies are installed in the global environment):

```bash
pip install -r requirements.txt
```

Insert this into your polybar config:

```ini
[module/ticker]
type = custom/script

exec = python /path/to/folder/src/main.py
tail = true
# interval = .64
click-left = echo "next" | nc 127.0.0.1 14888
click-middle = echo "change-handler" | nc 127.0.0.1 14888
click-right = echo "prev" | nc 127.0.0.1 14888
```

Done! Now you just need to place the module in the panel.


## Adding Your Own Cryptocurrencies
The addition is made through the config.py file. You need to add a tuple where the first element is the name of the cryptocurrency (as it will be displayed in polybar), and the link to the pair.

You can find the pairs here: https://docs.gemini.com/websocket-api/#all-supported-symbols 

Or you can find them by trial and error :)


Example:
```python
# To add a new cryptocurrency, you need to add the websocket connection link from the site below
# Pairs can be found here:
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

