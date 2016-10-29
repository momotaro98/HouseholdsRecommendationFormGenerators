import csv
import datetime

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
    for home_id in range(2008, 2009):
        house = Household(home_id)
        house_group.append(house)

    ### *** 家庭グループ準備処理 End *** ###

    ###=== FormGeneratorアプリケーション 実行フェーズ Start ===###

    ###+++ Non Switching Case Start +++###
    # switch flags phase
    for house in house_group.get_iter():
        sw_fs = UseFlagSwitcher(house)
        sw_fs.run()  # Do Nothing
    # generate form phase
    for house in house_group.get_iter():
        start_time = datetime.datetime(2015, 8, 1)
        end_time = datetime.datetime(2015, 8, 7)
        form_generator = FormGenerator(
            house, start_time=start_time, end_time=end_time
        )
        print("home_id", house.id)
        form_generator.run()
    # reset flags phase
    for house in house_group.get_iter():
        fs = UseFlagSwitcher(house)
        fs.reset()
    ###+++ Non Switching Case End +++###

    """
    ###+++ Classification Tree Way Case Start +++###
    # switch flags phase
    for house in house_group.get_iter():
        sw_fs = ClassificationTreeWayUseFlagSwitcher(house)
        sw_fs.run()
    # generate form phase
    for house in house_group.get_iter():
        timeframe = 'from 2016-08-01 to 2016-08-07'
        form_generator = FormGenerator(house, timeframe)
        print("home_id", house.id)
        form_generator.run()
    # reset flags phase
    for house in house_group.get_iter():
        fs = UseFlagSwitcher(house)
        fs.reset()
    ###+++ Classification Tree Way Case End +++###
    """

    ###=== FormGeneratorアプリケーション 実行フェーズ End ===###
