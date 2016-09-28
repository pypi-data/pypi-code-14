import django.core.cache

def put(key, value, timeout):
    django.core.cache.cache.set(key, value, timeout)
    
def get(key):
    return django.core.cache.cache.get(key)

def delete(key):
    django.core.cache.cache.delete(key)
    
def clear():
    django.core.cache.cache.clear()
