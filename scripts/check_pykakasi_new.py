from pykakasi import kakasi

def test_conversion_rules():
    # 新しいAPIを使用した設定
    kks = kakasi()

    test_cases = [
        '漢字',
        'ひらがな',
        'カタカナ',
        'テスト123',
        'A・B・C',
        'A・RA・SHI',
        '追憶のマーメイド',
        'こんにちは 世界',
        '薔薇の花'
    ]

    print("\n=== PyKakasi conversion results (new API) ===")
    for text in test_cases:
        # 文字列全体を一度に変換
        result = kks.convert(text)
        print(f"\nInput: {text}")
        print("Word-by-word output:")
        for item in result:
            print(f"  Original: {item['orig']}")
            print(f"  Romaji:   {item['hepburn'].capitalize()}")
        print("-" * 40)

        # 全体をromajiに変換した場合
        romaji = " ".join(item['hepburn'].capitalize() for item in result)
        print(f"Combined romaji: {romaji}")
        print("=" * 40)

if __name__ == '__main__':
    test_conversion_rules()
