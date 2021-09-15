import telebot
from datetime import datetime


class TelegramBot:

    __icons = {
        "up": "\U0001F53A",
        "down": "\U0001F53B",
        "-": "", #"\U00002796",
        "bank": "\U0001F3E6",
    }

    def __init__(self, token):
        self.bot = telebot.TeleBot(token, parse_mode="HTML")

    def __arrow(self, icon):
        return str(self.__icons[icon])

    def __prepareMessage(self, results):
        message = [f'<b>{results["title"]}</b>', ""]

        for val in results["values"]:
            val["updated"] = datetime.strptime(val["updated"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M %d.%m.%y")
            message.append(f'{self.__icons["bank"]} <b>{val["bank_name"]}</b>')
            message.append(" / ".join([
                f'{self.__arrow(val["bid_icon"])} <code>{val["bid"]:.2f}</code>'.strip(),
                f'{self.__arrow(val["ask_icon"])} <code>{val["ask"]:.2f}</code>'.strip(),
            ]))
            message.append(f'(<i>{val["updated"]}</i>)')
            message.append("")
        return "\n".join(message)

    def sendMessage(self, chat_id, results):
        try:
            self.bot.send_message(chat_id, self.__prepareMessage(results))
            return True
        except Exception as e:
            print(e)
            return False
