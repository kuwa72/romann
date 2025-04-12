# romann

日本語テキストを自然なローマ字表記に変換するライブラリです。
視認性の悪い液晶ディスプレイで曲のタイトルなどを確認する用途に最適化されており、以下のような変換を行います。

* 薔薇の花 -> Bara No Hana
* 追憶のマーメイド -> Tsuioku No Mermaid
* A・RA・SHI -> A Ra Shi
* さよならCOLOR -> Sayonara Color
* SAKURAドロップス -> Sakura Drops
* さようなら、また明日 -> Sayonara, Mata Ashita

## 特徴

- SudachiPyによる高精度な形態素解析
- 外来語を自然な英語表記に変換
- 4x8ドット文字でも視認性の高いローマ字表記

## 変換ルール

- 単語の先頭は大文字
- 単語はスペース区切り
- 外来語は可能な限り英単語に変換
  - 例: アース -> Earth, ドア -> Door
- 記号類はそのまま（「、」「。」は「,」「.」に変換）
- 前後の空白は削除
- 連続する空白は1つの空白に変換

## インストール

```bash
pip install romann
```

## 依存ライブラリ

- pykakasi: 日本語のローマ字変換
- SudachiPy: 形態素解析
- jaconv: 文字コード変換

## 使用方法

```python
from romann import RomanConverter

converter = RomanConverter()

# 日本語テキストをローマ字に変換
text = "薔薇の花"
romaji = converter.to_roman(text)
print(romaji)  # 出力: "Bara No Hana"

# 外来語を含むテキストの変換
text = "アースウィンド"
romaji = converter.to_roman(text)
print(romaji)  # 出力: "Earth Wind"
```

## 外来語辞書のカスタマイズ

外来語の変換は `hiragana_english.json` ファイルに基づいて行われます。このファイルをカスタマイズすることで、特定の単語の変換方法を調整できます。

```json
{
  "あーす": "earth",
  "どあ": "door",
  "らぶ": "love"
}
```

## 使用例

```python
from romann import RomanConverter

converter = RomanConverter()
result = converter.to_roman("こんにちは")
print(result)  # 出力: Konnichiha
```

## 関連

* [Kanjiconv](https://zenn.dev/sea_turt1e/articles/e7dc022231a86c)
