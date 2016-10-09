from unittest import TestCase

from household_recommendation_form_generators \
    import (Household, HouseholdIterator)


class HouseholdIteratorTestCase(TestCase):
    def setUp(self):
        '''
        Household型を用意しておく
        '''
        self.a_house = Household(home_id=100)
        self.list_num = 10
        self.household_list = [Household(num) for num in range(self.list_num)]

    def test_instanciation(self):
        '''
        インスタンスをテスト
        '''
        house_iter = HouseholdIterator()
        self.assertEqual(house_iter._i, 0)
        self.assertEqual(house_iter._households_list, [])

    def test_basic_iter_function(self):
        '''
        HouseholdIteratorのイテレータとしての基本機能をテスト
        '''
        house_iter = HouseholdIterator()
        for house in self.household_list:
            house_iter.append(house)
        # インスタンス型のリストにHousehold型が指定の数だけ入ったか確認
        self.assertEqual(len(house_iter._households_list), self.list_num)
        # イテレータとしてfor文を実行できるか確認
        for house in house_iter:
            self.assertIsInstance(house, Household)
        # イテレータ内のカウントが指定の数であるか確認
        self.assertEqual(house_iter._i, self.list_num)

    def test_append_isHousehold(self):
        house_iter = HouseholdIterator()
        house_iter.append(Household(home_id=101))
        house_iter.append('Household')  # Household型ではないものを加えようとする
        house_iter.append(Household(home_id=102))
        self.assertEqual(len(house_iter._households_list), 2)
        for house in house_iter:
            self.assertIsInstance(house, Household)
