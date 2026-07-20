import json
from datetime import datetime

def get_current_date():
    """Get the current date and time"""

    return json.dumps({"datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})