import argparse
from matplotlib.pyplot import title
from helpers.buy_sell_products import buy_product, sell_product
from helpers.report_inventory import report_inventory
from helpers.report_finance import report_revenue, report_profit
from helpers.display_graphic import display_graphic
from datetime import date, timedelta, datetime
from rich.console import Console

__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


console = Console()
today = datetime.today().strftime("%d/%m/%Y")


# Advances time by given amount of days.
def advance_time(days=0):
    currentday = open("data/date.txt", "r").read()
    if len(currentday) == 0 and days == 0:
        new_date = today
    elif len(currentday) == 0 and days != 0:
        currentday = datetime.strptime(today, "%d/%m/%Y")
        new_date = (currentday + timedelta(days=days)).strftime("%d/%m/%Y")
        open("data/date.txt", "w").write(new_date)
    else:
        currentday = datetime.strptime(currentday, "%d/%m/%Y")
        new_date = (currentday + timedelta(days=days)).strftime("%d/%m/%Y")
        open("data/date.txt", "w").write(new_date)

    return new_date

# Checks if date is given in valid format.
def valid_date(s):
    try:
        return datetime.strptime(s, "%d/%m/%Y").strftime("%d/%m/%Y")
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)


# Creates all arguments for the command line
def parser():
    parser = argparse.ArgumentParser(description="SuperPy Inventory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser._positionals.title = "Positional arguments"
    parser._optionals.title = "Optional arguments"

    advance = subparsers.add_parser("advance-time", help="Advance time with given amount of days")
    advance.add_argument("-d", "--days", type=int, help="Amount of days", required=True)

    buy = subparsers.add_parser("buy", help="Buy product and add to inventory")
    buy.add_argument("-n", "--name", type=str, help="Name of product", required=True)
    buy.add_argument("-p", "--price", type=float, help="Price of product per unit", required=True)
    buy.add_argument("-q", "--quantity", type=int, help="Quantity of product", required=True)
    buy.add_argument("-e", "--exp_date", type=valid_date, help="Expiration date of product - format dd/mm/yyyy", required=True)

    sell = subparsers.add_parser("sell", help="Sell product, remove from inventory and add to sold list")
    sell.add_argument("-n", "--name", type=str, help="Name of sold product", required=True)
    sell.add_argument("-p", "--price", type=float, help="Sell price of product per unit", required=True)
    sell.add_argument("-q", "--quantity", type=int, help="Sold quantity of product", required=True)

    inventory = subparsers.add_parser("report_inventory", help="Report inventory of entered date")
    inventory.add_argument("-d", "--date", type=valid_date, help="Report inventory - format dd/mm/yyyy", default=advance_time())

    revenue = subparsers.add_parser("report_revenue", help="Report revenue of entered date")
    revenue.add_argument("-d", "--date", type=valid_date, help="Report revenue - format dd/mm/yyyy", default=advance_time())

    profit = subparsers.add_parser("report_profit", help="Report profit of entered date")
    profit.add_argument("-d", "--date", type=valid_date, help="Report profit - format dd/mm/yyyy", default=advance_time())

    graphic = subparsers.add_parser("graphic_revenue", help="Display revenue graphic of period between 2 given dates")
    graphic.add_argument("-s", "--start_date", type=valid_date, help="Start date of period to display - format dd/mm/yyyy", required=True)
    graphic.add_argument("-e", "--end_date", type=valid_date, help="Start date of period to display - format dd/mm/yyyy", required=True)

    graphic = subparsers.add_parser("graphic_profit", help="Display profit graphic of period between 2 given dates")
    graphic.add_argument("-s", "--start_date", type=valid_date, help="Start date of period to display - format dd/mm/yyyy", required=True)
    graphic.add_argument("-e", "--end_date", type=valid_date, help="Start date of period to display - format dd/mm/yyyy", required=True)

    return parser.parse_args()


def main():
    args = parser()

    if args.command == "advance-time":
        print(f"This is the new date: {advance_time(args.days)}")

    elif args.command == "buy":
        buy_product(advance_time(), args.name, args.price, args.exp_date, args.quantity)

    elif args.command == "sell":
        sell_product(args.name, args.quantity, args.price, advance_time())

    elif args.command == "report_inventory":
        report_inventory(args.date)

    elif args.command == "report_revenue":
        console.print(f"The revenue on {args.date}: €{report_revenue(args.date, 'revenue')}0", style="#fdca96")

    elif args.command == "report_profit":
        console.print(f"The profit on {args.date}: €{report_profit(args.date, 'profit')}0", style="#ABCED8")
    
    elif args.command == "graphic_revenue":
        display_graphic(args.start_date, args.end_date, "revenue")

    elif args.command == "graphic_profit":
        display_graphic(args.start_date, args.end_date, "profit")

    else:
        print ("\n Please enter valid input. \n"
               " Optional commands are buy, sell, report_revenue, report_profit, graphic_revenue, graphic_profit"
               "\n\n Type 'python super.py -h' for additional information.\n")

if __name__ == "__main__":
    main()
