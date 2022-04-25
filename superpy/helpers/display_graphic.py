from datetime import date, timedelta
import matplotlib.pyplot as plt
from helpers.report_finance import report_profit, report_revenue


# Creates list of all dates between the 2 given dates.
def daterange(date1, date2):
    date_list = []
    for n in range(int ((date2 - date1).days)+1):
        date_list.append(date1 + timedelta(n))
    return date_list


# Processes date list and creates graphic.
def plotter(date_list, income):
    fig, ax = plt.subplots()
    result_list = []
    print(date_list)
    for date in date_list:
        if income == "profit":
            result_list.append(report_profit(date, income))
        elif income == "revenue":
            result_list.append(report_revenue(date, income))
    ax.plot(date_list, result_list)
    plt.xticks(rotation=30)
    return plt.show()
    

# Connects list of dates to the plotter.
def display_graphic(sd, ed, income):
    date_list = []

    sd = [int(i) for i in sd.split("/")]
    ed = [int(i) for i in ed.split("/")]

    start_date = date(sd[2], sd[1], sd[0])
    end_date = date(ed[2], ed[1], ed[0])

    data = daterange(start_date, end_date)
    for dt in data:
        formatted_date = dt.strftime("%d/%m/%Y")
        date_list.append(formatted_date)
    plotter(date_list, income)