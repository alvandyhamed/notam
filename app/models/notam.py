from app import mongo


class Notam:
    @staticmethod
    def create(total_notams,notam_id,notams):
        notam={
            'total_notam':total_notams,
            'notam_id':notam_id,
            'notams':notams
        }
        mongo.db.notam.insert_one(notam)

        return notam