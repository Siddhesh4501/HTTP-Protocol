import os
from HeaderGenerator import statusCodes,getGeneralHeader,getEntityHeader,getResponseHeader,getFileContent,getEtag,getLastModified,isRangeSatisfiable,compareHttpDates,fileNotFound,notSupported,updateFileInfo,isPathFile,removeFileInfo,updateAccessLog
from Value import dirpath,RESOURCE,GETEMPTYFILE,SAVESUCCESFULLY,UPDATESUCCESFULLY
import json
import uuid
import shutil
def GET(message,method="GET"):
    data=message.split("\r\n\r\n")[0]
    body=message.split("\r\n\r\n")[1]
    reqheader=data.split("\r\n")[0]
    reqallheaders={}
    for i in data.split("\r\n")[1:]:
        reqallheaders[i.split(":")[0]]=i.split(":")[1:]
    # print(reqallheaders)
    userAgent=reqallheaders["User-Agent"][0][1:]
    flag=False
    cookieId=0
    if (('Cookie' in reqallheaders.keys()) and " id" in reqallheaders["Cookie"]):
        flag=True
        cookieId=reqallheaders["Cookie"][1]

    filename=reqheader.split()[1][1:]
    if(filename==""):
        filename+="index.html"
    # print(filename)
    pathfile=RESOURCE+filename
    

    status_code=200
    messageToSend=""
    start=-1
    end=-1
    
    if(os.path.exists(pathfile)):

        if("Range" in reqallheaders.keys()):
            start=int(reqallheaders["Range"][0][7:].split('-')[0])
            end=int(reqallheaders["Range"][0][7:].split('-')[1])
            # print("In range")
            if("If-Range" in reqallheaders.keys()):
                # print("in If-Rage")
                # print(reqallheaders["If-Range"][0][1:])
                # print(str(getEtag(pathfile)))
                if(reqallheaders["If-Range"][0][1:]==str(getEtag(pathfile))):
                    status_code=206
                else:
                    status_code=200
                    start=-1
                    end=-1
            
            elif("If-Match" in reqallheaders.keys()):
                if(reqallheaders["If-Match"][0][1:]==str(getEtag(pathfile))):
                    status_code=206
                else:
                    status_code=412
                    start=-2
            else:
                status_code=206

        elif("If-Modified-Since" in reqallheaders.keys()):
            if(compareHttpDates(reqallheaders["If-Modified-Since"][0][1:]==getLastModified(pathfile))):
                status_code=304
                start=-2
            else:
                status_code=200

        status_code,content_range,content_length=isRangeSatisfiable(start,end,pathfile,status_code)
        

        status_line="HTTP/1.1 "+str(status_code)+" "+statusCodes[status_code]+"\r\n"
        general_header=getGeneralHeader()
        entity_header=getEntityHeader(pathfile,1,content_range,content_length,pathfile)
        response_header=getResponseHeader(pathfile,cookieId)
        header=status_line+general_header+entity_header+response_header
        # header=status_line+general_header+entity_header
        header+="\r\n"
        messageToSend=getFileContent(pathfile,start,end,status_code)
        # print(header+messageToSend)
        updateAccessLog(userAgent,pathfile,method)
        return header+messageToSend
    else:
        status_code=404
        return fileNotFound()

def HEAD(message):
    # print("In header")
    response=GET(message,"HEAD")
    response= response.split("\r\n\r\n")[0]
    # print(response)
    return response+"\r\n\r\n"

