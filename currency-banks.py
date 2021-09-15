from classes.Config import Config
from classes.MinfinCurrency import MinfinCurrency
from classes.Database import Database


config = Config(__file__, "config.json").read()
currency = MinfinCurrency()
db = Database(config["sqlite"])
# print(db.getLastRow("privatbank", "usd"))

for c in config["currencies"]:
    # print(c)
    result = currency.getCurrencyValues(c, config["banks"])
    for (index, val) in enumerate(result["values"]):
        lastRow = db.getLastRow(val["bank_id"], c) or {}
        if not lastRow or lastRow and lastRow["datetime"] != val["updated"]:
            db.insertRow(val["bank_id"], c, val["bid"], val["ask"], val["updated"])
        for i in ["bid", "ask"]:
            diff = (val[i] - lastRow[i]) if lastRow else 0
            if diff == 0:
                val[f"{i}_icon"] = "-"
            else:
                val[f"{i}_icon"] = "up" if diff > 0 else "down"
        result["values"][index] = val
        # print()
        # print(lastRow)
        print(val)
    print()
    print(result)
    print()
