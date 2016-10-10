from datetime import datetime as dt
import csv


class DataFormat:
    """
    Top Abstract Model
    データフォーマットのトップ

    意味としてはDBテーブルにおける1カラム分

    JavaでいうDTOにあたる
    """
    format_type = 'DataFormat'


class DataRows:
    """
    家庭が持つデータ型

    意味としてはDBにおけるテーブル・ビュー

    JavaでいうDAOにあたる?
    """
    def __init__(self, home_id=None, duration=None):
        self._home_id = home_id
        self._duration = duration
        self._rows_list = []  # 実態 型の中にデータの本体の内部リストを持つ

    def _append(self, row):
        # リストに入れる型がDataFormat型であるかチェック
        if not self._is_the_type(row):
            raise Exception  # TODO: ちゃんとしたエラーを出すようにする
        self._rows_list.append(row)

    def _is_the_type(self, row):
        return isinstance(row, DataFormat)

    def get_rows_iter(self):
        self._query_and_append()
        return iter(self._rows_list)

    def _query_and_append(self):
        pass


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


class ACLogDataRows(DataRows):
    '''
    DAO like object for ACLogDataFormat class
    '''
    def __init__(self, home_id=None, duration=None):
        super().__init__(home_id, duration)

    def _is_the_type(self, row):
        return isinstance(row, ACLogDataFormat)

    def get_rows_iter(self, home_id=None, duration=None):
        if home_id is not None:
            self._home_id = home_id
        if duration is not None:
            self._duration = duration
        self._query_and_append()
        return iter(self._rows_list)

    def _query_and_append(self):
        '''
        Query from any data source (CSV file or DB) and
        append ACLogDataFormat to self._rows_list
        '''
        CSVFILE_PATH = 'test.csv'
        with open(CSVFILE_PATH) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self._append(
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


class WebViewLogDataFormat(LogDataFormat):
    """
    Practical Model

    レコメンドレポート閲覧ログデータ
    """
    format_type = 'WebViewLogDataFormat'


class WebViewLogDataRows(DataRows):
    def _is_the_type(self, row):
        return isinstance(row, WebViewLogDataFormat)


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


class SmartMeterDataRows(DataRows):
    def _is_the_type(self, row):
        return isinstance(row, SmartMeterDataFormat)


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


class IsDoneDataRows(DataRows):
    def _is_the_type(self, row):
        return isinstance(row, IsDoneDataFormat)


class MetaDataFormat(DataFormat):
    """
    Abstract Model

    家族構成データ・住まい地域などのデータ形式
    """
    format_type = 'MetaDataFormat'
