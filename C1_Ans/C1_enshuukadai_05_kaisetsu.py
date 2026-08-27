# -*- coding: utf-8 -*-
"""
演習：原液を希釈して作業用試薬を調製する（解説付き解答版）

【想定する場面】
濃度の分かっている原液（ストック溶液）を水で薄めて、実験や検査で使う
作業用試薬を作りたい。希釈後の最終濃度と、原液に対して何倍に薄めたか
（希釈倍率）を求める。

（課題）
1. 原液の体積と加える水の体積から、最終的な液量を求める。
2. 原液の濃度・体積と最終液量から、希釈後の最終濃度を求める。
3. 最終液量が原液の体積の何倍かを表す希釈倍率を求める。
"""

stock_concentration = 0.050  # 原液の濃度（mol/L）
stock_volume_ml = 10.0       # 原液の体積（mL）
water_volume_ml = 50.0       # 加える水の体積（mL）

# 原液と水を混ぜた後の、全体の液量を求めます。
final_volume_ml = stock_volume_ml + water_volume_ml

# 「原液に含まれていた溶質の量」は薄めても変わりません。
# 溶質の量 = 濃度 × 体積 なので、
#   希釈前の溶質量（stock_concentration × stock_volume_ml）
#   = 希釈後の溶質量（final_concentration × final_volume_ml）
# という関係が成り立ちます。これを最終濃度について解くと、
#   final_concentration = stock_concentration × stock_volume_ml ÷ final_volume_ml
# という式になります。
final_concentration = stock_concentration * stock_volume_ml / final_volume_ml

# 希釈倍率は「最終的な液量が、原液の体積の何倍になったか」を表します。
dilution_factor = final_volume_ml / stock_volume_ml

print(f"最終液量: {final_volume_ml:.1f} mL")
print(f"希釈倍率: {dilution_factor:.1f}倍")
print(f"最終濃度: {final_concentration:.5f} mol/L")
print("注意：体積が単純加算できる理想的な演習条件です。")

# 【ポイント】
# ・「濃度×体積＝溶質量」は薄める前後で変わらない、という考え方が希釈計算の基本です。
# ・実際の溶液では、混合によって体積がわずかに変化することがあるため、
#   厳密な調製では単純な体積の足し算が成り立たない場合もあります。
