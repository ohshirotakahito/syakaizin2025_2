# -*- coding: utf-8 -*-
"""解答版：曜日・時間帯別の来店人数をヒートマップで確認する。"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

traffic = pd.DataFrame(
    [[12,24,38,31,20],[15,26,41,35,22],[14,28,45,39,24],
     [16,30,48,42,27],[20,36,58,51,34],[28,45,70,66,50],[25,40,62,59,46]],
    index=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
    columns=["9-11","11-13","13-15","15-17","17-19"],
)
sns.heatmap(traffic, annot=True, fmt="d", cmap="YlOrRd")
plt.title("Store Traffic by Day and Time"); plt.xlabel("Time"); plt.ylabel("Day")
plt.tight_layout(); plt.show()

