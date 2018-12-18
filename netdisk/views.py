from django.shortcuts import render
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
import os
import mimetypes
from mysite.settings import BASE_DIR


# Create your views here.


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

def showPath(request):
    repath = request.path[9:] # 跳过/netdisk/
    base = BASE_DIR
    # base = '/Users/wcy/Documents/mysite2/'
    path = base +'/' + repath

    if request.method == 'GET':

        # 判断请求地址是文件夹还是文件
        if os.path.isdir(path):  # 文件夹
            try:
                list = os.listdir(path) #读取目录列表
                # list.sort(key=lambda a: a.lower())
                dirlist = []  # 文件夹列表
                filelist = []  # 文件名列表
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

                if len(repath.split('/')) >2:
                    t = repath.split('/')[:-2]
                    pre = '/netdisk/' + '/'.join(t)
                else:
                    pre = '/netdisk/'


                return render(request, 'disk/index.html',
                              {'cwd': repath, 'pre':pre, 'dirlist': dirlist, 'filelist':filelist})
            except os.error:
                return HttpResponse("No permission to list directory")

        elif os.path.isfile(path):
            # 请求内容是文件

            # fileext = os.path.splitext(path)[1]
            # for e in mimedic:
            #     if e[0] == fileext:
            #         mimetype = e[1]
            #         sendReply = True

            content_type, encoding = mimetypes.guess_type(str(path))
            content_type = content_type or 'application/octet-stream'

            try:
                f = open(path, 'rb')
                response = FileResponse(f, content_type=content_type)
                return response
                # f.close()

            except IOError:
                return HttpResponse(" 无法打开该文件，请检查文件名 ")

    else:  # POST
        files = request.FILES.getlist('files')  # 类型为mutilist
        # n = request.POST.get('name')

        i = 0
        for f in files:
            path = path + f.name

            ff = open(path, 'wb+')
            # print(path)
            # print(f.name)
            for chunk in f.chunks():
                ff.write(chunk)
            ff.close()
            i = i + 1
        return HttpResponseRedirect(request.path)


def makedir(request):

    repath = request.path[9:] # 跳过/netdisk/
    base = BASE_DIR
    # base = '/Users/wcy/Documents/mysite2/'
    path = base +'/' + repath
    return HttpResponse("wait")


