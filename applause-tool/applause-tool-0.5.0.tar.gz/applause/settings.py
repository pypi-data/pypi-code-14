try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

# Not so secret client credentials :>
CLIENT_ID = "1d0b9ed3538cbd35e1a5ab66b656379e"
CLIENT_SECRET = "ad71e753d6535f748f5f793537562e56"

# Applause Auth
OAUTH_BASE_URL = 'https://auth.applause.com'

# Applause Builds
BUAPS_BASE_URL = 'https://builds.applause.com/api/v1/'
BUAPS_STORE_URL = urljoin(BUAPS_BASE_URL, 'storage/')
BUAPS_STATUS_URL = urljoin(BUAPS_BASE_URL, 'storage/{token}/status/')
BUAPS_SUCCESS_URL = urljoin(BUAPS_BASE_URL, 'handlers/success/{token}/')

# Applause SDK
SDK_BASE_URL = 'https://sdk.applause.com/sdk/api/v1/'
SDK_INSTALLER_STORE_URL = urljoin(SDK_BASE_URL, "resources/installer/store/")
SDK_DISTRIBUTE_URL = urljoin(SDK_BASE_URL, "companies/{company_id}/applications/{app_id}/distributions/")

# Applause MBM
MBM_ROOT_URL = 'https://beta.applause.com/'
MBM_BASE_URL = urljoin(MBM_ROOT_URL, 'beta/api/v1/')
MBM_INSTALLER_STORE_URL = urljoin(MBM_BASE_URL, "resources/installer/store/")
MBM_DISTRIBUTE_URL = urljoin(MBM_BASE_URL, "applications/{app_id}/distributions/")

# AIS Server
AIS_BASE_URL = 'https://ais.applause.com/autoinstrumentation/'
AIS_UPLOAD_DATA_URL = urljoin(AIS_BASE_URL, 'upload-data')
AIS_STATUS_URL = urljoin(AIS_BASE_URL, 'status/')
AIS_INSTRUMENT_URL = urljoin(AIS_BASE_URL, 'instrument')