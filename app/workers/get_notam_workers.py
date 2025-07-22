from datetime import datetime

import requests


def get_notam_from_thirdparty_site(retrieveLocId):
    print(f"Retrieving Notam from thirdparty site:{retrieveLocId}")
    return retrieveLocId,200