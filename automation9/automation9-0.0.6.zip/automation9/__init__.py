import names
import requests

def random_username(sex='female', no_of_digits=3):
    import random
    digits = random.randrange(100,1000) # interger from 100 to 999
    #first_name = names.get_first_name(gender=sex)
    fullname = names.get_full_name(gender=sex)
    return fullname.replace(" ","") + str(digits)

def get_temp_email_online():
    """
    service: 'guerilla', 'getairmail'
    """
    r = requests.get('https://api.guerrillamail.com/ajax.php?f=get_email_address&lang=en')
    email = r.json()['email_addr']
    sid_token = r.json()['sid_token']
    return email, sid_token

def custom_guerrilla_mail_session(**kwargs):
    """
    get new email -> read the content -> click link
    """
    from guerrillamail import GuerrillaMailSession
    aSession = GuerrillaMailSession()
    aSession.get_session_state()
##    print(session.get_email_list()[0].guid)
##    mail_body = aSession.get_email(1).body
##    print(aSession.session_id)
    aSession.set_email_address(kwargs['username'])
    return aSession
##    return {
##        'email': aSession.email_address,
##        'username': aSession.email_address.split('@')[0],
##        'password': kwargs['password'],
##        }
    
if __name__ == "__main__":
    session = get_guerrilla_mail_session()
    print(session.session_id)
##    print(session.email_address)
##    print(session.get_email_list()[0].guid)
