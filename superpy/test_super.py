from helpers.report_finance import report_profit, report_revenue
from helpers.buy_sell_products import buy_product, sell_product

def test_report_profit():
    if sell_product("banana", 1, 4):
        assert report_profit('25/04/2022', 'profit') == 4

def test_report_profit():
    if sell_product("banana", 1, 6) and buy_product("pineapple", 0.8, "03/05/2022", 2):
        assert report_profit('25/04/2022', 'profit') == 4.4

def test_report_revenue():
    if sell_product("pineapple", 1.2, 1) and sell_product("bread", 1.4, 2):
        assert report_revenue('25/04/2022', 'revenue') == 4

def test_report_revenue():
    if sell_product("pineapple", 1.2, 2) and buy_product("bread", 0.5, "05/04/2022", 4):
        assert report_revenue('25/04/2022', 'revenue') == 2.4
