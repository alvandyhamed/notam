from bs4 import BeautifulSoup
import re
import json


def extract_notams_to_json(html_file_path, json_output_path):
    """
    این تابع NOTAM ها را از یک فایل HTML استخراج کرده و در یک فایل JSON ذخیره می کند.
    همچنین تعداد کل NOTAM ها را نیز استخراج می کند.

    Args:
        html_file_path (str): مسیر فایل HTML ورودی.
        json_output_path (str): مسیر فایل JSON خروجی.
    """
    notams_data = []
    total_notams_count = 0  # برای نگهداری تعداد کل NOTAM ها

    with open(html_file_path, 'r', encoding='ISO-8859-1') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # استخراج تعداد کل NOTAM ها
    # این اطلاعات در یک تگ <TD> با کلاس "textRed12" و حاوی "Number of NOTAMs" قرار دارد.
    total_notams_tag = soup.find('td', class_='textRed12', string=re.compile(r'Number of NOTAMs:'))
    if total_notams_tag:
        match = re.search(r'Number of NOTAMs: (\d+)', total_notams_tag.get_text(strip=True))
        if match:
            total_notams_count = int(match.group(1))

    # هر NOTAM در یک تگ <PRE> داخل یک <td> قرار دارد.
    # ما به دنبال تگ های <PRE> می گردیم که حاوی NOTAM ها هستند.
    notam_pres = soup.find_all('pre')

    for pre_tag in notam_pres:
        notam_text = pre_tag.get_text(strip=True)

        # استخراج NOTAM ID (مثلاً O0310/25)
        notam_id_match = re.match(r'^(O\d{4}/\d{2})', notam_text)
        notam_id = notam_id_match.group(1) if notam_id_match else "N/A"

        # استخراج اطلاعات Issued for (اگر وجود داشته باشد)
        issued_for_match = re.search(r'\(Issued for (.+?)\)', notam_text)
        issued_for = issued_for_match.group(1).split() if issued_for_match else []

        # استخراج تاریخ UNTIL
        until_match = re.search(r'UNIL (.+?)(?=\. CREATED:|$)', notam_text)
        until_date = until_match.group(1).strip() if until_match else "N/A"
        # اگر UNIL پیدا نشد، ممکن است PERM باشد
        if until_date == "N/A":
            perm_match = re.search(r'UNTIL\s+PERM', notam_text)
            if perm_match:
                until_date = "PERM"

        # استخراج تاریخ CREATED
        created_match = re.search(r'CREATED: (.+)$', notam_text)
        created_date = created_match.group(1).strip() if created_match else "N/A"

        # استخراج متن اصلی NOTAM با حذف ID و اطلاعات تاریخ
        main_text = notam_text
        if notam_id != "N/A":
            main_text = re.sub(r'^(O\d{4}/\d{2}) - ', '', main_text, 1)
        if issued_for_match:
            main_text = main_text.replace(issued_for_match.group(0), '').strip()
        if until_match:
            main_text = main_text.replace(f"UNIL {until_match.group(1)}", '').strip()
        if created_match:
            main_text = main_text.replace(f"CREATED: {created_match.group(1)}", '').strip()

        # پاکسازی اضافی متن
        main_text = re.sub(r'CNS\d+W SEQUENCE CHECK FOR UUUUYNYX O --.+?RETCODE = \d+\.', '', main_text,
                           flags=re.DOTALL)
        # حذف موارد تکراری Issued for که در issued_for پردازش شده اند
        main_text = main_text.replace('(Issued for UTAA UTAV)', '').replace('(Issued for UTAV UTAA)', '')
        main_text = main_text.replace('(Issued for UTAA UTAK)', '').replace('(Issued for UTAK UTAA)', '')
        main_text = main_text.replace('(Issued for UTAA UTAK UTAT UTAV)', '')

        main_text = main_text.strip()

        # حذف هرگونه " - " اضافی که ممکن است به خاطر پردازش بالا مانده باشد
        if main_text.startswith('-'):
            main_text = main_text[1:].strip()

        notams_data.append({
            "notam_id": notam_id,
            "issued_for": issued_for,
            "main_content": main_text,
            "until_date": until_date,
            "created_date": created_date
        })

    # ساختار نهایی JSON
    output_json = {
        "total_notams": total_notams_count,
        "notams": notams_data
    }

    with open(json_output_path, 'w', encoding='utf-8') as json_f:
        json.dump(output_json, json_f, indent=4, ensure_ascii=False)


# مثال استفاده:
html_file = 'notam_response_UTAA.html'
json_file = 'notams_output.json'

extract_notams_to_json(html_file, json_file)
print(f"اطلاعات NOTAM با موفقیت در {json_file} ذخیره شد.")