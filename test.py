
import os


d = "[\u4e00-\u9fa5]+"  # 中文 匹配
d2 = "[d]+"  # 匹配 数字

s = '我是-1234-王'

# 白千里-有片子

# re.findall(d, s)
#
# re.match(d, s)