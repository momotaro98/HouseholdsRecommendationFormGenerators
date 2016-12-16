from unittest import TestCase
from datetime import datetime as dt

from household_recommendation_form_generators \
    import (Household, HouseholdGroup, HouseholdIterator,
            RecommendModulesUseFlags, ACLogDataRows,
            FormGenerator)


class HouseholdTestCase(TestCase):
    def test_basic_function(self):
        house = Household(10000)  # Instanciation
        self.assertEqual(house.id, 10000)
        self.assertIsInstance(
            house.module_use_flgas, RecommendModulesUseFlags)

    def test_get_data_rows_methods(self):
        house = Household(10001)  # Instanciation
        ac_log = house.get_ac_log()
        self.assertIsInstance(ac_log, ACLogDataRows)


class HouseholdGroupTestCase(TestCase):
    def test_basic_function(self):
        house_group = HouseholdGroup(list(range(10011, 10021)))
        self.assertEqual(len(house_group._households_list), 10)
        # Output Phase
        for house in house_group.get_iter():
            self.assertIsInstance(house, Household)
        self.assertEqual(len(house_group._households_list), 10)


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


class RecommendModulesUseFlagsTestCase(TestCase):
    def test_basic_function(self):
        # Instanciation
        flags = RecommendModulesUseFlags()
        self.assertTrue(flags.use_ST)
        self.assertTrue(flags.use_RU)
        self.assertTrue(flags.use_CU)

        # Change the flags
        flags.use_ST = False
        self.assertFalse(flags.use_ST)
        flags.use_RU = False
        self.assertFalse(flags.use_RU)
        flags.use_CU = False
        self.assertFalse(flags.use_CU)

        # Test not change if invalid type
        flags.use_ST = 'True'
        self.assertFalse(flags.use_ST)
        flags.use_RU = 'True'
        self.assertFalse(flags.use_RU)
        flags.use_CU = 'True'
        self.assertFalse(flags.use_CU)

    def test_reset_method(self):
        flags = RecommendModulesUseFlags()
        flags.use_ST = False
        flags.use_CU = False
        flags.reset()
        self.assertTrue(flags.use_ST)
        self.assertTrue(flags.use_RU)
        self.assertTrue(flags.use_CU)


class FormGeneratorTestCase(TestCase):
    def setUp(self):
        self.house_group = HouseholdGroup(list(range(10031, 10041)))

    def test_basic_function(self):
        for house in self.house_group.get_iter():
            start_time = dt(2016, 4, 1)
            end_time = dt(2016, 4, 15)
            form_generator = FormGenerator(house, start_time=start_time, )
            form_generator.run()
