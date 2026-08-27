# -*- coding: utf-8 -*-
"""解答版：設備振動の時系列を正常・異常へ分類する。"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng=np.random.default_rng(42); time=np.linspace(0,1,120); sequences=[]; labels=[]
for label in [0,1]:
    for _ in range(250):
        frequency=rng.normal(12,.5); signal=np.sin(2*np.pi*frequency*time+rng.uniform(0,2*np.pi))
        if label: signal+=.6*np.sin(2*np.pi*frequency*2*time)+rng.normal(0,.25,time.size)
        else: signal+=rng.normal(0,.08,time.size)
        sequences.append(signal); labels.append(label)
X=np.asarray(sequences); y=np.asarray(labels)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
model=make_pipeline(StandardScaler(),MLPClassifier(hidden_layer_sizes=(48,),early_stopping=True,max_iter=1000,random_state=42))
model.fit(X_train,y_train); pred=model.predict(X_test)
print(classification_report(y_test,pred,target_names=["Normal","Fault"]))
ConfusionMatrixDisplay.from_predictions(y_test,pred,display_labels=["Normal","Fault"],cmap="Blues")
plt.title("Motor Vibration Classification"); plt.tight_layout(); plt.show()

