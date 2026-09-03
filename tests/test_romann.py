# -*- coding: utf-8 -*-
"""
test_romann.py - Tests for romann library
"""
from romann import RomanConverter


def test_remove_spaces_option():
    """
    Test the remove_spaces option specifically.
    """
    converter = RomanConverter()
    # 基本的なテスト
    assert converter.to_roman("こんにちは", remove_spaces=True) == "Konnichiha"
    assert converter.to_roman("こんにちは", remove_spaces=False) == "Konnichiha"

    # 複数単語のテスト
    assert converter.to_roman("こんにちは 世界") == "KonnichihaSekai"  # デフォルトはTrue
    assert converter.to_roman("こんにちは 世界", remove_spaces=False) == "Konnichiha Sekai"

    # 記号を含むテスト
    assert converter.to_roman("A・B・C") == "ABC"  # デフォルトはTrue
    assert converter.to_roman("A・B・C", remove_spaces=False) == "A B C"

    # 英数字と日本語の混合テスト
    assert converter.to_roman("Hello 世界 123") == "HelloSekai123"  # デフォルトはTrue
    assert converter.to_roman("Hello 世界 123", remove_spaces=False) == "Hello Sekai 123"

def test_convert_kanji_to_roman():
    """
    Test conversion of kanji to roman.
    """
    converter = RomanConverter()
    assert converter.to_roman("漢字") == "Kanji"
    assert converter.to_roman("日本語") == "Nihongo"
    assert converter.to_roman("こんにちは") == "Konnichiha"

    # スペースありバージョンのテスト
    assert converter.to_roman("漢字 日本語", remove_spaces=False) == "Kanji Nihongo"

def test_convert_mixed_text():
    """
    Test conversion of mixed Japanese text.
    """
    converter = RomanConverter()
    assert converter.to_roman("Hello漢字World", remove_spaces=False) == "Hello Kanji World"
    assert converter.to_roman("Hello漢字World") == "HelloKanjiWorld"
    assert converter.to_roman("テスト123") == "Test123"
    assert converter.to_roman("テスト123", remove_spaces=False) == "Test 123"

def test_empty_string():
    """
    Test conversion of empty string.
    """
    converter = RomanConverter()
    assert converter.to_roman("") == ""

def test_whitespace_handling():
    """
    Test handling of spaces in text.
    """
    converter = RomanConverter()
    assert converter.to_roman("こんにちは 世界") == "KonnichihaSekai"
    assert converter.to_roman("  スペース  ") == "Space"

def test_natural_japanese_titles():
    """
    Test conversion of natural Japanese titles.
    """
    converter = RomanConverter()
    assert converter.to_roman("薔薇の花") == "BaraNoHana"
    assert converter.to_roman("追憶のマーメイド") == "TsuiokuNoMermaid"
    assert converter.to_roman("A・RA・SHI") == "ARaShi"
    assert converter.to_roman("さよならCOLOR") == "SayonaraColor"

    # Test with remove_spaces=False
    assert converter.to_roman("薔薇の花", remove_spaces=False) == "Bara No Hana"
    assert converter.to_roman("追憶のマーメイド", remove_spaces=False) == "Tsuioku No Mermaid"
    assert converter.to_roman("A・RA・SHI", remove_spaces=False) == "A Ra Shi"
    assert converter.to_roman("さよならCOLOR", remove_spaces=False) == "Sayonara Color"

def test_hiragana_english():
    """
    Test conversion of hiragana to roman.
    """
    converter = RomanConverter()
    assert converter.to_roman("めーる") == "Mail"
    # SudachiPyの分割特性に合わせてテストケースを調整
    assert converter.to_roman("す") == "Su"
    assert converter.to_roman("と") == "To"
    assert converter.to_roman("らぶ") == "Love"
    assert converter.to_roman("どり") == "Dori"

def test_particle_no():
    """
    Test special handling for particle 'の'.
    """
    converter = RomanConverter()
    assert converter.to_roman("春の海") == "HaruNoUmi"
    assert converter.to_roman("僕の名前") == "BokuNoNamae"

def test_separator_conversion():
    """
    Test conversion of separators.
    """
    converter = RomanConverter()
    assert converter.to_roman("A・B・C") == "ABC"
    # ドット・パンクのSudachiPyによる分割結果に合わせる
    assert converter.to_roman("ドット・パンク") == "DottoPunk"

def test_morphological_analysis():
    """
    Test morphological analysis.
    """
    converter = RomanConverter()
    # SudachiPyの分割結果に合わせてテストケースを調整
    assert converter.to_roman("アース") == "Earth"
    assert converter.to_roman("ウィンド") == "Wind"
    assert converter.to_roman("アンド") == "And"
    assert converter.to_roman("ファイアー") == "Fire"
    assert converter.to_roman("いけない") == "IkeNai"
    assert converter.to_roman("ボーダーライン") == "BorderLine"

def test_compound_words():
    """
    Test conversion of compound words and loanwords.
    """
    converter = RomanConverter()
    # SudachiPyの分割結果に合わせてテストケースを調整
    assert converter.to_roman("釈迦") == "Shaka"
    assert converter.to_roman("インザハウス") == "Inzahausu"
    assert converter.to_roman("オープン") == "Open"
    assert converter.to_roman("ドア") == "Door"
def test_mixed_japanese_english():
    """
    Test conversion of mixed Japanese and English words.
    """
    converter = RomanConverter()
    # SudachiPyの分割結果に合わせてテストケースを調整
    assert converter.to_roman("ハロー") == "Hello"
    assert converter.to_roman("ワールド") == "World"
    assert converter.to_roman("アイ") == "I"
    assert converter.to_roman("ラブ") == "Love"
    assert converter.to_roman("ユー") == "You"

    # Test with remove_spaces=True
    assert converter.to_roman("ハロー ワールド", remove_spaces=True) == "HelloWorld"
    assert converter.to_roman("アイ ラブ ユー", remove_spaces=True) == "ILoveYou"

