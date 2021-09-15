from classes.Config import Config

config = Config(__file__, "config.json").read()
print(config)
