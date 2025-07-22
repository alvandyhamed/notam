from app.extentions import mongo


class Logs:
    @staticmethod
    def create(type,date,message):
        log={
            'type':type,
            'date':date,
            'message':message
        }
        mongo.db.logs.insert_one(log)