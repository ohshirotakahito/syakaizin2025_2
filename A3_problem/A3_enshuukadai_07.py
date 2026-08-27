# -*- coding: utf-8 -*-
"""
7. シンプルなToDoリスト管理:

（課題）
ToDoリストを管理するクラスToDoListを作成する。
タスクを追加するメソッドadd_taskと、タスクを完了としてマークするメソッドcomplete_taskを追加する。
全タスクの一覧を表示するメソッドdisplay_tasksを追加する。
"""

class ToDoList:
    def __init__(self):
        """ ToDoリストの初期化 """
        # TODO: ここに実装してください
        pass

    def add_task(self, task_name):
        """ タスクを追加する """
        # TODO: ここに実装してください
        pass

    def complete_task(self, task_name):
        """ タスクを完了としてマークする（存在しない場合はその旨を表示する） """
        # TODO: ここに実装してください
        pass

    def display_tasks(self):
        """ 全タスクの一覧を表示する（空の場合は「ToDoリストは空です。」と表示する） """
        # TODO: ここに実装してください
        pass

# ToDoリストの使用例
todo_list = ToDoList()
todo_list.add_task("買い物")
todo_list.add_task("掃除")
todo_list.complete_task("買い物")
todo_list.display_tasks()
