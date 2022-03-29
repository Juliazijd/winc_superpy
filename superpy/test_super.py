from helpers.report_finance import report_profit, report_revenue

def test_report_profit():
    assert report_profit('14/03/2022', 'profit') == -4.5

def test_report_profit():
    assert report_profit('20/03/2022', 'profit') == 1.2


def test_report_revenue():
    assert report_revenue('14/03/2022', 'revenue') == -3.0

def test_report_revenue():
    assert report_revenue('20/03/2022', 'revenue') == 3.0
