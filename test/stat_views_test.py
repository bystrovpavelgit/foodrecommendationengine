""" unit-tests for load_form_data """
import unittest
from webapp.stat.views import load_form_data


class Holder:
    """ Holder class"""
    def __init__(self, data):
        """ init """
        self.data = data


class FormTester:
    """ Form Tester"""
    def __init__(self, dish, directions, ingredients):
        """ init method """
        self.dish = Holder(dish)
        self.directions = Holder(directions)
        self.rows = Holder(ingredients)


class StatViewsTest(unittest.TestCase):
    """ unit-tests for load_form_data """
    def test_load_form_data(self):
        """ unit-test for load_form_data """
        ingredients = [
            {'ingredient': "Утка", 'how_much': "8 кусков"},
            {'ingredient': "Салями", 'how_much': "8 кусков"}
        ]
        txt = """Срежьте с хлеба верхнюю и нижнюю корку.
        Из артишоков сделайте пюре и смешайте с майонезом. намажьте на хлеб. 
        Затем выложите слоями остальные ингредиенты и сверху накройте хлебом.
        Аккуратно прижмите. Используя большой нож нарежьте небольшие сэндвичи.
        Скрепите зубочисткой. На зубочистку оденьте ягоду клюквы."""
        form = FormTester("Сэндвичи с уткой", txt, ingredients)

        res_json, typ_, cuisine = load_form_data(form)

        self.assertIsNotNone(res_json)
        self.assertEqual(res_json[0]["name"], "Сэндвичи с уткой")
        self.assertTrue("pic_url" in res_json[0])
        self.assertTrue("pic" in res_json[0])
        self.assertEqual(res_json[0]["ingredients"], "['Утка', 'Салями']")
        self.assertEqual(res_json[0]["mera"], "['8 кусков', '8 кусков']")
        self.assertEqual(res_json[0]["directions"], txt)
        self.assertTrue("cusine" in res_json[0])
        self.assertTrue("typed" in res_json[0])
        self.assertTrue("url" in res_json[0])
        self.assertIsNotNone(typ_)
        self.assertIsNotNone(cuisine)
