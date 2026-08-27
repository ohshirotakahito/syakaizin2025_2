# -*- coding: utf-8 -*-
"""
演習：タイタニック号の乗客データから生存を予測する

【想定する場面】
タイタニック号の乗客データ（年齢、性別、運賃、乗船港など）を使い、
生存したかどうかを予測するモデルを作る。欠損値の補完、カテゴリ変数の
数値化（One-Hot Encoding）、Random Forestによる分類までを
1つのPipelineにまとめる。

※ 実行するには data/datasets_11657_16098_train.csv を用意してください。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix


# =============================================================================
# 1. データを読み込み、不要な列を除く
# =============================================================================

file_path = DATA_DIR / "datasets_11657_16098_train.csv"
data = pd.read_csv(file_path)

# 'Cabin'は欠損が多く、'Name'と'Ticket'は今回は使わない列として除きます。
data_cleaned = data.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'])

# 目的変数'Survived'と、それ以外の特徴量に分けます。
X = data_cleaned.drop(columns=['Survived'])
y = data_cleaned['Survived']

categorical_cols = ['Sex', 'Embarked']
numerical_cols = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare']


# =============================================================================
# 2. 数値列・カテゴリ列それぞれの前処理を定義する
# =============================================================================

# TODO: numerical_cols用の前処理（欠損値を中央値で補完）を作ってください
# ヒント： SimpleImputer(strategy='median')
numeric_transformer = None

# TODO: categorical_cols用の前処理（欠損値を最頻値で補完し、One-Hot Encoding）を
#       Pipelineとして作ってください
# ヒント： Pipeline(steps=[
#             ('imputer', SimpleImputer(strategy='most_frequent')),
#             ('encoder', OneHotEncoder(handle_unknown='ignore'))
#         ])
categorical_transformer = None

# TODO: numeric_transformerとcategorical_transformerをColumnTransformerで
#       組み合わせたpreprocessorを作ってください
preprocessor = None


# =============================================================================
# 3. 前処理とRandomForestClassifierを1つのPipelineにまとめる
# =============================================================================

# TODO: preprocessorとRandomForestClassifier(random_state=42)を
#       Pipelineとして組み合わせてください
model = None


# =============================================================================
# 4. 学習・予測・評価を行う
# =============================================================================

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TODO: model.fit()で学習し、model.predict()でX_testを予測してください
y_pred = None

accuracy = accuracy_score(y_test, y_pred)
print(accuracy)


# =============================================================================
# 5. 混同行列を表示する
# =============================================================================

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
disp.plot()

plt.title('Confusion Matrix for Survival Prediction')
plt.show()
