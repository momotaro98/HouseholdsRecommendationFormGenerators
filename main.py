import csv
from datetime import datetime
from datetime import timedelta
import time
import random

from household_recommendation_form_generators import *


class PredictionEvaluation:
    """
    >>> pe = PredictionEvaluation([0, 1, 0, 0], [0, 1, 1, 0])
    >>> precision = pe.ret_Precision()
    >>> recall = pe.ret_Recall()
    >>> fvalue = pe.ret_Fvalue()
    >>> precsioin, recall, fvalue = pe.ret_Precisioin_Recall_Fvalue()
    """
    '''
    精度(Precision)、再現率(Recall)、F値(F-measure)を求めるためのクラス
    '''
    def __init__(self, y_true, y_pred):
        if len(y_true) != len(y_pred):
            raise Exception("True, Predの2つのリストの長さがちゃうで")
        self.TP = 0
        self.FP = 0
        self.TN = 0
        self.FN = 0
        for true, pred in zip(y_true, y_pred):
            if true and pred:
                self.TP += 1
            elif true and not pred:
                self.FN += 1
            elif not true and pred:
                self.FP += 1
            elif not true and not pred:
                self.TN += 1

    def ret_Precision(self):
        return self.TP / (self.TP + self.FP)

    def ret_Recall(self):
        return self.TP / (self.TP + self.FN)

    def ret_Fvalue(self):
        try:
            precision = self.ret_Precision()
            recall = self.ret_Recall()
            fvalue = (2 * recall * precision) / (recall + precision)
        except ZeroDivisionError:
            fvalue = 0.0
        return fvalue

    def ret_Precisioin_Recall_Fvalue(self):
        return self.ret_Precision(), self.ret_Recall(), self.ret_Fvalue()


class MyPredictionEvaluation:
    """
    修論研究における評価量である精度(Precision)を求める

    >>> pe = MyPredictionEvaluation([0, 1, 0, 0], [0, 1, 1, 0])
    >>> precision = pe.ret_Precision()
    """
    def __init__(self, y_true, y_pred):
        if len(y_true) != len(y_pred):
            raise Exception("True, Predの2つのリストの長さがちゃうで")
        self.TP = 0
        self.FP = 0
        self.TN = 0
        self.FN = 0
        for true, pred in zip(y_true, y_pred):
            if true and pred:
                self.TP += 1
            elif true and not pred:
                self.FN += 1
            elif not true and pred:
                self.FP += 1
            elif not true and not pred:
                self.TN += 1

    def ret_Precision(self):
        try:
            ret = self.TP / (self.TP + self.FP)
        except ZeroDivisionError:
            ret = 0.0
        return ret


def _ret_act_list(eyh_instance):
    act_y_list = [ay[1] for ay in eyh_instance.ret_act_Y_list()]
    return act_y_list


def _ret_pred_list(isreco_instance, start_dt, end_dt):
    pred_y_list = []
    s_dt = start_dt
    while s_dt <= end_dt:
        pred_Y = isreco_instance.ret_pred_Y(s_dt.date())
        pred_y_list.append(pred_Y)

        s_dt += timedelta(days=1)
    return pred_y_list


def ret_act_and_pred_y_list(house_group, target_home_id):
    # 家庭クラスタの決定木モデルから得られる2016年冬時期のY予測値
    start_dt = datetime(2016, 12, 1, 0, 0, 0)
    end_dt = datetime(2016, 12, 14, 23, 59, 59)
    '''
    contents_dict = {
        'tu': {'act': None, 'pred': None},
        'cu': {'act': None, 'pred': None},
    }
    '''
    content_list = ['tu', 'cu']
    # content_list = ['tu']
    # content_list = ['cu']
    contents_dict = {}
    for content in content_list:
        contents_dict[content] = {}
        for act_or_pred in ('act', 'pred'):
            if content == 'tu' and act_or_pred == 'act':
                contents_dict[content][act_or_pred] = ExperimentHomesYactTotalUsage(
                    home_id=target_home_id,  # ikexp実験宅
                    start_train_dt=start_dt,
                    end_train_dt=end_dt,
                )
            elif content == 'cu' and act_or_pred == 'act':
                contents_dict[content][act_or_pred] = ExperimentHomesYactChangeUsage(
                    home_id=target_home_id,  # ikexp実験宅
                    start_train_dt=start_dt,
                    end_train_dt=end_dt,
                )
            elif content == 'tu' and act_or_pred == 'pred':
                contents_dict[content][act_or_pred] = IsTotalUsage(house_group)
            elif content == 'cu' and act_or_pred == 'pred':
                contents_dict[content][act_or_pred] = IsChangeUsage(house_group)

    act_y_list = []
    pred_y_list = []
    for content, ac_dict in contents_dict.items():
        act_y_list += _ret_act_list(ac_dict['act'])
        pred_y_list += _ret_pred_list(ac_dict['pred'], start_dt, end_dt)

    return act_y_list, pred_y_list


