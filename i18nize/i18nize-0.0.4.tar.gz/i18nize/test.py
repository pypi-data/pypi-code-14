from client import Client

client = Client(
    project_id='86416ce4-fd52-4daf-9764-46f35b07af23',
    destination_dir='locales/',
    live=False)

client.get_all_locales()
