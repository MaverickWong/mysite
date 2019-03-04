from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from boards.models import Person, Tag, Post,Image
import json
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from mysite.settings import BASE_DIR

import socket

from linkedcare.syncDB import get_patients_fill_DB, logIn, get_baseinfo_of_patient, add_id_for_person
from linkedcare.getXrayofLinked import getXrayOfperson

from mysite.settings import STATICFILES_DIRS

# from filemanager import FileManager
#
# def filemanager(request,path):
#
#     fm = FileManager(STATICFILES_DIRS[0]+'/')
#     return fm.render(request, path)
#
@login_required()
def show_home(request):
    return render(request, 'show-index.html')

#
# @login_required()
# def home_adminlte(request):
#     return  render(request,'starter.html')


@login_required()
def home(request):
    docname = request.user.username
    if request.user.is_authenticated:
        if docname == 'zdl': #  用户名为zdl时，可以查看所有患者[:16]
            persons = Person.objects.order_by('pk').reverse()
            total_person_num = Person.objects.all().count()

        else:  #  只能看该医生的患者
            persons = Person.objects.filter(doctor=docname).order_by('pk')
            total_person_num = Person.objects.filter(doctor=docname).count()

        # tags = Tag.objects.all()

        # 分页
        page = request.GET.get('page', 1)
        paginator = Paginator(persons, 6)
        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            # fallback to the first page
            topics = paginator.page(1)
        except EmptyPage:
            # probably the user tried to add a page number
            # in the url, so we fallback to the last page
            topics = paginator.page(paginator.num_pages)

        tgroups = []
        for i in range(10):
            tgroup = Tag.objects.filter(type=i)
            tgroups.append(tgroup)
        # tgroups.append(Tag.objects.filter(type=101)) # 添加101其他
        tags = Tag.objects.filter(type=101)

        total_posts_num = Post.objects.all().count()
        total_img_num = Image.objects.all().count()
        tag_count = Tag.objects.all().count()

        contx = {'persons': topics, 'total_person_num': total_person_num, 'total_posts_num':total_posts_num,
                 'total_img_num':total_img_num, 'tgroups':tgroups, 'tags':tags, 'tag_islink':True}

        return render(request, 'index.html', contx)
    else:
        return redirect('login')


def bad(request):
    ''' 升级维护用 '''
    return render(request, '404.html')

'''############################################'''


def summary_index(request):
    docname = request.user.username
    if request.user.is_authenticated:
        if docname == 'zdl':  # 用户名为zdl时，可以查看所有患者[:16]
            total_person_num = Person.objects.all().count()

        else:  # 只能看该医生的患者
            total_person_num = Person.objects.filter(doctor=docname).count()

        # tags = Tag.objects.all()
        total_posts_num = Post.objects.all().count()
        total_img_num = Image.objects.all().count()
        tag_count = Tag.objects.all().count()

        contx = {'total_person_num': total_person_num, 'total_posts_num': total_posts_num,
                 'total_img_num': total_img_num, 'tag_count':tag_count, 'tag_islink': True}
        return render(request, 'index.html', contx)
    else:
        return redirect('login')


def get_host_ip(request):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return HttpResponse(ip)


def hello(request):
    return render(request, 'upload-vue2.html')


# 所有post统计
def allposts(request):
    return render(request, 'log_counPostNum0219-152149.html')
# def home(request):
# 	t = get_template('index.html')
# 	c = {'board': 'i am ok ', 'a':'aaaaa'}
# 	return HttpResponse( t.render(c))
#     #return render(request, 'home.html',{'board':'what ', 'a':'aaa'})


# 组装paginator, 返回persons
def get_paginator(queryset, page):
    paginator = Paginator(queryset, 5)
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        p = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        p = paginator.page(paginator.num_pages)

    return p


# 搜索框输入字符串，先判断是否tag，及人名
def search_person_with_str(s, docname): # 搜索字符串和医生名字
    if s.isnumeric(): # 搜索内容是数字
        if docname == 'zdl':
            persons = Person.objects.filter(idnum__contains=s)
        else:
            persons = Person.objects.filter(idnum__contains=s, doctor=docname)
    elif s == '':
        persons = Person.objects.none()

    else:
        list = s.split(' ') # 按空格分割关键词
        if docname == 'zdl':
            pt = persons = Person.objects.all()
            pts =  Person.objects.none()
            for i in list:
                qn = Person.objects.filter(name__contains=i)
                if qn.count() >0:
                    persons = persons.intersection(qn)
                    continue
            # persons = Person.objects.filter(name__contains=s)
                tags = Tag.objects.filter(name__contains=i)
                for t in tags:
                    qts = t.persons.all()
                    pts = pts.union(qts)
                if pts.count()>0:
                    pt = pt.intersection(pts)

            if pt.count()>0 and (not pt.count() == Person.objects.all().count()) :
                if persons.count() >0:
                    persons = persons.intersection(pt)
                else:
                    persons = persons.union(pt)
            elif persons.count() == Person.objects.all().count():
                persons = Person.objects.none()
            #     persons = persons

        else:
            persons = Person.objects.all()
            for i in list:
                q = Person.objects.filter(name__contains=i, doctor=docname)
                persons = persons.intersection(q)
            # persons = Person.objects.filter(name__contains=s, doctor=docname)
    return persons



# 搜索框搜索
def search(request):
    docname = request.user.username
    s = request.GET['s']
    if s =='':
        return redirect('home')
    else:
        persons = search_person_with_str(s, docname)

    if persons.count() == 1:
        return redirect('person_detail', persons.first().pk)
    else:
        ps = persons.order_by('pk')
        total = ps.count()
        page = request.GET.get('page', 1)

        persons = get_paginator(ps, page)
        return render(request, 'search_result.html', {'persons': persons, 's': s, 'total':total})

