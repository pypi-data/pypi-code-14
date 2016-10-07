from pyrex import email

def test_valid_email():
  assert email("test123@domain.com")
  assert email("test1.test2+test3@sub.domain.com")

def test_invalid_email():
  assert not email("not-an-email")
  assert not email("test@test")
  assert not email("test@test.")
  assert not email("@test.com")

def test_valid_domain():
  assert email("test@domain.com", domain="domain.com")
  assert email("test@sub.domain.com", domain="sub.domain.com")

def test_invalid_domain():
  assert not email("test@domain.com", domain="invalid.com")
  assert not email("test@domain.com", domain="sub.domain.com")
  assert not email("test@sub.domain.com", domain="domain.com")
