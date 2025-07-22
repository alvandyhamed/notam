import os

from bs4 import BeautifulSoup
import re


def extract_notams_data(html_content):

    notams_data = []
    total_notams_count = 0

    soup = BeautifulSoup(html_content, 'html.parser')


    total_notams_tags = soup.find_all('td', class_='textRed12')
    for tag in total_notams_tags:
        tag_text = tag.get_text(strip=True)
        match = re.search(r'Number of NOTAMs: (\d+)', tag_text)
        if match:
            total_notams_count = int(match.group(1))
            break


    notam_pres = soup.find_all('pre')

    for pre_tag in notam_pres:
        notam_text = pre_tag.get_text(strip=False)  # Keep newlines for better regex matching, strip later

        notam_id = "N/A"
        issued_for = []
        until_date = "N/A"
        created_date = "N/A"


        notam_id_match = re.match(r'^\s*<b>([A-Z]\d{4}/\d{2})</b>', notam_text, re.DOTALL)
        if not notam_id_match:
            notam_id_match = re.match(r'^\s*([A-Z]\d{4}/\d{2})', notam_text, re.DOTALL)

        if notam_id_match:
            notam_id = notam_id_match.group(1)

            notam_text = re.sub(r'^\s*<b>' + re.escape(notam_id) + r'</b>\s*-\s*', '', notam_text, 1, re.DOTALL)
            notam_text = re.sub(r'^\s*' + re.escape(notam_id) + r'\s*-\s*', '', notam_text, 1,
                                re.DOTALL)  # In case <b> was not there


        issued_for_match = re.search(r'\(Issued for (.+?)\)', notam_text)
        if issued_for_match:
            issued_for = issued_for_match.group(1).split()

            notam_text = notam_text.replace(issued_for_match.group(0), '').strip()


        created_match = re.search(r'CREATED:\s*(.+?)\s*$', notam_text, re.DOTALL)
        if created_match:
            created_date = created_match.group(1).strip()

            notam_text = notam_text.replace(created_match.group(0), '').strip()


        until_match = re.search(r'UNTIL\s*(.+?)(?=\.|\s*CREATED:|$)', notam_text, re.DOTALL)
        if until_match:
            until_date = until_match.group(1).strip()
            if until_date.endswith('.'):
                until_date = until_date[:-1]

            if re.search(r'PERM', until_date, re.IGNORECASE):
                until_date = "PERM"

            notam_text = notam_text.replace(f"UNTIL {until_match.group(1)}", '').strip()

            if notam_text.endswith('.'):
                notam_text = notam_text[:-1].strip()


        main_text = re.sub(r'CNS\d+W SEQUENCE CHECK FOR UUUUYNYX O --.+?RETCODE = \d+\.', '', notam_text,
                           flags=re.DOTALL).strip()


        if main_text.startswith('-'):
            main_text = main_text[1:].strip()


        if main_text.endswith('.'):
            main_text = main_text[:-1].strip()


        main_text = os.linesep.join([s for s in main_text.splitlines() if s.strip()])
        main_text = main_text.strip()

        notams_data.append({
            "notam_id": notam_id,
            "issued_for": issued_for,
            "main_content": main_text,
            "until_date": until_date,
            "created_date": created_date
        })

    return {
        "total_notams": total_notams_count,
        "notams": notams_data
    }