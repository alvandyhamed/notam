from datetime import datetime

from app.extentions import mongo

import jdatetime



class Notam:
    @staticmethod
    def create(total_notams,notams):
        now = datetime.now()
        jalali_date = jdatetime.date.today()
        notam={
            'total_notam':total_notams,
            'date':now.isoformat(),
            'jalali':jalali_date.strftime('%Y-%m-%d'),
            'notams':notams
        }
        mongo.db.notam.insert_one(notam)

        return notam