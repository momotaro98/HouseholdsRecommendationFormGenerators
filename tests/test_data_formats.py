from unittest import TestCase
from datetime import datetime as dt

from household_recommendation_form_generators \
    import (DataRows, DataFormat, MetaDataRow)


class DataRowsTestCase(TestCase):
    def test_basis_function(self):
        '''
        DataRowsの基本機能をテスト
        '''
        home_id = 333
        start_time = dt(2016, 4, 1)
        end_time = dt(2016, 4, 15)
        dr = DataRows(
            home_id, start_time=start_time, end_time=end_time
        )
        num = 10
        for _ in range(num):
            dr._append(DataFormat())
        count = 0
        for row in dr.get_rows_iter():
            count += 1
        self.assertEqual(count, num)


'''
# home_metaテーブルを消してしまったので、作り直したらコメントを外す
class MetaDotaRowTestCase(TestCase):
    def test_basis_function(self):
        # My Caution. This test needs DB's data
        row = MetaDataRow(home_id=2008).get_row()
        self.assertEqual(row.family_num, 3)
        self.assertEqual(row.kind_type, 2)
        self.assertEqual(row.area_type, 3)
'''
