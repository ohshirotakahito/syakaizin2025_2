# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 10:18:02 2023

@author: ohshi
"""

# =============================================================================
# 解答版：チーム業務の完了状態を管理するタスクリスト
# 7. シンプルなToDoリスト管理:
# 
# （課題）
# ToDoリストを管理するクラスToDoListを作成する。
# タスクを追加するメソッドadd_taskと、タスクを完了としてマークするメソッドcomplete_taskを追加する。
# 全タスクの一覧を表示するメソッドdisplay_tasksを追加する。
# 
# =============================================================================

class ToDoList:
    def __init__(self):
        """ ToDoリストの初期化 """
        self.tasks = {}

    def add_task(self, task_name):
        """ タスクを追加する """
        self.tasks[task_name] = False
        print(f"タスク '{task_name}' が追加されました。")

    def complete_task(self, task_name):
        """ タスクを完了としてマークする """
        if task_name in self.tasks:
            self.tasks[task_name] = True
            print(f"タスク '{task_name}' は完了としてマークされました。")
        else:
            print(f"タスク '{task_name}' は見つかりませんでした。")

    def display_tasks(self):
        """ 全タスクの一覧を表示する """
        if not self.tasks:
            print("ToDoリストは空です。")
        else:
            for task, completed in self.tasks.items():
                status = "完了" if completed else "未完了"
                print(f"{task}: {status}")

# ToDoリストの使用例
todo_list = ToDoList()
todo_list.add_task("買い物")
todo_list.add_task("掃除")
todo_list.complete_task("買い物")
todo_list.display_tasks()




