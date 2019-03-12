# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.db.models import ProtectedError
from boards.models import Person, Tag, Post, Image
from mysite.settings import BASE_DIR
from datetime import datetime
import os
import json
from PIL import Image as Image2
import readFoldersWithNameIdDate

import mimetypes, zipfile
from django.utils.encoding import smart_str
from django.utils.encoding import escape_uri_path

import django.dispatch
from django.dispatch import receiver

# Create your views here.
# TODO 高级用户名是zdl

sep = '_'
# 新信号
post_upload_done = django.dispatch.Signal(providing_args=['post_pk'])


def importFolders(request):
    """
    导入图像文件夹
    """
    fname = readFoldersWithNameIdDate.start()
    # with open(fname, 'r') as f:
    #     content = f.readlines()
    # return HttpResponse(content)

    content_type, encoding = mimetypes.guess_type(str(fname))
    content_type = content_type or 'application/octet-stream'
    try:
        f = open(fname, 'rb')
        response = FileResponse(f, content_type=content_type)
        response['Content-Disposition'] = 'attachment;filename="111.txt"'
        return response

    except IOError:
        return HttpResponse(" 无法打开记录文件，请手工检查图像是否导入 ")


def down_zip(request, pk):
    """
    查询person的所有image，根据地址打包所有文件到zip文件
    """
    # todo 下载文件夹可能有两个
    p = Person.objects.get(pk=pk)
    # source_dir = BASE_DIR + '/' + p.privateDir
    output_filename = '/tmp/all.zip'
    zipf = zipfile.ZipFile(output_filename, 'w')  # zip文件

    imgs = p.images.all()
    for img in imgs:
        pathfile = BASE_DIR + img.path  # 要打包的文件
        if os.path.exists(pathfile):
            # 在zip中的相对路径
            relative_path = os.path.basename(os.path.dirname(pathfile))
            arcname = relative_path + os.path.sep + os.path.basename(pathfile)
            zipf.write(pathfile, arcname)
    zipf.close()

    '''
     zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            if ('small' in filename) or ( 'medium' in filename):
                # 去除small， medium 文件
                continue
            pathfile = os.path.join(parent, filename) # 要打包的文件
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 在zip中的相对路径
            zipf.write(pathfile, arcname)
    zipf.close()
    '''

    content_type, encoding = mimetypes.guess_type(str(output_filename))
    content_type = content_type or 'application/octet-stream'

    try:
        f = open(output_filename, 'rb')
        response = FileResponse(f, content_type=content_type)
        # response['Content-Disposition'] = 'attachment;filename="example.tar.gz"'
        response['Content-Disposition'] = 'attachment; filename="' + smart_str(p.name) + '.zip"'
        # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(p.name.encode('utf-8'))

        return response
    except IOError:
        return HttpResponse(" 无法打开该文件，请检查文件名 ")


def test(request):
    return HttpResponse("good")


def get_tag_groups():
    tgroups = []
    for i in range(10):
        tgroup = Tag.objects.filter(type=i)
        tgroups.append(tgroup)
    return tgroups


def s_search(request):
    tgroups = get_tag_groups()
    tags = Tag.objects.all()

    return render(request, 's_search.html', {'tags': tags, 'tgroups': tgroups})


@login_required()
def person_detail(request, pk):
    p = Person.objects.get(pk=pk)
    name = p.name

    picurl = ''
    if p.icon:
        picurl = p.icon
        print(picurl)

    posts = p.posts

    contex = {'patient': p, 'posts': posts, 'first_tab': 0}

    if request.GET.get('tab'):
        t = request.GET.get('tab')
        contex = {'patient': p, 'posts': posts, 'first_tab': t}

    # return render(request, 'detail.html', contex)
    return render(request, 'boards/detail2.html', contex)

@login_required()

def delperson(request, pk):
    p = Person.objects.get(pk=pk)
    p.delete()
    return redirect('home')


# TODO
@login_required()
def delpost(request, ppk, postpk):
    # try:
    po = Post.objects.get(pk=postpk)
    po.delete()
    # except ProtectedError:
    #     err = "无法删除该复诊"
    #     return  HttpResponse(err)
    # pk = int(ppk)
    # return HttpResponseRedirect( reverse('person_detail', args=(ppk)) )
    return redirect('posts', ppk)


def save_upload_file_make_logo(file, dir):
    # 保存文件
    logoPath = dir + 'logo.jpg'
    if os.path.exists(logoPath):
        ff = open(logoPath, 'wb+')
        for chunk in file.chunks():
            ff.write(chunk)
        ff.close()

        # 制作缩略图函数
        im = Image2.open(logoPath)
        ssize = (400, 400)
        if im:
            try:
                im.thumbnail(ssize)
                im.save(logoPath, "JPEG")
                return logoPath
            except IOError:
                print("cannot create thumbnail")
                return False


