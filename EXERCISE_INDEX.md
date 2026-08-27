# Python演習教材 索引

各教材は、誘導・穴埋め・選択・考察を含む問題版と、コメント付き完成コードの解答版に分かれています。

- 教材ペア数: **99**
- 問題版: `*_problem`フォルダ
- 解答版: `*_Ans`フォルダ
- 実行基準ディレクトリ: リポジトリ直下

## 推奨環境

Python 3.14で検証しています。主なライブラリはNumPy、Pandas、Matplotlib、SciPy、
scikit-learn、Seaborn、OpenCV、Pillow、openpyxlです。グラフを表示する解答では、
実行後にグラフウィンドウを閉じると処理が終了します。

## 教材構成

| 系列 | ペア数 | 主な内容 |
|---|---:|---|
| A1 | 1 | 変数、型、演算、条件分岐、反復 |
| A2 | 1 | リスト、タプル、辞書、集合 |
| A3 | 10 | 関数、クラス、文字列、ファイル、業務ツール |
| B1 | 10 | NumPy・Pandasによる表データ操作 |
| B2 | 11 | 業務データの可視化 |
| B3 | 1 | 長期気候データ分析 |
| C1 | 5 | 数値計算、検量線、希釈、回帰 |
| C2 | 16 | 統計検定、前処理、画像・スペクトル解析 |
| C3 | 10 | 科学・材料データの機械学習とシミュレーション |
| D1 | 8 | PCA、クラスタリング、分類、回帰の90分演習 |
| Other | 26 | 科学計測、画像、時系列、機械学習の発展教材 |

## A1 系

| No. | テーマ | 問題版 | 解答版 |
|---:|---|---|---|
| 1 | カフェの1日を題材にPythonの基本構文を学ぼう | [問題](A1_problem/A1_enshuukadai_problem.py) | [解答](A1_Ans/A1_enshuukadai_Ans.py) |

## A2 系

| No. | テーマ | 問題版 | 解答版 |
|---:|---|---|---|
| 1 | 商品・注文データでリスト、タプル、辞書、集合を学ぼう | [問題](A2_problem/A2_enshuukadai_problem.py) | [解答](A2_Ans/A2_enshuukadai_Ans.py) |

## A3 系

| No. | テーマ | 問題版 | 解答版 |
|---:|---|---|---|
| 1 | コールセンターの応答時間を関数で集計しよう | [問題](A3_problem/A3_enshuukadai_01_problem.py) | [解答](A3_Ans/A3_enshuukadai_01_Ans.py) |
| 2 | 英語の問い合わせ件名を点検する文字列関数を作ろう | [問題](A3_problem/A3_enshuukadai_02_problem.py) | [解答](A3_Ans/A3_enshuukadai_02_Ans.py) |
| 3 | 不正な入出金を防ぐ銀行口座クラスを作ろう | [問題](A3_problem/A3_enshuukadai_03_problem.py) | [解答](A3_Ans/A3_enshuukadai_03_Ans.py) |
| 4 | 配送地点が営業所の担当範囲内か判定しよう | [問題](A3_problem/A3_enshuukadai_04_problem.py) | [解答](A3_Ans/A3_enshuukadai_04_Ans.py) |
| 5 | お客様アンケートの頻出語を調べよう | [問題](A3_problem/A3_enshuukadai_05_problem.py) | [解答](A3_Ans/A3_enshuukadai_05_Ans.py) |
| 6 | 海外工場と共有する温度記録を変換しよう | [問題](A3_problem/A3_enshuukadai_06_problem.py) | [解答](A3_Ans/A3_enshuukadai_06_Ans.py) |
| 7 | チームの業務タスクを管理するクラスを作ろう | [問題](A3_problem/A3_enshuukadai_07_problem.py) | [解答](A3_Ans/A3_enshuukadai_07_Ans.py) |
| 8 | 設備の連続稼働日パターンを分析しよう | [問題](A3_problem/A3_enshuukadai_08_problem.py) | [解答](A3_Ans/A3_enshuukadai_08_Ans.py) |
| 9 | 見積金額を計算する安全な業務電卓を作ろう | [問題](A3_problem/A3_enshuukadai_09_problem.py) | [解答](A3_Ans/A3_enshuukadai_09_Ans.py) |
| 10 | 社員台帳から研修対象者を検索しよう | [問題](A3_problem/A3_enshuukadai_10_problem.py) | [解答](A3_Ans/A3_enshuukadai_10_Ans.py) |

