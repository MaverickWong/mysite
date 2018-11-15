from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from boards.models import *
from linkedcare.syncDB import queryPatients, logIn
import json
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from mysite.settings import BASE_DIR


def hello(request):
    return render(request, 'upload-vue2.html')

# def home(request):
# 	t = get_template('index.html')
# 	c = {'board': 'i am ok ', 'a':'aaaaa'}
# 	return HttpResponse( t.render(c))
#     #return render(request, 'home.html',{'board':'what ', 'a':'aaa'})

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


def search(request):
    docname = request.user.username
    s = request.GET['s']
    if s =='':
        return redirect('home')
    else:
        persons = search_person_with_str(s, docname)

    return render(request, 'search.html', {'persons': persons})

def tag_search(request, tag):
    docname = request.user.username
    ut = str(tag)
    t = Tag.objects.get(name=ut)
    if docname == 'zdl':
        ps = t.persons.all()
    else:
        ps= t.persons.filter(doctor=docname)
    return render(request, 'search.html', {'persons': ps})

def search_suggest(request):
    docname = request.user.username
    s = request.GET['s']
    if s =='':
        persons =Person.objects.none()
    else:
        persons = search_person_with_str(s, docname)

    data = []
    for p in persons:
        data.append({'姓名':p.name, '病历号':p.idnum, '图像数':p.posts.count()})
    # data = {'name':"<a href='/'>沃</a>", 'pk':1}
    res = {"code": 200,
           "redirect": "",
           "value":data
          }
    return  JsonResponse(res)
    # return HttpResponse(json.dumps(res), content_type="application/json")



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

    return render(request, 'search.html', {'persons': persons})


    # return render(request, 'super_search.html')

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

@login_required()
def home(request):
    docname = request.user.username
    if request.user.is_authenticated:
        if docname == 'zdl': #  用户名为zdl时，可以查看所有患者[:16]
            persons = Person.objects.order_by('pk').reverse()
            total = Person.objects.all().count()

        else:  #  只能看该医生的患者
            persons = Person.objects.filter(doctor=docname).order_by('pk')
            total = Person.objects.filter(doctor=docname).count()

        tags = Tag.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(persons, 14)
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

        contx = {'persons': topics, 'total':total, 'tgroups':tgroups, 'tags':tags, 'tag_islink':True}

        return render(request, 'index.html', contx)
    else:
        return redirect('login')




# 从易看牙同步患者基本信息
def syncDB(request):
    dt = datetime.now()
    time2 = dt.strftime("%m%d-%H%M%S")

    # officeId 劲松122 华贸124

    # print(data['pageCount'])
    repeated = []
    succeded = []
    office =['124', '122']
    # s = logIn()
    for id in office:
        s = logIn(officeId=id)
        data = queryPatients(s) # 从易看牙获得数据

        # 保存到文件
        try:
            fname = BASE_DIR+ '/linkedcare/get_patients' + id +'_'+time2 +'.txt'
            with open(fname, 'w') as f:
                json.dump(data, f)
        except:
            pass

        # 导入数据
        for item in data['items']:
            n = Person.objects.filter(idnum__contains=item['privateId']).filter(name__contains=item['name']).count()
            if n > 0:  # 先根据id判断是否有重复患者，如果有则登记。没有则新建患者
                repeated.append(item['privateId'] + item['name'])

            elif n == 0:
                if item['birth']:
                    birth = item['birth'][0:10]
                else:
                    birth = None
                p = Person.objects.create(idnum=item['privateId'], name=item['name'], nameCode=item['nameCode'],
                                          mobile=item['mobile'],
                                          otherPrivateId=item['otherPrivateId'], birth=birth, sex=item['sex'], doctor='zdl',
                                          doctorId=item['doctorId'], officeId=item['officeId'], clinic=item['officeId'],
                                          email=item['email'],
                                          occupation=item['occupation'], qq=item['qq'], weixin=item['weixin'],
                                          identityCard=item['identityCard'], homeAddress=item['homeAddress'],
                                          patientType=item['patientType'], lastVisit=item['lastVisit'],
                                          lastDoctorId=item['lastDoctorId']
                                          )
                succeded.append(item['privateId'] + '.' +item['name']+'.'+ id)


    fname2 = BASE_DIR +  '/log/log-syncDB' + time2 + '.txt'

    with open(fname2, 'w') as f:
        # f.write("{}  {}  {}  {}\n".format(title, price, scrible, pic))
        f.write('succeded *******************************\n')
        for i in succeded:
            f.write(i)
            f.write('\n')

        f.write('\n\n\n')
        f.write('repeated *******************************\n')
        for i in repeated:
            f.write(i)
            f.write('\n')

    return redirect('home')