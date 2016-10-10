import csv
import datetime

from household_recommendation_form_generators import *


if __name__ == "__main__":
    '''
    # アプリケーション側(FormGenerator側)が利用する家庭群を用意する処理
    # を始めに行う必要がある

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
    '''

    ### *** *** ### 家庭グループ準備処理 Start

    # Instanciate HouseholdGroup
    house_group = HouseholdGroup()
    for home_id in range(1001, 4000):
        house = Household(home_id)
        house_group.append(house)

    ### *** *** ### 家庭グループ準備処理 End

    # アプリケーション側
    for house in house_group.get_iter():
        the_house_ac_log = house.get_ac_log()  # DataRowsはHouseholdインスタンスから取得する
        duration = '2016-08-01'
        print("house.id: ", house.id)
        for row in the_house_ac_log.get_rows_iter(duration=duration):
            print(row.timestamp, row.on_off)
        # アプリケーション側はそのhouseインスタンスの家庭の指定の期間のデータが欲しい(durationのこと)

    # FormGeneratorアプリケーション 実行フェーズ開始

    # instanciate EachHomeWayFormGemerator
    # ehw_fg = EachHomeWayFormGemerator(house_group)
    # run EachHomeWayFormGemerator instance
    # ehw_fg.run()

    # instanciate ClusteringWayFormGenerator
    # cw_fg = ClusteringWayFormGenerator(house_group)
    # run ClusteringWayFormGenerator instance
    # cw_fg.run()

    # instanciate ClassificationTreeWayFormGenerator
    # ctw_fg = ClassificationTreeWayFormGenerator(house_group)
    # run ClassificationTreeWayFormGenerator instance
    # ctw_fg.run()
