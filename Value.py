import os
dirpath=os.path.abspath(os.getcwd())
print(dirpath)
maxConnection=100

Cookiepath=str(dirpath)+"/Log/cookie.csv"
FileInfoPath=str(dirpath)+"/Log/fileinfo.csv"
FILE_NOT_FOUND=str(dirpath)+"/ResponsePages/fileNotFound.html"
MEDIA_NOT_SUPPORTED=str(dirpath)+"/ResponsePages/mediaNotSupported.html"
RESOURCE=str(dirpath)+"/PostData/"
GETEMPTYFILE=str(dirpath)+"/ResponsePages/emptyFile.html"
SAVESUCCESFULLY=str(dirpath)+"/ResponsePages/saveSuccesfully.html"
UPDATESUCCESFULLY=str(dirpath)+"/ResponsePages/updateSuccesfully.html"
ACCESSLOG=str(dirpath)+"/Log/access.csv"