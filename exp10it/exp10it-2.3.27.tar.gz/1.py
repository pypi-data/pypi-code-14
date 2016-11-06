from exp10it import Xcdn
ip=Xcdn("www.catholic.org.hk").return_value
if ip!=0:
    print(ip)
