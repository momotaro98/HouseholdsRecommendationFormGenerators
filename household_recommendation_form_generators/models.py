# condig: utf-8

# レコメンドレポートに載せる内容モジュールをインポート
from home_electric_usage_recommendation_modules \
    import (SettingTemp, ReduceUsage, ChangeUsage)

from .data_formats import ACLogDataFormat


class Household:
    """
    家庭はデータの固まりをいくつか持つ

    データ形式
    時系列データ TimeSeriesDataFormat -> SmartMeterDataFormat
    操作ログデータ LogDataFormat -> ApplianceLogDataFormat -> ACLogDataFormat
    内容実行二択データ TwoSelectionsDataFormat -> IsDoneDataFormat

    MetaDataFormat
    # 家族構成情報
    # 住まい地域情報
    """
    def __init__(self, ac_operating_DF=None, smart_meter_DF=None):
        '''
        DataFormat型のモデルをいくつか保持するものが家庭
        DataFormat型のモデルというのがつまりDBの各テーブルにあたる
        '''
        self.ac_operating_DF = ac_operating_DF
        self.smart_meter_DF = smart_meter_DF


class HouseholdIterator:
    """
    Householdモデルを持つイテレータ
    """
    def __init__(self):
        self._households_list = []
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._i == len(self._households_list):
            raise StopIteration()
        household = self._households_list[self._i]
        self._i += 1
        return household

    def append(self, household):
        '''
        Householdモデルをself._households_listへ入れ込む
        '''
        # Household型かチェック
        if not self._is_Household(household):
            return
        self._households_list.append(household)

    def _is_Household(self, h):
        '''
        Householdモデルであるかチェックする
        '''
        return isinstance(h, Household)


class FormGenerator:
    '''
    Abstract Model
    '''
    def __init__(self, house_iter):
        """
        初期化ではHouseholdIteratorインスタンスを受け取る
        """
        self.house_iter = house_iter

    def run(self):
        """
        フォームジェネレータを実行するメソッド
        """
        # 提案手法では分類木生成・ライバル手法では個別処理にあたる
        # データ前処理フェーズ
        self.process_data_for_preprocessing()

        # home_electric_usage_recommendation_modules を利用して
        # レコメンド内容を生成する処理フェーズ
        self.process_data_for_output_recommendation_form()

    def process_data_for_preprocessing(self):
        """
        事前処理にあたる反応データ処理用のメソッド

        * ここが研究要素であり提案手法・ライバル手法で異なる
            * 提案手法ではここで木構造を生成する
            * 個別手法では個別家庭毎でどのレポート内容を実行するかの処理を行う
            * クラスタリング手法ではクラスタリング処理を行う

        この処理において利用するデータが「反応データ」と呼ぶもので
            * 実行したかどうかの2択データ -> IsDoneDataFormat
            * レポート画面閲覧ログデータ -> WebPageViewLogDataFormat
            * 実際の電力消費データ -> ACLogDataFormat 'or' SmartMeterDataFormat
        2016-10-05の段階ではこの3つで行っていく予定としている
        """
        pass

    def process_data_for_output_recommendation_form(self):
        """
        レコメンドレポート生成用の処理をする部分
        home_electric_usage_recommendation_modules ライブラリはここで利用する

        この処理において利用するデータが「解析用データ」と呼ぶもので
            * 実際の電力消費データ -> ACLogDataFormat 'or' SmartMeterDataFormat
        を利用する
        """
        pass

    def generate_html(self):
        """
        HTML文を吐き出すメソッド
        """
        pass


class EachHomeWayFormGemerator(FormGenerator):
    def process_data_for_preprocessing(self):
        pass

    def process_data_for_output_recommendation_form(self):
        pass


class ClusteringWayFormGenerator(FormGenerator):
    def process_data_for_preprocessing(self):
        pass

    def process_data_for_output_recommendation_form(self):
        pass


class ClassificationTreeWayFormGenerator(FormGenerator):
    def process_data_for_preprocessing(self):
        pass

    def process_data_for_output_recommendation_form(self):
        pass


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
    with open(CSVFILE_PATH) as csvfile:
        reader = csv.DictReader(csvfile)

    # house_iterを用意したのち

    # instanciate EachHomeWayFormGemerator
    # ehw_fg = EachHomeWayFormGemerator(house_iter)
    # run EachHomeWayFormGemerator instance
    # ehw_fg.run()

    # instanciate ClusteringWayFormGenerator
    # cw_fg = ClusteringWayFormGenerator(house_iter)
    # run ClusteringWayFormGenerator instance
    # cw_fg.run()

    # instanciate ClassificationTreeWayFormGenerator
    # ctw_fg = ClassificationTreeWayFormGenerator(house_iter)
    # run ClassificationTreeWayFormGenerator instance
    # ctw_fg.run()
