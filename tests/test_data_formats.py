from unittest import TestCase

from household_recommendation_form_generators \
    import (DataRows, DataFormat)


class DataRowsTestCase(TestCase):
    def test_basis_function(self):
        '''
        DataRowsの基本機能をテスト
        '''
        dr = DataRows(DataFormat.format_type)
        self.assertEqual(dr.format_type, 'DataFormat')
        num = 10
        for _ in range(num):
            dr.append(DataFormat())
        count = 0
        for row in dr.get_rows_iter():
            self.assertEqual(row.format_type, 'DataFormat')
            count += 1
        self.assertEqual(count, num)
