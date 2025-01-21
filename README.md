[Русский](https://github.com/devoqub/polybar-ticker/blob/main/README%20RU.md) | English | [Japanese](https://github.com/devoqub/polybar-ticker/blob/main/README%20JP.md)

# Polybar Ticker

The simple module for [Polybar](https://github.com/polybar/polybar) — a cryptocurrency tracker that integrates cryptocurrency data directly into the panel. 

It provides quick access, ease of use, and simple configuration.

The module works asynchronously and supports output in several formats [Default, Simple (only price), All currencies, Hidden]. You can also create your own.

Examples

![photo_2025-01-19_18-45-12](https://github.com/user-attachments/assets/059d1725-7c7d-46f7-af14-c85d818bab66)
<video src="https://github.com/user-attachments/assets/7306b5c1-7203-43a7-974c-3bbda063e987"> </video>



## Quick guide
Left click - next crypto

Middle click - change rendering style

Right click - prev crypto


## Installation
Dependencies:
- curl_cffi / aiohttp 
- psutil

Python 3.12 was used during development.
Before installation, navigate to the directory where the project will be stored (it is recommended to place it in the same path as polybar, typically ~/.config/polybar/).

```bash
git clone https://github.com/devoqub/polybar-ticker/ &&
cd polybar-ticker
```

Next, create a virtual env and install the dependencies:

```bash
python -m venv venv && 
source venv/bin/activate && 
pip install -r requirements.txt
```

Insert this into your polybar config:

```ini
[module/ticker]
type = custom/script

# exec = /path/to/polybar/venv/bin/python /path/to/folder/src/main.py
exec = ~/.config/polybar/polybar-ticker/venv/bin/python ~/.config/polybar/polybar-ticker/src/main.py
tail = true

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
# https://docs.gemini.com/websocket-api/#all-supported-symbols
tickers = [
    # ("TITLE", "wss://link"),
    ("BTC", "wss://api.gemini.com/v1/marketdata/btcusd"),
    ("ETH", "wss://api.gemini.com/v1/marketdata/ethusd"),
    ("LTC", "wss://api.gemini.com/v1/marketdata/ltcusd"),
]
```


## Changelog
### 0.0.2 (2025-01-21)
Added:
- aiohttp support (new class AioHTTPWSConnection)

Fixed:
- startup without virtual env

Other:
- code quality
- new config option 
- changed README file and startup method
