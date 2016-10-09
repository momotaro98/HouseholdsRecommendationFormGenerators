# condig: utf-8

# レコメンドレポートに載せる内容モジュールをインポート
from home_electric_usage_recommendation_modules \
    import (SettingTemp, ReduceUsage, ChangeUsage)
from .data_formats import *


class Household:
    """
    家庭はデータの固まりをいくつか持つ

    DataFormat型のモデルをいくつか保持するものが家庭
    DataFormat型のモデルというのがつまりDBの各テーブルにあたる

    データ形式
    時系列データ TimeSeriesDataFormat -> SmartMeterDataFormat
    操作ログデータ LogDataFormat -> ApplianceLogDataFormat -> ACLogDataFormat
    内容実行二択データ TwoSelectionsDataFormat -> IsDoneDataFormat

    MetaDataFormat
    # 家族構成情報
    # 住まい地域情報

    2016-10-06 現状、以下のPractical DataFormatのみを持つようにする

    1. SmartMeterDataFormat
    2. ACLogDataFormat
    3. WebViewLogDataFormat
    4. IsDoneDataFormat
    """
    def __init__(self, home_id):
        self.id = home_id

    def get_smart_meter(self):
        pass

    def get_ac_log(self):
        return ACLogDataRows(self.id)

    def get_web_view_log(self):
        pass

    def get_is_done(self):
        pass


class HouseholdGroup:
    '''
    Household型のシーケンス
    '''
    def __init__(self):
        self._households_list = []

    def append(self, house):
        if not isinstance(house, Household):
            return
        self._households_list.append(house)

    def get_iter(self):
        '''
        for文用に利用する内部リストのイテレータを返すメソッド
        '''
        return iter(self._households_list)


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
    def __init__(self, house_group):
        """
        初期化ではHouseholdIteratorインスタンスを受け取る
        """
        self.house_group = house_group

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
            * レポート画面閲覧ログデータ -> WebViewLogDataFormat
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
