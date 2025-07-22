# from flask import Flask, jsonify, request
# import requests
# from datetime import datetime
# import threading
# import time
# import random
# from bs4 import BeautifulSoup
# import re
# import json
# import os
#
# app = Flask(__name__)
#
# ERROR_LOG = 'error_log.txt'
# SUCCESS_LOG = 'success_log.txt'
#
#
# if not os.path.exists(ERROR_LOG):
#     open(ERROR_LOG, 'a').close()
# if not os.path.exists(SUCCESS_LOG):
#     open(SUCCESS_LOG, 'a').close()
#
# icao_codes = [
#     # FIR ایران و کشورهای مجاور
#     "OIIX",  # Tehran FIR - ایران
#     "ORBB",  # Baghdad FIR - عراق
#     "LTAA",  # Ankara FIR - ترکیه
#     "UDDD",  # Yerevan FIR - ارمنستان
#     "UBBA",  # Baku FIR - آذربایجان
#     "UTAA",  # Ashgabat FIR - ترکمنستان
#     "OAKX",  # Kabul FIR - افغانستان
#     "OPKR",  # Karachi FIR - پاکستان
#     "OKAC",  # Kuwait FIR - کویت
#     "OEJD",  # Jeddah FIR - عربستان سعودی
#     "OBBB",  # Bahrain FIR - بحرین
#     "OTHH",  # Doha FIR - قطر
#     "OMAE",  # Emirates FIR - امارات
#     "OOMS",  # Muscat FIR - عمان
#     # فرودگاه‌های اصلی ایران
#     "OIIE",  # Imam Khomeini Intl
#     "OIII",  # Mehrabad Intl
#     "OIMM",  # Mashhad
#     "OISS",  # Shiraz
#     "OIFM",  # Isfahan
#     "OITT",  # Tabriz
#     "OIAW",  # Ahvaz
#     "OIBK",  # Kish
#     "OIKB",  # Bandar Abbas
#     "OIZC",  # Chabahar
#     "OIKK",  # Kerman
#     "OIYY",  # Yazd
#     "OITR",  # Urmia
#     "OIGG",  # Rasht
#     "OINZ",  # Sari
#     "OIZH",  # Zahedan
#     "OICS",  # Sanandaj
#     "OICI",  # Ilam
#     "OICK",  # Khorramabad
#     "OIMN"  # Bojnord
# ]
#
#
# def extract_notams_data(html_content):
#
#     notams_data = []
#     total_notams_count = 0
#
#     soup = BeautifulSoup(html_content, 'html.parser')
#
#
#     total_notams_tags = soup.find_all('td', class_='textRed12')
#     for tag in total_notams_tags:
#         tag_text = tag.get_text(strip=True)
#         match = re.search(r'Number of NOTAMs: (\d+)', tag_text)
#         if match:
#             total_notams_count = int(match.group(1))
#             break
#
#
#     notam_pres = soup.find_all('pre')
#
#     for pre_tag in notam_pres:
#         notam_text = pre_tag.get_text(strip=False)  # Keep newlines for better regex matching, strip later
#
#         notam_id = "N/A"
#         issued_for = []
#         until_date = "N/A"
#         created_date = "N/A"
#
#
#         notam_id_match = re.match(r'^\s*<b>([A-Z]\d{4}/\d{2})</b>', notam_text, re.DOTALL)
#         if not notam_id_match:
#             notam_id_match = re.match(r'^\s*([A-Z]\d{4}/\d{2})', notam_text, re.DOTALL)
#
#         if notam_id_match:
#             notam_id = notam_id_match.group(1)
#
#             notam_text = re.sub(r'^\s*<b>' + re.escape(notam_id) + r'</b>\s*-\s*', '', notam_text, 1, re.DOTALL)
#             notam_text = re.sub(r'^\s*' + re.escape(notam_id) + r'\s*-\s*', '', notam_text, 1,
#                                 re.DOTALL)  # In case <b> was not there
#
#
#         issued_for_match = re.search(r'\(Issued for (.+?)\)', notam_text)
#         if issued_for_match:
#             issued_for = issued_for_match.group(1).split()
#
#             notam_text = notam_text.replace(issued_for_match.group(0), '').strip()
#
#
#         created_match = re.search(r'CREATED:\s*(.+?)\s*$', notam_text, re.DOTALL)
#         if created_match:
#             created_date = created_match.group(1).strip()
#
#             notam_text = notam_text.replace(created_match.group(0), '').strip()
#
#
#         until_match = re.search(r'UNTIL\s*(.+?)(?=\.|\s*CREATED:|$)', notam_text, re.DOTALL)
#         if until_match:
#             until_date = until_match.group(1).strip()
#             if until_date.endswith('.'):
#                 until_date = until_date[:-1]
#
#             if re.search(r'PERM', until_date, re.IGNORECASE):
#                 until_date = "PERM"
#
#             notam_text = notam_text.replace(f"UNTIL {until_match.group(1)}", '').strip()
#
#             if notam_text.endswith('.'):
#                 notam_text = notam_text[:-1].strip()
#
#
#         main_text = re.sub(r'CNS\d+W SEQUENCE CHECK FOR UUUUYNYX O --.+?RETCODE = \d+\.', '', notam_text,
#                            flags=re.DOTALL).strip()
#
#
#         if main_text.startswith('-'):
#             main_text = main_text[1:].strip()
#
#
#         if main_text.endswith('.'):
#             main_text = main_text[:-1].strip()
#
#
#         main_text = os.linesep.join([s for s in main_text.splitlines() if s.strip()])
#         main_text = main_text.strip()
#
#         notams_data.append({
#             "notam_id": notam_id,
#             "issued_for": issued_for,
#             "main_content": main_text,
#             "until_date": until_date,
#             "created_date": created_date
#         })
#
#     return {
#         "total_notams": total_notams_count,
#         "notams": notams_data
#     }
#
#
# def call_notam(retrieveLocId):
#
#     url = 'https://www.notams.faa.gov/dinsQueryWeb/queryRetrievalMapAction.do'
#     params = {
#         'reportType': 'Report',
#         'retrieveLocId': retrieveLocId,
#         'actionType': 'notamRetrievalByICAOs',
#         'submit': 'View NOTAMs'
#     }
#     headers = {
#         'Host': 'www.notams.faa.gov',
#         'Cache-Control': 'max-age=0',
#         'Sec-Ch-Ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
#         'Sec-Ch-Ua-Mobile': '?0',
#         'Sec-Ch-Ua-Platform': '"macOS"',
#         'Origin': 'https://www.notams.faa.gov',
#         'Dnt': '1',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#         'Sec-Fetch-Site': 'same-origin',
#         'Sec-Fetch-Mode': 'navigate',
#         'Sec-Fetch-User': '?1',
#         'Sec-Fetch-Dest': 'document',
#         'Referer': 'https://www.notams.faa.gov/dinsQueryWeb/',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8,fr;q=0.7,ar;q=0.6',
#         'Priority': 'u=0, i',
#     }
#     now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     try:
#         response = requests.get(url, params=params, headers=headers)
#         if response.status_code == 200:
#
#             filename = f'notam_response_{retrieveLocId}.html'
#             with open(filename, 'w', encoding=response.encoding or 'utf-8') as f:
#                 f.write(response.text)
#             with open(SUCCESS_LOG, 'a') as slog:
#                 slog.write(f"{now}: {response.status_code}: success ({retrieveLocId})\n")
#             return True, response.status_code, None, response.text
#         else:
#             with open(ERROR_LOG, 'a') as elog:
#                 elog.write(f"{now}: {response.status_code}: {response.reason} ({retrieveLocId})\n")
#             return False, response.status_code, response.reason, None
#     except Exception as e:
#         with open(ERROR_LOG, 'a') as elog:
#             elog.write(f"{now}: N/A: {str(e)} ({retrieveLocId})\n")
#         return False, None, str(e), None
#
#
# @app.route('/get_notam', methods=['GET'])
# def get_notam():
#
#     retrieveLocId = request.args.get('retrieveLocId', 'OIMM')
#
#
#     success, status_code, error, html_content = call_notam(retrieveLocId)
#
#     if success:
#         try:
#
#             notam_json_data = extract_notams_data(html_content)
#
#
#             json_filename = f'notam_data_{retrieveLocId}.json'
#             with open(json_filename, 'w', encoding='utf-8') as f:
#                 json.dump(notam_json_data, f, indent=4, ensure_ascii=False)
#
#
#             return jsonify(notam_json_data), 200
#         except Exception as e:
#             now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             with open(ERROR_LOG, 'a') as elog:
#                 elog.write(f"{now}: N/A: Error parsing HTML for {retrieveLocId}: {str(e)}\n")
#             return jsonify(
#                 {'status': 'error', 'message': f'Failed to parse NOTAM data for {retrieveLocId}', 'error': str(e)}), 500
#     else:
#         return jsonify({'status': 'error', 'message': f'Failed to fetch NOTAM for {retrieveLocId}',
#                         'error': error}), status_code or 500
#
#
# def background_notam_caller():
#
#     while True:
#         retrieveLocId = random.choice(icao_codes)
#
#         success, status_code, error, html_content = call_notam(retrieveLocId)
#         if success:
#
#             try:
#                 notam_json_data = extract_notams_data(html_content)
#                 json_filename = f'notam_data_{retrieveLocId}_background.json'
#                 with open(json_filename, 'w', encoding='utf-8') as f:
#                     json.dump(notam_json_data, f, indent=4, ensure_ascii=False)
#             except Exception as e:
#                 now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                 with open(ERROR_LOG, 'a') as elog:
#                     elog.write(f"{now}: N/A: Error parsing HTML in background for {retrieveLocId}: {str(e)}\n")
#
#         sleep_time = random.randint(2 * 60, 10 * 60)
#         time.sleep(sleep_time)
#
#
# def start_background_thread():
#
#     t = threading.Thread(target=background_notam_caller, daemon=True)
#     t.start()
#
#
#
# start_background_thread()
#
# if __name__ == '__main__':
#
#     app.run(debug=True, port=5000)