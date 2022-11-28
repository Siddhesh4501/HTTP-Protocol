# from datetime import date
import os
from Value import RESOURCE
import uuid
import json
import shutil
# # import socket
# # print(socket.gethostname())
# # import os
# # myhost = os.uname()[1]
# # print(myhost)

# # d={
# #     "data": date.today()
# # }

# # print(d)

# with open("fileinfo.csv") as f:
#     data=f.read().split("\n")[1:]
#     print(data)

# def fun():
#     return 2,3

# a,b=fun()
# print(a)
# print(b)


# # with open("/home/siddhesh/Documents/CN projects/index.html","r") as f:
# #     data=f.read()
# #     print(data)

# day,month,year,time,location="31 Dec 1999 23:59:59 GMT".split(" ")
# print(day,month,year,time)

dirpath=os.path.abspath(os.getcwd())

path=RESOURCE+"contact/name/"+"hello.json"

print(os.path.exists(path))
# 
# os.makedirs(path)

# print(os.path.getsize(RESOURCE+"index.html"))

# with open(RESOURCE+"address/") as f:

# print(os.path.i("abc/dcg/sample.txt"))


import os
 
dir = dirpath+"/temp"
# for f in os.listdir(dir):
#     os.remove(os.path.join(dir, f))

# shutil.rmtree(dir)

# os.makedirs(RESOURCE+"local/storage")
# with open("/home/siddhesh/Documents/CN projects/PostData/local/storagge",'w') as f:
#     f.write("siddhesh")

# print(os.path.exists(RESOURCE+"/local/storadge"))
# os.rmdir(RESOURCE+"/local/storage")
# shutil.rmtree(RESOURCE+"/local/storage")
