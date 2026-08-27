# -*- coding: utf-8 -*-
"""
D1 演習課題4（問題版）：購買履歴から顧客施策を考えよう
====================================================

【この課題で行うこと】
あなたはECサイトのCRM（顧客関係管理）担当者です。全員に同じ案内を送る
のではなく、購買行動が似ている顧客をグループに分け、それぞれに合った施策を
考えます。

今回は、正解となるグループ名が最初から用意されていません。そのため、正解
ラベルなしで似たデータをまとめる「教師なし学習」のk-meansを使います。

【使用する3つの特徴】
・annual_orders   ：過去1年間の注文回数
・avg_order_yen   ：1回あたりの平均注文額（円）
・days_since_last ：最終購入からの経過日数（日。小さいほど最近購入）

【用語】
・クラスタ：購買行動が似ている顧客のグループ
・クラスタ中心：各グループの平均的な顧客像を表す値
・シルエット係数：クラスタのまとまり具合を表す値。大きいほど分かれ方が明確
・標準化：単位や桁が違う項目を、同じ尺度で比較できるようにする処理

【取り組み方】
すべてのコードを一から書く必要はありません。説明と選択肢を読み、コード内の
「____」だけを埋めてください。繰り返し処理、顧客像の命名、グラフ描画などの
複雑な部分は記入済みです。

注意：「____」が残っている間は、プログラムは正しく実行できません。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


# 32人の架空顧客について、過去1年間の購買履歴を用意しています。
# このデータは変更せずに使用してください。
customers = pd.DataFrame({
    "customer_id": [f"C{number:03d}" for number in range(1, 33)],
    "annual_orders": [
        24, 28, 21, 30, 19, 26, 23, 27,
        32, 38, 29, 35, 40, 31, 36, 34,
        6, 8, 5, 9, 7, 4, 10, 6,
        2, 5, 3, 6, 1, 4, 3, 5,
    ],
    "avg_order_yen": [
        16800, 19200, 14500, 21800, 13200, 18400, 15700, 20500,
        3200, 4100, 2800, 4600, 3500, 3900, 4300, 3000,
        18500, 22000, 15800, 24500, 19800, 17200, 23100, 21000,
        3800, 6200, 2900, 7100, 2400, 5400, 4500, 6800,
    ],
    "days_since_last": [
        8, 3, 14, 2, 18, 6, 11, 4,
        5, 2, 9, 3, 1, 7, 4, 6,
        145, 110, 190, 95, 130, 220, 88, 165,
        75, 42, 120, 35, 180, 65, 98, 50,
    ],
})

print("【顧客データ：先頭5行】")
print(customers.head())


# ==================================================================
# 問題1：機械学習で比較する3列を選ぼう
# ==================================================================
# customer_idは顧客を識別する名前であり、購買行動の大きさを表す数値では
# ありません。そのため、k-meansには3つの数値列だけを渡します。
# 「____」へ入る列名を選んでください。
#
# 選択肢：
# A. ["annual_orders", "avg_order_yen", "days_since_last"]
# B. ["customer_id", "annual_orders", "avg_order_yen"]
# C. ["customer_id"]
# 自分の答え：
feature_names = ____
features = customers[feature_names]


# 【確認問題1】customer_idをk-meansへ渡さない理由はどれですか。
# A. 顧客IDは購買行動を表す量的な特徴ではないから
# B. k-meansでは3列までしか使えないから
# C. 顧客IDには必ず欠損値があるから
# 自分の答え：


# ==================================================================
# 問題2：3項目を標準化しよう
# ==================================================================
# 平均注文額は数万円、注文回数は数十回なので、数値の桁が大きく違います。
# そのまま距離を計算すると、平均注文額の影響が強くなりやすいため、各列を
# 平均0、標準偏差1の尺度へそろえます。
#
# 問題2-A：「____」へ入るクラス名を選んでください。
# 選択肢：A. KMeans    B. StandardScaler    C. PCA
# 自分の答え：
scaler = ____()

# 問題2-B：標準化の計算と変換を行うメソッドを選んでください。
# 選択肢：A. fit_transform    B. value_counts    C. inverse_transform
# 自分の答え：
scaled_features = scaler.____(features)


# 【確認問題2】標準化せずにk-meansを行うと、特に影響が強くなりそうな
# 項目はどれですか。
# A. annual_orders    B. avg_order_yen    C. customer_id
# 自分の答え：
# 理由：


# ==================================================================
# 問題3：クラスタ数を2～6まで試そう
# ==================================================================
# 顧客を何グループに分けるかは、最初から決まっていません。ここでは2～6の
# それぞれについてk-meansを行い、シルエット係数を比較します。
# rangeの終了値は含まれないため、2～6を作るにはrange(2, 7)とします。
candidate_k = range(2, 7)
silhouette_scores = []

for k in candidate_k:
    # n_clustersには、現在試しているクラスタ数kを指定します。
    # 問題3-A：「____」へ入るものを選んでください。
    # 選択肢：A. k    B. 32    C. "customer_id"
    candidate_model = KMeans(
        n_clusters=____,
        random_state=42,
        n_init=10,
    )

    # fit_predict()は、モデルの学習と各顧客のクラスタ割り当てを行います。
    candidate_labels = candidate_model.fit_predict(scaled_features)

    # 問題3-B：まとまり具合を評価する関数名を選んでください。
    # 選択肢：A. silhouette_score    B. StandardScaler    C. argmax
    score = ____(scaled_features, candidate_labels)
    silhouette_scores.append(score)
    print(f"クラスタ数={k}: シルエット係数={score:.3f}")


# ==================================================================
# 問題4：評価が最も高いクラスタ数を選ぼう
# ==================================================================
# np.argmax()は、リスト内で最大値がある位置を返します。その位置を
# candidate_kに対応させ、最もシルエット係数が高いクラスタ数を選びます。
#
# 選択肢：A. argmax    B. mean    C. append
# 自分の答え：
best_k = list(candidate_k)[int(np.____(silhouette_scores))]
print(f"\n採用するクラスタ数: {best_k}")


# 【確認問題3】シルエット係数について正しい説明はどれですか。
# A. 大きいほど、同じクラスタ内がまとまり、別クラスタから離れている
# B. 小さいほど、分類の正解率が高い
# C. 顧客の平均注文額を表す
# 自分の答え：


# ==================================================================
# 問題5：選んだクラスタ数で最終モデルを作ろう
# ==================================================================
# best_kを使って最終的なk-meansモデルを作ります。
# 問題5-A：クラスタ数へ入れる変数を選んでください。
# 選択肢：A. best_k    B. candidate_k    C. customer_id
# 自分の答え：
model = KMeans(n_clusters=____, random_state=42, n_init=10)

# 問題5-B：学習とクラスタ割り当てを行うメソッドを選んでください。
# 選択肢：A. fit_predict    B. inverse_transform    C. round
# 自分の答え：
cluster_numbers = model.____(scaled_features)


# 【確認問題4】クラスタ番号0、1、2、3について正しい説明はどれですか。
# A. 数字が大きいほど価値の高い顧客である
# B. 番号はグループを識別するだけで、順位や良し悪しの意味はない
# C. 0は必ず休眠顧客を表す
# 自分の答え：


# ==================================================================
# 問題6：クラスタ中心を元の単位へ戻そう
# ==================================================================
# model.cluster_centers_は標準化後の値です。そのままでは「注文額○円」の
# ように解釈できないため、scalerを使って円・回・日の元の単位へ戻します。
#
# 選択肢：A. fit_transform    B. inverse_transform    C. value_counts
# 自分の答え：
centers_original = scaler.____(model.cluster_centers_)


# ここからは、クラスタ中心を読みやすい表へ整える完成コードです。
cluster_summary = pd.DataFrame(centers_original, columns=feature_names)
cluster_summary["customers"] = (
    pd.Series(cluster_numbers).value_counts().sort_index().to_numpy()
)


# ==================================================================
# 準備：各クラスタへ分かりやすい顧客像の名前を付けよう
# ==================================================================
# k-meansが付ける番号には意味がないため、クラスタ中心の値を使って名前を
# 付けます。この判定コードは記入済みです。

# 最終購入からの日数が最も長いクラスタ：休眠・離反注意
dormant_cluster = cluster_summary["days_since_last"].idxmax()

# 休眠クラスタ以外で、平均注文額が最も高いクラスタ：優良VIP
remaining = cluster_summary.drop(index=dormant_cluster)
vip_cluster = remaining["avg_order_yen"].idxmax()

# 残りの中で、注文回数が最も多いクラスタ：頻繁・お手頃
remaining = remaining.drop(index=vip_cluster)
frequent_cluster = remaining["annual_orders"].idxmax()

# 最後に残ったクラスタ：育成候補
developing_cluster = remaining.drop(index=frequent_cluster).index[0]

persona_by_cluster = {
    dormant_cluster: "Dormant / Win-back",
    vip_cluster: "Loyal VIP",
    frequent_cluster: "Frequent / Value",
    developing_cluster: "Developing",
}

customers["cluster"] = cluster_numbers
customers["persona"] = customers["cluster"].map(persona_by_cluster)
cluster_summary["persona"] = cluster_summary.index.map(persona_by_cluster)

print("\n【クラスタごとの平均的な顧客像】")
print(cluster_summary.set_index("persona").round(1))


# 【確認問題5】顧客像と説明の正しい組み合わせを選んでください。
# A. Dormant / Win-back：最終購入から長期間経過している
# B. Loyal VIP：平均注文額が最も低く、購入から長期間経過している
# C. Frequent / Value：注文回数が最も少ない
# 自分の答え：


# ==================================================================
# 準備：顧客像に合った施策例を表示しよう
# ==================================================================
# 施策は顧客像から機械的に決まる正解ではありません。ここでは検討例を示します。
actions = {
    "Loyal VIP": "先行販売、限定商品、VIP会員特典",
    "Frequent / Value": "まとめ買い割引、送料無料条件の提案",
    "Dormant / Win-back": "再購入クーポン、離反理由アンケート",
    "Developing": "初回購入後のフォロー、関連商品の紹介",
}

print("\n【顧客像ごとの施策例】")
for persona, action in actions.items():
    count = (customers["persona"] == persona).sum()
    print(f"{persona:22s} ({count}人): {action}")


# ==================================================================
# 準備：分析結果をグラフで確認しよう
# ==================================================================
# 描画処理は複雑なので記入済みです。左はクラスタ数とシルエット係数、
# 右は3つの特徴をPCAで2次元に要約した顧客分布です。
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(list(candidate_k), silhouette_scores, marker="o", color="#4C78A8")
axes[0].axvline(best_k, color="#E45756", linestyle="--",
                label=f"Selected k = {best_k}")
axes[0].set_xlabel("Number of clusters (k)")
axes[0].set_ylabel("Silhouette score")
axes[0].set_title("Selecting the Number of Customer Segments")
axes[0].set_xticks(list(candidate_k))
axes[0].grid(alpha=0.25)
axes[0].legend()

pca = PCA(n_components=2)
points_2d = pca.fit_transform(scaled_features)

persona_colors = {
    "Loyal VIP": "#E45756",
    "Frequent / Value": "#4C78A8",
    "Dormant / Win-back": "#B279A2",
    "Developing": "#54A24B",
}

for persona, color in persona_colors.items():
    selected = customers["persona"] == persona
    axes[1].scatter(points_2d[selected, 0], points_2d[selected, 1],
                    color=color, s=75, alpha=0.85, label=persona)

for index, customer_id in enumerate(customers["customer_id"]):
    axes[1].annotate(customer_id, points_2d[index], xytext=(4, 3),
                     textcoords="offset points", fontsize=7)

axes[1].set_xlabel("PCA component 1")
axes[1].set_ylabel("PCA component 2")
axes[1].set_title("Customer Segments")
axes[1].grid(alpha=0.25)
axes[1].legend(title="Recommended action group", fontsize=8)
fig.tight_layout()
plt.show()


# ==================================================================
# 最後の考察
# ==================================================================
# 1. Dormant / Win-backの顧客へ、強い割引を全員一律に送る前に、何を確認
#    するとよいでしょうか。離反理由や施策費用も考えて答えてください。
# 自分の答え：


# 2. より適切な顧客分類にするため、追加したい情報を2つ以上選んでください。
# A. 購入商品の種類    B. クーポンへの反応    C. 返品履歴
# D. 顧客IDの文字数    E. ファイルを保存した時刻
# 自分の答え：


# 3. このクラスタだけで顧客の価値を決めてはいけないのはなぜですか。
# 購買履歴に含まれない事情、データの変化、顧客への公平性を考えてください。
# 自分の答え：


print("\n【注意】")
print("クラスタは施策を考える手掛かりであり、顧客の価値を決めるものではありません。")
print("実務では定期的に再学習し、施策後の反応も検証する必要があります。")
