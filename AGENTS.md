# Endfield Damage Calculator Project Axis 第2版

## 目的

アークナイツ：エンドフィールドのダメージ計算機を作る。

単に計算式を動かすだけではなく、
オペレーター、攻撃、スキル、敵、防御補正、耐性補正などを
段階的に追加できる構造にする。

このプロジェクトは、ダメージ計算機の制作と同時に、
Python、SQLite、Flask、設計、テスト、Git の学習も目的とする。

---

## 現在の進行状況

現時点では、以下の基礎部分を作成・検討している。

- Flask を使った画面表示
- HTML テンプレートの分割
- 共通 CSS とページ専用 CSS の分離
- SQLite を使ったデータ管理
- CSV から SQLite データベースを作成する仕組み
- operator_master テーブル
- operator_statuses テーブル
- Repository によるデータ取得
- Service による計算処理
- OperatorCondition などの条件データ
- StaticFinalAtkCalculator による最終攻撃力計算
- pytest によるテスト
- Git / GitHub によるプロジェクト管理

---

## 基本方針

最初から完璧な設計を目指さない。

ただし、後から機能を追加しやすいように、
以下の分離を意識する。

- データそのもの
- データ取得処理
- 計算処理
- オペレーターの状態
- 攻撃やスキルの表現
- 画面表示

特に、計算ロジックとデータベース操作は混ぜない。

---

## 優先順位

1. まずは最小限のダメージ計算が正しく動くこと
2. SQLite から必要なデータを取得できること
3. テストで計算結果を確認できること
4. 攻撃・スキル・敵情報を追加しやすくすること
5. UI を使いやすくすること
6. コード全体の整理・命名・設計改善を行うこと

---

## データベース方針

SQL の学習も兼ねるため、データ管理には SQLite を使う。

データベースファイルは data/endfield.db とする。
ただし、endfield.db は生成物なので Git 管理には含めない。

基本的には以下の流れにする。

1. CSV に元データを書く
2. schema.sql にテーブル定義を書く
3. scripts/init_db.py で DB を作り直す
4. Repository から DB の値を取得する

---

## テーブル設計方針

オペレーターごとにテーブルを分けない。

オペレーターの基本情報やステータスは、
全オペレーターを同じテーブルで管理する。

現在の中心テーブルは以下。

- operator_master
- operator_statuses

operator_master は、オペレーターの基本情報を持つ。

例：

- operator_id
- operator_name
- main_stat
- sub_stat

operator_statuses は、レベルごとのステータスを持つ。

例：

- operator_id
- level
- strength
- agility
- intellect
- will
- base_atk

operator_id と level の組み合わせで、
特定のオペレーターの特定レベルのステータスを取得する。

---

## 命名方針

データベースの列名は、意味が分かりやすい名前にする。

例：

- id ではなく operator_id
- name ではなく operator_name
- level は、文脈上オペレーターレベルだと分かる場合は level のままでよい

Repository のメソッド名は、目的によって使い分ける。

- find：条件に合うデータを探す
- get：存在することが前提の値を取得する

ただし、現段階では厳密にしすぎず、
読みやすさと使いやすさを優先する。

---

## フォルダ構成方針

役割ごとにファイルやフォルダを分ける。

主な役割は以下。

- constants：定数
- entities：状態や条件を表すクラス
- repositories：DB からデータを取得するクラス
- services：計算や処理の中心
- templates：HTML
- static：CSS や JavaScript
- scripts：DB 初期化などの補助スクリプト
- tests：テストコード

Repository は DB とのやり取りを担当する。
Service は計算や処理の流れを担当する。
Entity は条件や状態などのデータを表す。

---

## オペレーター設計方針

オペレータークラスは、
すべての処理を自分で持つ巨大なクラスにはしない。

オペレーターは主に以下を持つ。

- operator_id
- level
- base_atk
- 使用可能な攻撃やスキル情報

ただし、ダメージ計算そのものは Service 側に寄せる。

つまり、

「オペレーターが攻撃を実行する」

という考え方は残しつつ、
実際の計算式は Calculator / Service に分離する。

---

## 攻撃・スキル設計方針

今後は、通常攻撃、落下攻撃、終撃、戦技、連携技、必殺技を扱う。

攻撃は 1 段ごとに属性や倍率が違う可能性があるため、
攻撃全体をまとめて 1 つの倍率で表すのではなく、
攻撃段階ごとに表現できる形にする。

