def get_current_Date():
    """ GEt the current date and time"""

    from datetime import datetime

    return json.dumps({"datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})