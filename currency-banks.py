from classes.Config import Config
from classes.MinfinCurrency import MinfinCurrency

config = Config(__file__, "config.json").read()
currency = MinfinCurrency()

for c in config["currencies"]:
    values = currency.getCurrencyValues(c, config["banks"])
    print(values)
