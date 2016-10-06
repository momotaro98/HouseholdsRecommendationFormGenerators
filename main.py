import csv

from household_recommendation_form_generators import *


if __name__ == "__main__":
    CSVFILE_PATH = 'test.csv'

    # 始めにレコメンドレポートを発行する家庭群を用意する

    # a. DB, CSVファイル等からDataFormatを用意して
    # b. 家庭ごとにHousehold型へ入れ込む
    # c. そのHousehold型の複数のインスタンス達を
    # c. HouseholdIteratorへ突っ込む

    # a. DataFormatの用意
    # とりあえずすぐに用意できるACLogDataFormatを利用する
    # とりあえずCSVファイルから取り出す DBから取り出す場合もある
    # TODO: 家庭1つ分しかないのでなんとかする
    # TODO: このデータを入れ込むのが大変

    # Instanciate HouseholdGroup
    house_group = HouseholdGroup()

    # 入力データ側で家庭ごと、必要データを管理する必要がある
    '''
    for house_num in houses:
        # EACH_HOUSE_START
        house = Household()
        rows = SQL('select * from table where home_num=house_num')
        # ある家庭のある期間のあるデータ
        # この中で処理する
        for row in rows:
            pass
        # EACH_HOUSE_END
    '''

    # EACH_HOUSE_START

    # 必要なDataRowsを用意する
    # 1種類目のDataRows
    ac_log_DF = DataRows(ACLogDataFormat.format_type)  # first DataRows
    with open(CSVFILE_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ac_log_DF.append(
                ACLogDataFormat(
                timestamp=row['timestamp'],
                on_off=row['on_off'],
                operating=row['operating'],
                set_temperature=row['set_temperature'],
                wind=row['wind'],
                temperature=row['temperature'],
                pressure=row['pressure'],
                humidity=row['humidity'],
                IP_Address=row['IP_Address'],
                ))

    # Instanciate Household with DataRows_es
    house = Household(ac_log=ac_log_DF)
    # house = Household(smart_meter=XXX, is_done=XXX)  # という感じで

    # HouseholdインスタンスにDataRowsを入れ込む
    house_group.append(house)

    # EACH_HOUSE_END

    # データ入力、HouseholdIterator準備フェーズ終了

    # FormGenerator 実行フェーズ開始

    # お試し
    for hosue in house_group.get_iter():
        print("house: ", house)

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
