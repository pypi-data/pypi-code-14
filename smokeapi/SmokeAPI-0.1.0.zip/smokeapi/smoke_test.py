from smokeapi import SmokeAPI, SmokeAPIError
SMOKE = SmokeAPI('aa6cb28600cfa209789a33284bca4b025beed39c5dfb171d5030c88189403d81')
try:
	post_ids = [44800, 44799, 800000]
	posts = SMOKE.fetch('posts', ids=post_ids)
except SmokeAPIError as e:
    print("   Error URL: %s" % (e.url))
    print("   Error Code: %s" % (e.error_code))
    print("   Error Name: %s" % (e.error_name))
    print("   Error Message: %s" % (e.error_message))

import pprint
pprint.pprint(posts)