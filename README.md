[Русский](https://github.com/devoqub/polybar-ticker/blob/main/README%20RU.md) | English | [Japanese](https://github.com/devoqub/polybar-ticker/blob/main/README%20JP.md)

# Polybar Ticker

Module for Polybar — a cryptocurrency tracker that integrates cryptocurrency data directly into the panel. It provides
quick access, ease of use, and simple configuration.

## Installation

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

## Changelog
...

