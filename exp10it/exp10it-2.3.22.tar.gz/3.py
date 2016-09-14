from exp10it import *
import urlparse
#get_http_domain_pattern_from_uri("http://ssldkf.slkj.noa./")
tmp=urlparse.urlparse("http://www.baidu.com/a/1.php?aho=1&2")
print tmp.netloc
print tmp.path
print tmp.scheme+"://"+tmp.netloc+tmp.path
