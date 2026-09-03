"""
romann.py - Japanese to natural romaji/English conversion library.
"""

import os
import re
import json
import jaconv
from pykakasi import kakasi
from sudachipy import tokenizer, dictionary

class RomanConverter:
    """
    RomanConverter class for converting Japanese text to natural romaji/English.
    Uses SudachiPy for morphological analysis and customizable dictionaries.
    """
    # ヘボン式ローマ字の外来語英語の辞書
    hira_dict_path = os.path.join(os.path.dirname(__file__), "hiragana_english.json")
    with open(hira_dict_path, encoding="utf-8") as f:
        HIRAGANA_ENGLISH = json.load(f)

    # 漢字語の英語表記。読みではなく表記そのものをキーにするので衝突しない。
    # 英語のつづりが定まっている固有名詞だけを入れること。
    kanji_dict_path = os.path.join(os.path.dirname(__file__), "kanji_english.json")
    with open(kanji_dict_path, encoding="utf-8") as f:
        KANJI_ENGLISH = json.load(f)

    # SudachiPy の読みを上書きしたい語。ローマ字にはするが読みだけ差し替える。
    # 「私」はワタクシと読まれるが曲名ではわたしが普通、といった手当て用。
    reading_dict_path = os.path.join(os.path.dirname(__file__), "kanji_reading.json")
    with open(reading_dict_path, encoding="utf-8") as f:
        KANJI_READING = json.load(f)

    # 外来語辞書は読み（ひらがな）で引くため、読みが偶然一致するだけの語まで
    # 巻き込んでしまう。カタカナ表記そのものが外来語のしるしなので、そこを軸に絞る。
    # 例:「愛」(あい)→I、「食べたい」の「たい」→Tie、「Vol.」(ぼりゅーむ)→Volume を防ぐ。
    KATAKANA_ONLY = re.compile(r'^[ァ-ヶー゛゜ヽヾ]+$')
    HIRAGANA_ONLY = re.compile(r'^[ぁ-んーゝゞ]+$')
    LATIN_OR_KANJI = re.compile(r'[A-Za-zＡ-Ｚａ-ｚ一-鿿々〆]')
    # 「々」「〆」は単体では読めない繰り返し・略記号なので、読みを信用する対象から外す
    JAPANESE_CHAR = re.compile(r'[ぁ-んァ-ヶ一-鿿]')
    # 連結して辞書を引くときに見る最大トークン数
    MAX_SPAN_TOKENS = 4
    LOANWORD_POS = ("名詞", "形状詞")

    def __init__(self):
        """
        Initialize the RomanConverter with kakasi and SudachiPy.
        """
        self.converter = kakasi()
        # SudachiPyの初期化
        self.tokenizer_obj = dictionary.Dictionary().create()
        self.mode = tokenizer.Tokenizer.SplitMode.C  # 最も粗い（複合語をまとめる）分割モード

    def convert_hiragana_english(self, word: str) -> str:
        """
        Convert romanized hiragana to English if it exists in the dictionary.
        """
        return self.HIRAGANA_ENGLISH.get(word.lower(), word).capitalize()

    def _is_loanword_candidate(self, token) -> bool:
        """
        外来語辞書を引いてよいトークンかどうか。

        - カタカナ表記: そのまま引く
        - ひらがな表記: 名詞・形状詞だけ引く（助動詞「たい」→Tie などを防ぐ）
        - 漢字・ラテン文字を含む: 引かない
        - それ以外（記号）: 引く（「＆」(あんど)→And のため）
        """
        surface = token.surface()
        if self.KATAKANA_ONLY.match(surface):
            return True
        if self.HIRAGANA_ONLY.match(surface):
            return token.part_of_speech()[0] in self.LOANWORD_POS
        return not self.LATIN_OR_KANJI.search(surface)

    def _process_token(self, token) -> str:
        """Process a single token from SudachiPy."""
        surface = token.surface()

        # Handle alphanumeric tokens
        if re.match(r'^[a-zA-Z0-9]+$', surface):
            return surface

        # Kanji words are looked up by their surface form
        if surface in self.KANJI_ENGLISH:
            return self.KANJI_ENGLISH[surface]

        # Get reading and convert to hiragana
        reading = token.reading_form()
        hiragana = self.KANJI_READING.get(surface, jaconv.kata2hira(reading))

        # Check if in dictionary
        if self._is_loanword_candidate(token) and hiragana in self.HIRAGANA_ENGLISH:
            return self.HIRAGANA_ENGLISH[hiragana]

        # Special case for particle "no"
        if surface == "の" or hiragana == "の":
            return "no"

        # Skip empty tokens
        if not surface.strip():
            return ""

        # Convert to romaji using kakasi.
        # 表記から引くと漢字を文脈なしで読んでしまう（「君」→Kun、「テレ東」→Terehigashi）。
        # SudachiPy は文脈を見た読みを返すので、日本語の語はそちらを使う。
        return self._to_hepburn(hiragana if self._reading_is_reliable(token) else surface)

    def _reading_is_reliable(self, token) -> bool:
        """
        SudachiPy の読みを使ってよいトークンかどうか。

        仮名・漢字で書かれた語に限る。記号やラテン文字には読みが振られるが
        表記とは別物なので使えない（「(」→キゴウ、「Vol.」→ボリューム）。
        """
        if not token.reading_form():
            return False
        return bool(self.JAPANESE_CHAR.search(token.surface()))

    def _to_hepburn(self, text: str) -> str:
        """Convert text to Hepburn romaji with kakasi."""
        expanded = self._expand_iteration_mark(text)
        return ''.join(item['hepburn'] for item in self.converter.convert(expanded))

    @staticmethod
    def _expand_iteration_mark(text: str) -> str:
        """
        踊り字「々」を直前の文字に開く（良々木 → 良良木）。

        kakasi は「々」を "(kurikaesi)" という文字列にしてしまうので、
        kakasi に渡す直前だけ開く。SudachiPy は「時々」→トキドキのように
        正しく読めるので、分かち書きの前に触ってはいけない。
        """
        chars = list(text)
        for i in range(1, len(chars)):
            if chars[i] == "々":
                chars[i] = chars[i - 1]
        return ''.join(chars)

    def _match_span(self, tokens, start: int):
        """
        start から始まる複数トークンが、まとめて辞書に載っていないか調べる。

        SudachiPy は「エイリアンズ」を エイリ+アンズ に割ってしまうなど、
        外来語を必ずしも1語にまとめてくれない。1トークンずつ引くだけでは
        辞書に載せても届かないので、長い方から順に連結して引く。

        Returns:
            (英語表記, 消費したトークン数) 見つからなければ (None, 0)
        """
        longest = min(self.MAX_SPAN_TOKENS, len(tokens) - start)
        for length in range(longest, 1, -1):
            span = tokens[start:start + length]
            if not all(self._is_loanword_candidate(t) for t in span):
                continue
            reading = ''.join(t.reading_form() for t in span)
            english = self.HIRAGANA_ENGLISH.get(jaconv.kata2hira(reading))
            if english:
                return english, length
        return None, 0

    def _process_tokens(self, tokens) -> list:
        """Process every token, letting multi-token loanwords match first."""
        results = []
        index = 0
        while index < len(tokens):
            english, length = self._match_span(tokens, index)
            if english:
                results.append(english)
                index += length
                continue
            token = tokens[index]
            if token.surface() == "々":
                # 単独で切り出された踊り字は、前のトークンの末尾をもう一度読む。
                # 繰り返す先がなければ読みようがないので落とす。
                previous = tokens[index - 1].surface() if index > 0 else ""
                results.append(self._to_hepburn(previous[-1]) if previous else "")
            else:
                results.append(self._process_token(token))
            index += 1
        return results

    def to_roman(self, text: str, remove_spaces: bool = True) -> str:
        """
        Convert Japanese text (kanji, hiragana, katakana) to romaji.
        Preserves non-Japanese characters as they are.
        Uses SudachiPy for morphological analysis to better handle loan words.

        Args:
            text (str): Input text containing Japanese characters
            remove_spaces (bool, optional): Whether to remove spaces from the output.
                Defaults to True.


        Returns:
            str: Romanized text with natural capitalization and formatting
        """
        if not text:
            return ""

        # Process tokens
        tokens = list(self.tokenizer_obj.tokenize(text.replace("・", " "), self.mode))
        processed_tokens = self._process_tokens(tokens)

        # Filter out empty tokens and join with spaces
        result_text = ' '.join(filter(None, processed_tokens))

        # Capitalize words and clean up spaces
        result_text = ' '.join(word.capitalize() for word in result_text.split())
        result_text = re.sub(r'\s+', ' ', result_text).strip()

        # Remove spaces if requested
        return result_text.replace(' ', '') if remove_spaces else result_text

    def _kata_to_hira(self, text: str) -> str:
        """
        カタカナをひらがなに変換する
        """
        return jaconv.kata2hira(text)