def POST(message):
    print(message)
    data=message.split("\r\n\r\n")[0]
    body=message.split("\r\n\r\n")[1:]
    newbody=[]
    contentLocation=""
    for i in body:
        for j in i.split("\r\n"):
            newbody.append(j)
    reqheader=data.split("\r\n")[0]
    filename=reqheader.split()[1][1:]
    print(filename)
    reqallheaders={}
    # flag=False
    cookieId=0
    print("cookie")
    binary=False
    # print(data)
    # print(newbody)
    status_code=201
    for i in data.split("\r\n")[1:]:
        reqallheaders[i.split(":")[0]]=i.split(":")[1:]
    # print(reqallheaders.keys())
    userAgent=reqallheaders["User-Agent"][0][1:]
    if (('Cookie' in reqallheaders.keys()) and " id" in reqallheaders["Cookie"]):
        flag=True
        cookieId=reqallheaders["Cookie"][1]
        print("cookieidis",cookieId)
    # print(reqallheaders)
    if "image/png" in "".join(reqallheaders["Content-Type"]):
        binary=True
    
    if(reqallheaders["Content-Type"]==[" application/x-www-form-urlencoded"]):
        if(not(os.path.exists(RESOURCE+filename+"/"))):
            os.makedirs(RESOURCE+filename+"/")
        dataToBeStored={}
        for j in [i.split("=") for i in body[0].split("&")]:
            dataToBeStored[j[0]]=j[1]
        print(dataToBeStored)
        dataToBeStored=json.dumps(dataToBeStored)
        # print(dataToBeStored)
        id=uuid.uuid1()
        filepath=RESOURCE+filename+"/"+str(id)+".json"
        contentLocation=filename+"/"+str(id)+".json"
        with open(filepath,'w') as f:
            updateFileInfo(filepath,"GET DELETE HEAD PUT")
            f.write(dataToBeStored)

    elif("multipart/form-data" in reqallheaders["Content-Type"][0][1:]):
        if(not(os.path.exists(RESOURCE+filename+"/"))):
            os.makedirs(RESOURCE+filename+"/")
        tempData = data
        boundryLine = reqallheaders['Content-Type'][0][1:].split('boundary=')[1]
        print(boundryLine)
        dataToBeStored=[]
        for i in range(1,len(newbody[1:])):
            if(i%3==1):
                dataToBeStored.append(newbody[i].split("name=")[1][1:-1]) 
            elif(i%3==2):
                dataToBeStored.append(newbody[i])
        # print(dataToBeStoreda)
        def Convert(lst):
            res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
            return res_dct
        dataToBeStored=Convert(dataToBeStored)
        dataToBeStored=json.dumps(dataToBeStored)
        print(dataToBeStored)
        id=uuid.uuid1()
        filepath=RESOURCE+filename+"/"+str(id)+".json"
        contentLocation=filename+"/"+str(id)+".json"
        print("filepath",filepath)
        with open(filepath,'w') as f:
            updateFileInfo(filepath,"GET DELETE PUT")
            f.write(dataToBeStored)
    else:
        status_code=405
        return notSupported()
    start=-1
    end=-1
    pathfile=SAVESUCCESFULLY
    status_code,content_range,content_length=isRangeSatisfiable(start,end,pathfile,status_code)
        
    status_line="HTTP/1.1 "+str(status_code)+" "+statusCodes[status_code]+"\r\n"
    general_header=getGeneralHeader()
    entity_header=getEntityHeader(pathfile,1,content_range,content_length,contentLocation)
    pathfile=filepath
    response_header=getResponseHeader(pathfile,cookieId)
    header=status_line+general_header+entity_header+response_header
    header+="\r\n"
    start=-1
    end=-1
    pathfile=SAVESUCCESFULLY
    messageToSend=getFileContent(pathfile,start,end,status_code)
    # print(header+messageToSend)
    updateAccessLog(userAgent,filepath,"POST")
    return header+messageToSend





