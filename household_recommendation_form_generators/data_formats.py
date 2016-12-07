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
    def __init__(self, home_id, start_time, end_time):
        self.home_id = home_id
        self.start_time = start_time
        self.end_time = end_time
        if not self._check_the_relation_start_and_end():
            raise Exception  # TODO: Implement Error
        self._rows_list = []  # 実態 型の中にデータの本体の内部リストを持つ
        self._queryData_and_appendRows()

    @property
    def home_id(self):
        return self._home_id

    @home_id.setter
    def home_id(self, home_id):
        if isinstance(home_id, int) and 0 < home_id:
            self._home_id = home_id
            return
        raise Exception

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

    def _append(self, row):
        # リストに入れる型がDataFormat型であるかチェック
        if not self._is_the_type(row):
            raise TypeError  # TODO: ちゃんとしたエラーを出すようにする
        self._rows_list.append(row)

    def _is_the_type(self, row):
        return isinstance(row, DataFormat)

    def get_rows_iter(self):
        return iter(self._rows_list)

    def _queryData_and_appendRows(self):
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
    FormGeneratorアプリケーション用にhome_idとtimeframeを持たせる
    """
    def __init__(self, home_id, start_time=None, end_time=None):
        super().__init__(home_id, start_time, end_time)

    # _is_the_type()メソッドはオーバーライドする
    def _is_the_type(self, row):
        return isinstance(row, ACLogDataFormat)

    def _queryData_and_appendRows(self):
        '''
        query from DB
        append ACLogDataFormat to self._rows_list
        '''
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

        sql_script = self._generate_sql_script()

        with psycopg2.connect(
            host=Config.HOST,
            dbname=Config.DBNAME,
            user=Config.USER,
            password=Config.PASSWORD
                ) as conn:

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

    def _generate_sql_script(self):
        if self.start_time and self.end_time:
            sql_script = """
                SELECT *
                FROM ac_logs
                WHERE home_id={home_id}
                AND timestamp>='{start_time}'
                AND timestamp<='{end_time}'
                ORDER BY timestamp
            """.format(
                home_id=self.home_id,
                start_time=self.start_time,
                end_time=self.end_time
            )
            return sql_script
        elif self.start_time:
            sql_script = """
                SELECT *
                FROM ac_logs
                WHERE home_id={home_id}
                AND timestamp>='{start_time}'
                ORDER BY timestamp
            """.format(
                home_id=self.home_id,
                start_time=self.start_time
            )
            return sql_script
        elif self.end_time:
            sql_script = """
                SELECT *
                FROM ac_logs
                WHERE home_id={home_id}
                AND timestamp<='{end_time}'
                ORDER BY timestamp
            """.format(
                home_id=self.home_id,
                end_time=self.end_time
            )
            return sql_script
        else:
            sql_script = """
                SELECT *
                FROM ac_logs
                WHERE home_id={home_id}
                ORDER BY timestamp
            """.format(
                home_id=self.home_id
            )
            return sql_script


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

    def __init__(self, family_num, kind_type, area_type):
        '''
        family_num: 家族情報の番号 1人暮らし, 2人暮らし, etc...
        house_type_num: 家のタイプ マンション, 一軒家, etc...
        region_num: 地域情報の番号 東京 神奈川 etc...
        '''
        self.family_num = family_num
        self.kind_type = kind_type
        self.area_type = area_type


class MetaDataRow:
    def __init__(self, home_id):
        self.home_id = home_id
        self._queryData()

    def _queryData(self):
        with psycopg2.connect(
            host=Config.HOST,
            dbname=Config.DBNAME,
            user=Config.USER,
            password=Config.PASSWORD
                ) as conn:

            cur = conn.cursor()
            sql_script = self._generate_sql_script()
            cur.execute(sql_script)
            row = cur.fetchone()

            self._row = MetaDataFormat(
                family_num=row[2],
                kind_type=row[3],
                area_type=row[4],
            )

    def _generate_sql_script(self):
        sql_script = """
            SELECT *
            FROM home_meta
            WHERE home_id={home_id}
        """.format(
             home_id=self.home_id
        )
        return sql_script

    def get_row(self):
        return self._row
