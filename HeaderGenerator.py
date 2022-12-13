from datetime import date,datetime,timedelta
import time
import socket
from Value import Cookiepath,FileInfoPath,FILE_NOT_FOUND,MEDIA_NOT_SUPPORTED,ACCESSLOG
import uuid
import os



generalHeader={
    "Date":0,
    "Server":0,
    "Cache-control": "no-cache",
    "Connection": "keep-alive",
    "Pragma":"no-cache"
}

responseHeader={
	"Accept-Ranges" : "bytes", 
    "Age" : 0,  
    "ETag" : 0, 
    "Location" : 0,
    "Proxy-Authenticate" : 0,
    "Retry-After" : 0,
    "Set-Cookie":0,
    "WWW-Authenticate" : 0
}

entityHeader = {
	"Allow": "GET, HEAD, PUT",
	"Content-Encoding": "identity",  
	"Content-Language": "en",
	"Content-Length": 0,
	"Content-Location": "", 
	"Content-MD5": 0,  
	"Content-Range": 0,
	"Content-Type": "",
	"Expires": 0,  
	"Last-Modified": 0,
	}


statusCodes = {
	101 : "Switching Protocols",
	200 : "OK",
	201 : "Created",
	202 : "Accepted",
	203 : "Non-Authoritative Information",
	204 : "No Content",
	205 : "Reset Content",
	206 : "Partial Content",
	300 : "Multiple Choices",
	301 : "Moved Permanently",
	302 : "Found",
	303 : "See Other",
	304 : "Not Modified",
	305 : "Use Proxy",
	307 : "Temporary Redirect",
	400 : "Bad Request",
	401 : "Unauthorized",
	402 : "Payment Required",
	403 : "Forbidden",
	404 : "Not Found",
	405 : "Method Not Allowed",
	406 : "Not Acceptable",
	407 : "Proxy Authentication Required",
	408 : "Request Time-out",
	409 : "Conflict",
	410 : "Gone",
	411 : "Length Required",
	412 : "Precondition Failed",
	413 : "Request Entity Too Large",
	414 : "Request-URI Too Large",
	415 : "Unsupported Media Type",
	416 : "Requested range not satisfiable",
	417 : "Expectation Failed",
	500 : "Internal Server Error",
	501 : "Not Implemented",
	502 : "Bad Gateway",
	503 : "Service Unavailable",
	504 : "Gateway Time-out",
	505 : "HTTP Version not supported"
	}

contentType={
    "html":"text/html",
    "css":"text/css",
    "json":"application/json",
    "js":"text/js",
    "txt":"text/plain"
}

weekDaysMapping = ("Mon", "Tue",
                   "Wed", "Thu",
                   "Fri", "Sat",
                   "Sun")
monthMapping=(
    "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"
)

def getdate():
    Today=""
    today = date.today()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    Today+=weekDaysMapping[today.weekday()]
    Today+=', '
    Today+=today.strftime("%d %b %Y")
    Today+=" "
    Today+=current_time
    Today+=" GMT"
    return Today

def getexpiry():
    weekDaysMapping = ("Mon", "Tue",
                   "Wed", "Thu",
                   "Fri", "Sat",
                   "Sun")
    Today=""
    today = date.today()+timedelta(days=1)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    Today+=weekDaysMapping[today.weekday()]
    Today+=', '
    Today+=today.strftime("%d %b %Y")
    Today+=" "
    Today+=current_time
    Today+=" GMT"
    return Today

def isPathFile(path):
    if("." in path):
        return True
    return False

def getFileSize(path):
    return os.path.getsize(path)

def getLastModified(path):
    with open(FileInfoPath,"r") as f:
        data=f.read().split("\n")
    for i in data:
        if(path==i.split(",")[0]):
           return i.split(",")[2].replace('-',',')
    return ""

def getGeneralHeader():
    header=""
    for i in generalHeader:
        header+=i
        header+=": "
        if(i=="Date"):
            header+=getdate()
        elif(i=="Server"):
            header+=str(socket.gethostname())
        else:
            header+=generalHeader[i]
        header+="\r\n"
    return header

def getCookieCount(cookieId):
    if(cookieId==0):
        id=uuid.uuid1()
        with open(Cookiepath,'a') as f:
            f.write(f"\n{id},{1}")
        return id
    with open(Cookiepath,'r') as f:
        data=f.read().split("\n")
    newdata=[]
    for i in data:
        if(i.split(',')[0]==cookieId):
            newdata.append(f"{cookieId},{int(i.split(',')[1])+1}")
        else:
           newdata.append(i)
    with open(Cookiepath,'w') as f:
        f.write("\n".join(newdata))
    return cookieId
    
def getEtag(path):
    print(path)
    print("int Etag")
    with open(FileInfoPath,"r") as f:
        data=f.read().split("\n")
    for i in data:
        if(path==i.split(",")[0]):
           return i.split(",")[1]
    return 0

def getResponseHeader(path,cookieId):
    cookieCount=getCookieCount(cookieId)
    ETAG=getEtag(path)
    header=""
    for i in responseHeader:
        header+=i
        header+=": "
        if i=="ETag":
            header+=str(ETAG)
        elif i=="Location":
            header+=""
        elif i=="Set-Cookie":
            header+=f"id:{cookieCount}"
        else:
           header+=str(responseHeader[i])
        header+="\r\n"
    return header

