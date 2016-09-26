from floraconcierge.shortcuts import get_apiclient


def search(phone, short=None):
    return get_apiclient().services.phone.search(phone, short=short)
