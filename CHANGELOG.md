# Changelog

All notable changes to this project will be documented in this file.

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
