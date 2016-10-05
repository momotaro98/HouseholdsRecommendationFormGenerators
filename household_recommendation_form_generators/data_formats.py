# condig: utf-8


class DataFormat:
    """
    Abstract Model

    家庭が持つデータ
    """
    pass


class LogDataFormat:
    """
    Abstract Model

    何かを閲覧したり操作するときのログデータ
    """
    pass


class ApplianceLogDataFormat(DataFormat):
    """
    Abstract Model

    家電操作のデータ形式
    """
    pass


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
    def __init__(self, timestamp, on_off=None, operating=None,
                 set_temperature=None, wind=None,
                 temperature=None, pressure=None, humidity=None,
                 IP_Address=None):
        self.timestamp = dt.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        self.on_off = str(on_off) if on_off else on_off
        self.operating = str(operating) if operating else operating
        self.set_temperature = int(set_temperature)\
            if set_temperature else set_temperature
        self.wind = str(wind) if wind else wind
        self.temperature = float(temperature) if temperature else wind
        self.pressure = float(pressure) if pressure else pressure
        self.humidity = float(humidity) if humidity else humidity
        self.IP_Address = str(IP_Address) if IP_Address else IP_Address


class WebPageViewLogDataFormat(LogDataFormat):
    """
    Practical Model

    レコメンドレポート閲覧ログデータ
    """
    pass


class TimeSeriesDataFormat(DataFormat):
    """
    Abstract Model

    時系列データのデータ形式
    """
    pass


class SmartMeterDataFormat(TimeSeriesDataFormat):
    """
    Practical Model

    スマートメータのデータ形式
    """
    pass


class TwoSelectionsDataFormat(DataFormat):
    """
    Abstract Model

    Yes/No 等の2択データ
    """
    pass


class IsDoneDataFormat(TwoSelectionsDataFormat):
    """
    Practical Model

    レコメンドレポート内容を実行したかどうかの2択データ
    """
    pass


class MetaDataFormat(DataFormat):
    """
    Abstract Model

    家族構成データ・住まい地域などのデータ形式
    """
    pass