## B1 系

| No. | テーマ | 問題版 | 解答版 |
|---:|---|---|---|
| 1 | 10店舗の販売実績をNumPyで集計しよう | [問題](B1_problem/B1_enshuukadai_01_problem.py) | [解答](B1_Ans/B1_enshuukadai_01_Ans.py) |
| 2 | 研修参加者名簿をDataFrameで作ろう | [問題](B1_problem/B1_enshuukadai_02_problem.py) | [解答](B1_Ans/B1_enshuukadai_02_Ans.py) |
| 3 | 品質検査CSVを読み、内容を確認しよう | [問題](B1_problem/B1_enshuukadai_03_problem.py) | [解答](B1_Ans/B1_enshuukadai_03_Ans.py) |
| 4 | 品質検査結果へ判定列を追加して保存しよう | [問題](B1_problem/B1_enshuukadai_04_problem.py) | [解答](B1_Ans/B1_enshuukadai_04_Ans.py) |
| 5 | 在庫不足の商品だけを抽出しよう | [問題](B1_problem/B1_enshuukadai_05_problem.py) | [解答](B1_Ans/B1_enshuukadai_05_Ans.py) |
| 6 | 配送依頼を優先度と締切で並べよう | [問題](B1_problem/B1_enshuukadai_06_problem.py) | [解答](B1_Ans/B1_enshuukadai_06_Ans.py) |
| 7 | 配送時間の平均・中央値・最大値を求めよう | [問題](B1_problem/B1_enshuukadai_07_problem.py) | [解答](B1_Ans/B1_enshuukadai_07_Ans.py) |
| 8 | 冷蔵庫の欠測温度を適切に補完しよう | [問題](B1_problem/B1_enshuukadai_08_problem.py) | [解答](B1_Ans/B1_enshuukadai_08_Ans.py) |
| 9 | 店舗売上表へ客単価列を追加しよう | [問題](B1_problem/B1_enshuukadai_09_problem.py) | [解答](B1_Ans/B1_enshuukadai_09_Ans.py) |
| 10 | 東西2拠点の研修名簿を統合しよう | [問題](B1_problem/B1_enshuukadai_10_problem.py) | [解答](B1_Ans/B1_enshuukadai_10_Ans.py) |

## B2 系

| No. | テーマ | 問題版 | 解答版 |
|---:|---|---|---|
| 1 | 新商品の週次売上を折れ線グラフにしよう | [問題](B2_problem/B2_enshuukadai_01_problem.py) | [解答](B2_Ans/B2_enshuukadai_01_Ans.py) |
| 2 | 健康診断受診者の年齢分布を調べよう | [問題](B2_problem/B2_enshuukadai_02_problem.py) | [解答](B2_Ans/B2_enshuukadai_02_Ans.py) |
| 3 | 問い合わせ理由別件数を棒グラフにしよう | [問題](B2_problem/B2_enshuukadai_03_problem.py) | [解答](B2_Ans/B2_enshuukadai_03_Ans.py) |
| 4 | 配送会社ごとの所要時間を箱ひげ図で比べよう | [問題](B2_problem/B2_enshuukadai_04_problem.py) | [解答](B2_Ans/B2_enshuukadai_04_Ans.py) |
| 5 | 広告費と問い合わせ数の関係を散布図で調べよう | [問題](B2_problem/B2_enshuukadai_05_problem.py) | [解答](B2_Ans/B2_enshuukadai_05_Ans.py) |
| 6 | 月次売上の実績と目標を重ねて表示しよう | [問題](B2_problem/B2_enshuukadai_06_problem.py) | [解答](B2_Ans/B2_enshuukadai_06_Ans.py) |
| 7 | 在庫推移グラフへ発注点を追加しよう | [問題](B2_problem/B2_enshuukadai_07_problem.py) | [解答](B2_Ans/B2_enshuukadai_07_Ans.py) |
| 8 | キャンペーン開始を売上グラフへ注釈しよう | [問題](B2_problem/B2_enshuukadai_08_problem.py) | [解答](B2_Ans/B2_enshuukadai_08_Ans.py) |
| 9 | 倉庫床面の高さ測定を3D表示しよう | [問題](B2_problem/B2_enshuukadai_09_problem.py) | [解答](B2_Ans/B2_enshuukadai_09_Ans.py) |
| 10 | 試作品の複数寸法をペアプロットで比較しよう | [問題](B2_problem/B2_enshuukadai_10_problem.py) | [解答](B2_Ans/B2_enshuukadai_10_Ans.py) |
| 11 | 曜日・時間帯別の来店人数をヒートマップにしよう | [問題](B2_problem/B2_enshuukadai_11_problem.py) | [解答](B2_Ans/B2_enshuukadai_11_Ans.py) |

