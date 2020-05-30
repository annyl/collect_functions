import requests
import json
import time

total_count = 0

for day in range(11, 27):
    items = []
    total_count = 0
    if len(str(day)) == 1:
        date = '2020-02-' + '0' + str(day)
    else:
        date = '2020-02-' + str(day)
    print('Processing date ', date)

    for hour in range(24):
        time_str = ''
        if hour < 10:
            hour_str = '0' + str(hour)
        else:
            hour_str = str(hour)
        print('Processing hour ', hour)
        for minute in range(60):
            if minute < 10:
                time_str = hour_str + ':' + '0' + str(minute)
            else:
                time_str = hour_str + ':' + str(minute)
            r = requests.get('https://api.github.com/search/repositories?q=+language:python+created:'+date+'T'+time_str+'&page:1', auth=('annyl', 'jyfteh-poPcym-pynhy4'))
            time.sleep(2)
            result = r.text
            result = result.replace('false', 'False')
            result = result.replace('null', 'None')
            result = result.replace('true', 'True')
            result_eval = eval(result)

            if result_eval["total_count"] > 30:
                total_count += 30
                items.extend(result_eval["items"])
            else:
                total_count += result_eval["total_count"]
                items.extend(result_eval["items"])

    print(total_count)
    with open(date+'.txt', 'w') as outfile:
        json.dump({date:items}, outfile)
