from itertools import zip_longest
from collections import OrderedDict
import math

0.7
7.0
2.2


def roundup(x):
    x = round(x) / 10
    x = round(x + 0.5)
    return x * 10


class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = list()

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        total = 0
        for item in self.ledger:
            items += (
                f"{item['description'][0:23]:23}" + f"{item['amount']:>7.2f}" + "\n"
            )
            total += item["amount"]
        output = title + items + "Total: " + str(total)
        return output

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        total_cash = 0
        for item in self.ledger:
            total_cash += item["amount"]
        return total_cash

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + category.name)
            category.deposit(amount, "Transfer from " + self.name)
            return True

        return False

    def check_funds(self, amount):
        if self.get_balance() >= amount:
            return True
        return False


def verticalPrint(astring):
    wordList = astring.split(" ")
    wordAmount = len(wordList)

    maxLen = 0
    for i in range(wordAmount):
        length = len(wordList[i])
        if length >= maxLen:
            maxLen = length

    ### makes all words the same length to avoid range errors ###
    for i in range(wordAmount):
        if len(wordList[i]) < maxLen:
            wordList[i] = wordList[i] + (" ") * (maxLen - len(wordList[i]))

    for i in range(wordAmount):
        for j in range(maxLen):
            print(wordList[i][j])


def create_spend_chart(categories):
    s = "Percentage spent by category\n"

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

    for n in range(100, -10, -10):
        s += f"{n}|".rjust(4)
        for val in cats.values():
            if val > n:
                s += " o "
            else:
                s += "   "
        s += " \n"

    length = len(cats.values())
    s += "    " + "-" * (length * 3 + 1) + "\n"

    temp_string = ""
    for key in cats.keys():
        temp_string += key.lower().capitalize() + " "
    for x in zip_longest(*temp_string.split(" "), fillvalue=" "):
        s += "     " + "  ".join(x) + "  \n"

    return s


food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")

food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)
hmm = create_spend_chart([business, food, entertainment])

lul = "Percentage spent by category\n100|          \n 90|          \n 80|          \n 70|    o     \n 60|    o     \n 50|    o     \n 40|    o     \n 30|    o     \n 20|    o  o  \n 10|    o  o  \n  0| o  o  o  \n    ----------\n     B  F  E  \n     u  o  n  \n     s  o  t  \n     i  d  e  \n     n     r  \n     e     t  \n     s     a  \n     s     i  \n           n  \n           m  \n           e  \n           n  \n           t  "

print(bool(hmm == lul))
print(hmm)
