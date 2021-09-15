from classes.Config import Config
from classes.MinfinCurrency import MinfinCurrency
from classes.Database import Database
from classes.TelegramBot import TelegramBot


config = Config(__file__, "config.json").read()
currency = MinfinCurrency()
db = Database(config["sqlite"])
bot = TelegramBot(config["telegram"]["bot-token"])

for c in config["currencies"]:
    results = currency.getCurrencyValues(c, config["banks"])
    for (index, val) in enumerate(results["values"]):
        lastRow = db.getLastRow(val["bank_id"], c) or {}
        if not lastRow or lastRow and lastRow["datetime"] != val["updated"]:
            db.insertRow(val["bank_id"], c, val["bid"], val["ask"], val["updated"])
        for i in ["bid", "ask"]:
            diff = (val[i] - lastRow[i]) if lastRow else 0
            if diff == 0:
                val[f"{i}_icon"] = "-"
            else:
                val[f"{i}_icon"] = "up" if diff > 0 else "down"
        results["values"][index] = val
    bot.sendMessage(config["telegram"]["chat_id"], results)
