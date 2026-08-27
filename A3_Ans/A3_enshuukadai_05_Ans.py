from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 10:18:02 2023

@author: ohshi
"""

# =============================================================================
# 解答版：お客様アンケートの頻出語を集計するテキスト処理
# 5. テキスト処理ツール:
# 
# （課題）
# 与えられたテキストファイルから単語を読み込む関数load_wordsを作成する。
# 単語の出現回数を数える関数count_word_frequencyを作成する。
# 頻繁に出現する単語のリストを返す関数get_most_common_wordsを作成する。
# =============================================================================


import re
from collections import Counter

def load_words(file_path):
    """ テキストファイルから単語を読み込む """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()
        words = re.findall(r'\b\w+\b', text)
    return words

def count_word_frequency(words):
    """ 単語の出現回数を数える """
    return Counter(words)

def get_most_common_words(frequency, n=10):
    """ 頻繁に出現する単語のリストを返す """
    return frequency.most_common(n)

# テキストファイルの例（ファイルパスは適宜変更してください）
file_path = DATA_DIR / "example.txt"

# 単語を読み込む
words = load_words(file_path)

# 単語の出現回数を数える
word_frequency = count_word_frequency(words)

# 頻繁に出現する単語のリストを取得
most_common_words = get_most_common_words(word_frequency)
print("最も頻繁に出現する単語:")
for word, freq in most_common_words:
    print(f"{word}: {freq}回")