## B3 系

| No. | テーマ | 問題版 | 解答版 |
|---:|---|---|---|
| 1 | 自治体の環境計画担当者として長期気候データを分析しよう | [問題](B3_problem/B3_enshuukadai_01_problem.py) | [解答](B3_Ans/B3_enshuukadai_01_Ans.py) |

## C1 系

| No. | テーマ | 問題版 | 解答版 |
|---:|---|---|---|
| 1 | 検査サービス25検体分の請求額を計算しよう | [問題](C1_problem/C1_enshuukadai_01_problem.py) | [解答](C1_Ans/C1_enshuukadai_01_Ans.py) |
| 2 | 倉庫レイアウトの距離と棚容量を求めよう | [問題](C1_problem/C1_enshuukadai_02_problem.py) | [解答](C1_Ans/C1_enshuukadai_02_Ans.py) |
| 3 | 標準液の濃度と吸光度の関係を確認しよう | [問題](C1_problem/C1_enshuukadai_03_problem.py) | [解答](C1_Ans/C1_enshuukadai_03_Ans.py) |
| 4 | 検量線を作り、未知試料の濃度を推定しよう | [問題](C1_problem/C1_enshuukadai_04_problem.py) | [解答](C1_Ans/C1_enshuukadai_04_Ans.py) |
| 5 | 0.050 mol/L原液10mLへ水50mLを加えた濃度を求めよう | [問題](C1_problem/C1_enshuukadai_05_problem.py) | [解答](C1_Ans/C1_enshuukadai_05_Ans.py) |

## C2 系