# 处理上传文件
def handle_file(request, person, post):
    docname = request.user.username
    files = request.FILES.getlist('files[]')  # 类型为mutilist
    # n = request.POST.get('name')
    sep = '_'  # 文件名中的分隔符

    # 返回结果
    results = {}
    results["files"] = []
    print(files)

    i = 0
    for f in files:
        dt = datetime.now()
        times = dt.strftime("%f")
        datestr = dt.strftime("%Y%m%d")
        # static / picture / 张飞_233 /
        dir = 'static/picture/' + docname +'/' +person.name + sep + str(person.idnum) + '/'
        post.dir = dir  # 保存post的文件夹
        post.save()
        # 保存到person作为私人文件夹
        if person.privateDir:
            dir = person.privateDir
        else:
            person.privateDir = dir
            person.save()

        if dir[0] == '/':  # 检查开头是否有 '/'，如果有，则去除
            dir = dir[1:]
        # icondir = dir  + 'small' + '/'
        if not dir[-1] == '/':  # 检查末尾是否有 '/'，如果没有，添加
            dir = dir + '/'

        # TODO 相对目录有时容易出问题
        dir = os.path.join(BASE_DIR, dir)

        icondir = dir
        mediumdir = dir
        if not os.path.exists(dir):
            os.makedirs(dir)
        if not os.path.exists(icondir):
            os.makedirs(icondir)
        if not os.path.exists(mediumdir):
            os.makedirs(icondir)
        # 文件名及路径
        # n2 = f.name
        # # suf = n2.split('.')[-1]
        suf = 'jpg'
        # 文件名   张飞_20180101_S0_041411.jpg
        fname = person.name + sep + datestr + sep + 'S' + str(post.type) + sep + str(i) + times + '.' + suf
        # 相对全路径 static / picture / 张飞_233 / 张飞_20180101_041411.jpg
        path = dir + fname
        iconpath = icondir + 'small' + fname
        mediumpath = mediumdir + 'medium' + fname

        # 保存文件
        ff = open(path, 'wb+')
        for chunk in f.chunks():
            ff.write(chunk)
        ff.close()
        i = i + 1

        # 制作缩略图函数
        if os.path.exists(path):
            im = Image2.open(path)
            ssize = (400, 400)
            msize = (1200, 1200)
            if im:
                try:
                    im.thumbnail(msize)
                    im.save(mediumpath, "JPEG")
                    im.thumbnail(ssize)
                    im.save(iconpath, "JPEG")

                except IOError:
                    print("cannot create thumbnail")

        # 制作url，及保存到数据库
        path = path.replace(BASE_DIR, '')
        iconpath = iconpath.replace(BASE_DIR, '')
        mediumpath = mediumpath.replace(BASE_DIR, '')

        if not path[0] == '/':  # 检查开头是否有 '/'，如果有，则去除
            pathU = '/' + path
        else:
            pathU = path
        if not iconpath[0] == '/':  # 检查开头是否有 '/'，如果有，则去除
            iconpathU = '/' + iconpath
        else:
            iconpathU = iconpath
        if not mediumpath[0] == '/':  # 检查开头是否有 '/'，如果有，则去除
            mediumpathU = '/' + mediumpath
        else:
            mediumpathU = mediumpath

        # 保存到image
        image = Image.objects.create(path=pathU, thumbnail=iconpathU, post=post, person=person, size_m=mediumpathU)

        # 添加头像
        # if post.type ==0 and i ==1:
        #     person.icon = iconpathU
        #     person.save()
        # if dir[0] == '/': #  检查开头是否有 '/'，如果有，则去除
        #     dir = dir[1:]

        path = BASE_DIR + path
        # 返回上传信息
        if os.path.exists(path):  # 再次确认文件是否保存
            t1 = "上传成功:  " + fname
        else:
            t1 = "服务器保存失败"
        info = {
            "name": t1,
            "size": os.path.getsize(path),
            "url": path,
            "thumbnailUrl": iconpathU,
            "deleteUrl": '',
            "deleteType": "DELETE", }
        results["files"].append(info)

    return results


