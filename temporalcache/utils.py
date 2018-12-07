
def calc(seconds=0, minutes=0, hours=0, days=0, weeks=0, months=0, years=0):
    return seconds + \
           minutes*60 + \
           hours*60*60 + \
           days*24*60*60 + \
           weeks*7*24*60*60 + \
           months*30*7*24*60*60 + \
           years*365*24*60*60