def ret_learning_time(house_group, n_clusters):
    start = time.time()
    cu_pred_Y = IsChangeUsage(house_group).ret_pred_Y()
    tu_pred_Y = IsTotalUsage(house_group).ret_pred_Y()
    end = time.time()
    elapsed_time = end - start
    learning_time = elapsed_time * n_clusters
    return learning_time


def run_csv_output(n_clusters, learning_time, precision):
    with open('eval_cluter.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([n_clusters, learning_time, precision])


def run_eval():
    # make homes_id_list
    homes_id_list = ret_homes_id_list()

    # make all house group
    all_house_group = HouseholdGroup(homes_id_list)  # All ModulesUseFlags are True

    # Instanciate HomesClusteringWithKMeans
    hcwk = HomesClusteringWithKMeans(all_house_group)

    # set n_clusters_list
    n_clusters_list = [
        10,
        9,
        8,
        7,
        6,
        5,
        4,
        3,
        2,
        1,
    ]
    for n_clusters in n_clusters_list:
        print('=' * 79)

        # print current n_clusters for evaluations
        print('n_clusters: ', n_clusters)

        # Evaluation 01. Eval Learning Computing Time
        # 学習計算コスト評価
        learning_time = 0

        # Evaluation 02. Eval Quality of Recommendations
        # レコメンド品質を検証する評価
        # set empty act_y_list and pred_y_list
        act_y_list = []
        pred_y_list = []

        # set target_home_id
        # target_home_id_list = [1, 8, 9, 11]
        target_home_id_list = [1, 9, 11]  # 採用！！！
        # target_home_id_list = [8, 9, 11]
        # target_home_id_list = [9, 11]
        print('target_homes_id', target_home_id_list)
        for target_home_id in target_home_id_list:  # ikexp
            # make target home's cluter's home_id list
            target_home_cluster_homes_id_list = hcwk.run(
                target_home_id=target_home_id,
                n_clusters=n_clusters
            )
            # print('homes num: ', len(target_home_cluster_homes_id_list))

            clustered_house_group = HouseholdGroup(target_home_cluster_homes_id_list)

            # Evaluation 01. Eval Learning Computing Time
            # 学習計算コスト評価
            learning_time += ret_learning_time(clustered_house_group, n_clusters)

            # Evaluation 02. Eval Quality of Recommendations
            # レコメンド品質を検証する評価
            new_act_y_list, new_pred_y_list = ret_act_and_pred_y_list(
                clustered_house_group,
                target_home_id,
            )
            act_y_list += new_act_y_list
            pred_y_list += new_pred_y_list

        # Evaluation 01. Eval Learning Computing Time
        # 学習計算コスト評価
        learning_time = learning_time / len(target_home_id_list)
        print('learning_time: ', learning_time, ' [sec]')

        # Evaluation 02. Eval Quality of Recommendations
        # レコメンド品質を検証する評価
        # print('act_y_list: ', act_y_list)
        # print('pre_y_list: ', pred_y_list)
        precision = MyPredictionEvaluation(act_y_list, pred_y_list).ret_Precision()
        print('Precision', precision)

        run_csv_output(n_clusters, learning_time, precision)


def ret_homes_id_list(hems='all'):
    ikexp_homes_id_list = [1, 8, 9, 11]
    kosugi_homes_id_list = [
        2004, 2010, 2011, 2012, 2014, 2017, 2018, 2019, 2020, 2021,
        2023, 2025, 2027, 2030, 2047, 2048, 2053, 2054, 2059, 2070,
        2071, 2073, 2079, 2082, 2087, 2088, 2096, 2099, 2104, 2105,
        2106, 2112, 2113, 2114, 2115, 2116, 2117, 2118, 2121, 2122,
        2123, 2124, 2126, 2129, 2130, 2131, 2137, 2150, 2151, 2152,
    ]  # 50件
    if hems == 'all':
        homes_id_list = ikexp_homes_id_list + kosugi_homes_id_list
    elif hems == 'ikexp':
        homes_id_list = ikexp_homes_id_list
    elif hems == 'kosugi':
        homes_id_list = kosugi_homes_id_list
    return homes_id_list


if __name__ == "__main__":
    """
    # アプリケーション側(FormGenerator側)が利用する家庭群を
    # 用意する処理を始めに行う必要がある

    # 前処理段階ではデータを格納しない
    # アプリケーションが必要なときにデータを得られるようにする
    # 家庭番号(user_id)とデータ期間(timestamp)のみが必要(のはず)
    # 家庭番号はHouseholdインスタンスが持つ各DataRows型のインスタンスが保持する
    # 期間はアプリケーション側が指定する

    # 研究における家庭番号割り当てについて
    池田実験協力家庭
    0000番台を割り当てる
    実際宅 [
        0001: Shiraki,
        0008: Ikeda,
        0009: Matsuoka,
        0010: Shiobara,
        0011: Nakamura
    ]

    栗原 家庭
    1000番台を割り当てる
    実際数 1001〜1016

    武蔵小杉 家庭
    2000番台を割り当てる
    実際数 2001〜2160
    """

    # *** 家庭グループ準備処理 Start ***

    # homes_id_list = ret_homes_id_list()

    # ひとまずランダムにクラスタ作成
    # TODO: metaデータを用いてk-meansクラスタリング処理
    # random.shuffle(homes_id_list)  # homes_id_listに対する破壊的処理


    # @@@@ HomeMeta情報に基づきK-Meansクラスタリングでグループ化 Start @@@
    # list to make
    '''
    [
        # [home_id, family_type, kind_type, area_type],
        [1, 1, 2, 3],
        [8, 2, 2, 3],
        [9, 3, 1, 3],
        [10, 3, 1, 3],
        [11, 2, 2, 3],

        [2004, 1, 2, 3],
        [2005, 2, 3, 2],

        [2152, 1, 2, 3],
    ]
    '''
    # house = Household(home_id=2006)
    # meta_row = house.get_home_meta()
    # print('meta_row', meta_row)
    # print('meta_row.family_num', meta_row.family_num)

    '''
    # Test HomesClusteringWithKMeans
    house_group = HouseholdGroup()  # All ModulesUseFlags are True
    for home_id in homes_id_list:
        # 各家庭が自家庭のHouseholdインスタンスを持つ
        house = Household(home_id)
        house_group.append(house)
    # print(HomesClusteringWithKMeans(house_group).ret_homes_id_pred_dict(n_clusters=4))
    # print(HomesClusteringWithKMeans(house_group).ret_target_home_cluster_homes_id_list(target_home_id=9))
    # print(HomesClusteringWithKMeans(house_group).run(target_home_id=9, n_clusters=4))
    # @@@@ HomeMeta情報に基づきK-Meansクラスタリングでグループ化 End @@@
    '''

    # *** 家庭グループ準備処理 End ***

    run_eval()


    """
    ###=== FormGeneratorアプリケーション 実行フェーズ Start ===###

    elapsed_time_dict = {}

    ###+++ Non Switching Case Start +++###
    # generate form phase
    start = time.time()
    for house in house_group.get_iter():
        # 以下の処理は各家庭のコンピュータが行う
        start_time = datetime(2015, 8, 1)
        end_time = datetime(2015, 9, 7)
        form_generator = FormGenerator(
            house, start_time=start_time, end_time=end_time
        )
        print("home_id", house.id)
        form_generator.run()
    end = time.time()
    elapsed_time_dict['Non Switching'] = end - start
    ###+++ Non Switching Case End +++###


    ###+++ Switching Case Start +++###
    # Switch flags phase
    # この処理はサーバ側で実行される
    for house in house_group.get_iter():
        sw_fs = UseFlagSwitcher(house)
        sw_fs.run()  # Switching

    # generate form phase
    start = time.time()
    for house in house_group.get_iter():
        start_time = datetime(2015, 8, 1)
        end_time = datetime(2015, 9, 7)
        form_generator = FormGenerator(
            house, start_time=start_time, end_time=end_time
        )
        print("home_id", house.id)
        form_generator.run()
    end = time.time()
    elapsed_time_dict['Switching'] = end - start

    # reset flags phase
    for house in house_group.get_iter():
        fs = UseFlagSwitcher(house)
        fs.reset()
    ###+++ Non Switching Case End +++###

    ###=== FormGeneratorアプリケーション 実行フェーズ End ===###


    # 各場合の計算時間を表示
    print(elapsed_time_dict)
    """
