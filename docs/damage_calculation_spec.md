Endfield Damage Calculator - Codex用ダメージ仕様メモ
作成日: 2026-05-12
対象プロジェクト: endfield_damage_calculator
目的: Codex/AIに渡して、ダメージ計算ロジック・DB設計・テスト実装の前提にするための仕様メモ。

重要:
- アークナイツ: エンドフィールドのダメージ式は、少なくとも調査時点では公式が完全な計算式を公開しているわけではない。
- このファイルは、公式情報ではなく、有志Wiki・検証記事・コミュニティ検証を照合した「実装用の暫定仕様」である。
- ゲーム更新で仕様が変わる可能性があるため、式・係数・端数処理はテストしやすい形に分離して実装する。
- 不明なものは推測で埋めず、unknown / TODO / need_verification として扱う。

============================================================
1. 実装対象の優先順位
============================================================

最初に実装する:
1. 通常の攻撃ヒット1発のダメージ
2. final_atk の計算
3. skill_multiplier / hit_multiplier の適用
4. defense_coef = 0.5 の適用
5. resistance_coef の適用
6. critical_coef の適用
7. damage_bonus / damage_taken / susceptibility / break の係数を、値があれば適用できる構造にする

後で実装する:
1. vulnerability stack を使う物理状態異常
2. Lift / Knock Down / Crush / Breach
3. Arts Infliction / Arts Burst / Arts Reaction
4. Combustion / Corrosion / Electrification / Solidification / Shatter
5. 持続時間、スタック、消費、再付与
6. 複数オペレーター・複数敵・時系列シミュレーション

============================================================
2. 用語
============================================================

damage:
- 画面に表示される最終ダメージ。
- 最終的に四捨五入されるとされる。
- 実装では途中計算はfloatまたはDecimalで保持し、最後にroundする。

hit:
- 攻撃1ヒット。
- 1つの攻撃モーションに複数ヒットがある場合は、hit_noで分ける。
- ダメージ計算の基本単位。

attack_type:
- basic_attack
- final_strike
- dive_attack
- battle_skill
- combo_skill
- ultimate

damage_type / attribute:
- physical
- heat
- electric
- cryo
- nature
- aether
- arts は heat/electric/cryo/nature の総称として扱う。
- physical は arts reaction とは基本的に別系統。

operator_condition:
- operator_id
- level
- skill_rank
- weapon_id / weapon_rank など、将来拡張する条件をまとめる。

enemy_condition:
- enemy_id
- resistance values
- current statuses
- break state
- まだ未実装でも、将来追加しやすいように分ける。

============================================================
3. 通常ヒットの基本ダメージ式
============================================================

暫定式:

raw_damage =
    final_atk
    * hit_multiplier
    * critical_coef
    * damage_bonus_coef
    * amp_coef
    * link_coef
    * defense_coef
    * resistance_coef
    * damage_taken_coef
    * susceptibility_coef
    * break_coef

display_damage = round(raw_damage)

注意:
- hit_multiplier はゲーム内の「攻撃力xxx%」を小数に変換したもの。
  例: 150% -> 1.5
- 各係数は未適用なら 1.0。
- defense_coef は現時点では通常 0.5 を初期値にする。
- final_atk と hit_multiplier 以外は、最初は省略可能にしてよい。
- ただし、引数やデータ構造は後から足せるようにする。

Python実装イメージ:

def calculate_hit_damage(params):
    raw_damage = (
        params.final_atk
        * params.hit_multiplier
        * params.critical_coef
        * params.damage_bonus_coef
        * params.amp_coef
        * params.link_coef
        * params.defense_coef
        * params.resistance_coef
        * params.damage_taken_coef
        * params.susceptibility_coef
        * params.break_coef
    )
    return round(raw_damage)

============================================================
4. final_atk の計算
============================================================

暫定式:

base_total_atk = operator_base_atk + weapon_base_atk

ability_bonus_coef =
    1
    + main_attribute_value * 0.005
    + sub_attribute_value * 0.002

final_atk =
    (
        base_total_atk * (1 + atk_percent_bonus_sum)
        + flat_atk_bonus_sum
    )
    * ability_bonus_coef

