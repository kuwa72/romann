#!/usr/bin/env python
"""iTunes ライブラリ XML から、辞書に載っていないカタカナ語を頻度つきで洗い出す。

辞書を育てるための調査用。出力をそのまま辞書に入れてはいけない。
「サヨナラ」「キミ」のような日本語のカタカナ表記や、人名・造語が混ざるので、
外来語だけを人が選ぶこと。

    python tools/find_missing_loanwords.py ~/Music/ライブラリ.xml
"""
import argparse
import collections
import json
import os
import plistlib
import re
import sys

import jaconv
from sudachipy import dictionary, tokenizer

DICT_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "romann")
FIELDS = ("Name", "Artist", "Album", "Album Artist", "Composer")
KATAKANA_ONLY = re.compile(r"^[ァ-ヶー゛゜ヽヾ]+$")


def load_texts(path):
    """XML から曲名・アーティスト名などの文字列を集める。"""
    with open(path, "rb") as f:
        plist = plistlib.load(f)
    texts = set()
    for track in plist.get("Tracks", {}).values():
        for key in FIELDS:
            if track.get(key):
                texts.add(track[key])
    return texts


def main():
    """未収録のカタカナ語を頻度順に、辞書に貼れる形で標準出力に書く。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("library_xml", help="iTunes の ライブラリ.xml")
    parser.add_argument("-n", "--min-count", type=int, default=1,
                        help="この回数以上出てくる語だけ表示する")
    args = parser.parse_args()

    with open(os.path.join(DICT_DIR, "hiragana_english.json"), encoding="utf-8") as f:
        hira_dict = json.load(f)

    texts = load_texts(args.library_xml)
    tok = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.C

    missing = collections.Counter()
    examples = {}
    for text in texts:
        for token in tok.tokenize(text.replace("・", " "), mode):
            surface = token.surface()
            if not KATAKANA_ONLY.match(surface):
                continue
            if jaconv.kata2hira(token.reading_form() or surface) in hira_dict:
                continue
            missing[surface] += 1
            examples.setdefault(surface, text)

    print(f"文字列 {len(texts)} 件 / 未収録のカタカナ語 {len(missing)} 種 "
          f"{sum(missing.values())} 延べ", file=sys.stderr)
    for surface, count in missing.most_common():
        if count < args.min_count:
            break
        print(f'{count:5d}  "{surface}": ""   # {examples[surface]}')


if __name__ == "__main__":
    main()
