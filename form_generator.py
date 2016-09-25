# condig: utf-8

"""
レコメンドレポートに載せる内容モジュールをインポート
from recomodules import (SettingTemp, ReduceUsage, ChangeUsage)
"""


class Household:
    """
    家庭における設計を記す

    Example:
    電力時系列データ
    家族構成データ
    """
    pass


class HouseIterator:
    def __init__(self):
        pass


class FormGenerator:
    def __init__(self, houseiter):
        """初期化ではHouseIteratorインスタンスを受け取る
        """
        pass

    def run(self):
        """フォームジェネレータを実行するメソッド
        """
        pass

    def generate_html(self):
        pass


class EachHomeWayFormGemerator(FormGenerator):
    pass


class ClusteringWayFormGenerator(FormGenerator):
    pass


class ClassificationTreeWayFormGenerator(FormGenerator):
    pass


if __name__ == "__main__":
    pass

    # 始めにレコメンドレポートを発行する家庭群を用意する
    # データセットからの家庭群をHouseIteratorとして収納
    # CSVとかDBからのデータをHouseIteratorにする
    # houses = HouseIterator("データセットからのデータ")

    # instanciate EachHomeWayFormGemerator
    # ehw_fg = EachHomeWayFormGemerator(houses)
    # run EachHomeWayFormGemerator instance
    # ehw_fg.run()

    # instanciate ClusteringWayFormGenerator
    # cw_fg = ClusteringWayFormGenerator(houses)
    # run ClusteringWayFormGenerator instance
    # cw_fg.run()

    # instanciate ClassificationTreeWayFormGenerator
    # ctw_fg = ClassificationTreeWayFormGenerator(houses)
    # run ClassificationTreeWayFormGenerator instance
    # ctw_fg.run()
