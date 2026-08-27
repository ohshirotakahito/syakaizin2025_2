# -*- coding: utf-8 -*-
"""
3. シンプルな銀行アプリケーション:

（課題）
口座残高を管理するAccountクラスを作成する。
入金（deposit）と引き出し（withdraw）の機能を持つメソッドを追加する。
口座の現在の残高を表示するメソッドdisplay_balanceを追加する。
"""

class Account:
    def __init__(self, balance=0):
        """ 口座の初期化 """
        # TODO: ここに実装してください
        pass

    def deposit(self, amount):
        """ 入金処理 """
        # TODO: ここに実装してください
        pass

    def withdraw(self, amount):
        """ 引き出し処理（残高不足なら「残高不足です。」と表示する） """
        # TODO: ここに実装してください
        pass

    def display_balance(self):
        """ 現在の残高を表示 """
        # TODO: ここに実装してください
        pass

# アカウントの使用例
account = Account()
account.deposit(1000)
account.display_balance()
account.withdraw(500)
account.display_balance()
account.withdraw(600)  # 残高不足の例