例：

- attack_type
- attack_name
- attack_step
- hit_no
- damage_type
- multiplier
- skill_rank

hit_no は、同じ攻撃段階の中で複数ヒットがある場合に使う。
attack_step は、通常攻撃1段目、2段目などの段階を表す。
skill_rank は、ゲーム内のスキルレベル表記に合わせる。

---

## 状態異常・バフ・デバフ方針

今後、battle_skill などが vulnerable や physical vulnerability のような
状態異常・デバフを付与する場合がある。

この場合、攻撃ダメージそのものとは分けて考える。

攻撃には以下の2種類の効果があり得る。

1. ダメージを与える効果
2. 状態異常・バフ・デバフを付与する効果

そのため、将来的には以下のような分離を検討する。

- attack_hits：ダメージ用
- attack_effects：状態異常・バフ・デバフ用

最初から複雑に作りすぎず、
まずはダメージ計算に必要な情報を優先する。

---

## 計算処理方針

計算式は Service または Calculator にまとめる。

現時点では、以下のような役割分担を意識する。

- StaticFinalAtkCalculator：最終攻撃力を計算する
- DamageCalculator：ダメージを計算する
- Repository：必要な数値を DB から取得する
- Condition / Entity：計算条件をまとめる

計算処理の中に SQL を直接書かない。
SQL の取得処理は Repository に任せる。

---

## テスト方針

pytest を使って、計算結果や Repository の動作を確認する。

優先してテストするものは以下。

- operator_id と level から base_atk を取得できるか
- 最終攻撃力が正しく計算されるか
- ダメージ計算結果が期待値と一致するか
- DB 初期化後に必要なデータが存在するか

テストが失敗した場合は、
計算式が間違っているのか、
データ取得が間違っているのか、
期待値が間違っているのかを分けて確認する。

---

## UI 方針

UI は後回しでよい。

まずは計算が正しく動くことを優先する。

ただし、HTML と CSS は以下のように分ける。

- base.html：共通レイアウト
- damage_calculator.html：ダメージ計算ページ
- global.css：全体共通
- base.css：基本レイアウト
- header.css：ヘッダー
- main.css：メイン領域
- sidebar.css：サイドバー
- damage_calculator.css：ダメージ計算ページ専用

ページ専用 CSS は static/pages に置く。

---

## Git / GitHub 方針

GitHub を使って、異なる PC 間でもプロジェクトを共有できるようにする。

Git 管理するもの。

- Python ファイル
- HTML
- CSS
- SQL
- CSV
- tests
- README.md
- requirements.txt

Git 管理しないもの。

- endfield.db
- __pycache__
- .pytest_cache
- 仮想環境
- 個人環境に依存する設定ファイル

endfield.db は scripts/init_db.py で再生成できるようにする。

---

## 今後の実装順

次に進める順番は以下。

1. 現在の DB・Repository・Calculator の整理
2. operator_master / operator_statuses の安定化
3. base_atk と最終攻撃力の計算をテストで固定
4. 攻撃データのテーブル設計
5. 通常攻撃や戦技を 1 段ごとに表現
6. ダメージ計算に攻撃倍率を組み込む
7. 敵の防御・耐性を追加
8. 防御補正・耐性補正を計算に追加
9. 状態異常・バフ・デバフを追加
10. UI から条件を選択できるようにする

---

## 現時点でやりすぎないこと

以下は、今すぐ完璧に作らなくてよい。

- 全オペレーター対応
- 全スキル対応
- 全敵対応
- 複雑なバフ・デバフ管理
- 完璧な UI
- 高度なクラス設計
- 完全なデータベース正規化

まずは、1人のオペレーター、1つの攻撃、1体の敵で、
正しくダメージが出る状態を目指す。

---

## 第2版の結論

このプロジェクトは、
「まず動く最小構成」を作りながら、
少しずつ設計を整理していく。

現時点では、

- DB からデータを取る
- 条件を Entity にまとめる
- 計算を Service / Calculator に分ける
- テストで確認する
- UI は後から整える

という方針で進める。

最終的には、
オペレーター、攻撃、スキル、敵、補正、状態異常を
データとして追加していけるダメージ計算機を目指す。

---

## 重要仕様

ダメージ計算に関する詳細仕様は以下を参照する。

- docs/damage_calculation_spec.md
