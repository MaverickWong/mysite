from django.http import HttpResponse

from django.shortcuts import render,redirect
from django.template import Template, Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from boards.models import *
from linkedcare.syncDB import query
import json, datetime
def hello(request):
    return render(request, 'upload-vue2.html')

# def home(request):
# 	t = get_template('index.html')
# 	c = {'board': 'i am ok ', 'a':'aaaaa'}
# 	return HttpResponse( t.render(c))
#     #return render(request, 'home.html',{'board':'what ', 'a':'aaa'})



# 患者详细信息展示

@login_required()
def home(request):
    docname = request.user.username
    if request.user.is_authenticated:
        if docname == 'zdl': #  用户名为zdl时，可以查看所有患者
            persons = Person.objects.order_by('pk').reverse()[:16]
            total = Person.objects.all().count()

        else:  #  只能看该医生的患者
            persons = Person.objects.filter(doctor=docname).order_by('pk')[:16]
            total = Person.objects.filter(doctor=docname).count()

        tags = Tag.objects.all()
        return render(request, 'index.html', {'persons': persons, 'total':total, 'tags':tags})
    else:
        return redirect('login')

@login_required()
def person_detail(request, pk):
    p = Person.objects.get(pk=pk)
    name = p.name

    picurl = ''
    if p.icon:
        picurl = p.icon
        print(picurl)

    posts = p.posts

    contex = {'patient': p,  'posts': posts}

    # return render(request, 'detail.html', contex)
    return render(request, 'detail2.html', contex)


# 从易看牙同步数据
def syncDB(request):

    # officeId 劲松122 华贸124

    # print(data['pageCount'])
    repeated = []
    succeded = []
    office =['124', '122']
    for id in office:
        data = query(id) # 从易看牙获得数据

        # 保存到文件
        fname = 'patients' + id
        with open(fname, 'w') as f:
            json.dump(data, f)

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

    dt = datetime.now()
    time = dt.strftime("%f")
    with open('log-syncDB.txt', 'w') as f:
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