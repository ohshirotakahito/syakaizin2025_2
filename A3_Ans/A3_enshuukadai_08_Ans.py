# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 10:18:02 2023

@author: ohshi
"""

# =============================================================================
# 解答版：連続稼働日と点検日のパターンを分析する
# 8. 数字のパターン分析:
# 
# （課題）
# 整数のリストを受け取り、その中で連続する数字の最長シーケンスを見つける関数find_longest_sequenceを作成する。
# 同じリストを使って、偶数と奇数の数をそれぞれ数える関数count_even_oddを作成する。
# 
# =============================================================================

def find_longest_sequence(numbers):
    """ 連続する数字の最長シーケンスを見つける """
    if not numbers:
        return []

    longest = current = [numbers[0]]

    for i in range(1, len(numbers)):
        if numbers[i] == numbers[i-1] + 1:
            current.append(numbers[i])
            if len(current) > len(longest):
                longest = current
        else:
            current = [numbers[i]]

    return longest

def count_even_odd(numbers):
    """ 偶数と奇数の数をそれぞれ数える """
    even_count = sum(1 for num in numbers if num % 2 == 0)
    odd_count = len(numbers) - even_count
    return even_count, odd_count

# 数字のリストの例
numbers = [1, 2, 3, 5, 6, 7, 9, 10, 11, 12]

# 連続する数字の最長シーケンスを見つける
longest_sequence = find_longest_sequence(numbers)
print(f"最長の連続するシーケンス: {longest_sequence}")

# 偶数と奇数の数を数える
even_count, odd_count = count_even_odd(numbers)
print(f"偶数の数: {even_count}, 奇数の数: {odd_count}")


