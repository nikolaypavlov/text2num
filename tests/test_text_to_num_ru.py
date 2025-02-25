# MIT License

# Copyright (c) 2018-2019 Groupe Allo-Media

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys

"""
Test the ``text_to_num`` library.
"""
from unittest import TestCase
from text_to_num import alpha2digit, text2num


class TestTextToNumRU(TestCase):
    def test_text2num(self):
        test1 = (
            "пятьдесят три миллиарда двести сорок три тысячи семьсот двадцать четыре"
        )
        self.assertEqual(text2num(test1, "ru"), 53_000_243_724)

        test2 = "пятьдесят один миллион пятьсот семьдесят восемь тысяч триста два"
        self.assertEqual(text2num(test2, "ru"), 51_578_302)

        test3 = "восемьдесят пять"
        self.assertEqual(text2num(test3, "ru"), 85)

        test4 = "восемьдесят один"
        self.assertEqual(text2num(test4, "ru"), 81)

        self.assertEqual(text2num("пятьнадцать", "ru"), 15)
        self.assertEqual(text2num("сто пятьнадцать", "ru"), 115)
        self.assertEqual(text2num("сто пятнадцать", "ru"), 115)
        self.assertEqual(text2num("семьдесят пять тысяч", "ru"), 75000)
        self.assertEqual(text2num("тысяча девятьсот двадцать", "ru"), 1920)
        self.assertEqual(text2num("одна тысяча девятьсот двадцать", "ru"), 1920)

    def test_text2num_centuries(self):
        self.assertEqual(text2num("тысяча девятьсот семьдесят три", "ru"), 1973)

    def test_text2num_exc(self):
        self.assertRaises(ValueError, text2num, "тысяча тысяча двести", "ru")
        self.assertRaises(ValueError, text2num, "шестьдесят пятьдесят", "ru")
        self.assertRaises(ValueError, text2num, "шестьдесят сто", "ru")

    def test_text2num_zeroes(self):
        self.assertEqual(0, text2num("ноль", "ru"))
        self.assertEqual(8, text2num("ноль восемь", "ru"), 8)
        self.assertEqual(125, text2num("ноль ноль сто двадцать пять", "ru"))
        self.assertRaises(ValueError, text2num, "пять ноль", "ru")
        self.assertRaises(ValueError, text2num, "пять ноль три", "ru")
        self.assertRaises(ValueError, text2num, "пятьдесят три ноль", "ru")

    def test_alpha2digit_phones(self):
        source = "восемь девятьсот два сто один ноль один ноль один"
        expected = "8 902 101 01 01"
        self.assertEqual(expected, alpha2digit(source, "ru"))

        source = "плюс семь восемьсот пятьдесят девять сто один ноль сто один"
        expected = "+7 859 101 0101"
        self.assertEqual(expected, alpha2digit(source, "ru"))

        source = "Телефон восемь девятьсот шестьдесят два пятьсот девятнадцать семьдесят ноль ноль"
        expected = "Телефон 8 962 519 70 00"
        self.assertEqual(expected, alpha2digit(source, "ru"))

        source = "три сто пять сто один ноль один ноль один"
        expected = "3 105 101 01 01"
        self.assertEqual(expected, alpha2digit(source, "ru"))

    def test_alpha2digit_integers(self):
        source = "Двадцать пять коров, двенадцать сотен цыплят и сто двадцать пять точка сорок кг картофеля."
        expected = "25 коров, 1200 цыплят и 125.40 кг картофеля."
        self.assertEqual(expected, alpha2digit(source, "ru"))

        source = "Одна сотня огурцов, две сотни помидор, пять сотен рублей."
        expected = "100 огурцов, 200 помидор, 500 рублей."
        self.assertEqual(expected, alpha2digit(source, "ru"))

        source = "одна тысяча двести шестьдесят шесть рублей."
        expected = "1266 рублей."
        self.assertEqual(expected, alpha2digit(source, "ru"))
        source = "тысяча двести шестьдесят шесть рублей."
        self.assertEqual(expected, alpha2digit(source, "ru"))

        source = "один, два, три, четыре, двадцать, пятьнадцать"
        expected = "1, 2, 3, 4, 20, 15"
        self.assertEqual(expected, alpha2digit(source, "ru"))

        source = "двадцать один, тридцать один."
        expected = "21, 31."
        self.assertEqual(expected, alpha2digit(source, "ru"))

    def test_relaxed(self):
        source = "один два три четыре двадцать пять."
        expected = "1 2 3 4 25."
        self.assertEqual(expected, alpha2digit(source, "ru", relaxed=True))

        source = "один два три четыре двадцать, пять."
        expected = "1 2 3 4 20, 5."
        self.assertEqual(expected, alpha2digit(source, "ru", relaxed=True))

    def test_alpha2digit_formal(self):
        source = "плюс тридцать три, девять, шестьдесят, ноль шесть, двенадцать, двадцать один"
        expected = "+33, 9, 60, 06, 12, 21"
        self.assertEqual(expected, alpha2digit(source, "ru"))

        source = "ноль девять, шестьдесят, ноль шесть, двенадцать, двадцать один"
        expected = "09, 60, 06, 12, 21"
        self.assertEqual(expected, alpha2digit(source, "ru"))

        source = "Сам по себе я одиночка"
        self.assertEqual(source, alpha2digit(source, "ru"))

        source = "Он один? Она одна? Оно одно? Двадцать один? Двадцать одна? Двадцать одно?"
        expected = "Он один? Она одна? Оно одно? 21? 21? 21?"
        self.assertEqual(expected, alpha2digit(source, "ru"))

    def test_alpha2digit_if_alone(self):
        source = "Он нуль? Он один? Она одна? Оно одно? Двадцать один? Двадцать одна? Двадцать одно?"
        expected = "Он нуль? Он один? Она одна? Оно одно? 21? 21? 21?"
        self.assertEqual(expected, alpha2digit(source, "ru"))

    def test_and(self):
        source = "пятьдесят, шестьдесят, тридцать и одиннадцать"
        expected = "50, 60, 30 и 11"
        self.assertEqual(expected, alpha2digit(source, "ru"))

    def test_alpha2digit_zero(self):
        source = "тринадцать тысяч, ноль девяносто"
        expected = "13000, 090"
        self.assertEqual(expected, alpha2digit(source, "ru"))

        self.assertEqual("0", alpha2digit("ноль", "ru"))

    def test_alpha2digit_ordinals_force(self):
        source = "Пятый, третий, второй, двадцать первый, сотый, тысяча двести тридцатый, двадцать пятый, тридцать восьмой, сорок девятый."
        expected = "5-й, 3-й, 2-й, 21-й, 100-й, 1230-й, 25-й, 38-й, 49-й."
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))
        source = (
            "первый, второй, третий, четвёртый, четвертый, пятый, шестой, седьмой, восьмой, девятый, десятый, "
            "одиннадцатый, двенадцатый, тринадцатый, четырнадцатый, пятнадцатый, шестнадцатый, семнадцатый, восемнадцатый, девятнадцатый, двадцатый, "
            "двадцать первый, двадцать второй, двадцать третий, двадцать четвёртый, двадцать четвертый, двадцать пятый, двадцать шестой, двадцать седьмой, двадцать восьмой, двадцать девятый, "
            "тридцатый, сорок первый, пятьдесят второй, шестьдесят третий, семьдесят четвёртый, восемьдесят четвертый, девяносто пятый, "
            "сто первый, сто второй, сто третий, сто четвёртый, сто четвертый, сто пятый, сто шестой, сто седьмой, сто восьмой, сто девятый, сто десятый"
        )
        expected = (
            "1-й, 2-й, 3-й, 4-й, 4-й, 5-й, 6-й, 7-й, 8-й, 9-й, 10-й, 11-й, 12-й, 13-й, 14-й, 15-й, 16-й, 17-й, 18-й, 19-й, 20-й, "
            "21-й, 22-й, 23-й, 24-й, 24-й, 25-й, 26-й, 27-й, 28-й, 29-й, 30-й, 41-й, 52-й, 63-й, 74-й, 84-й, 95-й, "
            "101-й, 102-й, 103-й, 104-й, 104-й, 105-й, 106-й, 107-й, 108-й, 109-й, 110-й"
        )
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = (
            "первая, вторая, третья, четвёртая, четвертая, пятая, шестая, седьмая, восьмая, девятая, десятая, "
            "одиннадцатая, двенадцатая, тринадцатая, четырнадцатая, пятнадцатая, шестнадцатая, семнадцатая, восемнадцатая, девятнадцатая, двадцатая, "
            "двадцать первая, двадцать вторая, двадцать третья, двадцать четвёртая, двадцать четвертая, двадцать пятая, двадцать шестая, двадцать седьмая, двадцать восьмая, двадцать девятая, "
            "тридцатая, сорок первая, пятьдесят вторая, шестьдесят третья, семьдесят четвёртая, восемьдесят четвертая, девяносто пятая, "
            "сто первая, сто вторая, сто третья, сто четвёртая, сто четвертая, сто пятая, сто шестая, сто седьмая, сто восьмая, сто девятая, сто десятая"
        )
        expected = (
            "1-я, 2-я, 3-я, 4-я, 4-я, 5-я, 6-я, 7-я, 8-я, 9-я, 10-я, 11-я, 12-я, 13-я, 14-я, 15-я, 16-я, 17-я, 18-я, 19-я, 20-я, "
            "21-я, 22-я, 23-я, 24-я, 24-я, 25-я, 26-я, 27-я, 28-я, 29-я, 30-я, 41-я, 52-я, 63-я, 74-я, 84-я, 95-я, "
            "101-я, 102-я, 103-я, 104-я, 104-я, 105-я, 106-я, 107-я, 108-я, 109-я, 110-я"
        )
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = (
            "первой, второй, третьей, четвёртой, четвертой, пятой, шестой, седьмой, восьмой, девятой, десятой, "
            "одиннадцатой, двенадцатой, тринадцатой, четырнадцатой, пятнадцатой, шестнадцатой, семнадцатой, восемнадцатой, девятнадцатой, двадцатой, "
            "двадцать первой, двадцать второй, двадцать третьей, двадцать четвёртой, двадцать четвертой, двадцать пятой, двадцать шестой, двадцать седьмой, двадцать восьмой, двадцать девятой, "
            "тридцатой, сорок первой, пятьдесят второй, шестьдесят третьей, семьдесят четвёртой, восемьдесят четвертой, девяносто пятой, "
            "сто первой, сто второй, сто третьей, сто четвёртой, сто четвертой, сто пятой, сто шестой, сто седьмой, сто восьмой, сто девятой, сто десятой"
        )
        expected = (
            "1-й, 2-й, 3-й, 4-й, 4-й, 5-й, 6-й, 7-й, 8-й, 9-й, 10-й, 11-й, 12-й, 13-й, 14-й, 15-й, 16-й, 17-й, 18-й, 19-й, 20-й, "
            "21-й, 22-й, 23-й, 24-й, 24-й, 25-й, 26-й, 27-й, 28-й, 29-й, 30-й, 41-й, 52-й, 63-й, 74-й, 84-й, 95-й, "
            "101-й, 102-й, 103-й, 104-й, 104-й, 105-й, 106-й, 107-й, 108-й, 109-й, 110-й"
        )
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = (
            "первого, второго, третьего, четвёртого, четвертого, пятого, шестого, седьмого, восьмого, девятого, десятого, "
            "одиннадцатого, двенадцатого, тринадцатого, четырнадцатого, пятнадцатого, шестнадцатого, семнадцатого, восемнадцатого, девятнадцатого, двадцатого, "
            "двадцать первого, двадцать второго, двадцать третьего, двадцать четвёртого, двадцать четвертого, двадцать пятого, двадцать шестого, двадцать седьмого, двадцать восьмого, двадцать девятого, "
            "тридцатого, сорок первого, пятьдесят второго, шестьдесят третьего, семьдесят четвёртого, восемьдесят четвертого, девяносто пятого, "
            "сто первого, сто второго, сто третьего, сто четвёртого, сто четвертого, сто пятого, сто шестого, сто седьмого, сто восьмого, сто девятого, сто десятого"
        )
        expected = (
            "1-го, 2-го, 3-го, 4-го, 4-го, 5-го, 6-го, 7-го, 8-го, 9-го, 10-го, 11-го, 12-го, 13-го, 14-го, 15-го, 16-го, 17-го, 18-го, 19-го, 20-го, "
            "21-го, 22-го, 23-го, 24-го, 24-го, 25-го, 26-го, 27-го, 28-го, 29-го, 30-го, 41-го, 52-го, 63-го, 74-го, 84-го, 95-го, "
            "101-го, 102-го, 103-го, 104-го, 104-го, 105-го, 106-го, 107-го, 108-го, 109-го, 110-го"
        )
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = (
            "первому, второму, третьему, четвёртому, четвертому, пятому, шестому, седьмому, восьмому, девятому, десятому, "
            "одиннадцатому, двенадцатому, тринадцатому, четырнадцатому, пятнадцатому, шестнадцатому, семнадцатому, восемнадцатому, девятнадцатому, двадцатому, "
            "двадцать первому, двадцать второму, двадцать третьему, двадцать четвёртому, двадцать четвертому, двадцать пятому, двадцать шестому, двадцать седьмому, двадцать восьмому, двадцать девятому, "
            "тридцатому, сорок первому, пятьдесят второму, шестьдесят третьему, семьдесят четвёртому, восемьдесят четвертому, девяносто пятому, "
            "сто первому, сто второму, сто третьему, сто четвёртому, сто четвертому, сто пятому, сто шестому, сто седьмому, сто восьмому, сто девятому, сто десятому"
        )
        expected = (
            "1-му, 2-му, 3-му, 4-му, 4-му, 5-му, 6-му, 7-му, 8-му, 9-му, 10-му, 11-му, 12-му, 13-му, 14-му, 15-му, 16-му, 17-му, 18-му, 19-му, 20-му, "
            "21-му, 22-му, 23-му, 24-му, 24-му, 25-му, 26-му, 27-му, 28-му, 29-му, 30-му, 41-му, 52-му, 63-му, 74-му, 84-му, 95-му, "
            "101-му, 102-му, 103-му, 104-му, 104-му, 105-му, 106-му, 107-му, 108-му, 109-му, 110-му"
        )
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = (
            "первым, вторым, третьим, четвёртым, четвертым, пятым, шестым, седьмым, восьмым, девятым, десятым, "
            "одиннадцатым, двенадцатым, тринадцатым, четырнадцатым, пятнадцатым, шестнадцатым, семнадцатым, восемнадцатым, девятнадцатым, двадцатым, "
            "двадцать первым, двадцать вторым, двадцать третьим, двадцать четвёртым, двадцать четвертым, двадцать пятым, двадцать шестым, двадцать седьмым, двадцать восьмым, двадцать девятым, "
            "тридцатым, сорок первым, пятьдесят вторым, шестьдесят третьим, семьдесят четвёртым, восемьдесят четвертым, девяносто пятым, "
            "сто первым, сто вторым, сто третьим, сто четвёртым, сто четвертым, сто пятым, сто шестым, сто седьмым, сто восьмым, сто девятым, сто десятым"
        )
        expected = (
            "1-м, 2-м, 3-м, 4-м, 4-м, 5-м, 6-м, 7-м, 8-м, 9-м, 10-м, 11-м, 12-м, 13-м, 14-м, 15-м, 16-м, 17-м, 18-м, 19-м, 20-м, "
            "21-м, 22-м, 23-м, 24-м, 24-м, 25-м, 26-м, 27-м, 28-м, 29-м, 30-м, 41-м, 52-м, 63-м, 74-м, 84-м, 95-м, "
            "101-м, 102-м, 103-м, 104-м, 104-м, 105-м, 106-м, 107-м, 108-м, 109-м, 110-м"
        )
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = (
            "первую, вторую, третью, четвёртую, четвертую, пятую, шестую, седьмую, восьмую, девятую, десятую, "
            "одиннадцатую, двенадцатую, тринадцатую, четырнадцатую, пятнадцатую, шестнадцатую, семнадцатую, восемнадцатую, девятнадцатую, двадцатую, "
            "двадцать первую, двадцать вторую, двадцать третью, двадцать четвёртую, двадцать четвертую, двадцать пятую, двадцать шестую, двадцать седьмую, двадцать восьмую, двадцать девятую, "
            "тридцатую, сорок первую, пятьдесят вторую, шестьдесят третью, семьдесят четвёртую, восемьдесят четвертую, девяносто пятую, "
            "сто первую, сто вторую, сто третью, сто четвёртую, сто четвертую, сто пятую, сто шестую, сто седьмую, сто восьмую, сто девятую, сто десятую"
        )
        expected = (
            "1-ю, 2-ю, 3-ю, 4-ю, 4-ю, 5-ю, 6-ю, 7-ю, 8-ю, 9-ю, 10-ю, 11-ю, 12-ю, 13-ю, 14-ю, 15-ю, 16-ю, 17-ю, 18-ю, 19-ю, 20-ю, "
            "21-ю, 22-ю, 23-ю, 24-ю, 24-ю, 25-ю, 26-ю, 27-ю, 28-ю, 29-ю, 30-ю, 41-ю, 52-ю, 63-ю, 74-ю, 84-ю, 95-ю, "
            "101-ю, 102-ю, 103-ю, 104-ю, 104-ю, 105-ю, 106-ю, 107-ю, 108-ю, 109-ю, 110-ю"
        )
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = (
            "первыми, вторыми, третьими, четвёртыми, четвертыми, пятыми, шестыми, седьмыми, восьмыми, девятыми, десятыми, "
            "одиннадцатыми, двенадцатыми, тринадцатыми, четырнадцатыми, пятнадцатыми, шестнадцатыми, семнадцатыми, восемнадцатыми, девятнадцатыми, двадцатыми, "
            "двадцать первыми, двадцать вторыми, двадцать третьими, двадцать четвёртыми, двадцать четвертыми, двадцать пятыми, двадцать шестыми, двадцать седьмыми, двадцать восьмыми, двадцать девятыми, "
            "тридцатыми, сорок первыми, пятьдесят вторыми, шестьдесят третьими, семьдесят четвёртыми, восемьдесят четвертыми, девяносто пятыми, "
            "сто первыми, сто вторыми, сто третьими, сто четвёртыми, сто четвертыми, сто пятыми, сто шестыми, сто седьмыми, сто восьмыми, сто девятыми, сто десятыми"
        )
        expected = (
            "1-ми, 2-ми, 3-ми, 4-ми, 4-ми, 5-ми, 6-ми, 7-ми, 8-ми, 9-ми, 10-ми, 11-ми, 12-ми, 13-ми, 14-ми, 15-ми, 16-ми, 17-ми, 18-ми, 19-ми, 20-ми, "
            "21-ми, 22-ми, 23-ми, 24-ми, 24-ми, 25-ми, 26-ми, 27-ми, 28-ми, 29-ми, 30-ми, 41-ми, 52-ми, 63-ми, 74-ми, 84-ми, 95-ми, "
            "101-ми, 102-ми, 103-ми, 104-ми, 104-ми, 105-ми, 106-ми, 107-ми, 108-ми, 109-ми, 110-ми"
        )
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = (
            "первом, втором, третьем, четвёртом, четвертом, пятом, шестом, седьмом, восьмом, девятом, десятом, "
            "одиннадцатом, двенадцатом, тринадцатом, четырнадцатом, пятнадцатом, шестнадцатом, семнадцатом, восемнадцатом, девятнадцатом, двадцатом, "
            "двадцать первом, двадцать втором, двадцать третьем, двадцать четвёртом, двадцать четвертом, двадцать пятом, двадцать шестом, двадцать седьмом, двадцать восьмом, двадцать девятом, "
            "тридцатом, сорок первом, пятьдесят втором, шестьдесят третьем, семьдесят четвёртом, восемьдесят четвертом, девяносто пятом, "
            "сто первом, сто втором, сто третьем, сто четвёртом, сто четвертом, сто пятом, сто шестом, сто седьмом, сто восьмом, сто девятом, сто десятом"
        )
        expected = (
            "1-м, 2-м, 3-м, 4-м, 4-м, 5-м, 6-м, 7-м, 8-м, 9-м, 10-м, 11-м, 12-м, 13-м, 14-м, 15-м, 16-м, 17-м, 18-м, 19-м, 20-м, "
            "21-м, 22-м, 23-м, 24-м, 24-м, 25-м, 26-м, 27-м, 28-м, 29-м, 30-м, 41-м, 52-м, 63-м, 74-м, 84-м, 95-м, "
            "101-м, 102-м, 103-м, 104-м, 104-м, 105-м, 106-м, 107-м, 108-м, 109-м, 110-м"
        )
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = (
            "первое, второе, третье, четвёртое, четвертое, пятое, шестое, седьмое, восьмое, девятое, десятое, "
            "одиннадцатое, двенадцатое, тринадцатое, четырнадцатое, пятнадцатое, шестнадцатое, семнадцатое, восемнадцатое, девятнадцатое, двадцатое, "
            "двадцать первое, двадцать второе, двадцать третье, двадцать четвёртое, двадцать четвертое, двадцать пятое, двадцать шестое, двадцать седьмое, двадцать восьмое, двадцать девятое, "
            "тридцатое, сорок первое, пятьдесят второе, шестьдесят третье, семьдесят четвёртое, восемьдесят четвертое, девяносто пятое, "
            "сто первое, сто второе, сто третье, сто четвёртое, сто четвертое, сто пятое, сто шестое, сто седьмое, сто восьмое, сто девятое, сто десятое"
        )
        expected = (
            "1-е, 2-е, 3-е, 4-е, 4-е, 5-е, 6-е, 7-е, 8-е, 9-е, 10-е, 11-е, 12-е, 13-е, 14-е, 15-е, 16-е, 17-е, 18-е, 19-е, 20-е, "
            "21-е, 22-е, 23-е, 24-е, 24-е, 25-е, 26-е, 27-е, 28-е, 29-е, 30-е, 41-е, 52-е, 63-е, 74-е, 84-е, 95-е, "
            "101-е, 102-е, 103-е, 104-е, 104-е, 105-е, 106-е, 107-е, 108-е, 109-е, 110-е"
        )
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = (
            "первых, вторых, третьих, четвёртых, четвертых, пятых, шестых, седьмых, восьмых, девятых, десятых, "
            "одиннадцатых, двенадцатых, тринадцатых, четырнадцатых, пятнадцатых, шестнадцатых, семнадцатых, восемнадцатых, девятнадцатых, двадцатых, "
            "двадцать первых, двадцать вторых, двадцать третьих, двадцать четвёртых, двадцать четвертых, двадцать пятых, двадцать шестых, двадцать седьмых, двадцать восьмых, двадцать девятых, "
            "тридцатых, сорок первых, пятьдесят вторых, шестьдесят третьих, семьдесят четвёртых, восемьдесят четвертых, девяносто пятых, "
            "сто первых, сто вторых, сто третьих, сто четвёртых, сто четвертых, сто пятых, сто шестых, сто седьмых, сто восьмых, сто девятых, сто десятых"
        )
        expected = (
            "1-х, 2-х, 3-х, 4-х, 4-х, 5-х, 6-х, 7-х, 8-х, 9-х, 10-х, 11-х, 12-х, 13-х, 14-х, 15-х, 16-х, 17-х, 18-х, 19-х, 20-х, "
            "21-х, 22-х, 23-х, 24-х, 24-х, 25-х, 26-х, 27-х, 28-х, 29-х, 30-х, 41-х, 52-х, 63-х, 74-х, 84-х, 95-х, "
            "101-х, 102-х, 103-х, 104-х, 104-х, 105-х, 106-х, 107-х, 108-х, 109-х, 110-х"
        )
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = (
            "двадцать второе место на двадцать первой олимпиаде занял первый и второй"
        )
        expected = "22-е место на 21-й олимпиаде занял 1-й и 2-й"
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = "каждый пятый на первый второй расчитайсь!"
        expected = "каждый 5-й на 1-й 2-й расчитайсь!"
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = "На двадцать четвертую олимпиаду пришли первый и второй"
        expected = "На 24-ю олимпиаду пришли 1-й и 2-й"
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = "Она была двести тринадцатая в очереди"
        expected = "Она была 213-я в очереди"
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = "Я отдал ключи Второму, а Сто Двадцать Третьему нет"
        expected = "Я отдал ключи 2-му, а 123-му нет"
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=0))

        source = "Первый, Пятый, Девятый, Одиннадцатый, Двадцать первый, Сто двадцать первый, Сто одиннадцатый"
        expected = "Первый, Пятый, 9-й, 11-й, 21-й, 121-й, 111-й"
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=8))

        source = "Первый, Пятый, Одиннадцатый, Двадцать первый, Сто двадцать первый, Сто одиннадцатый"
        expected = "Первый, Пятый, Одиннадцатый, 21-й, 121-й, 111-й"
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=20))

        source = "Сейчас пол второго ночи, а он будет в пол двенадцатого."
        expected = "Сейчас пол второго ночи, а он будет в пол двенадцатого."
        self.assertEqual(expected, alpha2digit(source, "ru", ordinal_threshold=12))

    def test_alpha2digit_decimals(self):
        source = (
            "двенадцать точка девяносто девять, сто двадцать точка ноль пять,"
            " сто двадцать целых ноль пять, одна целая двести тридцать шесть."
        )
        expected = "12.99, 120.05, 120.05, 1.236."
        self.assertEqual(expected, alpha2digit(source, "ru"))

        self.assertEqual("0.15", alpha2digit("точка пятьнадцать", "ru"))
        self.assertEqual("0.15", alpha2digit("ноль целых пятьнадцать", "ru"))

    def test_alpha2digit_signed(self):
        source = "В комнате плюс двадцать градусов, тогда как на улице минус пятьдесят."
        expected = "В комнате +20 градусов, тогда как на улице -50."
        self.assertEqual(expected, alpha2digit(source, "ru"))

    def test_uppercase(self):
        source = "ПЯТЬНАДЦАТЬ ОДИН ДЕСЯТЬ ОДИН"
        expected = "15 1 10 1"
        self.assertEqual(expected, alpha2digit(source, "ru"))

    def test_hundreds(self):
        source = "пятьдесят один миллион пятьсот семьдесят восемь тысяч триста два"
        expected = 51578302
        self.assertEqual(expected, text2num(source, "ru"))

        source = "восемьдесят один"
        expected = 81
        self.assertEqual(expected, text2num(source, "ru"))

        source = "восемьсот"
        expected = 800
        self.assertEqual(expected, text2num(source, "ru"))

        source = "сто"
        expected = 100
        self.assertEqual(expected, text2num(source, "ru"))

        source = "сто двадцать"
        expected = 120
        self.assertEqual(expected, text2num(source, "ru"))

        source = "сто два"
        expected = 102
        self.assertEqual(expected, text2num(source, "ru"))

        source = "семьсот один"
        expected = 701

        self.assertEqual(expected, text2num(source, "ru"))
        source = "восемьсот миллионов"
        expected = 800_000_000
        self.assertEqual(expected, text2num(source, "ru"))

    def test_big_numbers(self):
        source = "триллион миллиард миллион тысяча один"
        expected = 1_001_001_001_001
        self.assertEqual(expected, text2num(source, "ru"))

        source = "один триллион один миллиард один миллион одна тысяча один"
        expected = 1_001_001_001_001
        self.assertEqual(expected, text2num(source, "ru"))

        source = "одиннадцать триллионов одиннадцать миллиардов одиннадцать миллионов одиннадцать тысяч одиннадцать"
        expected = 11_011_011_011_011
        self.assertEqual(expected, text2num(source, "ru"))

        source = "сто одиннадцать триллионов сто одиннадцать миллиардов сто одиннадцать миллионов сто одиннадцать тысяч сто одиннадцать"
        expected = 111_111_111_111_111
        self.assertEqual(expected, text2num(source, "ru"))

        source = "сто десять триллионов сто десять миллиардов сто десять миллионов сто десять тысяч сто десять"
        expected = 110_110_110_110_110
        self.assertEqual(expected, text2num(source, "ru"))
