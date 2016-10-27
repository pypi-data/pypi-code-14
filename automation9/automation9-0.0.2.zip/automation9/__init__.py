import names

def random_username(sex='female', no_of_digits=3):
    import random
    digits = random.randrange(100,1000) # interger from 100 to 999
    #first_name = names.get_first_name(gender=sex)
    fullname = names.get_full_name(gender=sex)
    return fullname.replace(" ","") + str(digits)
