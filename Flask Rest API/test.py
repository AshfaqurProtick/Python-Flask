from flask import views
import requests
from werkzeug.wrappers import Response

BASE= "http://127.0.0.1:5000/"


data= [{"likes":10, "name":"Tim", "views":10000},
        {"likes":89, "name":"How to make RestAPI", "views":11009},
        {"likes":198, "name":"Tim's Wedding", "views":10500}]

for i in range(len(data)):
    response= requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
response= requests.get(BASE + "video/0")
print(response.json())
input()
response= requests.delete(BASE + "video/0")
print(response)
input()
response= requests.get(BASE + "video/0")
print(response.json())
input()
response= requests.get(BASE + "video/6")
print(response.json())



'''
response=requests.patch(BASE + "video/2", {"views":99, "likes":101})
print(response.json())

'''