from datetime import datetime

def getTime():
    time24hourformat = datetime.today().strftime('%H:%M')
    d = datetime.strptime(time24hourformat, '%H:%M')
    today = {
        "date" : datetime.today().strftime('%Y-%m-%d'),
        "time": d.strftime("%I:%M %p")
    }
    return today