def search_patients(request):
    tgroups = []
    for i in range(10):
        tgroup = Tag.objects.filter(type=i)
        tgroups.append(tgroup)
    # tgroups.append(Tag.objects.filter(type=101)) # 添加101其他
    tags = Tag.objects.filter(type=101)
    contx = {'tgroups':tgroups, 'tag_islink':True, 'tags':tags}
    return render(request, 'index_search_patients.html', contx  )


# 单个 tag 搜索
def tag_search(request, tag):
    docname = request.user.username
    ut = str(tag)
    # t = Tag.objects.get(name=ut)
    t = get_object_or_404(Tag, name=ut)
    if docname == 'zdl':
        ps = t.persons.all()
    else:
        ps= t.persons.filter(doctor=docname)

    ps = ps.order_by('pk')
    total = ps.count()
    page = request.GET.get('page', 1)

    persons = get_paginator(ps, page)

    return render(request, 'search_result.html', {'persons': persons, 'total':total})


# 多tag 相交搜索
def super_search(request):
    docname = request.user.username
    s = request.GET['s']
    if s == '':
        return redirect('home')
    else:
        # persons = search_person_with_str(s, docname)
        list = s.split(' ')  # 按空格分割关键词
        persons = Person.objects.all()

        for i in list:
            tags = Tag.objects.filter(name=i)
            if tags.count()==1:
                qts = tags[0].persons.all()
                persons = persons.intersection(qts)

    total = persons.count()

    return render(request, 'search_result.html', {'persons': persons, 'total':total})


# 搜索框推荐
def search_suggest(request):
    docname = request.user.username
    s = request.GET['s']
    if s == '':
        persons = Person.objects.none()
    else:
        persons = search_person_with_str(s, docname)

    data = []
    for p in persons:
        data.append({'name': p.name, 'idnum': p.idnum, 'pnum': p.posts.count(), 'pk':p.pk})
    # data = {'name':"<a href='/'>沃</a>", 'pk':1}
    res = {"code": 200,
           "redirect": "",
           "value": data
           }
    return JsonResponse(res)
    # return HttpResponse(json.dumps(res), content_type="application/json")


# 患者详细信息展示
#
# @login_required()
# def home(request):
#     docname = request.user.username
#     if request.user.is_authenticated:
#         if docname == 'zdl': #  用户名为zdl时，可以查看所有患者
#             persons = Person.objects.order_by('pk').reverse()[:16]
#             total = Person.objects.all().count()
#
#         else:  #  只能看该医生的患者
#             persons = Person.objects.filter(doctor=docname).order_by('pk')[:16]
#             total = Person.objects.filter(doctor=docname).count()
#
#         tags = Tag.objects.all()
#         return render(request, 'index.html', {'persons': persons, 'total':total, 'tags':tags})
#     else:
#         return redirect('login')



#  从易看牙同步患者基本信息
def syncDB(request):

    get_patients_fill_DB(20)
    return redirect('home')


    # dt = datetime.now()
    # time2 = dt.strftime("%m%d-%H%M%S")
    # # officeId 劲松122 华贸124
    # repeated = []
    # succeded = []
    # office = ['124', '122']
    # # s = logIn()
    # for id in office:
    #     s = logIn(officeId=id)
    #     data = queryPatients(s) # 从易看牙获得数据bing保存到文件
    #
    #     totalPages = data['pageCount']
    #
    #     # 导入到数据库
    #     for item in data['items']:
    #         n = Person.objects.filter(idnum__contains=item['privateId']).filter(name__contains=item['name']).count()
    #         if n > 0:  # 先根据id判断是否有重复患者，如果有则登记。没有则新建患者
    #             repeated.append(item['privateId'] + item['name'])
    #
    #         elif n == 0:
    #             if item['birth']:
    #                 birth = item['birth'][0:10]
    #             else:
    #                 birth = None
    #             p = Person.objects.create(idnum=item['privateId'], name=item['name'], nameCode=item['nameCode'],
    #                                       mobile=item['mobile'],
    #                                       otherPrivateId=item['otherPrivateId'], birth=birth, sex=item['sex'], doctor='zdl',
    #                                       doctorId=item['doctorId'], officeId=item['officeId'], clinic=item['officeId'],
    #                                       email=item['email'],
    #                                       occupation=item['occupation'], qq=item['qq'], weixin=item['weixin'],
    #                                       identityCard=item['identityCard'], homeAddress=item['homeAddress'],
    #                                       patientType=item['patientType'], lastVisit=item['lastVisit'],
    #                                       lastDoctorId=item['lastDoctorId'], linkedcareId=item['id']
    #                                       )
    #             succeded.append(item['privateId'] + '.' +item['name']+'.'+ id)
    #
    # # 记录导入log
    # fname2 = BASE_DIR +  '/log/log-syncDB' + time2 + '.txt'
    # with open(fname2, 'w') as f:
    #     # f.write("{}  {}  {}  {}\n".format(title, price, scrible, pic))
    #     f.write('succeded *******************************\n')
    #     for i in succeded:
    #         f.write(i)
    #         f.write('\n')
    #
    #     f.write('\n\n\n')
    #     f.write('repeated *******************************\n')
    #     for i in repeated:
    #         f.write(i)
    #         f.write('\n')



from linkedcare.syncDB import get_baseinfo_of_patient


#  从易看牙同步患者基本信息
def sync_xray_of_linkedcare_for_person(request, pk):
    s = logIn()
    p= Person.objects.get(pk=pk)

    get_baseinfo_of_patient(s,p)
    getXrayOfperson(s, p)
    return redirect('person_detail', pk)
    # return HttpResponse("good，请返回")
    # else:
    #     return HttpResponse('此患者无linkedcareId，请联系管理员添加')




