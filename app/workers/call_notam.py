from datetime import datetime

import requests

from app.models.logs import Logs


def call_notam(retrieveLocId):
    url = 'https://www.notams.faa.gov/dinsQueryWeb/queryRetrievalMapAction.do'
    params = {
        'reportType': 'Report',
        'retrieveLocId': retrieveLocId,
        'actionType': 'notamRetrievalByICAOs',
        'submit': 'View NOTAMs'
    }
    headers = {
        'Host': 'www.notams.faa.gov',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Origin': 'https://www.notams.faa.gov',
        'Dnt': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.notams.faa.gov/dinsQueryWeb/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8,fr;q=0.7,ar;q=0.6',
        'Priority': 'u=0, i',
    }
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:

            # filename = f'notam_response_{retrieveLocId}.html'
            # with open(filename, 'w', encoding=response.encoding or 'utf-8') as f:
            #     f.write(response.text)
            # with open(SUCCESS_LOG, 'a') as slog:
            #     slog.write(f"{now}: {response.status_code}: success ({retrieveLocId})\n")
            Logs.create("Success", now, response.text)
            return True, response.status_code, None, response.text
        else:
            # with open(ERROR_LOG, 'a') as elog:
            #     elog.write(f"{now}: {response.status_code}: {response.reason} ({retrieveLocId})\n")
            Logs.create("Error", now, response)
            return False, response.status_code, response.reason, None
    except Exception as e:
        # with open(ERROR_LOG, 'a') as elog:
        #     elog.write(f"{now}: N/A: {str(e)} ({retrieveLocId})\n")
        Logs.create("Error", now, str(e))
        return False, None, str(e), None
