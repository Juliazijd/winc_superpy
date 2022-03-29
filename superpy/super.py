import sys
import os
from helpers.buy_sell_products import buy_product, sell_product
from helpers.report_inventory import report_inventory
from helpers.report_finance import report_revenue, report_profit
from helpers.display_graphic import display_graphic
from datetime import date, timedelta
from rich.console import Console

__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


console = Console()

today = date.today().strftime("%d/%m/%Y")
yesterday = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")


def main():
    args = sys.argv
    if args[1] == "report":
        report = input("Of what do you want to see a report? Enter inventory / revenue / profit: ")
        if report == "inventory":
            day = input(f"Of what day do you want to see {report}? Enter today / yesterday / other: ")
            if day == "today":
                report_inventory(today)
            elif day == "yesterday":
                report_inventory(yesterday)
            elif day == "other":
                date = input("Enter a date (dd/mm/yyyy): ")
                report_inventory(date)

        elif report == "revenue":
            day = input(f"Of what day do you want to see {report}? Enter today / yesterday / other: ")
            if day == "today":
                console.print(f"Today's revenue so far is €{report_revenue(today, day)}0", style="#fdca96")
            elif day == "yesterday":
                console.print(f"Yesterday's revenue was €{report_revenue(yesterday, day)}0", style="#fdca96")
            elif day == "other":
                date = input("Enter a date (dd/mm/yyyy): ")
                console.print(f"On {date} the revenue was €{report_revenue(date, day)}0", style="#fdca96")

        elif report == "profit":
            day = input(f"Of what day do you want to see {report}? Enter today / yesterday / other: ")
            if day == "today":
                console.print(f"Today's profit so far is €{report_profit(today, day)}0.", style="#fdca96")
            elif day == "yesterday":
                console.print(f"Yesterday's profit was €{report_profit(yesterday, day)}0", style="#fdca96")
            elif day == "other":
                date = input("Enter a date (dd/mm/yyyy): ")
                console.print(f"On {date} the profit was €{report_profit(date, day)}0", style="#fdca96")

    elif args[1] == "graphic":
        income = input("Of which income do you want to see a graphic? Enter revenue / profit: ")
        start_date = input("Enter a start date (dd/mm/yyyy): ")
        end_date = input("Enter a date (dd/mm/yyyy): ")
        if income == "revenue":
            display_graphic(start_date, end_date, income)
        elif income == "profit":
            display_graphic(start_date, end_date, income)
        else:
            print(f"{income} is not a valid entry, please try again.")

    elif args[1] == "buy":
        buy_product()

    elif args[1] == "sell":
        sell_product()

    elif args[1] == "--help" or "-h":
        console.print(f"usage: {os.getcwd()}        \n\
            ARGUMENTS \n\
            report:     report inventory, revenue or profit for today, yesterday or a specific past date.\n\
            graphic:    display graphic of revenue or profit of a certain period in the past.\n\
            sell:       remove a product from the inventory and add it to the sold file.\n\
            buy:        add product to the inventory.\
            \n\
            The options to choose from will be displayed after entering an argument.",
            style="#c8a2c8")


if __name__ == "__main__":
    main()
