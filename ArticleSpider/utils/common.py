import hashlib
import re
import datetime
import json

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()



def date_converts(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        print(create_date)
    except Exception as e:
        create_date = datetime.datetime.now().date()
        print(create_date)
    return create_date

def extract_num(text):
    #从字符串中提取数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

if __name__ == "__main__":
    c = date_converts("2017-12-20")

    # print(json.dumps(  type(c) ))
    print(type(c) )
    # print(json.dumps( '2017-12-20'))