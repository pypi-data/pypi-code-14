import names
import requests


def random_username(sex='female', no_of_digits=3):
    import random
    digits = random.randrange(100,1000) # interger from 100 to 999
    #first_name = names.get_first_name(gender=sex)
    fullname = names.get_full_name(gender=sex)
    return fullname.replace(" ","") + str(digits)

##def get_temp_email_online():
##    """
##    service: 'guerilla', 'getairmail'
##    """
##    r = requests.get('https://api.guerrillamail.com/ajax.php?f=get_email_address&lang=en')
##    email = r.json()['email_addr']
##    sid_token = r.json()['sid_token']
##    return email, sid_token

def custom_guerrilla_mail_session(**kwargs):
    """
    get new email -> read the content -> click link
    """
    from guerrillamail import GuerrillaMailSession
    aSession = GuerrillaMailSession()
    aSession.get_session_state()
    aSession.set_email_address(kwargs['username'])
    return aSession

def get_captcha(webdriver, element, path):
    from selenium.webdriver import ActionChains
    from PIL import Image
    action_chain = ActionChains(driver)
    action_chain.move_to_element(element)
    action_chain.perform()
    loc, size = element.location_once_scrolled_into_view, element.size
    left, top = loc['x'], loc['y']
    width, height = size['width'], size['height']
    box = (int(left), int(top), int(left + width), int(top + height))
    driver.save_screenshot(path)
    image = Image.open(path)
    captcha = image.crop(box)
    captcha.save(path, 'PNG')   
    
if __name__ == "__main__":
    session = get_guerrilla_mail_session()
    print(session.session_id)
##    print(session.email_address)
##    print(session.get_email_list()[0].guid)
##    mail_body = aSession.get_email(1).body
