from client import Client
client = Client(config_path='i18nize.json', destination_path='hello/')
client.get_all_locales()