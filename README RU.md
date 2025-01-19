Русский | English | Japanese

# Polybar Ticker

Модуль для Polybar — криптотрекер, интегрирующий данные о криптовалютах непосредственно в панель. Обеспечивает быстрый
доступ, удобство использования и простоту настройки.

## Установка

При разработке использовался Python 3.12

Перед установкой перейдите в дерикторию где которой будет хранится проект, затем клонируйте репозиторий:

```bash
git clone https://github.com/devoqub/polybar-ticker/
```

После этого установите зависимости (Обратите внимание, зависимости устанавливаются в глобальное окружение)

```bash
pip install -r requirements.txt
```

Вставьте это в конфиг polybar:

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

Готово! Осталось разместить модуль в панели.

## Changelog
...


