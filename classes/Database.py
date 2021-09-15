import os
import sqlite3
from datetime import datetime


class Database:

    def __init__(self, filename):
        self.__filename = filename + ".sqlite3"
        self.__createFile()

    def __createFile(self):
        connection = None
        try:
            connection = sqlite3.connect(self.__filename)
            self.__createTableBanks(connection)
        except sqlite3.Error:
            pass
        finally:
            if connection:
                connection.close()

    def __createTableBanks(self, connection):
        cursor = connection.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS "banks" (
                "ID" INTEGER NOT NULL,
                "Alias" TEXT NOT NULL,
                "Title" TEXT NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT)
            );
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()

    def getLastRow(self, bank, currency):
        connection = None
        try:
            connection = sqlite3.connect(self.__filename)
            self.__checkCurrencyTable(connection, bank, currency)
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            query = f"""
                select 
                    "ID" as "id",
                    "DateTime" as "datetime",
                    "Bid" as "bid",
                    "Ask" as "ask"
                from 
                    currency_{bank}_{currency}
                order by 
                    DateTime desc
                limit 1;
            """
            cursor.execute(query)
            row = cursor.fetchone()
            cursor.close()
            return dict(row) if row is not None else False
        except sqlite3.Error:
            pass
        finally:
            if connection:
                connection.close()

    def insertRow(self, bank, currency, bid, ask, updated):
        connection = None
        try:
            connection = sqlite3.connect(self.__filename)
            self.__checkCurrencyTable(connection, bank, currency)
            cursor = connection.cursor()
            query = f"""
                insert into currency_{bank}_{currency} (
                    DateTime, Bid, Ask
                ) values (
                    "{updated}", {bid}, {ask}
                );
            """
            cursor.execute(query)
            connection.commit()
            cursor.close()
        except sqlite3.Error:
            pass
        finally:
            if connection:
                connection.close()

    def __checkCurrencyTable(self, connection, bank, currency):
        cursor = connection.cursor()
        query = f"""
            CREATE TABLE IF NOT EXISTS "currency_{bank.lower()}_{currency.lower()}" (
                "ID" INTEGER NOT NULL,
                "DateTime" TEXT NOT NULL,
                "Bid" REAL NOT NULL,
                "Ask" REAL NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT)
            );
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()