def PUT(message):
    # print(message)
    data=message.split("\r\n\r\n")[0]
    body=message.split("\r\n\r\n")[1:]
    newbody=[]
    contentLocation=""
    for i in body:
        for j in i.split("\r\n"):
            newbody.append(j)
    reqheader=data.split("\r\n")[0]
    filename=reqheader.split()[1][1:]
    reqallheaders={}
    cookieId=0
    binary=False
    # print(data)
    for i in data.split("\r\n")[1:]:
        reqallheaders[i.split(":")[0]]=i.split(":")[1:]
    # print(reqallheaders.keys())
    userAgent=reqallheaders["User-Agent"][0][1:]
    if (('Cookie' in reqallheaders.keys()) and " id" in reqallheaders["Cookie"]):
        flag=True
        cookieId=reqallheaders["Cookie"][1]
        # print("cookieidis",cookieId)
    # print(reqallheaders)
    if "image/png" in "".join(reqallheaders["Content-Type"]):
        binary=True
    print(filename)
    print(newbody)

    status_code=""

    dataToBeStored=""
    if(reqallheaders["Content-Type"]==[" application/x-www-form-urlencoded"]):
        dataToBeStored={}
        for j in [i.split("=") for i in body[0].split("&")]:
            dataToBeStored[j[0]]=j[1]
        print(dataToBeStored)
        dataToBeStored=json.dumps(dataToBeStored)
        # print(dataToBeStored)

    elif("multipart/form-data" in reqallheaders["Content-Type"][0][1:]):
        tempData = data
        boundryLine = reqallheaders['Content-Type'][0][1:].split('boundary=')[1]
        print(boundryLine)
        dataToBeStored=[]
        for i in range(1,len(newbody[1:])):
            if(i%3==1):
                dataToBeStored.append(newbody[i].split("name=")[1][1:-1]) 
            elif(i%3==2):
                dataToBeStored.append(newbody[i])
        # print(dataToBeStoreda)

        def Convert(lst):
            res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
            return res_dct
        dataToBeStored=Convert(dataToBeStored)
        dataToBeStored=json.dumps(dataToBeStored)
        # print(dataToBeStored)

    else:
        print("int not supported")
        status_code=405
        return notSupported()

    path=""
    if(isPathFile(filename)):
        path=RESOURCE+"/".join(filename.split("/")[:-1])+"/"
    else:
        path=RESOURCE+filename+"/"
    
    # print(path)
    filepath=""
    if(os.path.isdir(path)):
        if(isPathFile(filename) and os.path.isfile(RESOURCE+filename)):
            status_code=204
            filepath=RESOURCE+filename
            contentLocation="/".join(filename.split("/")[:-1])
            with open(filepath,'w') as f:
                removeFileInfo(filepath)
                f.write(dataToBeStored)
                updateFileInfo(filepath,"GET DELETE HEAD PUT")
        elif(isPathFile(filename) and not(os.path.isfile(RESOURCE+filename))):
            status_code=201
            id=uuid.uuid1()
            filepath=path+str(id)+".json"
            contentLocation="/".join(filename.split("/")[:-1])+"/"+str(id)+".json"
            with open(filepath,'w') as f:
                f.write(dataToBeStored)
                updateFileInfo(filepath,"GET DELETE HEAD PUT")
        else:
            status_code=204
            shutil.rmtree(path)
            removeFileInfo(path)
            os.makedirs(path)
            id=uuid.uuid1()
            filepath=path+str(id)+".json"
            contentLocation=filename+str(id)+".json"
            with open(filepath,'w') as f:
                f.write(dataToBeStored)
                updateFileInfo(filepath,"GET DELETE HEAD PUT")

    else:
        status_code=201
        os.makedirs(path)
        id=uuid.uuid1()
        filepath=path+str(id)+".json"
        contentLocation=filename+"/"+str(id)+".json"
        with open(filepath,'w') as f:
            updateFileInfo(filepath,"GET DELETE PUT HEAD")
            f.write(dataToBeStored)



    start=-1
    end=-1
    pathfile=UPDATESUCCESFULLY
    status_code,content_range,content_length=isRangeSatisfiable(start,end,pathfile,status_code)
        
    status_line="HTTP/1.1 "+str(status_code)+" "+statusCodes[status_code]+"\r\n"
    general_header=getGeneralHeader()
    entity_header=getEntityHeader(pathfile,1,content_range,content_length,contentLocation)
    pathfile=filepath
    response_header=getResponseHeader(pathfile,cookieId)
    header=status_line+general_header+entity_header+response_header
    header+="\r\n"
    start=-1
    end=-1
    pathfile=UPDATESUCCESFULLY
    messageToSend=getFileContent(pathfile,start,end,status_code)
    # print(header+messageToSend)
    updateAccessLog(userAgent,filepath,"PUT")

    return header+messageToSend
    


def DELETE(message):
    data=message.split("\r\n\r\n")[0]
    body=message.split("\r\n\r\n")[1:]
    newbody=[]
    status_code=""
    contentLocation=""
    for i in body:
        for j in i.split("\r\n"):
            newbody.append(j)
    reqheader=data.split("\r\n")[0]
    filename=reqheader.split()[1][1:]
    reqallheaders={}
    cookieId=0
    binary=False
    for i in data.split("\r\n")[1:]:
        reqallheaders[i.split(":")[0]]=i.split(":")[1:]
    userAgent=reqallheaders["User-Agent"][0][1:]
    if (('Cookie' in reqallheaders.keys()) and " id" in reqallheaders["Cookie"]):
        flag=True
        cookieId=reqallheaders["Cookie"][1]
    print(filename)
    print(newbody)
    path=RESOURCE+filename
    if(os.path.exists(path)):
        status_code=204
        if(isPathFile(filename)):
            os.remove(path)
        else:
            shutil.rmtree(path)
        removeFileInfo(path)
    else:
        status_code=404
        return fileNotFound()

    status_line="HTTP/1.1 "+str(status_code)+" "+statusCodes[status_code]+"\r\n"
    general_header=getGeneralHeader()
    updateAccessLog(userAgent,path,"DELETE")

    return status_line+general_header+'\r\n'

    














    







    

