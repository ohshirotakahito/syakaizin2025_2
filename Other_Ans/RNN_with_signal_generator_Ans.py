# -*- coding: utf-8 -*-
"""解答版：周期・ドリフト・ノイズを含むポンプ圧力の次時点予測。"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng=np.random.default_rng(7); t=np.arange(1800)
pressure=210+10*np.sin(2*np.pi*t/80)+4*np.sin(2*np.pi*t/17)+.004*t+rng.normal(0,1.2,t.size)
window=40; X=np.asarray([pressure[i-window:i] for i in range(window,len(pressure))]); y=pressure[window:]
split=int(len(X)*.8); X_train,X_test=X[:split],X[split:]; y_train,y_test=y[:split],y[split:]
model=make_pipeline(StandardScaler(),MLPRegressor(hidden_layer_sizes=(48,24),early_stopping=True,max_iter=1200,random_state=42))
model.fit(X_train,y_train); pred=model.predict(X_test)
print(f"Test RMSE: {np.sqrt(mean_squared_error(y_test,pred)):.2f} kPa")
fig,axes=plt.subplots(2,1,figsize=(10,7))
axes[0].plot(y_test[:200],label="Actual"); axes[0].plot(pred[:200],label="Predicted"); axes[0].legend(); axes[0].set_ylabel("kPa")
axes[1].scatter(pred,y_test-pred,alpha=.5); axes[1].axhline(0,color="red",linestyle="--"); axes[1].set(xlabel="Predicted kPa",ylabel="Residual")
fig.tight_layout(); plt.show()
