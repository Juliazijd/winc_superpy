import csv
from datetime import date, timedelta
from rich.console import Console

console = Console()

today = date.today().strftime("%d/%m/%Y")
yesterday = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")


def report_revenue(date, calculate):
    total_revenue = 0
    total_cost = 0
    with open("data/sold.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            sold = dict(buy_price=row[3], sell_date=row[7], sell_price=row[8], quantity=row[9])
            if date == sold["sell_date"]:
                print(row)
                revenue = float(sold["sell_price"]) * int(sold["quantity"])
                print('revenue:', revenue)
                cost = float(sold["buy_price"]) * int(sold["quantity"])
                total_revenue = total_revenue + revenue
                print('total_revenue:',total_revenue)
                total_cost = total_cost + cost
                print('total cost:', total_cost)

        total_revenue = round(float(total_revenue), 1)
    
        if calculate == "revenue":
            print(total_revenue)
            return total_revenue
        else:
            return total_revenue - total_cost


def report_profit(date, calculate):
    total_loss = 0
    with open("data/expired.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            expired = dict(buy_price=row[3], exp_date=row[5], stock_quantity=row[6])
            if date == expired["exp_date"]:
                # print(row)
                loss = float(expired["buy_price"]) * int(expired["stock_quantity"])
                # print(loss)
                total_loss = total_loss + loss
                # print(total_loss)
    
        # print(report_revenue(date, calculate))
        profit = round((report_revenue(date, calculate) - total_loss), 1)
        return profit


# print(report_profit('21/03/2022', 'revenue'))