| No. | テーマ | 問題版 | 解答版 |
|---:|---|---|---|
| 1 | EC購入画面A/Bテストで平均注文額を比較しよう | [問題](C2_problem/C2_enshuukadai_01_problem.py) | [解答](C2_Ans/C2_enshuukadai_01_Ans.py) |
| 2 | 動画教材が試験得点へ与える影響を比較しよう | [問題](C2_problem/C2_enshuukadai_01_test_scores_problem.py) | [解答](C2_Ans/C2_enshuukadai_01_test_scores_Ans.py) |
| 3 | 3店舗の待ち時間平均をANOVAで比較しよう | [問題](C2_problem/C2_enshuukadai_02_problem.py) | [解答](C2_Ans/C2_enshuukadai_02_Ans.py) |
| 4 | 研修受講と事故有無の関連をカイ二乗検定で調べよう | [問題](C2_problem/C2_enshuukadai_03_problem.py) | [解答](C2_Ans/C2_enshuukadai_03_Ans.py) |
| 5 | 微生物培養数の指数増加を非線形回帰で表そう | [問題](C2_problem/C2_enshuukadai_04_problem.py) | [解答](C2_Ans/C2_enshuukadai_04_Ans.py) |
| 6 | ローン返済遅延をロジスティック回帰で分類しよう | [問題](C2_problem/C2_enshuukadai_05_problem.py) | [解答](C2_Ans/C2_enshuukadai_05_Ans.py) |
| 7 | 製品の複数品質指標をPCAで2次元に要約しよう | [問題](C2_problem/C2_enshuukadai_06_problem.py) | [解答](C2_Ans/C2_enshuukadai_06_Ans.py) |
| 8 | 支店の業績を階層的クラスタリングで整理しよう | [問題](C2_problem/C2_enshuukadai_07_problem.py) | [解答](C2_Ans/C2_enshuukadai_07_Ans.py) |
| 9 | 店舗を販売特性でk-means分類しよう | [問題](C2_problem/C2_enshuukadai_08_problem.py) | [解答](C2_Ans/C2_enshuukadai_08_Ans.py) |
| 10 | 店舗センサーの欠測値を補完しよう | [問題](C2_problem/C2_enshuukadai_09_problem.py) | [解答](C2_Ans/C2_enshuukadai_09_Ans.py) |
| 11 | 製造センサーの異常値をzスコアで検出しよう | [問題](C2_problem/C2_enshuukadai_10_problem.py) | [解答](C2_Ans/C2_enshuukadai_10_Ans.py) |
| 12 | 顧客基本情報と購買集計をIDで結合しよう | [問題](C2_problem/C2_enshuukadai_11_problem.py) | [解答](C2_Ans/C2_enshuukadai_11_Ans.py) |
| 13 | 支店・商品カテゴリ別の売上を集計しよう | [問題](C2_problem/C2_enshuukadai_12_problem.py) | [解答](C2_Ans/C2_enshuukadai_12_Ans.py) |
| 14 | 病理画像をグレースケール化し輝度分布を確認しよう | [問題](C2_problem/C2_enshuukadai_13_problem.py) | [解答](C2_Ans/C2_enshuukadai_13_Ans.py) |
| 15 | 蛍光顕微鏡画像を色別にセグメンテーションしよう | [問題](C2_problem/C2_enshuukadai_14_problem.py) | [解答](C2_Ans/C2_enshuukadai_14_Ans.py) |
| 16 | 質量スペクトルからノイズでないピークを抽出しよう | [問題](C2_problem/C2_enshuukadai_15_problem.py) | [解答](C2_Ans/C2_enshuukadai_15_Ans.py) |

## C3 系

| No. | テーマ | 問題版 | 解答版 |
|---:|---|---|---|
| 1 | 河川汚染物質の濃度から生物影響値を回帰予測しよう | [問題](C3_problem/C3_enshuukadai_01_problem.py) | [解答](C3_Ans/C3_enshuukadai_01_Ans.py) |
| 2 | 成分値だけからワイン試料を教師なし分類しよう | [問題](C3_problem/C3_enshuukadai_02_problem.py) | [解答](C3_Ans/C3_enshuukadai_02_Ans.py) |
| 3 | 13成分のワイン分析値をPCAで要約しよう | [問題](C3_problem/C3_enshuukadai_03_problem.py) | [解答](C3_Ans/C3_enshuukadai_03_Ans.py) |
| 4 | 反応物A+B→Cの時系列から反応速度を求めよう | [問題](C3_problem/C3_enshuukadai_04_problem.py) | [解答](C3_Ans/C3_enshuukadai_04_Ans.py) |
| 5 | 微粒子のブラウン運動をランダムウォークで再現しよう | [問題](C3_problem/C3_enshuukadai_05_problem.py) | [解答](C3_Ans/C3_enshuukadai_05_Ans.py) |
| 6 | 温度と粒径が拡散へ与える影響を比較しよう | [問題](C3_problem/C3_enshuukadai_06_problem.py) | [解答](C3_Ans/C3_enshuukadai_06_Ans.py) |
| 7 | 分子記述子から水への溶解度をニューラルネットで予測しよう | [問題](C3_problem/C3_enshuukadai_07_problem.py) | [解答](C3_Ans/C3_enshuukadai_07_Ans.py) |
| 8 | 溶解度データの関係を可視化してモデル前提を確認しよう | [問題](C3_problem/C3_enshuukadai_08_problem.py) | [解答](C3_Ans/C3_enshuukadai_08_Ans.py) |
| 9 | 樹脂配合から耐久性をRandom Forestで予測・最適化しよう | [問題](C3_problem/C3_enshuukadai_09_problem.py) | [解答](C3_Ans/C3_enshuukadai_09_Ans.py) |
| 10 | 樹脂材料の耐久性をDNNで予測しよう | [問題](C3_problem/C3_enshuukadai_10_problem.py) | [解答](C3_Ans/C3_enshuukadai_10_Ans.py) |

