# -*- coding: utf-8 -*-
"""
10. 簡単なデータベース検索ツール:

（課題）
人物の名前と年齢を格納する簡単なデータベース（辞書）を作成する。
特定の名前を検索して、その人物の年齢を返す関数find_ageを作成する。
年齢でデータベースをフィルタリングし、特定の年齢範囲に含まれる全ての人物の名前を返す関数filter_by_age_rangeを作成する。
"""

def find_age(database, name):
    """ 特定の名前の人物の年齢を返す（存在しない場合は「名前が見つかりません。」を返す） """
    # TODO: ここに実装してください
    pass

def filter_by_age_range(database, min_age, max_age):
    """ 特定の年齢範囲に含まれる全ての人物の名前を返す """
    # TODO: ここに実装してください
    pass

# 簡単なデータベース（辞書）の例
people_db = {
    "Alice": 30,
    "Bob": 25,
    "Carol": 27,
    "Dave": 35
}

# 特定の名前で年齢を検索
name = "Alice"
age = find_age(people_db, name)
print(f"{name}の年齢は {age}歳です。")

# 特定の年齢範囲の人物を検索
min_age, max_age = 26, 32
age_range_people = filter_by_age_range(people_db, min_age, max_age)
print(f"年齢が{min_age}歳から{max_age}歳の人物: {age_range_people}")
