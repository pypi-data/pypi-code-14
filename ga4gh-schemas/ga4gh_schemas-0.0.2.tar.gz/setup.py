# Don't import __future__ packages here; they make setup fail

import ga4gh_common.setup as setup

packageDict = {
    "name": "ga4gh_schemas",
    "description": "GA4GH api schemas",
    "packages": ["ga4gh_schemas"],
    "url": "https://github.com/dcolligan/ga4gh-schemas",
    "use_scm_version": {"write_to": "ga4gh_schemas/_version.py"},
    "entry_points": {},
}
setup.doSetup(packageDict)