@login_required()
def new_person(request):
    # board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':

        docname = request.user.username
        # message = request.POST['ID']
        tag_list = request.POST['newTags']
        name = request.POST['name']
        idnum = request.POST['ID']
        # birth = request.POST['nameCode']
        # nameCode=request.POST['nameCode']
        # 设定文件夹
        try:
            sex = request.POST['sex']
        except:
            sex = 0

        # dir = 'static/picture/' + name + '_' + idnum + '/'
        # 根据每个医生user名生成文件夹
        docDir = 'static/picture/' + docname + '/'
        if not os.path.exists(docDir):
            os.makedirs(docDir)

        privateDir = docDir + name + sep + str(idnum) + '/'
        if not os.path.exists(privateDir):
            os.makedirs(privateDir)

        if Person.objects.filter(name=name, idnum=idnum, doctor=docname).exists():
            return redirect('wrong')
        else:
            person = Person.objects.create(name=name, idnum=idnum, doctor=docname, privateDir=privateDir)
            # TODO 添加新患者信息
            # person = Person.objects.create(name=name,
            #                                idnum=idnum,
            #                                doctor=docname,
            #                                mobile=request.POST['mobile'],
            #                                nameCode=request.POST['nameCode'],
            #                                email=request.POST['email'],
            #                                QQ=request.POST['QQ'],
            #                                weixin=request.POST['weixin'],
            #                                occupation=request.POST['occupation'],
            #                                identityCard=request.POST['identityCard'],
            #                                homeAddress=request.POST['homeAddress'],
            #                                linkedcareId=request.POST['linkedcareId']
            #                                )
            try:
                person.mobile = request.POST['mobile']
                person.save()
                person.nameCode = request.POST['nameCode']
                person.save()
                person.email = request.POST['email']
                person.save()
                person.QQ = request.POST['QQ']
                person.save()
                person.weixin = request.POST['weixin']
                person.save()
                person.occupation = request.POST['occupation']
                person.save()
                person.identityCard = request.POST['identityCard']
                person.save()
                person.homeAddress = request.POST['homeAddress']
                person.save()
                person.linkedcareId = request.POST['linkedcareId']
                person.save()
                person.sex = request.POST['sex']
                person.save()
            except:
                pass

        # post = Post.objects.create(type=0, isFirst=1, person=person)

        # 处理上传图像，当做logo
        files = request.FILES.getlist('files[]')  # 类型为mutilist
        if files:
            # logoPath = privateDir + 'logo.jpg'
            path = save_upload_file_make_logo(files[0], privateDir)
            if path:
                person.icon = path
                person.save()

        # 处理新增tags
        new_tag_list = tag_list.split(' ')
        if new_tag_list:
            for t in new_tag_list:
                tags = Tag.objects.filter(name=t)
                if tags.count() == 1:  # 查到一个
                    tags[0].persons.add(person)
                    tags[0].save()
                elif tags.count() == 0:  # 未查到
                    tag2 = Tag.objects.create(name=t, type=101)
                    tag2.persons.add(person)
                    tag2.save()

        # result2 = json.dumps(results)
        return redirect('person_detail', person.pk)

    if request.method == 'GET':
        tgroups = []
        for i in range(10):
            tgroup = Tag.objects.filter(type=i)
            tgroups.append(tgroup)
        tags = Tag.objects.all()
        return render(request, 'upload/newPerson.html', {'tgroups': tgroups, "tags": tags})


# 上传x线功能
def addpost_xray(request, pk):
    """
        添加x线图片post
        :param request:
        :param pk:
        :return:
        """
    p = Person.objects.get(pk=pk)

    if request.method == 'GET':
        # TODO 应该获取posts总数，然后发到网页内部
        tags = Tag.objects.all()
        # print(tags)
        return render(request, 'upload/addpost_xray.html', {'patient': p})

    if request.method == 'POST':
        # p = Person.objects.get(pk=pk)
        postnum = request.POST.get('postType')
        tag_list = request.POST['newTags']
        comment = request.POST['comment']

        # 如果没有，直接新建
        if postnum.isnumeric():  # 有上传posttype， 往post type增加image
            i = Post.objects.filter(type=postnum, person=p, type__gte=100).count()
            if i == 0:
                post = Post.objects.create(type=postnum, person=p, comment=comment, name=comment)
            elif i == 1:
                post = Post.objects.get(type=postnum, person=p, comment=comment, name=comment)
        else:  # 未上传posttype， 新建post，type+1
            n = Post.objects.filter(person=p, type__gte=100).count()
            post = Post.objects.create(type=100 + n + 1, person=p, comment=comment, name=comment)
        # Image保存生成path
        results = handle_file(request, p, post)

        # 处理新增tags
        new_tag_list = tag_list.split(' ')
        if new_tag_list:
            add_tag_from_string_for_person(new_tag_list, p)

        result2 = json.dumps(results)
        return HttpResponse(result2, content_type='application/json')

    # return HttpResponse("暂未开放上传x线功能")


