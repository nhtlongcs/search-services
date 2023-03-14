
from datetime import datetime
import parsedatetime

def time_this(func):
    def calc_time(*args, **kwargs):
        before = datetime.now()
        x = func(*args, **kwargs)
        after = datetime.now()
        print("Function {} elapsed time: {}".format(func.__name__, after-before))
        return x
    return calc_time


def nlp2datetime(text: str):
    cal = parsedatetime.Calendar()    
    time_struct, parse_status = cal.parse(text)#, sourceTime=start)
    if parse_status == 0:
        return None
    return datetime(*time_struct[:6])
