from unittest import TestCase

from household_recommendation_form_generators \
    import (DataRows, DataFormat)


class DataRowsTestCase(TestCase):
    def test_basis_function(self):
        '''
        DataRowsの基本機能をテスト
        '''
        home_id = 333
        dr = DataRows(home_id)
        num = 10
        for _ in range(num):
            dr._append(DataFormat())
        count = 0
        for row in dr.get_rows_iter():
            count += 1
        self.assertEqual(count, num)
