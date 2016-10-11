

'''
def table_things(**kwargs):
    for name, value in kwargs.items():
        print '{0} = {1}'.format(name, value)

table_things(apple='fruit', cabbage='vegetable')
cabbage = vegetable
apple = fruit


def sorting(range):
    pass

MAX_RANDOM = 10

BooleanField
CharField
DateField
DateTimeField
EmailField
FileField
FloatField
ImageField
IntegerField
NullBooleanField
PositiveIntegerField
PositiveSmallIntegerField
SlugField
TextField
URLField
ForeignKey
OneToOneField

BooleanField = random.choice([True, False])
CharField = "Sample Post {}".format(randomize(range(MAX_RANDOM)))

AutoField = ''
BigAutoField = ''
BigIntegerField = ''
BinaryField =
BooleanField =
CharField =
CommaSeparatedIntegerField =
DateField =
DateTimeField =
DecimalField =
DurationField =
EmailField =
FileField =
FilePathField =
FloatField =
ImageField =
IntegerField =
GenericIPAddressField =
NullBooleanField =
PositiveIntegerField =
PositiveSmallIntegerField =
SlugField =
SmallIntegerField =
TextField =
TimeField =
URLField =
UUIDField =
'''


# djipsum.py


'''
else:
    self.stdout.write(
        self.style.WARNING('[-] Can not generate lorem ipsum!')
    )

import os
import sys
from django.conf import settings


def help():
    print("""
    Default 10 lorem     : $ ./manage.py djipsum <yourapp>"
    Custom maximum lorem : $ ./manage.py djipsum <yourapp> <max-lorem>"
    """)


def main():
    argv = sys.argv
    if len(argv) <= 1:
        return help()
    elif len(argv) == 2:
        app = argv[1]
        max_lorem = 10
        print(app, max_lorem)
        print(settings.INSTALLED_APPS)
    elif len(argv) == 3:
        app = argv[1]
        try:
            max_lorem = int(argv[2])
        except ValueError:
            print(argv[2], ' => Invalid number `max_lorem`!')
            sys.exit()
        print(app, max_lorem)
    else:
        return help()

if __name__ == '__main__':
    main()
'''
