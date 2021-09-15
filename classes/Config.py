import os
import json

# глобальные настройки скрипта
class Config:

    def __init__(self, dir, filename = 'config.json'):
        self._path = os.path.dirname(os.path.realpath(dir))
        self._filename = filename
        self._status = os.path.isfile("%s/%s" % (self._path, self._filename))

    def read(self):
        if not self._status:
            return None
        with open(self._filename) as content:
            config = json.load(content)
        return config