用語:
- operator_base_atk: オペレーター自身の基礎攻撃力
- weapon_base_atk: 武器の基礎攻撃力
- atk_percent_bonus_sum: 攻撃力+n% 系の合計。20%なら0.20。
- flat_atk_bonus_sum: 攻撃力+数値 系の合計。
- main_attribute_value: そのオペレーターのメイン能力値。
- sub_attribute_value: そのオペレーターのサブ能力値。
- メイン能力値は1点につき攻撃力+0.5%。
- サブ能力値は1点につき攻撃力+0.2%。

現在のプロジェクトでは、まず以下だけでよい:
- weapon_base_atk = 0
- atk_percent_bonus_sum = 0
- flat_atk_bonus_sum = 0
- operator_base_atk, main_attribute_value, sub_attribute_value はDBから取得

============================================================
5. 会心係数
============================================================

実ダメージ:
- 会心しない: critical_coef = 1.0
- 会心する: critical_coef = 1 + critical_damage_rate

期待値:
expected_critical_coef =
    1 + critical_rate * critical_damage_rate

例:
- critical_rate = 0.15
- critical_damage_rate = 0.50
- expected_critical_coef = 1 + 0.15 * 0.50 = 1.075

注意:
- critical_rate と critical_damage_rate は小数で扱う。
- 50%なら0.50。
- UIでは「会心する/しない/期待値」を選べるようにするとよい。

============================================================
6. 与ダメージ係数 damage_bonus_coef
============================================================

暫定式:

damage_bonus_coef = 1 + damage_bonus_sum

damage_bonus_sum に入る候補:
- all_damage_bonus
- physical_damage_bonus
- heat_damage_bonus
- electric_damage_bonus
- cryo_damage_bonus
- nature_damage_bonus
- battle_skill_damage_bonus
- ultimate_damage_bonus
- basic_attack_damage_bonus
- final_strike_damage_bonus

実装方針:
- まずは全て同じ damage_bonus_sum に加算してよい。
- ただし、将来的にカテゴリが違う可能性に備えて、source_type / bonus_category をDBに持たせる。
- 「与えるダメージ+n%」のような味方側バフはこの係数に入れる。

============================================================
7. Amp係数 amp_coef
============================================================

暫定式:

amp_coef = 1 + amp_sum

候補:
- arts_amp
- physical_amp
- heat_amp
- electric_amp
- cryo_amp
- nature_amp
- battle_skill_amp など

注意:
- Amp は「与ダメージアップ」と別カテゴリとして扱う。
- 同じ種類は加算、別カテゴリかどうかは要検証。
- 最初の実装では amp_coef = 1.0 固定でよい。

============================================================
8. Link係数 link_coef
============================================================

暫定値:
- battle_skill に Link が乗る場合: link_coef = 1.3
- ultimate に Link が乗る場合: link_coef = 1.2
- それ以外: link_coef = 1.0

注意:
- Link は「編成全体で次に発動する戦技または必殺技を強化する」系のバフ。
- 同種スタックや減衰の仕様は未実装でよい。
- 最初は link_active: bool と attack_type で係数を決める。

============================================================
9. 防御係数 defense_coef
============================================================

現時点の暫定:
- オペレーターが敵を攻撃する場合、defense_coef = 0.5 とする。

注意:
- これは「敵の防御力を使った式」ではなく、有志検証で見つかっている固定補正に近い扱い。
- 実態は不明。
- 敵レベル・味方レベルによるレベル差補正は確認されていないという報告がある。
- 将来の仕様変更に備え、固定値をコードに直書きせず、定数または設定値にする。

実装例:
DEFAULT_ENEMY_DEFENSE_COEF = 0.5

============================================================
10. 耐性係数 resistance_coef
============================================================

暫定式:

final_resistance = base_resistance - resistance_down - resistance_ignore

resistance_coef = (100 - final_resistance) / 100

小数で書くなら:

resistance_coef = 1 - final_resistance / 100

例:
- base_resistance = 20
- resistance_down = 0
- resistance_ignore = 0
- resistance_coef = 0.8

例:
- base_resistance = 0
- resistance_down = 20
- resistance_ignore = 0
- final_resistance = -20
- resistance_coef = 1.2

