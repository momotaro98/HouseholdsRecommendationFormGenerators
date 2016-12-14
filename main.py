import csv
import datetime
import time
import random

from household_recommendation_form_generators import *


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
    musako_homes_id = [
        2004, 2010, 2011, 2012, 2014, 2017, 2018, 2019, 2020, 2021,
        2023, 2025, 2027, 2030, 2047, 2048, 2053, 2054, 2059, 2070,
        2071, 2073, 2079, 2082, 2087, 2088, 2096, 2099, 2104, 2105,
        2106, 2112, 2113, 2114, 2115, 2116, 2117, 2118, 2121, 2122,
        2123, 2124, 2126, 2129, 2130, 2131, 2137, 2150, 2151, 2152,
    ]  # 50件
    # momotaro_homes_id = [1, 8, 9, 10, 11]
    # homes_id = momotaro_homes_id + musako_homes_id
    homes_id = musako_homes_id

    # ひとまずランダムにクラスタ作成
    # TODO: metaデータを用いてk-meansクラスタリング処理
    random.shuffle(homes_id)  # homes_idに対する破壊的処理
    homes_id_sliced = homes_id[:10]  # とりあえず10家庭のクラスタ
    # house_groupはランダムに家庭10件分
    house_group = HouseholdGroup()  # All ModulesUseFlags are True
    # for home_id in homes_id_sliced:
    for home_id in homes_id:
    # for home_id in musako_homes_id:
        # 各家庭が自家庭のHouseholdインスタンスを持つ
        house = Household(home_id)
        house_group.append(house)
    # *** 家庭グループ準備処理 End ***

    """
    exist_homes = []
    empty_homes = []
    for house in house_group.get_iter():
        ac12 = house.get_ac_log(
            start_time=datetime.datetime(2015, 12, 1),
            end_time=datetime.datetime(2016, 12, 31)
        )
        aclist12 = list(ac12.get_rows_iter())
        ac01 = house.get_ac_log(
            start_time=datetime.datetime(2016, 1, 1),
            end_time=datetime.datetime(2016, 1, 31)
        )
        aclist02 = list(ac01.get_rows_iter())
        if aclist12 and aclist02:
            exist_homes.append(house.id)
        else:
            empty_homes.append(house.id)
    print('exist_homes', exist_homes)
    print('empty_homes', empty_homes)
    """

    '''
    # test DecisionTreeSwitcherForHomeCluster
    dts = DecisionTreeSwitcherForHomeCluster(house_group)
    t_list = dts.ret_ac_logs_list()
    for row in t_list:
        print('row.timestamp', row.timestamp)
    '''

    """
    ###=== FormGeneratorアプリケーション 実行フェーズ Start ===###

    elapsed_time_dict = {}

    ###+++ Non Switching Case Start +++###
    # generate form phase
    start = time.time()
    for house in house_group.get_iter():
        # 以下の処理は各家庭のコンピュータが行う
        start_time = datetime.datetime(2015, 8, 1)
        end_time = datetime.datetime(2015, 9, 7)
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
        start_time = datetime.datetime(2015, 8, 1)
        end_time = datetime.datetime(2015, 9, 7)
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
