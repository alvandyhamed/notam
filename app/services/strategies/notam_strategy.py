from app.workers.get_notam_workers import get_notam_from_thirdparty_site


class NotamStrategy:
    def get_Notam(self,retrieveLocId,flight_number,user_id,date,rout):


        res,status_code=get_notam_from_thirdparty_site(retrieveLocId,flight_number,user_id,date,rout)
        return res,status_code
