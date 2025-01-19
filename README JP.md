「申し訳ありませんが、翻訳が正確でない場合があります」

[Русский](https://github.com/devoqub/polybar-ticker/blob/main/README%20RU.md) | [English](https://github.com/devoqub/polybar-ticker/blob/main/README.md) | Japanese

# Polybar Ticker

Polybarのモジュール — 仮想通貨トラッカーで、仮想通貨データを直接パネルに統合します。これにより、
迅速なアクセス、使いやすさ、簡単な設定が提供されます。
複数の表示オプションをサポートしています（[通常、簡易（価格のみ）、すべての通貨の表示、非表示]）、また独自の設定も可能です。

![photo_2025-01-19_18-40-33](https://github.com/user-attachments/assets/a734ca2c-06b2-4e7b-92c5-b203980be1dc)
![photo_2025-01-19_18-45-12](https://github.com/user-attachments/assets/059d1725-7c7d-46f7-af14-c85d818bab66)


## インストール

開発時にPython 3.12が使用されました。

インストールの前に、プロジェクトを保存するディレクトリに移動し、リポジトリをクローンします：

```bash
git clone https://github.com/devoqub/polybar-ticker/
```

次に、依存関係をインストールします（依存関係はグローバル環境にインストールされます）：

```bash
pip install -r requirements.txt
```

これをPolybarの設定に挿入します：

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

完了！次に、パネルにモジュールを配置するだけです。

## 自分の暗号通貨の追加

追加はconfig.pyファイルを通じて行います。タプルを追加する必要があり、最初の要素は暗号通貨の名前（polybarに表示される名前）で、2番目の要素はその対応するリンクです。

リンクはここで見つけることができます: https://docs.gemini.com/websocket-api/#all-supported-symbols 

または、試行錯誤の方法で見つけることもできます :)

例:
```python
# 新しい暗号通貨を追加するには、下記のサイトからWebSocket接続のリンクを追加する必要があります
# リンクはここで見つけることができます:
# https://docs.gemini.com/websocket-api/#all-supported-symbols
tickers = [
    # ("TITLE", "wss://link"),
    ("BTC", "wss://api.gemini.com/v1/marketdata/btcusd"),
    ("ETH", "wss://api.gemini.com/v1/marketdata/ethusd"),
    ("LTC", "wss://api.gemini.com/v1/marketdata/ltcusd"),
]
```

## 更新履歴
。。。




