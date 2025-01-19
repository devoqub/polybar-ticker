「申し訳ありませんが、翻訳が正確でない場合があります」

[Русский](https://github.com/devoqub/polybar-ticker/blob/main/README%20RU.md) | [English](https://github.com/devoqub/polybar-ticker/blob/main/README.md) | Japanese

# Polybar Ticker

Polybarのモジュール — 仮想通貨トラッカーで、仮想通貨データを直接パネルに統合します。これにより、
迅速なアクセス、使いやすさ、簡単な設定が提供されます。

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

## 更新履歴
...





