# condig: utf-8
import random
from datetime import datetime as dt

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
    5. HomeMeta <= New! 2016-11-17
    """
    def __init__(self, home_id):
        self.id = home_id
        # Instanciate ModulesUseFlags class
        self.module_use_flgas = RecommendModulesUseFlags()

    def get_smart_meter(self):
        pass

    def get_ac_log(self, start_time=None, end_time=None):
        return ACLogDataRows(
            home_id=self.id, start_time=start_time, end_time=end_time
        )

    def get_web_view_log(self):
        pass

    def get_is_done(self):
        pass

    def get_home_meta(self):
        # return MetaDataRow(home_id=self.id)
        return MetaDataRow(home_id=self.id).get_row()


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
    '''
    Householdモデルを持つイテレータ

    2016-10-05 時点で不必要で,代わりにHouseholdGroupを利用する
    '''
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


class RecommendModulesUseFlags:
    '''
    Ikeda's Reserach Factor
    Recommendation modules use flags to each household

    Flags
    use SettingTemp flag
    use ReduceUsage flag
    use ChangeUsage flag

    First, the flags are True.
    At the preprocess_with_reaction_data method in The FormGenerator's class,
    each flag gets False
    '''
    def __init__(self, use_ST=True, use_RU=True, use_CU=True):
        self._use_ST = use_ST
        self._use_RU = use_RU
        self._use_CU = use_CU

    @property
    def use_ST(self):
        return self._use_ST

    @use_ST.setter
    def use_ST(self, t_or_f):
        if not isinstance(t_or_f, bool):
            return
        self._use_ST = t_or_f

    @property
    def use_RU(self):
        return self._use_RU

    @use_RU.setter
    def use_RU(self, t_or_f):
        if not isinstance(t_or_f, bool):
            return
        self._use_RU = t_or_f

    @property
    def use_CU(self):
        return self._use_CU

    @use_CU.setter
    def use_CU(self, t_or_f):
        if not isinstance(t_or_f, bool):
            return
        self._use_CU = t_or_f

    def reset(self):
        self.use_ST = True
        self.use_RU = True
        self.use_CU = True


class UseFlagSwitcher:
    '''
    class for Ikeda's Research
    switcher for Household's ModulesUseFlags
    '''
    def __init__(self, house):
        '''
        receive Household instance
        '''
        if not isinstance(house, Household):
            raise TypeError  # TODO: write valid error
        self.house = house

    def run(self):
        """
        機能としてModulesUseFlagsのTrueをFalseにするメソッド
        各Householdが持つReaction Dataをもとにして
        各Householdが持つModulesUseFlagsのスイッチングをする

        * ここが研究要素であり提案手法・ライバル手法で異なる
            * 提案手法では生成済みの木構造からFlagを上げたり下げたりする

        * この処理において利用するデータが「反応データ」と呼ぶもので
            * レポート画面閲覧ログデータ -> WebViewLogDataFormat
            * 実際の電力消費データ -> ACLogDataFormat 'or' SmartMeterDataFormat
            * 家庭の家族情報や地域情報などのメタデータ -> MetaDataFormat

        * 学習の正答の答え合わせとして
            * 実行したかどうかの2択データ -> IsDoneDataFormat
        """

        '''
        どうしようもないのでランダムでフラグ立て
        '''
        if random.random() < 0.3:
            self.house.module_use_flgas.use_ST = False
        if random.random() < 0.3:
            self.house.module_use_flgas.use_RU = False
        if random.random() < 0.3:
            self.house.module_use_flgas.use_CU = False

    def reset(self):
        '''
        Reset the Household's ModulesUseFlags (All flags to True)
        '''
        self.house.module_use_flgas.reset()


class FormGenerator:
    '''
    class for generating recommendation form

    * レコメンドレポート生成用の処理をする部分
    * home_electric_usage_recommendation_modules
    ライブラリはここで利用する
    * 実際の電力消費データ -> ACLogDataFormat 'or' SmartMeterDataFormat
    を利用する
    '''
    def __init__(self, house, start_time=None, end_time=None):
        '''
        初期化でHouseholdインスタンスを受け取る
        '''
        self.house = house
        self.start_time = start_time
        self.end_time = end_time
        if not self._check_the_relation_start_and_end():
            raise Exception('Start and End Time Error')

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        if isinstance(start_time, dt) or start_time is None:
            self._start_time = start_time
            return
        raise TypeError

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        if isinstance(end_time, dt) or end_time is None:
            self._end_time = end_time
            return
        raise TypeError

    def _check_the_relation_start_and_end(self):
        if self.start_time is None or self.end_time is None:
            return True
        if (self.end_time - self.start_time).total_seconds() > 0.0:
            return True
        return False

    def run(self):
        '''
        run the FormGenerator
        '''

        # * Householdインスタンスが持つModulesUseFlagsの
        # フラグのTrue or Falseで対象のモジュールを実行するか判断する

        '''
        # 2016-10-28 written: 設定温度のレコメンドは学習においては省く
        # 設定温度レコメンド
        # Check RecommendModulesUseFlags.use_ST and run the module
        if self.house.module_use_flgas.use_ST:
            # Get ACLogDataRows Instance
            ac_log = self.house.get_ac_log(
                start_time=self.start_time, end_time=self.end_time
            )
            # Get ACLogDataRows Rows
            ac_log_rows_list = list(ac_log.get_rows_iter())

            st = SettingTemp(ac_log_rows_list)
            st.calculate_running_time()
        '''

        # 電力削減レコメンド
        # Check RecommendModulesUseFlags.use_RU and run the module
        if self.house.module_use_flgas.use_RU:
            # Get ACLogDataRows Instance
            ac_log = self.house.get_ac_log(
                start_time=self.start_time, end_time=self.end_time
            )
            # Get ACLogDataRows Rows
            ac_log_rows_list = list(ac_log.get_rows_iter())

            # Run ReduceUsage Module
            ru = ReduceUsage(ac_log_rows_list)
            ru.calculate_running_time()


        # 使用時間帯変更レコメンド
        # Check RecommendModulesUseFlags.use_CU and run the module
        if self.house.module_use_flgas.use_CU:
            # Get ACLogDataRows Instance
            ac_log = self.house.get_ac_log(
                start_time=self.start_time, end_time=self.end_time
            )
            # Get ACLogDataRows Rows
            ac_log_rows_list = list(ac_log.get_rows_iter())

            cu = ChangeUsage(ac_log_rows_list)
            cu.calculate_running_time()
