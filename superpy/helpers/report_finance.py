import csv
from rich.console import Console

console = Console()

# Calculates total revenue on certain date.
def report_revenue(date, income):
    total_revenue = 0
    total_cost = 0
    with open("data/sold.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            sold = dict(buy_price=row[3], sell_date=row[7], sell_price=row[8], quantity=row[9])
            if date == sold["sell_date"]:
                revenue = float(sold["sell_price"]) * int(sold["quantity"])
                cost = float(sold["buy_price"]) * int(sold["quantity"])
                total_revenue = total_revenue + revenue
                total_cost = total_cost + cost

        total_revenue = round(float(total_revenue), 1)
    
        if income == "revenue":
            return total_revenue
        else:
            return total_revenue - total_cost


# Calculates total profit on certain date.
def report_profit(date, income):
    total_loss = 0
    with open("data/expired.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            expired = dict(buy_price=row[3], exp_date=row[5], stock_quantity=row[6])
            if date == expired["exp_date"]:
                loss = float(expired["buy_price"]) * int(expired["stock_quantity"])
                total_loss = total_loss + loss

        profit = round((report_revenue(date, income) - total_loss), 1)
        return profit