敵の耐性ランクの暫定対応:
- D: 0
- C: 20
- B: 50

注意:
- Aランクなど未確認のものは unknown として扱う。
- 元耐性0に対しても耐性ダウンや耐性無視は有効とする。
- negative resistance は許可する。
- 上限/下限のclampは未確認なので、最初は行わない。
- ただし、将来的に clamp_resistance オプションを追加できるようにする。

============================================================
11. 被ダメージ係数 damage_taken_coef
============================================================

暫定式:

damage_taken_coef = 1 + damage_taken_debuff_sum

対象:
- 敵に付く「受けるダメージ+n%」系デバフ
- 受けるアーツダメージ+n%
- 受ける物理ダメージ+n%
- 受ける特定属性ダメージ+n%

注意:
- 味方側の「与えるダメージ+n%」とは別カテゴリ。
- damage_bonus_coef と damage_taken_coef は乗算で分ける。

============================================================
12. Susceptibility / 脆弱係数
============================================================

暫定式:

susceptibility_coef = 1 + susceptibility_sum

対象:
- Physical Susceptibility
- Arts Susceptibility
- Heat Susceptibility
- Electric Susceptibility
- Cryo Susceptibility
- Nature Susceptibility

注意:
- 英語圏情報では Susceptibility と呼ばれることが多い。
- 日本語では「物理脆弱」「アーツ脆弱」のように表現されることがある。
- 後述の Vulnerable stack とは別物として扱うこと。
- この2つを混同しないことが重要。

============================================================
13. Vulnerable stack
============================================================

Vulnerable stack は、物理状態異常のためのスタック。

性質:
- 最大4スタックとされる。
- Lift / Knock Down はVulnerableを付与または追加する。
- Crush / Breach はVulnerable stackを消費する。
- 通常のダメージ係数として常に乗算するものではない。
- Physical Susceptibilityとは別物。

実装上の名前:
- vulnerable_stack_count
- max_vulnerable_stack = 4

DBに入れる場合:
- effect_type = "vulnerable_stack"
- stack_change = +1
- max_stack = 4
- duration_sec = TODO
- consumes_stack = false

============================================================
14. 物理状態異常
============================================================

物理状態異常:
- Lift
- Knock Down
- Crush
- Breach

共通:
- 初回の物理状態異常付与は、実際の状態異常ではなくVulnerableを付与する場合がある。
- すでにVulnerableがある敵に対して、Lift / Knock Down はスタックを追加し、物理ダメージとStaggerを与える。
- すでにVulnerableがある敵に対して、Crush / Breach はスタックを消費して物理ダメージを与える。
- Breach はさらに Physical Damage Taken Increase / Physical Susceptibility 相当のデバフを付与する。

------------------------------------------------------------
14.1 Lift / Knock Down
------------------------------------------------------------

暫定倍率式:

lift_or_knock_down_multiplier_percent =
    120 * (1 + (operator_level - 1) / 392)

Lv90では約147%。

効果:
- Vulnerableを1スタック付与/追加。
- 敵がすでにVulnerableなら物理ダメージを与える。
- Staggerを10付与するという報告がある。

注意:
- 敵が浮遊/転倒できない場合でも、ダメージとStaggerは入るという報告がある。

------------------------------------------------------------
14.2 Crush
------------------------------------------------------------

暫定倍率式:

base_multiplier_percent =
    150 * (1 + (operator_level - 1) / 392)

final_multiplier_percent =
    base_multiplier_percent * (1 + consumed_vulnerable_stack_count)

Lv90目安:
- 1 stack: 約368%
- 2 stacks: 約552%
- 3 stacks: 約736%
- 4 stacks: 約920%

効果:
- Vulnerable stack がない場合はVulnerableを付与する。
- Vulnerable stack がある場合は全消費し、消費数に応じた物理ダメージを与える。
- Physical Susceptibility系デバフは基本的には付けない扱い。

------------------------------------------------------------
14.3 Breach
------------------------------------------------------------

暫定倍率式:

base_multiplier_percent =
    50 * (1 + (operator_level - 1) / 392)

final_multiplier_percent =
    base_multiplier_percent * (1 + consumed_vulnerable_stack_count)

