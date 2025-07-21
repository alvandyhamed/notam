from flask import Flask, jsonify, request
import requests
from datetime import datetime
import threading
import time
import random

app = Flask(__name__)

ERROR_LOG = 'error_log.txt'
SUCCESS_LOG = 'success_log.txt'

icao_codes = [
    # FIR ایران و کشورهای مجاور
    "OIIX",  # Tehran FIR - ایران
    "ORBB",  # Baghdad FIR - عراق
    "LTAA",  # Ankara FIR - ترکیه
    "UDDD",  # Yerevan FIR - ارمنستان
    "UBBA",  # Baku FIR - آذربایجان
    "UTAA",  # Ashgabat FIR - ترکمنستان
    "OAKX",  # Kabul FIR - افغانستان
    "OPKR",  # Karachi FIR - پاکستان
    "OKAC",  # Kuwait FIR - کویت
    "OEJD",  # Jeddah FIR - عربستان سعودی
    "OBBB",  # Bahrain FIR - بحرین
    "OTHH",  # Doha FIR - قطر
    "OMAE",  # Emirates FIR - امارات
    "OOMS",  # Muscat FIR - عمان
    # فرودگاه‌های اصلی ایران
    "OIIE",  # Imam Khomeini Intl
    "OIII",  # Mehrabad Intl
    "OIMM",  # Mashhad
    "OISS",  # Shiraz
    "OIFM",  # Isfahan
    "OITT",  # Tabriz
    "OIAW",  # Ahvaz
    "OIBK",  # Kish
    "OIKB",  # Bandar Abbas
    "OIZC",  # Chabahar
    "OIKK",  # Kerman
    "OIYY",  # Yazd
    "OITR",  # Urmia
    "OIGG",  # Rasht
    "OINZ",  # Sari
    "OIZH",  # Zahedan
    "OICS",  # Sanandaj
    "OICI",  # Ilam
    "OICK",  # Khorramabad
    "OIMN"   # Bojnord
]

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
            filename = f'notam_response_{retrieveLocId}.html'
            with open(filename, 'w', encoding=response.encoding or 'utf-8') as f:
                f.write(response.text)
            with open(SUCCESS_LOG, 'a') as slog:
                slog.write(f"{now}: {response.status_code}: success ({retrieveLocId})\n")
            return True, response.status_code, None
        else:
            with open(ERROR_LOG, 'a') as elog:
                elog.write(f"{now}: {response.status_code}: {response.reason} ({retrieveLocId})\n")
            return False, response.status_code, response.reason
    except Exception as e:
        with open(ERROR_LOG, 'a') as elog:
            elog.write(f"{now}: N/A: {str(e)} ({retrieveLocId})\n")
        return False, None, str(e)

@app.route('/get_notam', methods=['GET'])
def get_notam():
    retrieveLocId = request.args.get('retrieveLocId', 'OIMM')
    success, status_code, error = call_notam(retrieveLocId)
    if success:
        return jsonify({'status': 'success', 'message': f'NOTAM response saved for {retrieveLocId}'}), 200
    else:
        return jsonify({'status': 'error', 'message': f'Failed for {retrieveLocId}', 'error': error}), status_code or 500

def background_notam_caller():
    while True:
        retrieveLocId = random.choice(icao_codes)
        call_notam(retrieveLocId)
        sleep_time = random.randint(2*60, 10*60)  # 2 to 10 minutes in seconds
        time.sleep(sleep_time)

def start_background_thread():
    t = threading.Thread(target=background_notam_caller, daemon=True)
    t.start()

start_background_thread()

if __name__ == '__main__':
    app.run(debug=True)
