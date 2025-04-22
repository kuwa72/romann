from setuptools import setup, find_packages

setup(
    name="romann",
    version="0.1.0",
    description="日本語→自然なローマ字・英語変換ライブラリ（kakasi/SudachiPyベース＋外来語辞書対応）",
    author="ykuwa",
    author_email="",
    url="https://github.com/kuwa72/romann",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"romann": ["hiragana_english.json", "katakana_english.json"]},
    install_requires=[
        "pykakasi",
        "jaconv",
        "sudachipy",
    ],
    python_requires=">=3.12",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
)
