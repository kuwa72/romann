# romann

Kanjiconvをベースに見やすいローマ字化を提供するライブラリです。
視認性の悪い液晶で曲のタイトルなどを確認する用なので以下のような変換を行います。

* 薔薇の花 -> Bara No Hana
* 追憶のマーメイド -> Tsuioku No Mermaid
* A・RA・SHI -> A・Ra・Shi
* さよならCOLOR -> Sayonara Color
* SAKURAドロップス -> Sakura Drops
* さようなら、また明日 -> Sayonara, Mata Ashita

## 変換ルール

- ワードの先頭大文字
- ワードはスペース区切り
- カタカナ英語は可能な限り英単語に変換
- 記号類はそのまま（[、。]は[,.]に変換）
- 前後の空白は削除
- 連続する空白は1つの空白に変換
- 明日（Asu/Ashita）みたいなのはわからんのでKanjiconv任せです:pry:

## インストール

```bash
pip install romann
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
