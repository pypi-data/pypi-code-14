import re

email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

# Checks whether `email` is a valid email address
def email(email, domain=None):
  if not email:
    return False

  if type(email) is not str:
    raise TypeError("email must be a string")

  # Email addresses are limited to 254 characters
  if len(email) > 254:
    return False

  is_valid = email_regex.match(email) is not None

  # Check if address ends with given domain (optional)
  if domain is not None:
    if type(domain) is not str:
      raise TypeError("domain must be a string")
    is_valid = is_valid and email.endswith("@" + domain)

  return is_valid
