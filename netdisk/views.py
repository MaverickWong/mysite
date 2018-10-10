from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import os


# Create your views here.

# def showPath(request, repath):
#
#     base = '/Users/wcy/Documents/mysite2/'
#     path = base + repath
#     if os.path.isdir(path):
#         try:
#             list = os.listdir(repath)
#             list.sort(key=lambda a: a.lower())
#             return render(request, 'disk/index.html', {'cwd':repath, 'list':list})
#         except os.error:
#             return HttpResponse("No permission to list directory")
#
#     elif os.path.isfile(path):
#         try:
#             with open(path, 'rb') as f:
#                 content = f.read()
#                 # self.send_header('Content-type', mimetype)
#             return HttpResponse(content)
#
#         except IOError:
#             return HttpResponse("File Not Found: ")

#
# def home(request):
#     showPath(request, '/')

def showPath(request):
    repath = request.path[9:]
    base = '/Users/wcy/Documents/mysite2/'
    path = base + repath

    if os.path.isdir(path):
        try:
            list = os.listdir(path)
            # list.sort(key=lambda a: a.lower())
            list2 = []
            dirlist = []
            filelist = []
            for name in list:
                fullname = os.path.join(path, name)
                displayname = linkname = name
                # Append / for directories or @ for symbolic links
                if os.path.isdir(fullname):
                    displayname = name + "/"
                    linkname = name + "/"
                    dirlist.append(displayname)
                else:
                    filelist.append(name)

                if os.path.islink(fullname):
                    displayname = name + "@"
                # list2.append(displayname)

            return render(request, 'disk/index.html', {'cwd': repath, 'dirlist': dirlist, 'filelist':filelist})
        except os.error:
            return HttpResponse("No permission to list directory")

    elif os.path.isfile(path):
        try:
            with open(path, 'r') as f:
                content = f.readlines()
                # self.send_header('Content-type', mimetype)
            return HttpResponse(content)

        except IOError:
            return HttpResponse("File Not Found: ")






"""

# MIME-TYPE
mimedic = [
                        ('.html', 'text/html'),
                        ('.htm', 'text/html'),
                        ('.js', 'application/javascript'),
                        ('.css', 'text/css'),
                        ('.json', 'application/json'),
                        ('.png', 'image/png'),
                        ('.jpg', 'image/jpeg'),
                        ('.gif', 'image/gif'),
                        ('.txt', 'text/plain'),
                        ('.avi', 'video/x-msvideo'),
                    ]
                    
                    
    for e in mimedic:
            if e[0] == fileext:
                mimetype = e[1]
                sendReply = True                  
                    
def list_directory(self, path):
    Helper to produce a directory listing (absent index.html).

    Return value is either a file object, or None (indicating an
    error).  In either case, the headers are sent, making the
    interface the same as for send_head().

   
  
    f = StringIO()
    displaypath = cgi.escape(urllib.unquote(self.path))
    f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
    f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
    f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
    f.write("<hr>\n<ul>\n")
    
    

"""



