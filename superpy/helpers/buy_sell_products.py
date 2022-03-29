import csv
import os
import datetime
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
from rich.console import Console

console = Console()

current_date = date.today().strftime("%d/%m/%Y")

yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.strftime("%d/%m/%Y")


def generate_id(file_name):
    with open(file_name, "r") as csvfile:
        last_added = csvfile.readlines()[-1]
        if len(csvfile.read()) == 1:
            id_number = 1
            return id_number
        id_number = last_added.split(",", 1)[0]
        csvfile.close()
        id_number = int(id_number) + 1
        id_number = str(id_number)
        if len(id_number) < 2:
            return f"0{str(id_number)}"
        else:
            return id_number


def get_total_stock(product):
    with open("/Users/JULIA/Winc/SuperPy/superpy/data/inventory.csv", "r") as file:
        total_count = 0
        for line in file.readlines():
            if product in line:
                product_line = line.split(",")
                quantity = int(product_line[5])
                total_count += quantity
    return total_count


def buy_product():
    id = generate_id("data/inventory.csv")
    name = input("Enter name of bought product: ")
    price = input("Enter purchase price (50 cents = 0.5): ")
    exp_date = input("Enter experation date (dd/mm/yyyy): ")
    quantity = int(input("Enter amount of purchased product: "))
    new_product = [id, name, current_date, price, exp_date, quantity]
    with open("data/inventory.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(new_product)
        console.print(f"{quantity} pieces of {name} are added to the inventory.", style="#96fdca")


def sell_product():
    sold_product_name = input("Which product did you sell? ")
    sold_quantity = int(input(f"How many of {sold_product_name} did you sell? "))
    total_stock = get_total_stock(sold_product_name)

    if total_stock >= sold_quantity:
        update_inventory_file(check_and_update_stock(sold_product_name, sold_quantity))
    elif total_stock > 0:
        return console.print(f"You do not have enough stock, you can sell a maximum of {total_stock} 😅", style="#fdca96")
    else:
        return console.print(f"You do not have any {sold_product_name} in stock 😟", style="#fd9796")


def check_and_update_stock(product_name, sold_quantity):
    products_in_stock = []
    with open("data/inventory.csv", "r") as csvfile:
        readCSV = csv.reader(csvfile,delimiter=",")

        for row in readCSV:
            product = dict(id=row[0], product_name=row[1], buy_date=row[2], buy_price=row[3], exp_date=row[4], quantity=row[5])
            products_in_stock.append(product)

        updated_stock = 0
        for product in products_in_stock[1:]:
            
            if product["product_name"] == product_name:
                exp = datetime.strptime(product["exp_date"], "%d/%m/%Y")
                cur = datetime.strptime(current_date, "%d/%m/%Y")
                
                if cur < exp:
                    sell_price = float(input(f"For what price a piece do you sell the {product_name}? "))
                    stock = int(product["quantity"])

                    if stock >= sold_quantity and cur < exp:
                        stock = stock + updated_stock
                        stock = stock - sold_quantity
                        product["quantity"] = str(stock)
                        update_csv_file(product, sold_quantity, sell_price, current_date, "data/sold.csv")
                        if stock <= 0: products_in_stock.remove(product)
                        return products_in_stock
                    elif stock < sold_quantity and cur < exp:
                        stock = stock + updated_stock
                        updated_stock = stock - sold_quantity
                        sold_quantity = 0
                        product["quantity"] = str(updated_stock)
                        if updated_stock <= 0: products_in_stock.remove(product)
                
                elif cur >= exp and int(product["quantity"]) < get_total_stock(product["product_name"]):
                    products_in_stock.remove(product)
                    update_csv_file(product, 0, 0, "--", "data/expired.csv")
                    continue
                else:
                    console.print(f"Unfortunately your {product_name} stock is expired 🤭", style="#fd9796")
                    sold_quantity = 0
                    sell_price = 0
                    sell_date = "--"
                    products_in_stock.remove(product)
                    update_csv_file(product, sold_quantity, sell_price, sell_date, "data/expired.csv")
                    return products_in_stock


def update_csv_file(product, sold_quantity, sell_price, sell_date, file_name):
    id = generate_id(file_name)
    product = {
        "id": id,
        "product_name": product["product_name"],
        "buy_id": product["id"],
        "buy_price": product["buy_price"],
        "buy_date": product["buy_date"],
        "exp_date": product["exp_date"],
        "stock_quantity": product["quantity"],
        "sell_date": sell_date,
        "sell_price": sell_price,
        "sold_quantity": sold_quantity
    }
    with open(file_name, "a+", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
                                "id","product_name","buy_id","buy_price","buy_date",
                                "exp_date","stock_quantity","sell_date",
                                "sell_price","sold_quantity"])
        writer.writerow(product)


def update_inventory_file(inventory_dict):
    csv_header = inventory_dict[0].keys()
    updated_csv_file = "data/new_inventory.csv"
    with open(updated_csv_file, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        writer.writeheader()
        for product in inventory_dict[1:]:
            writer.writerow(product)
    old_csv_file = "data/inventory.csv"
    if (os.path.exists(old_csv_file) and os.path.isfile(old_csv_file)):
        os.remove(old_csv_file)
        os.rename(updated_csv_file, old_csv_file)