def getEntityHeader(path,istext,content_range,content_length,content_location):
    header=""
    for i in entityHeader:
        header+=i
        header+=": "
        if(i=="Content-Length"):
            header+=str(content_length)
        elif(i=="Content-Range"):
            header+=str(content_range)
        elif(i=="Content-Location"):
            if(content_length==0):
                header+=""
            else:
                header+=content_location
        elif(i=="Content-Type"):
            header+=contentType[path.split(".")[1]]
        elif(i=="Expires"):
            header+=getexpiry()
        elif(i=="Last-Modified"):
            header+=getLastModified(path)
        else:
            header+=str(entityHeader[i])
        header+="\r\n"
    return header

def getFileContent(path,start,end,status_code):
    if(status_code==416):
        return ""
    with open(path,"r") as f:
        data=f.read()
        if(start==-1 and end==-1):
           return data
        if(start==-2):
            return ""
        return data[start:end+1]
        
def isRangeSatisfiable(start,end,path,status_code):
    print("in range satifsifle")
    with open(path,"r") as f:
        data=f.read()
    last_byte=len(data)
    content_range="bytes "
   
    if(start==-1 and end==-1):
        content_range+=f"{str(0)}-{str(last_byte)}/{str(last_byte)}"
        content_length=str(last_byte)
        return status_code,content_range,content_length
    if(start==-2):
        content_range+=f"{str(0)}-{str(0)}/{str(last_byte)}"
        content_length="0"
        return status_code,content_range,content_length
    if(end>last_byte):
        content_range+=f"*/{str(last_byte)}"
        content_length="0"
        return 416,content_range,content_length
    content_length=str(end-start+1)
    content_range+=f"{str(start)}-{str(end)}/{str(last_byte)}"
    return status_code,content_range,content_length
          
def compareHttpDates(date1,date2):
    day1,month1,year1,time1,location1=date1.split(" ")
    day2,month2,year2,time2,location2=date2.split(" ")
    h1,m1,s1=map(int,time1.split(":"))
    h2,m2,s2=map(int,time2.split(":"))

    d1=datetime(int(year1),monthMapping.index(month1)+1,int(day1),h1,m1,s1)
    d2=datetime(int(year2),monthMapping.index(month2)+1,int(day2),h2,m2,s2)
    if(str(d2-d1)[0]=='-'):
        return True
    return False

def fileNotFound():
    status_code     = 404
    status_line     = "HTTP/1.1" +" "+ str(status_code) + " " +statusCodes[status_code] + "\r\n"
    general_header  = "Cache:no-cache\r\n" + "Date:" + getdate()+"\r\n" +"Connection:Keep-Alive\r\n"
    response_header =""
    entity_header   =""
    for i in responseHeader :
        response_header += i
        response_header += ":"
        response_header += str(responseHeader[i])
        response_header += "\r\n"
    for i in entityHeader :
        entity_header += i
        entity_header += ":"
        if i == "Content-Length":
            entity_header += str(getFileSize(FILE_NOT_FOUND))
        elif i == "Content-Type":
            entity_header+="text/html"
        else:
            entity_header += str(entityHeader[i])
        entity_header += "\r\n"
    response =  status_line+ general_header + response_header + entity_header 
    file_path = open(FILE_NOT_FOUND)
    message = file_path.read()
    file_path.close()
    return response+"\r\n"+ message

def notSupported():
    status_code = 415
    status_line     = "HTTP/1.1" +" "+ str(status_code) + " " +statusCodes[status_code] + "\r\n"
    general_header  = "Cache: no-cache\r\n" + "Date: " + getdate()+"\r\n" +"Connection: Keep-Alive\r\n"
    response_header =""
    entity_header   =""
    for i in responseHeader :
        response_header += i
        response_header += ": " 
        response_header += str(responseHeader[i])
        response_header += "\r\n"
    for i in entityHeader :
        entity_header += i
        entity_header += ": "
        if i == "Content-Length":
            entity_header += str(getFileSize(MEDIA_NOT_SUPPORTED))
        elif i== "Content-Range":
            entity_header+="bytes "+f"{str(0)}-{str(getFileSize(MEDIA_NOT_SUPPORTED))}/{str(getFileSize(MEDIA_NOT_SUPPORTED))}"
        elif i == "Content-Type":
            entity_header+="text/html"
        else:
            entity_header += str(entityHeader[i])
        entity_header += "\r\n"
    response  =  status_line+response_header+entity_header
    message=""
    with open(MEDIA_NOT_SUPPORTED,'r') as f:
        message=f.read()
    return response+'\r\n'+message

def updateFileInfo(path,allowedMethods):
    etag=uuid.uuid1()
    d=getdate()
    d=d.replace(',','-')
    with open(FileInfoPath,'a') as f:
        f.write(f"\n{path},{etag},{d},{allowedMethods}")

def removeFileInfo(path):
    data=""
    newdata=[]
    with open(FileInfoPath,'r') as f:
        data=f.read().split("\n")
    for row in data:
        if path!=row.split(",")[0][:len(path)]:
            newdata.append(row)
    newdata="\n".join(newdata)
    with open(FileInfoPath,'w') as f:
        f.write(newdata)

def updateAccessLog(host,path,method):
    with open(ACCESSLOG,'a') as f:
        f.write(f"\n{host},{path},{getdate()},{method}") 