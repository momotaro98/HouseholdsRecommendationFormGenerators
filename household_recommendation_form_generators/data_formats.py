from datetime import datetime as dt
import csv
import psycopg2

from .config import Config


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
    # FormGeneratorアプリケーション用に
    def __init__(self, home_id, duration):
        self._home_id = home_id
        self._duration = duration
        self._rows_list = []  # 実態 型の中にデータの本体の内部リストを持つ
        self._queryData_and_appendRows(home_id, duration)

    @property
    def home_id(self):
        return self._home_id

    @home_id.setter
    def home_id(self, home_id):
        if not 0 < home_id < 10000 or not isinstance(home_id, int):
            return
        self._home_id = home_id

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    def _append(self, row):
        # リストに入れる型がDataFormat型であるかチェック
        if not self._is_the_type(row):
            raise Exception  # TODO: ちゃんとしたエラーを出すようにする
        self._rows_list.append(row)

    def _is_the_type(self, row):
        return isinstance(row, DataFormat)

    def get_rows_iter(self):
        return iter(self._rows_list)

    def _queryData_and_appendRows(self, home_id, duration):
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
    """
    FormGeneratorアプリケーション用にhome_idとdurationを持たせる
    """
    def __init__(self, home_id, duration):
        super().__init__(home_id, duration)

    # _is_the_type()メソッドはオーバーライドする
    def _is_the_type(self, row):
        return isinstance(row, ACLogDataFormat)

    def _queryData_and_appendRows(self, home_id, duration):
        '''
        Query from any data source (CSV file or DB) and
        append ACLogDataFormat to self._rows_list
        '''
        # CSV
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
        '''

        # DB
        """
        row[0]: id, Type->int
        row[1]: home_id, Type->int
        row[2]: timestamp, Type->datetime.datetime
        row[3]: on_off, Type->str
        row[4]: operating, Type->str
        row[5]: set_temperature, Type->int
        row[6]: wind, Type->str
        row[7]: indoor_temperature, Type->float
        row[8]: indoor_pressure, Type->float
        row[9]: indoor_humidity, Type->float
        row[10]: operate_ipaddress, Type->str
        """

        '''
            SELECT *
            FROM ac_logs
            WHERE home_id=2010
            ORDER BY timestamp
        '''

        sql_script = """
            SELECT *
            FROM ac_logs
            WHERE home_id={home_id}
            ORDER BY timestamp
        """.format(home_id=home_id)
        with psycopg2.connect(
            host=Config.HOST,
            dbname=Config.DBNAME,
            user=Config.USER,
            password=Config.PASSWORD) as conn:

            cur = conn.cursor()
            cur.execute(sql_script)
            rows = cur.fetchall()

            for row in rows:
                self._append(
                    ACLogDataFormat(
                        timestamp=row[2],
                        on_off=row[3],
                        operating=row[4],
                        set_temperature=row[5],
                        wind=row[6],
                        temperature=row[7],
                        pressure=row[8],
                        humidity=row[9],
                        IP_Address=row[10],
                    )
                )


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

    def __init__(self, family_num, house_type_num, region_num):
        '''
        family_num: 家族情報の番号 1人暮らし, 2人暮らし, etc...
        house_type_num: 家のタイプ マンション, 一軒家, etc...
        region_num: 地域情報の番号 東京 神奈川 etc...
        '''
        self.family_num = family_num
        self.house_type_num = house_type_num
        self.region_num = region_num
