# -*- coding: utf-8 -*-
# 解答版：現実的な利用場面、処理の意味、結果の限界を確認します。
"""
採点の最も高いものと最も低いものを除いて平均をとることにより得点を求める
採点は長さ6のリストで与えられる。
"""
#得点を求めるリスト
a = [3.0, 4.0, 5.0, 4.4, 3.2, 5.5]
b = [4.0, 4.2, 5.0, 4.8, 2.2, 3.8]
c = [1.0, 3.0, 3.2, 6.4, 4.2, 3.5]

#関数を使わない場合
print((sum(a)-max(a)-min(a))/(len(a)-2 ))
print((sum(b)-max(b)-min(b))/(len(b)-2 ))
print((sum(c)-max(c)-min(c))/(len(c)-2 ))

#関数を使う場合
def score(x):
    return (sum(x)-max(x)-min(x))/(len(x)-2)

print(score(a) )    
print(score(b) ) 
print(score(c) ) 
