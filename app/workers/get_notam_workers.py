from datetime import datetime

import requests
from flask import json, jsonify

from app.models.notam import Notam

from app.workers.call_notam import call_notam
from app.workers.extract_notams_data import extract_notams_data


def get_notam_from_thirdparty_site(retrieveLocId):

    success, status_code, error, html_content = call_notam(retrieveLocId)

    if success:
        try:


            notam_json_data = extract_notams_data(html_content)


            Notam.create(notam_json_data['total_notams'],notam_json_data['notams'])



            return {
                "status":200,
                "message":"success get notam ",
                "total_notams":notam_json_data['total_notams'],
                "notams":notam_json_data['notams']


            },200


        except Exception as e:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            return {'status': 500, 'message': f'Failed to parse NOTAM data for {retrieveLocId}error : {str(e)} date : {now}'}, 500
    else:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {'status': 500, 'message': f'Failed to parse NOTAM data for {retrieveLocId} date : {now}' }, 500