Lv90目安:
- 1 stack: 約123%
- 2 stacks: 約184%
- 3 stacks: 約245%
- 4 stacks: 約307%

Breachの物理被ダメージ増加デバフ:

physical_damage_taken_increase_percent =
    4 * (2 + consumed_vulnerable_stack_count)

目安:
- 1 stack: 12%
- 2 stacks: 16%
- 3 stacks: 20%
- 4 stacks: 24%

持続時間の目安:
- 1 stack: 12 sec
- 2 stacks: 18 sec
- 3 stacks: 24 sec
- 4 stacks: 30 sec

注意:
- 持続時間はソース間で要確認。
- damage_taken_coef か susceptibility_coef のどちらに入れるかは、ゲーム内表記に合わせて決める。
- 実装上は effect_type = "physical_damage_taken_increase" としておくと安全。

============================================================
15. Arts Infliction / Arts Burst / Arts Reaction
============================================================

初期実装では未対応でよい。
ただし、設計だけは分離しておく。

Arts属性:
- heat
- electric
- cryo
- nature

Arts Infliction:
- 敵に付くArts系スタック。
- 同じ属性は最大4スタックとされる。
- 同じ属性を再付与するとArts Burstが発生し、同属性のスタックが増える。
- 異なる属性を付与するとArts Reactionが発生する。
- 反応の種類は「2番目に付与した属性」で決まるとされる。

------------------------------------------------------------
15.1 Arts Burst
------------------------------------------------------------

同じArts Inflictionを重ねると発生。

例:
- Heat Infliction + Heat Infliction = Heat Burst
- Electric Infliction + Electric Infliction = Electric Burst
- Cryo Infliction + Cryo Infliction = Cryo Burst
- Nature Infliction + Nature Infliction = Nature Burst

効果:
- 1スタック追加。
- 対応属性のArtsダメージを与える。

Lv90目安:
- Arts Burst: 約233% ATK

注意:
- Arts Burst / Reactionのダメージには、Arts Intensityが関係するという報告がある。
- 通常ヒットのskill_multiplier計算とは別の「状態異常ダメージ」として扱う。

------------------------------------------------------------
15.2 Arts Reaction
------------------------------------------------------------

異なるArts Inflictionを組み合わせると発生。
反応は2番目の属性で決まる。

2番目がHeat:
- Combustion
- 初期Heatダメージ + DoT

2番目がElectric:
- Electrification
- Electricダメージ + Arts DMG Taken Increase

2番目がCryo:
- Solidification
- Cryoダメージ + 凍結/拘束
- Solidification中にVulnerableまたは物理状態異常を入れるとShatter

2番目がNature:
- Corrosion
- Natureダメージ + 敵全属性耐性低下

Lv90目安:
infliction_stack_countごとのReaction倍率:
- 1 stack: 約233%
- 2 stacks: 約349%
- 3 stacks: 約465%
- 4 stacks: 約582%

ElectrificationのArts被ダメージ増加目安:
- 1 stack: 12%, 12 sec
- 2 stacks: 16%, 18 sec
- 3 stacks: 20%, 24 sec
- 4 stacks: 24%, 30 sec

Corrosionの最大耐性低下目安:
- 1 stack: -12%, 15 sec
- 2 stacks: -16%, 15 sec
- 3 stacks: -20%, 15 sec
- 4 stacks: -24%, 15 sec

注意:
- Arts Reactionの正確な端数・Arts Intensityの掛かり方は後回し。
- まずは effect table に表現できるようにするだけでよい。

============================================================
16. Break係数
============================================================

暫定:
- break_coef = 1.3
- Break中の敵にかかる補正。

注意:
- どのダメージ種別に乗るか、全てに乗るかは要検証。
- 最初は bool enemy_is_broken で 1.3 / 1.0 を切り替える。

============================================================
17. 端数処理
============================================================

暫定:
- ダメージ計算途中は生の値で計算する。
- 最後の表示ダメージだけ四捨五入する。

display_damage = round(raw_damage)

注意:
- Pythonのroundは銀行丸めになる場合がある。
- ゲーム内の四捨五入が「0.5以上切り上げ」なら、Decimal + ROUND_HALF_UP を使う方が安全。

Python例:

