from datetime import datetime as dt


class DataRows:
    """
    家庭が持つデータ型

    ACLogDataFormat型のシーケンス
    SmartMeterDataFormat型のシーケンス
    TwoSelectionsDataFormat型のシーケンス
    を持つ

    意味としてはDBにおけるテーブル・ビュー
    """
    def __init__(self, format_type):
        self._format_type = format_type
        self._rows_list = []  # 実態 型の中にデータの本体の内部リストを持つ

    @property
    def format_type(self):
        return self._format_type

    @format_type.setter
    def format_type(self, format_type):
        raise Exception  # TODO: ちゃんとしたエラーを出すようにする

    def append(self, row):
        # リストに入れる型がDataFormat型であるかチェック
        if not isinstance(row, DataFormat):
            return
        self._rows_list.append(row)

    def get_iter(self):
        '''
        for文用に利用する内部リストのイテレータを返すメソッド
        '''
        return iter(self._rows_list)


class DataFormat:
    """
    Top Abstract Model

    意味としてはDBテーブルにおける1カラム分
    """
    format_type = 'DataFormat'


class LogDataFormat(DataFormat):
    """
    Abstract Model

    何かを閲覧したり操作するときのログデータ
    """
    format_type = 'LogDataFormat'


class ApplianceLogDataFormat(LogDataFormat):
    """
    Abstract Model

    家電操作のデータ形式
    """
    format_type = 'ApplianceLogDataFormat'


class ACLogDataFormat(ApplianceLogDataFormat):
    """
    Practical Model

    エアコン操作のデータ形式 <- My Experiment!

    想定しているデータカラム
    --------------------------------------------------------------------------------------------
    timestamp,on_off,operating,set_temperature,wind,temperature,pressure,humidity,IP_Address
    --------------------------------------------------------------------------------------------
    timestamp:       操作時の日時時刻 datetime型
    on_off:          オンオフ操作 str型
    operating:       運転モード操作 str型
    set_temperature: 設定温度操作 int型
    wind:            設定風量 str型
    temperature:     室内温度 float型
    pressure:        室内気圧 float型
    humidity:        室内湿度 float型
    IP_Address:      操作者IPアドレス str型
    """
    format_type = 'ACLogDataFormat'

    def __init__(self, timestamp, on_off=None, operating=None,
                 set_temperature=None, wind=None,
                 temperature=None, pressure=None, humidity=None,
                 IP_Address=None):
        self.timestamp = dt.strptime(timestamp, '%Y-%m-%d %H:%M:%S')\
            if isinstance(timestamp, str) else timestamp
        self.on_off = str(on_off) if on_off else on_off
        self.operating = str(operating) if operating else operating
        self.set_temperature = int(set_temperature)\
            if set_temperature else set_temperature
        self.wind = str(wind) if wind else wind
        self.temperature = float(temperature) if temperature else temperature
        self.pressure = float(pressure) if pressure else pressure
        self.humidity = float(humidity) if humidity else humidity
        self.IP_Address = str(IP_Address) if IP_Address else IP_Address


class WebViewLogDataFormat(LogDataFormat):
    """
    Practical Model

    レコメンドレポート閲覧ログデータ
    """
    format_type = 'WebViewLogDataFormat'


class TimeSeriesDataFormat(DataFormat):
    """
    Abstract Model

    時系列データのデータ形式
    """
    format_type = 'TimeSeriesDataFormat'


class SmartMeterDataFormat(TimeSeriesDataFormat):
    """
    Practical Model

    スマートメータのデータ形式
    """
    format_type = 'SmartMeterDataFormat'


class TwoSelectionsDataFormat(DataFormat):
    """
    Abstract Model

    Yes/No 等の2択データ
    """
    format_type = 'TwoSelectionsDataFormat'


class IsDoneDataFormat(TwoSelectionsDataFormat):
    """
    Practical Model

    レコメンドレポート内容を実行したかどうかの2択データ
    """
    format_type = 'IsDoneDataFormat'


class MetaDataFormat(DataFormat):
    """
    Abstract Model

    家族構成データ・住まい地域などのデータ形式
    """
    format_type = 'MetaDataFormat'
