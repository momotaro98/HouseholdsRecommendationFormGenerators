import csv
import datetime
import time

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

    ### *** 家庭グループ準備処理 Start *** ###

    # Instanciate HouseholdGroup
    house_group = HouseholdGroup()  # All ModulesUseFlags are True
    for home_id in range(2004, 2156):
        # 各家庭が自家庭のHouseholdインスタンスを持つ
        house = Household(home_id)
        house_group.append(house)

    ### *** 家庭グループ準備処理 End *** ###

    elapsed_time_dict = {}

    ###=== FormGeneratorアプリケーション 実行フェーズ Start ===###

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