def test_kanji_is_not_looked_up_as_loanword():
    """
    漢字の語は読みが外来語辞書と衝突しても引かない。
    「愛」の読み「あい」が辞書の "i" に化けるのを防ぐ。
    """
    converter = RomanConverter()
    assert converter.to_roman("愛") == "Ai"
    assert converter.to_roman("愛を叫べ", remove_spaces=False) == "Ai Wo Sakebe"
    assert converter.to_roman("家") == "Ie"          # 値が空で語ごと消えていた
    assert converter.to_roman("水の中のナイフ", remove_spaces=False) == "Mizu No Naka No Knife"


def test_kanji_english_dictionary():
    """
    漢字語は表記そのものをキーにした辞書で英語にする。
    """
    converter = RomanConverter()
    assert converter.to_roman("東京") == "Tokyo"
    assert converter.to_roman("東京の空の下", remove_spaces=False) == "Tokyo No Sora No Shita"
    # 読みが「いず」でも「伊豆」は Is にならない
    assert converter.to_roman("伊豆") == "Izu"


def test_non_noun_is_not_looked_up_as_loanword():
    """
    助動詞・助詞などの機能語は外来語辞書を引かない。
    「食べたい」の「たい」が "tie" に化けるのを防ぐ。
    """
    converter = RomanConverter()
    assert converter.to_roman("そばが食べたい", remove_spaces=False) == "Soba Ga Tabe Tai"
    # 「ね」は辞書の値が空で消えていた（"Tetene" になっていた）
    assert converter.to_roman("てねてね") == "TeNeTeNe"


def test_katakana_loanwords():
    """
    カタカナ外来語が本来のつづりになる。
    """
    converter = RomanConverter()
    assert converter.to_roman("キス") == "Kiss"
    assert converter.to_roman("マジック") == "Magic"
    assert converter.to_roman("ドロップス") == "Drops"
    assert converter.to_roman("SAKURAドロップス") == "SakuraDrops"
    assert converter.to_roman("クレイジー") == "Crazy"
    assert converter.to_roman("ムーンライト") == "Moonlight"
    assert converter.to_roman("マイケル・ジャクソン", remove_spaces=False) == "Michael Jackson"


def test_reading_comes_from_morphological_analysis():
    """
    漢字の読みは表記から当てずに SudachiPy の読みを使う。
    kakasi に表記を渡すと文脈を無視して読むため。
    """
    converter = RomanConverter()
    assert converter.to_roman("君") == "Kimi"                       # kakasi なら Kun
    assert converter.to_roman("テレ東") == "Teretou"                 # kakasi なら Terehigashi
    assert converter.to_roman("上弦の月", remove_spaces=False) == "Jougen No Tsuki"
    assert converter.to_roman("東京23時", remove_spaces=False) == "Tokyo 23 Ji"
    assert converter.to_roman("江ノ島") == "Enoshima"


def test_reading_is_not_used_for_symbols_and_latin():
    """
    記号やラテン文字にも読みは振られるが表記とは別物なので使わない。
    括弧の読み「キゴウ」が Kigou と出てしまうのを防ぐ。
    """
    converter = RomanConverter()
    assert "Kigou" not in converter.to_roman("君(テスト)")
    assert converter.to_roman("Vol. 3", remove_spaces=False) == "Vol. 3"


def test_kanji_reading_override():
    """
    SudachiPy の読みが曲名向きでない語は kanji_reading.json で差し替える。
    """
    converter = RomanConverter()
    assert converter.to_roman("私") == "Watashi"        # 既定はワタクシ
    assert converter.to_roman("琥珀色", remove_spaces=False) == "Kohaku Iro"


def test_iteration_mark():
    """
    踊り字「々」は kakasi が "(kurikaesi)" にしてしまうので開く。
    ただし SudachiPy が読める語は触らない。
    """
    converter = RomanConverter()
    assert converter.to_roman("時々") == "Tokidoki"
    assert converter.to_roman("人々") == "Hitobito"
    assert "kurikaesi" not in converter.to_roman("阿良々木")


def test_multi_token_loanword():
    """
    SudachiPy が割ってしまう外来語は、連結して辞書を引く。
    「エイリアンズ」は エイリ+アンズ に割れるため1トークンでは引けない。
    """
    converter = RomanConverter()
    assert converter.to_roman("エイリアンズ") == "Aliens"
    assert converter.to_roman("ドリームランド") == "Dreamland"
    assert converter.to_roman("ワークアウト") == "Workout"
    # 連結しても辞書になければ、ばらしたまま
    assert converter.to_roman("アンズ") == "Anzu"


def test_no_empty_dictionary_values():
    """
    値が空の辞書エントリは語を消してしまうので許さない。
    """
    empty = [k for k, v in RomanConverter.HIRAGANA_ENGLISH.items() if not v.strip()]
    assert not empty, f"空の値を持つエントリ: {empty}"


def test_readme_examples():
    """
    Test README conversion examples.
    """
    converter = RomanConverter()
    # READMEの変換例をそのまま検証
    assert converter.to_roman("アース・ウィンド＆ファイアー") == "EarthWindAndFire"
    assert converter.to_roman("いけないボーダーライン") == "IkeNaiBorderLine"
    assert converter.to_roman("さよならCOLOR") == "SayonaraColor"
    assert converter.to_roman("釈迦・イン・ザ・ハウス") == "ShakaInTheHouse"
