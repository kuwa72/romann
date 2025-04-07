import pytest
from src.romann import RomanConverter

def test_convert_kanji_to_roman():
    converter = RomanConverter()
    assert converter.to_roman("漢字") == "Kanji"
    assert converter.to_roman("日本語") == "Nihongo"
    assert converter.to_roman("こんにちは") == "Konnichiha"

def test_convert_mixed_text():
    converter = RomanConverter()
    assert converter.to_roman("Hello漢字World") == "Hello Kanji World"
    assert converter.to_roman("テスト123") == "Test 123"

def test_empty_string():
    converter = RomanConverter()
    assert converter.to_roman("") == ""

def test_whitespace_handling():
    converter = RomanConverter()
    assert converter.to_roman("こんにちは 世界") == "Konnichiha Sekai"
    assert converter.to_roman("  スペース  ") == "Space"

def test_natural_japanese_titles():
    converter = RomanConverter()
    assert converter.to_roman("薔薇の花") == "Bara No Hana"
    assert converter.to_roman("追憶のマーメイド") == "Tsuioku No Mermaid"
    assert converter.to_roman("A・RA・SHI") == "A.Ra.Shi"
    assert converter.to_roman("さよならCOLOR") == "Sayonara Color"

def test_katakana_english():
    converter = RomanConverter()
    assert converter.to_roman("メール") == "Mail"
    assert converter.to_roman("ストーリー") == "Story"
    assert converter.to_roman("ラブ") == "Love"
    assert converter.to_roman("ドリーム") == "Dream"

def test_particle_no():
    converter = RomanConverter()
    assert converter.to_roman("春の海") == "Haru No Umi"
    assert converter.to_roman("僕の名前") == "Boku No Namae"

def test_separator_conversion():
    converter = RomanConverter()
    assert converter.to_roman("A・B・C") == "A・B・C"
    assert converter.to_roman("ドット・パンク") == "Dotto・Panku"
