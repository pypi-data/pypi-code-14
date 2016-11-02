import names
import requests
from guerrillamail import GuerrillaMailSession

def random_username(sex='female', no_of_digits=3):
    import random
    digits = random.randrange(100,1000) # interger from 100 to 999
    #first_name = names.get_first_name(gender=sex)
    fullname = names.get_full_name(gender=sex)
    return fullname.replace(" ","") + str(digits)

def custom_guerrilla_mail_session(**kwargs):
    """
    get new email -> read the content -> click link
    """
    aSession = GuerrillaMailSession()
    aSession.get_session_state()
    aSession.set_email_address(kwargs['username'])
    return aSession

def MAIL_get_verification_link(mailSessionID=None, subjectPattern=None, linkPattern=r"", mailService="Guerrilla"):
    import re
    if mailService == "Guerrilla":
        _mailSession = GuerrillaMailSession(mailSessionID)
        for mail in _mailSession.get_email_list():
            if subjectPattern in mail.subject:
                fetch_mail = _mailSession.get_email(mail.guid)
                body = fetch_mail.body
                m = re.search(linkPattern, body)
                if m:
                    link = m.group('veri_link')
                    print("LINK FOUND: "+link)
                    return link
    return 

def screenshot_captcha(webDriver, element, path):
    from selenium.webdriver import ActionChains
    from PIL import Image
    action_chain = ActionChains(webDriver)
    action_chain.move_to_element(element)
    action_chain.perform()
    loc, size = element.location_once_scrolled_into_view, element.size
    left, top = loc['x'], loc['y']
    width, height = size['width'], size['height']
    box = (int(left), int(top), int(left + width), int(top + height))
    webDriver.save_screenshot(path)
    image = Image.open(path)
    captcha = image.crop(box)
    captcha.save(path, 'PNG')   
    
if __name__ == "__main__":
    session = get_guerrilla_mail_session()
    print(session.session_id)
##    print(session.email_address)
##    print(session.get_email_list()[0].guid)
##    mail_body = aSession.get_email(1).body