## D1 系

| No. | テーマ | 問題版 | 解答版 |
|---:|---|---|---|
| 1 | D1 enshukadai 01 | [問題](D1_problem/D1_enshukadai_01_problem.py) | [解答](D1_Ans/D1_enshukadai_01_Ans.py) |
| 2 | D1 enshukadai 02 | [問題](D1_problem/D1_enshukadai_02_problem.py) | [解答](D1_Ans/D1_enshukadai_02_Ans.py) |
| 3 | D1 enshukadai 03 | [問題](D1_problem/D1_enshukadai_03_problem.py) | [解答](D1_Ans/D1_enshukadai_03_Ans.py) |
| 4 | D1 enshukadai 04 | [問題](D1_problem/D1_enshukadai_04_problem.py) | [解答](D1_Ans/D1_enshukadai_04_Ans.py) |
| 5 | D1 enshukadai 05 | [問題](D1_problem/D1_enshukadai_05_problem.py) | [解答](D1_Ans/D1_enshukadai_05_Ans.py) |
| 6 | D1 enshukadai 06 | [問題](D1_problem/D1_enshukadai_06_problem.py) | [解答](D1_Ans/D1_enshukadai_06_Ans.py) |
| 7 | D1 enshukadai 07 | [問題](D1_problem/D1_enshukadai_07_problem.py) | [解答](D1_Ans/D1_enshukadai_07_Ans.py) |
| 8 | D1 enshukadai 08 | [問題](D1_problem/D1_enshukadai_08_problem.py) | [解答](D1_Ans/D1_enshukadai_08_Ans.py) |

## Other 系