from decimal import Decimal, ROUND_HALF_UP

def round_damage(value: float) -> int:
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

能力値・装備・表示値の端数:
- 武器や防具の表示値には、内部的な小数が隠れている場合がある。
- 能力値、アーツ強度、%系ステータスで丸め方が異なるという検証がある。
- 初期実装では、DBに入れた値を正として使う。
- 端数の完全再現は後回し。

============================================================
18. DB設計方針
============================================================

現在のプロジェクトに合わせる。

------------------------------------------------------------
18.1 operator_master
------------------------------------------------------------

目的:
- オペレーターの基本情報を持つ。

候補列:
- operator_id
- operator_name
- rarity
- class_name
- main_attribute
- sub_attribute
- default_damage_type

------------------------------------------------------------
18.2 operator_statuses
------------------------------------------------------------

目的:
- レベルごとの基礎ステータスを持つ。

候補列:
- operator_id
- level
- base_atk
- strength
- agility
- intellect
- will
- arts_intensity
- crit_rate
- crit_damage

注意:
- crit_rate/crit_damageは後回しでもよい。
- arts_intensityも後回しでよい。

------------------------------------------------------------
18.3 operator_attack_hits
------------------------------------------------------------

目的:
- 攻撃1ヒットごとのダメージ情報を持つ。

候補列:
- operator_id
- attack_type
- attack_name
- attack_step
- hit_no
- skill_rank
- damage_type
- attack_attribute
- multiplier_percent
- stagger_value
- is_final_strike
- can_crit
- note

例:
- operator_id = "lifeng"
- attack_type = "basic_attack"
- attack_step = 1
- hit_no = 1
- damage_type = "physical"
- multiplier_percent = 80

------------------------------------------------------------
18.4 operator_attack_effects
------------------------------------------------------------

目的:
- ダメージ以外の効果を持つ。
- 状態異常、バフ、デバフ、スタック付与、スタック消費を表現する。

候補列:
- operator_id
- attack_type
- attack_name
- attack_step
- hit_no
- skill_rank
- effect_type
- effect_attribute
- effect_value
- value_unit
- duration_sec
- stack_change
- max_stack
- consume_stack_type
- consume_stack_count
- trigger_condition
- target
- note

effect_type候補:
- vulnerable_stack
- physical_susceptibility
- arts_susceptibility
- heat_susceptibility
- electric_susceptibility
- cryo_susceptibility
- nature_susceptibility
- damage_taken_increase
- physical_damage_taken_increase
- arts_damage_taken_increase
- resistance_down
- link
- amp
- break
- lift
- knock_down
- crush
- breach
- arts_infliction
- combustion
- corrosion
- electrification
- solidification
- shatter

value_unit候補:
- percent
- coefficient
- stack
- flat
- seconds
- boolean

target候補:
- self
- party
- enemy
- all_enemies

============================================================
19. Repository / Service 方針
============================================================

Repository:
- DBから値を取るだけ。
- 計算しない。
- SQLをServiceに書かない。

Service / Calculator:
- 計算する。
- DBの詳細を知らない。
- 引数はEntity/DTOで受け取る。

推奨クラス:
- StaticFinalAtkCalculator
- DamageCalculator
- ResistanceCalculator
- CriticalCalculator
- EffectResolver
- AttackExecutor

最初に必要:
- StaticFinalAtkCalculator.get_final_atk(condition)
- DamageCalculator.calculate_hit_damage(params)

============================================================
20. テスト方針
============================================================

最初に固定するテスト:
1. final_atk計算
2. multiplierだけのダメージ
3. defense_coef=0.5のダメージ
4. resistance_coefのダメージ
5. round_damageの四捨五入
6. operator_attack_hits_repositoryでヒット情報が取得できること

例:

base_atk = 100
main_attribute = 20
sub_attribute = 10

ability_bonus_coef = 1 + 20*0.005 + 10*0.002 = 1.12
final_atk = 100 * 1.12 = 112

hit_multiplier = 2.0
defense_coef = 0.5
resistance_coef = 1.0

raw_damage = 112 * 2.0 * 0.5 = 112
display_damage = 112

============================================================
21. 実装上の注意
============================================================

