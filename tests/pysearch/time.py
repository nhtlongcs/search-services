from datetime import datetime
import parsedatetime
import time

def parseYYYYmmDD(text):
    cal = parsedatetime.Calendar()    
    time_struct, parse_status = cal.parse(text)#, sourceTime=start)
    if parse_status == 0:
        return None
    return datetime(*time_struct[:6]).strftime('%Y%m%d')

last_year = datetime(2020, 1, 1, 0, 0, 0)

now = datetime(time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
print('input prompt: 12 month before today, 12:45')
print('now: ', now)
print('parse time: ')
print(parseYYYYmmDD("12 month before today, 12:45"))