def addpost(request, pk):
    """
    添加普通图片post
    :param request:
    :param pk:
    :return:
    """
    p = Person.objects.get(pk=pk)

    if request.method == 'GET':
        # TODO 应该获取posts总数，然后发到网页内部
        # tgroups = []
        # for i in range(10):
        #     tgroup = Tag.objects.filter(type=i)
        #     tgroups.append(tgroup)
        tags = Tag.objects.all()
        # print(tags)
        return render(request, 'upload/addpost.html', {'patient': p, "tags": tags})

    if request.method == 'POST':
        # p = Person.objects.get(pk=pk)
        postnum = request.POST.get('postType')
        tag_list = request.POST['newTags']
        comment = request.POST['comment']

        # 如果没有，直接新建
        if postnum.isnumeric():  # 有上传posttype， 往post type增加image
            i = Post.objects.filter(type=postnum, person=p).count()
            if i == 0:
                post = Post.objects.create(type=postnum, person=p, comment=comment, name=comment)
            elif i == 1:
                post = Post.objects.get(type=postnum, person=p, comment=comment, name=comment)
        else:  # 未上传posttype， 新建post，type+1
            n = Post.objects.filter(person=p).count()
            post = Post.objects.create(type=n + 1, person=p, comment=comment, name=comment)
        # Image保存生成path
        results = handle_file(request, p, post)

        # 处理新增tags
        new_tag_list = tag_list.split(' ')
        if new_tag_list:
            add_tag_from_string_for_person(new_tag_list, p)

        result2 = json.dumps(results)

        # 发送完成信号，进行后续处理
        post_upload_done.send(addpost, post_pk=post.pk)

        return HttpResponse(result2, content_type='application/json')

    # return HttpResponse('{"status":"success"}', content_type='application/json')


@receiver(post_upload_done, sender=addpost)
def post_upload_done_func(sender, **kwargs):
    '''
    上传后处理函数，
    :param sender: 
    :param kwargs: 
    :return: 
    '''
    print('upload done!')


def add_tag_from_string_for_person(new_tag_list, p):
    for t in new_tag_list:
        if not t == '':
            tags = Tag.objects.filter(name=t)
            if tags.count() == 1:  # 查到一个
                tags[0].persons.add(p)
                tags[0].save()
            elif tags.count() == 0:  # 未查到
                tag2 = Tag.objects.create(name=t, type=101)
                tag2.persons.add(p)
                tag2.save()


# 患者详细信息展示

# @login_required()
# def person_detail(request, pk):
#     p = Person.objects.get(pk=pk)
#     name = p.name
#
#     picurl = ''
#     if p.icon:
#         picurl = p.icon
#         print(picurl)
#
#     posts = p.posts
#
#     contex = {'patient': p,  'posts': posts}
#
#     # return render(request, 'detail.html', contex)
#     return render(request, 'detail2.html', contex)
#

@login_required()
def posts(request, pk):
    """
    获取所有患者的所有 普通post
    :param request:
    :param pk:
    :return:
    """
    p = Person.objects.get(pk=pk)
    name = p.name

    picurl = ''
    if p.icon:
        picurl = p.icon
        print(picurl)

    posts = p.posts.filter(type__lte=99).order_by('-type')
    contex = {'patient': p, 'posts': posts}

    return render(request, 'boards/detail3.html', contex)


def posts_xray(request, pk):
    """
    # 所有x线post（原易看牙导入图像）
    :param request:
    :param pk:
    :return:
    """
    p = Person.objects.get(pk=pk)
    name = p.name

    picurl = ''
    if p.icon:
        picurl = p.icon
        print(picurl)

    posts = p.posts.filter(type__gte=100)
    contex = {'patient': p, 'posts': posts, 'isXray': True}

    return render(request, 'boards/detail3.html', contex)



# def baseinfo(request, pk):
#     """
#     患者的基本信息
#     :param request:
#     :param pk:
#     :return:
#     """
#     p = Person.objects.get(pk=pk)
#     return render(request, 'baseinfo/baseInfo.html', {'person': p})


def wrong(request):
    return render(request, 'upload/wrong.html', {})


def add_tag_for_person(request, pk):
    if request.method == 'POST':
        p = get_object_or_404(Person, pk=pk)
        # postnum = request.POST.get('postType')
        tag_list = request.POST['s']
        # comment = request.POST['comment']

        # 处理新增tags
        new_tag_list = tag_list.split(' ')
        if new_tag_list:
            add_tag_from_string_for_person(new_tag_list, p)
        return redirect('person_detail', pk)

    else:
        p = get_object_or_404(Person, pk=pk)
        tgroups = get_tag_groups()
        tags = Tag.objects.all()

        return render(request, 'tag/add_tag.html', {'patient': p, 'tags': tags, 'tgroups': tgroups})
