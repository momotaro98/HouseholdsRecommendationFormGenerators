# condig: utf-8

# レコメンドレポートに載せる内容モジュールをインポート
from home_electric_usage_recommendation_modules \
    import (SettingTemp, ReduceUsage, ChangeUsage)


class DataFormat:
    """
    家庭が持つデータ
    """
    pass


class OperatingDataFormat(DataFormat):
    """
    家電操作のデータ形式
    """
    pass


class ACOperatingDataFormat(OperatingDataFormat):
    """
    エアコン操作のデータ形式 <- My Experiment!

    想定しているデータカラム
    --------------------------------------------------------------------------------------------
    timestamp,on_off,operating,set_temperature,wind,temperature,pressure,humidity,IP_Address
    --------------------------------------------------------------------------------------------
    timestamp:       操作時の日時時刻 datetime型
    on_off:          オンオフ操作 str型
    operating:       運転モード操作 str型
    set_temperature: 設定温度操作 str型
    wind:            設定風量 int型
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


class TimeSeriesDataFormat(DataFormat):
    """
    時系列データのデータ形式
    """
    pass


class MetaDataFormat(DataFormat):
    """
    家族構成データ・住まい地域などのデータ形式
    """
    pass


class Household:
    """
    家庭はデータを持つ

    Example:
    電力時系列データ
    家族構成データ
    """
    pass


class HouseIterator:
    """
    """
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