| No. | テーマ | 問題版 | 解答版 |
|---:|---|---|---|
| 1 | 顕微鏡画像から円形の血球候補を数えよう | [問題](Other_problem/blood_problem.py) | [解答](Other_Ans/blood_Ans.py) |
| 2 | 医薬品純度試験用のクロマトグラムを生成しよう | [問題](Other_problem/chromatogram_data_problem.py) | [解答](Other_Ans/chromatogram_data_Ans.py) |
| 3 | 電極評価用CVデータを生成してCSVへ保存しよう | [問題](Other_problem/CV_dummy_data_problem.py) | [解答](Other_Ans/CV_dummy_data_Ans.py) |
| 4 | 電池材料の酸化還元反応をCVで模擬しよう | [問題](Other_problem/CV_dummy_data_production_2_problem.py) | [解答](Other_Ans/CV_dummy_data_production_2_Ans.py) |
| 5 | 材料配合から耐久年数を多層ニューラルネットで予測しよう | [問題](Other_problem/DNN_material_problem.py) | [解答](Other_Ans/DNN_material_Ans.py) |
| 6 | 分光スペクトルから製品種類を分類しよう | [問題](Other_problem/enshu_day2_clf_problem.py) | [解答](Other_Ans/enshu_day2_clf_Ans.py) |
| 7 | 未知の分光試料をPCAとクラスタリングで探索しよう | [問題](Other_problem/enshu_day2_PCA_cluster_problem.py) | [解答](Other_Ans/enshu_day2_PCA_cluster_Ans.py) |
| 8 | UV-VisスペクトルをPCAで要約し品質変動を探そう | [問題](Other_problem/enshu_PCA_uv_vis_problem.py) | [解答](Other_Ans/enshu_PCA_uv_vis_Ans.py) |
| 9 | 複数試料の分光スペクトルを比較表示しよう | [問題](Other_problem/enshu_plot_problem.py) | [解答](Other_Ans/enshu_plot_Ans.py) |
| 10 | 1日の分析業務として分光データを読込・前処理・可視化しよう | [問題](Other_problem/enshuu_1day_problem.py) | [解答](Other_Ans/enshuu_1day_Ans.py) |
| 11 | 税率と単価を使い、小数計算の誤差を確認しよう | [問題](Other_problem/example_float_problem.py) | [解答](Other_Ans/example_float_Ans.py) |
| 12 | 送料を計算する再利用可能な関数を作ろう | [問題](Other_problem/example_function_problem.py) | [解答](Other_Ans/example_function_Ans.py) |
| 13 | 複数支店の月次売上Excelを安全に統合しよう | [問題](Other_problem/excel_problem.py) | [解答](Other_Ans/excel_Ans.py) |
| 14 | 手書き数字画像を前処理し、学習済みモデルで認識しよう | [問題](Other_problem/handwriting_recognition_problem.py) | [解答](Other_Ans/handwriting_recognition_Ans.py) |
| 15 | 手書き数字分類器を学習・保存しよう | [問題](Other_problem/handwriting_train_problem.py) | [解答](Other_Ans/handwriting_train_Ans.py) |
| 16 | 宅配需要を分析して配送エリアを設計しよう | [問題](Other_problem/kmeans_problem.py) | [解答](Other_Ans/kmeans_Ans.py) |
| 17 | 食品包装材の溶出試験で未知ピークを調べよう | [問題](Other_problem/Mass_spectrum_data_problem.py) | [解答](Other_Ans/Mass_spectrum_data_Ans.py) |
| 18 | 製造ライン洗浄後の残留物を模した質量スペクトルを作ろう | [問題](Other_problem/Mass_spectrum_production_data_problem.py) | [解答](Other_Ans/Mass_spectrum_production_data_Ans.py) |
| 19 | 回転機械の故障検知用振動データを作ろう | [問題](Other_problem/noise_and_sine_generator_problem.py) | [解答](Other_Ans/noise_and_sine_generator_Ans.py) |
| 20 | 顕微鏡画像の凝集粒子を分離して数えよう | [問題](Other_problem/particle_counting_problem.py) | [解答](Other_Ans/particle_counting_Ans.py) |
| 21 | Random Forestで材料耐久性を予測し配合候補を探索しよう | [問題](Other_problem/RF_material_problem.py) | [解答](Other_Ans/RF_material_Ans.py) |
| 22 | センサー履歴から次時点の値を予測しよう | [問題](Other_problem/RNN_analysis2_problem.py) | [解答](Other_Ans/RNN_analysis2_Ans.py) |
| 23 | 設備振動時系列を正常・異常へ分類しよう | [問題](Other_problem/RNN_analysis_problem.py) | [解答](Other_Ans/RNN_analysis_Ans.py) |
| 24 | ポンプ圧力信号を生成し、次時点予測モデルを検証しよう | [問題](Other_problem/RNN_with_signal_generator_problem.py) | [解答](Other_Ans/RNN_with_signal_generator_Ans.py) |
| 25 | 歴史的乗客データで生存分類と公平性を考えよう | [問題](Other_problem/titanic_problem.py) | [解答](Other_Ans/titanic_Ans.py) |
| 26 | 顧客離反の不均衡データを勾配ブースティングで分類しよう | [問題](Other_problem/XGBoost_analysis_problem.py) | [解答](Other_Ans/XGBoost_analysis_Ans.py) |

## 使い方

1. 問題版を開き、TODO部分へコードを書きます。
2. 選択問題と考察問題へ、自分の言葉で回答します。
3. 実行結果を確認した後、対応する解答版と比較します。
4. 解答を写すだけでなく、データや条件を変えて結果の変化を確認します。

## 注意

医療、品質、安全、融資などを題材にしたコードは学習用です。実際の診断・品質保証・
安全判断・顧客への不利益な意思決定へ、そのまま使用しないでください。
