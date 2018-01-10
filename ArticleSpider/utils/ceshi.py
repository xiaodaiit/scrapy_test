# str ='<meta name="entry" content="ZH.entrySignPage" data-module-id="page-index"><input type="hidden" name="_xsrf" value="3050a78bec5c7538274b1ea08cf673b3"/></body></html>'
# # print(str)
#
#
# ss ='''
# <script src="https://static.zhihu.com/static/revved/-/js/closure/page-index.7cc04a7b.js"></script>
# <meta name="entry" content="ZH.entrySignPage" data-module-id="page-index">
#
#
# <input type="hidden" name="_xsrf" value="39323863326635652d353931302d346434392d383332352d613566613435356463626663"/>
# </body>
# </html>
# '''
#
# with open("inde.html", "r",encoding="utf-8") as f:
#     text = f.read()
#
# import re
# # ss = text.replace("\n","")
# ss = text
# s = re.match('.*name="_xsrf" value="(.*?)"', ss)
# print(s.group(1))
# exit()
# import re
# ss = ss.replace("\n","")
# print(ss)
# # str = '<input type="hidden" name="_xsrf" value="3050a78bec5c7538274b1ea08cf673b3"/>'
# s = re.match('.*name="_xsrf" value="(.*?)"', ss)
# print(s.group(1))


import re
url = 'https://www.zhihu.com/question/264331588/answer/281090126'


match_obj = re.match("(.*zhihu.com.question/(\d+))(/|$).*", url)
print(match_obj)