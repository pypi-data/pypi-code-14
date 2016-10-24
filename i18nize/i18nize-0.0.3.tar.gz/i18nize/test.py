from client import Client

i18nize_config = {
    "PROJECT_ID": "86416ce4-fd52-4daf-9764-46f35b07af23",
    "LIVE": False,
    'DESTINATION_DIR': 'locales/',
}

client = Client(config=i18nize_config)
client.get_all_locales()
