import csv
from datetime import datetime
from tabulate import tabulate
from rich.console import Console

console = Console()

# Returns a table with the inventory on the given date.
# It adjusts the inventory by checking the expired.csv and sold.csv files 
# and putting the right products back into or removing from the inventory.
def report_inventory(date):
    report_date = datetime.strptime(date, "%d/%m/%Y")
    inventory = []

    with open("data/inventory.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            product = dict(id=row[0], product_name=row[1], buy_date=row[2], buy_price=row[3], exp_date=row[4], quantity=row[5])
            inventory.append(product)

    with open("data/expired.csv", "r") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            product = dict(id=row[2], product_name=row[1], buy_date=row[4], buy_price=row[3], exp_date=row[5], quantity=row[6])
            inventory.append(product)

    for product in inventory[1:]:
        exp_date = datetime.strptime(product["exp_date"], "%d/%m/%Y")
        if report_date >= exp_date:
            inventory.remove(product)

    with open("data/sold.csv", "r") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            sold_product = dict(id=row[2], product_name=row[1], buy_date=row[4], buy_price=row[3], exp_date=row[5], quantity=row[9])
            sell_date = dict(sell_date=row[7])
            sell_date = datetime.strptime(sell_date["sell_date"], "%d/%m/%Y")
            if report_date < sell_date:
                count = 0
                for product in inventory[1:]:
                    if sold_product["id"] == product["id"]:
                        total_stock = int(sold_product["quantity"]) + int(product["quantity"])
                        product["quantity"] = str(total_stock)
                        count += 1
                if count == 0:
                    inventory.append(sold_product)
    
    console.print(f"Inventory {date}", style="bold #c8a2c8")
    return console.print(tabulate(inventory, headers="firstrow", tablefmt="fancy_grid"), style="#c8a2c8")
