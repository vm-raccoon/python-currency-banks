from requests_html import HTMLSession
from datetime import datetime


class MinfinCurrency:

    __uri = "https://minfin.com.ua/currency/banks/[CURRENCY]/[DATE]"
    __allowed_currencies = {
        "usd": "Доллар",
        "eur": "Евро",
        "rub": "Рубль",
    }

    def getCurrencyTitle(self, currency_name):
        return self.__allowed_currencies[currency_name.lower()] or None;

    def getCurrencyValues(self, currency_name, banks=None):
        if not self.__is_currency_allowed(currency_name):
            return False
        return {
            "title": self.getCurrencyTitle(currency_name),
            "values": self.__getTableContent(currency_name, banks),
        }

    def __is_currency_allowed(self, currency_name):
        return currency_name.lower() in self.__allowed_currencies

    def __getTableContent(self, currency_name, banks):
        uri = self.__prepareUriTemplate(currency_name)
        session = HTMLSession()
        page = session.get(uri)
        table = page.html.find("#smTable", first=True)
        page.close()
        session.close()
        return self.__parseTableRows(table, banks)

    def __prepareUriTemplate(self, currency_name, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        return self.__uri \
            .replace("[CURRENCY]", currency_name) \
            .replace("[DATE]", date)

    def __parseTableRows(self, table, banks):
        rows = []
        for row in table.find("tbody > tr"):
            row = self.__parseTableRow(row)
            if row["bank_id"] in banks:
                rows.append(row)
        return rows

    def __parseTableRow(self, row):
        td = row.find("td")
        bank_id = td[0].find("a", first=True).attrs["href"].replace("/company/", "").replace("/", "")
        bank_name = td[0].text.strip()
        bid = float(td[1].text.strip())
        ask = float(td[3].text.strip())
        updated = datetime.strptime(td[7].text.strip(), "%Y.%m.%d %H:%M").strftime("%Y-%m-%d %H:%M:%S")
        return {
            "bank_id": bank_id,
            "bank_name": bank_name,
            "bid": bid,
            "ask": ask,
            "updated": updated,
        }




