import csv
import os
import datetime
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
from rich.console import Console

console = Console()

# Generates unique ID for each new line in each csv file
def generate_id(file_name):
    with open(file_name, "r") as file:
        csvReader = csv.reader(file)
        lines = []
        for line in csvReader:
            if line != []:
                lines.append(line)

        if len(lines) == 1:
            id_number = f"0{str(1)}"
            return id_number
        else:
            last_added = lines[-1]
            id_number = str(int(last_added[0]) + 1)
            if len(id_number) < 2:
                id_number = f"0{str(id_number)}"

    # Getting rid of blank lines
    f = open(file_name, "w+", newline="")
    f.truncate()
    f.close()
    with open(file_name, "w", newline="") as newfile:
        write = csv.writer(newfile)
        write.writerows(lines)
        
    return id_number


# Returns total available stock of a product in inventory
def get_total_stock(product):
    with open("data/inventory.csv", "r") as file:
        total_count = 0
        for line in file.readlines():
            if product in line:
                product_line = line.split(",")
                quantity = int(product_line[5])
                total_count += quantity
    return total_count


# Adds new product to inventory file
def buy_product(currentday, name, price, exp_date, quantity):
    id = generate_id("data/inventory.csv")
    new_product = [id, name, currentday, price, exp_date, quantity]
    with open("data/inventory.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(new_product)
        console.print(f"{quantity} pieces of {name} are added to the inventory.", style="#96fdca")


# Updates sold.csv and expired.csv files
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


# Updates inventory.csv file
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


# When a product is sold, this function checks if there is enough stock is available for selling 
# by checking quantities and expiration dates. 
# It automatically removes sold and/or expired stock.
def check_and_update_stock(product_name, sold_quantity, sell_price, sell_date):
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
                cur = datetime.strptime(sell_date, "%d/%m/%Y")
                
                if cur < exp:
                    stock = int(product["quantity"])

                    if stock >= sold_quantity and cur < exp:
                        stock = stock + updated_stock
                        stock = stock - sold_quantity
                        product["quantity"] = str(stock)
                        update_csv_file(product, sold_quantity, sell_price, sell_date, "data/sold.csv")
                        if stock <= 0: products_in_stock.remove(product)
                        console.print(f"{sold_quantity} pieces of {product_name} are removed from inventory.", style="#FBDBDF")
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


# Removes products from inventory.
def sell_product(sold_product_name, sold_quantity, sell_price, sell_date):
    total_stock = get_total_stock(sold_product_name)

    if total_stock >= sold_quantity:
        update_inventory_file(check_and_update_stock(sold_product_name, sold_quantity, sell_price, sell_date))

    elif total_stock > 0:
        return console.print(f"You do not have enough stock, you can sell a maximum of {total_stock} 😅", style="#fdca96")
    else:
        return console.print(f"You do not have any {sold_product_name} in stock 😟", style="#fd9796")