from datetime import datetime
from math import ceil

available_amount = 517000


def TLB(number: int):
    global available_amount
    if available_amount - number >= 0:
        available_amount -= number
        return number
    else:
        return 0


def GLB(number: int):
    global available_amount
    available_amount += number


def interest_rate_for_every_month(start_debt, months, interest_rate=0.3):
    return ceil(start_debt * ((1 + interest_rate) ** months))


class Client:

    def __init__(self, login, password, fullname, debt=0, date=0):
        self.login = login
        self.password = password
        self.fullname = fullname
        self.debt = debt
        self.date = date

    def tale_a_loan(self, number):
        self.debt += TLB(number)
        self.date = datetime.now()

    def give_credit(self, number):
        months = ceil((datetime.now() - self.date).days / 28)
        loan = interest_rate_for_every_month(self.debt, months)
        if number == loan:
            GLB(number)

    def show_debt(self):
        return interest_rate_for_every_month(self.debt, ceil((datetime.now() - self.date).days / 28))


def main():
    C = Client("jdc", "dnwcwe", "jHbjbjdcb")
    C1 = Client("jdc", "dnwcwe", "jHbjbjdcb")
    C.tale_a_loan(100000)
    C1.tale_a_loan(100000)
    C.date = datetime(2021, 10, 22)
    #  print(C.show_debt())
    C.give_credit(3937377)


if __name__ == "__main__":
    main()
