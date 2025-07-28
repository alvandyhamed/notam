from datetime import datetime

from app.extentions import mongo

import jdatetime



class Notam:
    @staticmethod
    def create(total_notams,notams,flight_number,user_id,date,rout):
        now = datetime.now()
        jalali_date = jdatetime.date.today()
        notam={
            'flight_number':flight_number,
            'user_id':user_id,
            'report_date':date,
            "rout":rout,
            'total_notam':total_notams,
            'date':now.isoformat(),
            'jalali':jalali_date.strftime('%Y-%m-%d'),
            'notams':notams
        }
        mongo.db.notam.insert_one(notam)

        return notam