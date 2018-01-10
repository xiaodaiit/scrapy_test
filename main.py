

from scrapy.cmdline import  execute
import sys
import datetime
import os
import selenium
# print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy","crawl", "jobbole"])
# execute(["scrapy","crawl", "zhihu"])
execute(["scrapy","crawl", "lagou"])

# create_date = datetime.datetime.now().date()
# print(create_date)