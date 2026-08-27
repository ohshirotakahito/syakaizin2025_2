# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 10:18:02 2023

@author: ohshi
"""

# =============================================================================
# 解答版：入出金と残高不足を管理する銀行口座クラス
# 3. シンプルな銀行アプリケーション:
# 
# （課題）
# 口座残高を管理するAccountクラスを作成する。
# 入金（deposit）と引き出し（withdraw）の機能を持つメソッドを追加する。
# 口座の現在の残高を表示するメソッドdisplay_balanceを追加する。
# 
# =============================================================================
class Account:
    def __init__(self, balance=0):
        """ 口座の初期化 """
        self.balance = balance

    def deposit(self, amount):
        """ 入金処理 """
        if amount > 0:
            self.balance += amount
            print(f"{amount}が入金されました。")
        else:
            print("正の金額を入力してください。")

    def withdraw(self, amount):
        """ 引き出し処理 """
        if amount > self.balance:
            print("残高不足です。")
        elif amount <= 0:
            print("正の金額を入力してください。")
        else:
            self.balance -= amount
            print(f"{amount}が引き出されました。")

    def display_balance(self):
        """ 現在の残高を表示 """
        print(f"現在の残高は{self.balance}です。")

# アカウントの使用例
account = Account()
account.deposit(1000)
account.display_balance()
account.withdraw(500)
account.display_balance()
account.withdraw(600)  # 残高不足の例



