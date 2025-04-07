import re
from pykakasi import kakasi

class RomanConverter:
    # ヘボン式ローマ字のカタカナ英語の辞書
    KATAKANA_ENGLISH = {
        # 基本的な英語
        'meeru': 'mail',
        'rabu': 'love',
        'sutoorii': 'story',
        'doriimu': 'dream',
        'karaa': 'color',
        'maameido': 'mermaid',
        'haato': 'heart',
        'tesuto': 'test',
        'supeesu': 'space',
        
        # 音楽関連
        'myuujikku': 'music',
        'dansu': 'dance',
        'suteeji': 'stage',
        'rizumu': 'rhythm',
        'songu': 'song',
        
        # ウェブ・IT関連
        'intaanetto': 'internet',
        'konpyuutaa': 'computer',
        'fairu': 'file',
        'messeeji': 'message',
        
        # その他一般
        'sutairu': 'style',
        'dezain': 'design',
        'shisutemu': 'system',
        'puroguramu': 'program',
        'dotto': 'dotted',
        'panku': 'punk',
    }
    def __init__(self):
        self.converter = kakasi()
    
    def convert_katakana_english(self, word: str) -> str:
        """
        Convert romanized katakana to English if it exists in the dictionary
        """
        return self.KATAKANA_ENGLISH.get(word.lower(), word).capitalize()
    

    def to_roman(self, text: str) -> str:
        """
        Convert Japanese text (kanji, hiragana, katakana) to romaji.
        Preserves non-Japanese characters as they are.
        
        Args:
            text (str): Input text containing Japanese characters
            
        Returns:
            str: Romanized text with natural capitalization and formatting
        """
        if not text:
            return ""
        
        # romanize by kakasi
        result = self.converter.convert(text)

        # collect hepburn
        result = [item['hepburn'].split("・") for item in result]

        # flatten list
        result = [word for sublist in result for word in sublist]
        
        # Convert katakana English to proper English
        result = [self.convert_katakana_english(word) for word in result]
        
        # Join words with spaces
        result = ' '.join(result)
        
        # Handle consecutive spaces
        result = re.sub(r'\s+', ' ', result)

        return result.strip()