- パーセントはDBに 150 のように入れて、計算時に /100 してもよい。
- ただし、コード内では decimal rate に統一する。
  - 150% -> 1.5
  - 20% -> 0.20
- 「倍率」と「補正」は名前を分ける。
  - multiplier_percent: スキル倍率・ヒット倍率
  - coef: 乗算係数
  - rate: パーセントを小数化した値
- Vulnerable stack と Susceptibility を混同しない。
- battle_skillが状態異常だけを与える場合に備え、hitとeffectは別テーブルにする。
- 1つの攻撃が「ダメージ + 状態異常」を持つ場合、operator_attack_hitsとoperator_attack_effectsの両方に行を持つ。
- 1つの攻撃が状態異常だけなら、operator_attack_effectsだけでよい。

============================================================
22. 現時点の未確定事項
============================================================

未確定:
- 防御係数0.5の正体。
- 敵のAランク耐性など全ランク対応表。
- 各種係数の完全なカテゴリ分け。
- 同種バフのスタックルール。
- Linkの複数スタック時の減衰。
- Arts Intensityの正確な計算位置。
- Arts Burst / Arts Reactionの正確な端数処理。
- 能力値の内部小数と丸め。
- PythonのROUND_HALF_UPでゲーム内表示を完全再現できるか。

実装方針:
- 未確定値は設定ファイル・定数・DBで差し替え可能にする。
- テストで仮説を固定し、あとで仕様変更しやすくする。

============================================================
23. 参照した主な情報源
============================================================

1. Endfield Talos Wiki / Damage calculation
   https://endfield.wiki.gg/wiki/Damage_calculation
   備考: web取得時に403で本文取得不可。ただし検索結果上で存在を確認。

2. 針金「エンドフィールド 推定ダメージ計算式」
   https://note.com/ujaio/n/n625fc936ba1c
   備考: 基本式、final_atk、会心、与ダメージ、Link、防御係数、耐性、被ダメージ、脆弱、Breakの参考。

3. 針金「エンドフィールド 猛撃／破砕／浮遊／転倒のダメージ倍率」
   https://note.com/ujaio/n/n8170abdb0e6a
   備考: Lift/Knock Down/Crush/Breach相当の倍率、消費スタック、Breach系デバフの参考。

4. AT-Stasis「ダメージ計算に関わる小数と端数処理 - アークナイツ：エンドフィールド」
   https://note.com/at67275/n/n7b62db8a57a2
   備考: 表示値、端数、ダメージ表示の四捨五入、途中計算の扱いの参考。

5. Mobalytics "Arknights: Endfield Keywords & Effects Explained"
   https://mobalytics.gg/arknights-endfield/guides/keywords-effects
   備考: 用語、Vulnerable、Lift、Knock Down、Crush、Breach、Arts Infliction、Reactionの参考。

6. Mobalytics "Arknights: Endfield Effects & Status"
   https://mobalytics.gg/arknights-endfield/profile/mattjestic-multigaming/guides/arknights-endfield-effects-and-status
   備考: Susceptibility、Arts/Physical Status、各属性付着の参考。

7. Prydwen "Arknights: Endfield Elements & Reactions"
   https://www.prydwen.gg/arknights-endfield/guides/elements-and-reactions/
   備考: Physical/Artsの分離、Vulnerable stack、物理状態異常、Arts Reaction、Lv90倍率表の参考。

8. GameWith「アーツ異常と物理異常の起こし方と効果」
   https://gamewith.jp/akendfield/540393
   備考: 日本語でのArts異常・物理異常の概念確認。

============================================================
24. Codexへの作業指示
============================================================

この仕様を使って実装する場合、Codexは以下を守ること。

1. いきなり全仕様を実装しない。
2. まず通常ヒット1発の計算を通す。
3. RepositoryとCalculatorを混ぜない。
4. DBの行は辞書ではなく、必要ならEntity/dataclassに変換する。
5. 既存のoperator_attack_hits.csv / operator_attack_effects.csvの役割を崩さない。
6. 未確定の係数は定数化する。
7. 仕様が不明な部分はTODOコメントを残す。
8. テストを先に追加または同時に追加する。
9. 既存テストを壊さない。
10. 変更後は pytest が通ることを確認する。

以上。
