#!/usr/bin/env python
# coding=utf-8

from datetime import datetime

end = '08-12-2018'

now = datetime.now()
now = now.strftime("%d-%m-%Y")

end = datetime.strptime(end, "%d-%m-%Y")
end = end.strftime("%d-%m-%Y")

if type(end) == type(now):
    print('True')
else:
    print('false')


print(now)
print(end)
