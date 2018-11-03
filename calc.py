import sys


class Mortgage():

    def __init__(self, val, fee,  years, fix_len, fix_int, var_int, add_fix=0, add_var=0):

        self.val = val
        self.fee = fee
        self.years = years
        self.installments = years * 12

        self.fixed = self.generate("Fixed", 0, fix_len, fix_int, val, add_fix)
        self.var = self.generate("Variable", fix_len, years,  var_int, self.fixed["end_val"], add_var)

        self.total_paid = self.fixed["total_paid"] + self.var["total_paid"] + self.fee
        self.total_interest = self.total_paid - self.val
        print
        print ("Mortgage of {} over {} years".format(self.val, self.years))
        print ("{} years at {}%, paying base of {} and additional {} per month"\
            .format(self.fixed["length"], self.fixed["int"] * 100, int(self.fixed["repay"]), self.fixed["additional"]))
        print ("{} years at {}%, paying base of {} and additional {} per month"\
            .format(self.var["length"], self.var["int"] * 100, int(self.var["repay"]), self.var["additional"]))

        print ("Fee : {}".format(self.fee))
        print ("Total Paid: {}".format(int(self.total_paid)))
        print ("Total Interest : {}".format(int(self.total_interest)))

        print("Finish in year %.2f" % self.finish_year)

    def generate(self, name, start, end, int, start_val, additional):
        period = {}
        period["name"] = name
        period["start"] = start
        period["end"] = end
        period["length"] = end - start
        period["installments"] = (end - start)* 12
        period["int"] = int / 100
        period["int_installment"] = int / (100 * 12)
        period["initial_int"] = start_val * period["int_installment"]
        period["additional"] = additional

        period["repay"]= self.repay(period)
        period["start_val"] = start_val
        values = self.value(period)
        period["installments_completed"] = values[0]
        period["end_val"] = values[1]
        period["total_paid"] = self.total(period)
        return period

    def repay(self, period):
        # calculate payment during fixed period
        # and total paid during this period
        denominator = 1 - ( 1 + period["int_installment"] ) ** - ((self.years - period["start"]) * 12)

        repay = period["initial_int"] / float(denominator)

        print("{} Period min repay: {}".format(period["name"], round(repay, 2)))
        return repay

    def value(self, period):
        installments = period["installments"]
        repay_amount = period["repay"] + period["additional"]

        value = period["start_val"]
        for i in range(installments):
            value = value * (1 + period["int_installment"]) - repay_amount
            if value <= 1 :
                break

        self.finish_year = period["start"] + (i+1)/ 12
        print ( "{} Period end value of {}".format(period["name"], round(value,2)))
        return (i+1, value)

    def total(self, period):
        total = period["installments_completed"] * (period["repay"] + period["additional"])
        print ("{} Period total paid {}".format(period["name"], round(total, 2)))
        return total

if __name__ == "__main__":

    args = sys.argv
    print(args)
    if len(args) == 1:
        print("""
        usage :<mortgage val> <fee>  <length in years>
        <fixed rate length in years> <fixed rate interest>
        <variable rate interest>
        <additional payments in fixed period> <addition paymsents in variable period>
        """)

    else:
        val = int(args[1])
        fee = int(args[2])
        years = int(args[3])
        fix_len = int(args[4])
        fix_int = float(args[5])
        var_int = float(args[6])
        add_fix = int(args[7])
        add_var = int(args[8])

        mortgage = Mortgage(val, fee, years, fix_len, fix_int, var_int, add_fix, add_var)
