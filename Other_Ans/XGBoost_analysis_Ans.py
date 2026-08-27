# -*- coding: utf-8 -*-
"""解答版：不均衡な設備故障データを勾配ブースティングで分類する。"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

rng=np.random.default_rng(42); n=2400
temperature=rng.normal(68,8,n); vibration=rng.gamma(2,1.2,n)
maintenance_hours=rng.integers(0,1800,n); load=rng.normal(75,15,n)
score=-5.2+.07*(temperature-68)+.5*(vibration-2.4)+.0018*(maintenance_hours-700)+.025*(load-75)
probability=1/(1+np.exp(-score)); failure=rng.binomial(1,probability)
data=pd.DataFrame({"temperature":temperature,"vibration":vibration,
                   "maintenance_hours":maintenance_hours,"load":load,"failure":failure})
print(f"故障率: {data['failure'].mean():.1%}")
X=data.drop(columns="failure"); y=data["failure"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)

# 少数派故障へ大きな重みを付け、見逃しを抑えます。
positive_weight=(y_train==0).sum()/(y_train==1).sum()
sample_weight=np.where(y_train==1,positive_weight,1.0)
model=HistGradientBoostingClassifier(max_iter=180,learning_rate=.06,max_leaf_nodes=15,random_state=42)
model.fit(X_train,y_train,sample_weight=sample_weight)
prob=model.predict_proba(X_test)[:,1]

# 業務目的に合わせ、標準0.5より低いしきい値0.35で故障判定します。
threshold=.35; pred=(prob>=threshold).astype(int)
print(f"ROC-AUC: {roc_auc_score(y_test,prob):.3f}")
print(classification_report(y_test,pred,target_names=["Normal","Failure"],zero_division=0))
ConfusionMatrixDisplay.from_predictions(y_test,pred,display_labels=["Normal","Failure"],cmap="Oranges")
plt.title(f"Failure Detection (threshold={threshold})"); plt.tight_layout(); plt.show()
print("しきい値を下げると見逃しは減りやすい一方、誤警報と点検コストが増えます。")
