from app.workers.get_notam_workers import get_notam_from_thirdparty_site, get_bach_from_thirdparty_site


class NotamStrategy:
    def get_Notam(self,retrieveLocId,flight_number,user_id,date,rout):

        res,status_code=get_notam_from_thirdparty_site(retrieveLocId,flight_number,user_id,date,rout)
        return res,status_code
    def get_Notams(self,data):
       try:

        date = data['date']
        flight_number = data['flight_number']
        retrieveLocIds = data['retrieveLocIds']
        rout = data['rout']
        user_id = data['user_id']
        res,status_code=get_bach_from_thirdparty_site(retrieveLocIds,flight_number,user_id,date,rout)
        return res,status_code


       except Exception as e:
           return f"there is an issue {str(e)}",500