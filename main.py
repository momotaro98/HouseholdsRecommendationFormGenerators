import csv
from datetime import datetime
from datetime import timedelta
import time
import random

from household_recommendation_form_generators import *


def eval03(act_y_list, pred_y_list):
    '''
    F値などで評価する必要がある
    '''
    if len(act_y_list) != len(pred_y_list):
        raise Exception('act_y_list and pred_y_list len must be same.')
    print('act_y_list', act_y_list)
    print('pre_y_list', pred_y_list)


def eval02(house_group):
    # 家庭クラスタの決定木モデルから得られる2016年冬時期のY予測値
    start_dt = datetime(2016, 12, 1, 0, 0, 0)
    end_dt = datetime(2016, 12, 14, 23, 59, 59)
    pred_y_list = []
    s_dt = start_dt
    while s_dt <= end_dt:
        # TotalUsage
        # tu_pred_Y = IsTotalUsage(house_group).ret_pred_Y(s_dt.date())
        # pred_y_list.append(tu_pred_Y)
        # print('tu_pred_Y', tu_pred_Y)

        # ChangeUsage
        cu_pred_Y = IsChangeUsage(house_group).ret_pred_Y(s_dt.date())
        pred_y_list.append(cu_pred_Y)
        # print('cu_pred_Y', cu_pred_Y)

        s_dt += timedelta(days=1)

    # 実験家庭から得られる2016年冬時期のY実際値
    ehy = ExperimentHomesYact(
        home_id=9,
        start_train_dt=start_dt,
        end_train_dt=end_dt,
    )
    # TotalUsage
    act_y_list = [ay[1] for ay in ehy.ret_TU_act_Y_list()]
    # ChangeUsage
    # act_y_list = [ay[1] for ay in ehy.ret_CU_act_Y_list()]

    # TODO: r_dは真偽におけるF値で評価する必要がある
    eval03(act_y_list, pred_y_list)


def eval01(homes_id_list, number_of_houses):
    # クラスタごとの計算結果を得る評価
    homes_id_sliced = homes_id_list[:number_of_houses]  # とりあえず10家庭のクラスタ
    # house_groupはランダムに家庭10件分
    house_group = HouseholdGroup()  # All ModulesUseFlags are True
    for home_id in homes_id_sliced:
    # for home_id in homes_id_list:
    # for home_id in musako_homes_id_list:
        # 各家庭が自家庭のHouseholdインスタンスを持つ
        house = Household(home_id)
        house_group.append(house)

    start = time.time()
    cu_pred_Y = IsChangeUsage(house_group).ret_pred_Y()
    tu_pred_Y = IsTotalUsage(house_group).ret_pred_Y()
    # print('pred_Y', pred_Y)
    end = time.time()
    elapsed_time = end - start
    print('number_of_houses', number_of_houses)
    print('elapsed_time', elapsed_time)

    # レコメンド品質を検証する評価
    print('=' * 79)
    eval02(house_group)


if __name__ == "__main__":
    """
    # アプリケーション側(FormGenerator側)が利用する家庭群を
    # 用意する処理を始めに行う必要がある

    # 前処理段階ではデータを格納しない
    # アプリケーションが必要なときにデータを得られるようにする
    # 家庭番号(user_id)とデータ期間(timestamp)のみが必要(のはず)
    # 家庭番号はHouseholdインスタンスが持つ各DataRows型のインスタンスが保持する
    # 期間はアプリケーション側が指定する

    # 研究における家庭番号割り当てについて

    栗原 家庭
    1000番台を割り当てる
    実際数 1001〜1016

    武蔵小杉 家庭
    2000番台を割り当てる
    実際数 2001〜2160

    池田実験協力家庭
    3000番台を割り当てる
    実際数 3001〜3005
    """

    # *** 家庭グループ準備処理 Start ***

    # Instanciate HouseholdGroup
    musako_homes_id_list = [
        2004, 2010, 2011, 2012, 2014, 2017, 2018, 2019, 2020, 2021,
        2023, 2025, 2027, 2030, 2047, 2048, 2053, 2054, 2059, 2070,
        2071, 2073, 2079, 2082, 2087, 2088, 2096, 2099, 2104, 2105,
        2106, 2112, 2113, 2114, 2115, 2116, 2117, 2118, 2121, 2122,
        2123, 2124, 2126, 2129, 2130, 2131, 2137, 2150, 2151, 2152,
    ]  # 50件
    # momotaro_homes_id_list = [1, 8, 9, 10, 11]
    # homes_id_list = momotaro_homes_id_list + musako_homes_id_list
    homes_id_list = musako_homes_id_list

    # ひとまずランダムにクラスタ作成
    # TODO: metaデータを用いてk-meansクラスタリング処理
    random.shuffle(homes_id_list)  # homes_id_listに対する破壊的処理

    # *** 家庭グループ準備処理 End ***

    # eval01(homes_id_list, number_of_houses=1)
    # eval01(homes_id_list, number_of_houses=5)
    eval01(homes_id_list, number_of_houses=10)
    # eval01(homes_id_list, number_of_houses=20)
    # eval01(homes_id_list, number_of_houses=30)
    # eval01(homes_id_list, number_of_houses=40)
    # eval01(homes_id_list, number_of_houses=50)




    """
    ###=== FormGeneratorアプリケーション 実行フェーズ Start ===###

    elapsed_time_dict = {}

    ###+++ Non Switching Case Start +++###
    # generate form phase
    start = time.time()
    for house in house_group.get_iter():
        # 以下の処理は各家庭のコンピュータが行う
        start_time = datetime(2015, 8, 1)
        end_time = datetime(2015, 9, 7)
        form_generator = FormGenerator(
            house, start_time=start_time, end_time=end_time
        )
        print("home_id", house.id)
        form_generator.run()
    end = time.time()
    elapsed_time_dict['Non Switching'] = end - start
    ###+++ Non Switching Case End +++###


    ###+++ Switching Case Start +++###
    # switch flags phase
    # この処理はサーバ側で実行される
    for house in house_group.get_iter():
        sw_fs = UseFlagSwitcher(house)
        sw_fs.run()  # Switching

    # generate form phase
    start = time.time()
    for house in house_group.get_iter():
        start_time = datetime(2015, 8, 1)
        end_time = datetime(2015, 9, 7)
        form_generator = FormGenerator(
            house, start_time=start_time, end_time=end_time
        )
        print("home_id", house.id)
        form_generator.run()
    end = time.time()
    elapsed_time_dict['Switching'] = end - start

    # reset flags phase
    for house in house_group.get_iter():
        fs = UseFlagSwitcher(house)
        fs.reset()
    ###+++ Non Switching Case End +++###

    ###=== FormGeneratorアプリケーション 実行フェーズ End ===###


    # 各場合の計算時間を表示
    print(elapsed_time_dict)
    """
