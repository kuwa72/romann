# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2026-09-03
### Changed
- 漢字の読みを表記から当てるのをやめ、SudachiPy の読みを使うようにした。
  kakasi に表記を渡すと文脈を無視して読んでしまう
  - 「君」→ Kun が Kimi に、「テレ東」→ Terehigashi が Teretou に
  - 「江ノ島」→ Kounoshima、「阿佐ヶ谷」→ Asaketani、「東京23時」→ 23 Toki なども直る
  - 記号とラテン文字には読みが振られても使わない（「(」→キゴウ、「Vol.」→ボリューム）

### Added
- 複数トークンにまたがる外来語を連結して辞書を引くようにした。
  SudachiPy が「エイリアンズ」を エイリ+アンズ に割るため1語では引けなかった
  - エイリアンズ → Aliens、ドリームランド → Dreamland、ワークアウト → Workout
- `kanji_reading.json`: SudachiPy の読みを語ごとに差し替える（「私」→わたし など）

### Fixed
- 踊り字「々」が "(kurikaesi)" という文字列になっていた

## [0.2.0] - 2026-09-02
### Changed
- 外来語辞書を引く条件を絞った。読みが一致するだけの語を巻き込んでいたのを、
  カタカナ表記／ひらがなの名詞・形状詞／記号に限定した
  - 「愛」→ I、「食べたい」の「たい」→ Tie、「Vol.」→ Volume が直る

### Added
- 外来語辞書に約990語を追加（曲名・アーティスト名の実データから抽出）
- `kanji_english.json`: 漢字語を表記そのものをキーにして引く辞書

### Fixed
- 値が空の辞書エントリが語を消していた（「テレビ」「ドーム」「ミニスカート」など15件）

## [0.1.3] - 2025-05-21
### Fixed
- Fixed pylint issues (trailing whitespace, too many local variables)
- Improved code organization and maintainability

## [0.1.2] - 2025-05-21
### Changed
- Changed default behavior to remove spaces between words for better compatibility with display constraints
  - Use `remove_spaces=False` to include spaces between words

## [0.1.1] - 2025-05-20
### Improved
- Enhanced dictionary support
- Bug fixes and performance improvements

## [0.1.0] - 2025-04-23
### Added
- Initial release: Japanese to natural romaji/English conversion library (kakasi/SudachiPy-based, dictionary-driven)
- Supports customizable external dictionaries (hiragana_english.json, katakana_english.json)
- High-accuracy morphological analysis with SudachiPy
- TDD-based quality assurance
