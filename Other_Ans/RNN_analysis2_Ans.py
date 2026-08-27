# -*- coding: utf-8 -*-
"""解答版：センサーの過去24点から次時点の値を予測する。"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng=np.random.default_rng(42); t=np.arange(1200)
signal=20+2*np.sin(2*np.pi*t/96)+.003*t+rng.normal(0,.25,t.size)
window=24; X=[]; y=[]
for index in range(window,len(signal)): X.append(signal[index-window:index]); y.append(signal[index])
X=np.asarray(X); y=np.asarray(y); split=int(len(X)*.8)
X_train,X_test=X[:split],X[split:]; y_train,y_test=y[:split],y[split:]
model=make_pipeline(StandardScaler(),MLPRegressor(hidden_layer_sizes=(32,),early_stopping=True,max_iter=1000,random_state=42))
model.fit(X_train,y_train); pred=model.predict(X_test)
print(f"時系列テストMAE: {mean_absolute_error(y_test,pred):.3f}")
plt.plot(y_test[:180],label="Actual"); plt.plot(pred[:180],label="Predicted")
plt.title("Next-step Sensor Forecast"); plt.xlabel("Test time step"); plt.ylabel("Temperature")
plt.legend(); plt.grid(alpha=.2); plt.tight_layout(); plt.show()

