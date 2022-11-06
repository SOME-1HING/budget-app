from itertools import zip_longest
from collections import OrderedDict


class Category:
    def __init__(self, name):
        self.name = name
        self.total = 0.00
        self.ledger = []

    def __repr__(self):
        response = f"{self.name:*^30}\n"
        for item in self.ledger:
            response += f'{item["description"][0:23]:23}{item["amount"]:>7.2f}\n'
        response += f"Total: {self.total}"
        return response

    def deposit(self, amount, description=""):
        self.total += amount
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.total -= amount
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return self.total

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + category.name)
            category.deposit(amount, "Transfer from " + self.name)
            return True

        return False

    def check_funds(self, amount):
        if self.total >= amount:
            return True
        return False


def roundup(x):
    x = round((round(x) / 10) + 0.5) * 10
    return x


def create_spend_chart(categories):
    text = "Percentage spent by category\n"

    total = 0
    cats = OrderedDict()
    for cat in categories:
        cat_total = 0
        for item in cat.ledger:
            amount = item["amount"]
            if amount < 0:
                total += amount
                cat_total += amount
        cats[cat.name] = abs(cat_total)

    for key, val in cats.items():
        percent = (val / abs(total)) * 100
        cats[key] = roundup(percent)

    for i in range(100, -10, -10):
        text += f"{i}|".rjust(4)
        for val in cats.values():
            if val > i:
                text += " o "
            else:
                text += "   "
        text += " \n"

    length = len(cats.values())
    text += "    " + "-" * (length * 3 + 1) + "\n"

    temp_string = ""
    for key in cats.keys():
        temp_string += key.lower().capitalize() + " "
    for x in zip_longest(*temp_string.split(), fillvalue=" "):
        text += "     " + "  ".join(x) + "  \n"
    text = text.rstrip() + "  "
    return text
