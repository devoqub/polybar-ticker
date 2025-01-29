「申し訳ありませんが、翻訳が正確でない場合があります」

[Русский](https://github.com/devoqub/polybar-ticker/blob/main/README%20RU.md) | [English](https://github.com/devoqub/polybar-ticker/blob/main/README.md) |
Japanese

# Polybar Ticker

Polybarのモジュール — 仮想通貨トラッカーで、仮想通貨データを直接パネルに統合します。これにより、
迅速なアクセス、使いやすさ、簡単な設定が提供されます。
複数の表示オプションをサポートしています（[通常、簡易（価格のみ）、すべての通貨の表示、非表示]）、また独自の設定も可能です。

の例
![photo_2025-01-19_18-45-12](https://github.com/user-attachments/assets/059d1725-7c7d-46f7-af14-c85d818bab66)
<video src="https://github.com/user-attachments/assets/7306b5c1-7203-43a7-974c-3bbda063e987"> </video>

## クイックガイド

左クリック - 次の仮想通貨

中クリック - 表示スタイルの変更

右クリック - 前の仮想通貨

## インストール

開発時にPython 3.12が使用されました。
インストール前に、プロジェクトを保存するディレクトリに移動してください（通常はpolybarと同じパスに配置することをお勧めします：
`~/.config/polybar/`）。

```bash
git clone https://github.com/devoqub/polybar-ticker/ &&
cd polybar-ticker
```

次に、仮想環境を作成し、依存関係をインストールします：

```bash
python -m venv venv && 
source venv/bin/activate && 
pip install -r requirements.txt
```

これをPolybarの設定に挿入します：

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


## 開発者を応援してください <3
<img src="https://img.icons8.com/?size=100&id=DEDR1BLPBScO&format=png&color=000000" width=24> USDT TRC20 

TWLA1d9qNZzuikcbhezmp4m5uc4fCiJ4Kr

<img src="https://img.icons8.com/?size=100&id=anv9gQeahNxD&format=png&color=000000" width=20> Monero 

46vDbwch8RHBunMr3sWf7ictdxQWQSdCQTKb99GnwFcx217roD4MVoD9D22SibBGT3CKAKMCocVbRBgtv6rqoaTBGH9VHeo


## Changelog

### 0.0.2 (2025-01-21)

追加:

- aiohttpサポート（新しいクラス AioHTTPWSConnection）

修正:

- 仮想環境なしでのスタートアップ

その他:

- コード品質の改善
- 新しい設定オプション
- READMEファイルとスタートアップメソッドの変更




