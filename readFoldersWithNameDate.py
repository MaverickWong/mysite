#!/usr/bin/python
# -*- coding:utf8 -*-


# 这个一定要
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
# django版本大于1.7时需要这两句

"""
# 针对单个文件夹的导入
# 要求：文件夹名格式：姓名  日期， 例如："张飞 2314 20180101" 
#      无id，设为0000
# 
"""


# python3 -u /home/zdl/mysite2/readfiles.py

from boards.models import *
import re,shutil
# from PIL  import Image as Image2
from pathlib import PurePosixPath
from datetime import date, time, datetime
from imgeprocess2 import processImg
from mysite.settings import  BASE_DIR

def is_img(ext):
    ext = ext.lower()
    if ext in ['jpg', 'JPG', 'png','PNG', 'jpeg','JPEG', 'bmp','BMP']:
        return True
    else:
        return False


def find_creat_Tag(name, person):
    tags = Tag.objects.filter(name__contains=name)
    if tags.count() == 1:  # 查到一个，则往该tag增加person
        tags[0].persons.add(person)
        tags[0].save()
    elif tags.count() == 0:  # 未查到则新建tag
        tag2 = Tag.objects.create(name=name)
        tag2.persons.add(person)
        tag2.save()

#/Users/wcy/Documents/mysite2/static/待导入图像
# /home/zdl/mysite2/static/a待导入图片
# base = "/Users/wcy/Documents/mysite2"
# base = "/home/zdl/mysite2"

base = BASE_DIR
# inputDir = '/static/a待导入图像'
inputDir = '/static/a待导入图片'

picDir = base + '/static/picture'
# /Volumes/张栋梁病例照片/正畸患者照片/唇侧正畸/A/
# dir = "/static/picture/老硬盘照片"
# dir = "/static/picture/a正畸患者照片"

# path = base+ dir
path = base + inputDir

allpatients = []
repeated = []
# repeatedDic = {'name':'', 'id':'', 'path':''}
added = []
# addedDic = {'name':'', 'id':'', 'pk':'', 'path':''}
created = []
# createdDic = {'name':'', 'id':'', 'pk':'', 'path':''}
pics =[]
posts = []
picpks = [] #存储新图片的pk

err = []
d = u"[\u4e00-\u9fa5]+"  # 中文 匹配
d2 = u"[d]+"  # 匹配 数字
patternDigt = re.compile(r'\d+')   # 查找数字
patternA = re.compile(d)  # 中文

dt = datetime.now()
sep = '_'


def start():
    for root, dirs, files in os.walk(path):
        # 先判断该文件夹是否有图像文件
        have_file = False
        for file in files:
            # print("File:%s,  %s" %(file, root))fro
            ext = file.split('.')[-1]
            if is_img(ext):
                have_file = True
                break

        if have_file:
            post = root.split('/')[-1]  # 患者文件夹名
            if not post == 'small':
                try:
                    # pfull = root.split('/')[-2]  # 患者文件夹名
                    print("\n读取。。" +"  " + post)
                    privDir = ''
                    isNew = False
                    newP = Person.objects.get(pk=4) # 先随便取出一个人

                    # 提取名字+id ----
                    # TODO 名字只是中文
                    nameList = patternA.findall(post)  # 名字
                    # todo idlsit 当做日期list
                    idlist = patternDigt.findall(post) # 数字

                    #  创建或者提取患者 newPerson
                    name = nameList[0]
                    # zlist = ['张', '栋', '梁']
                    # exit_flag =False
                    # for nnn in nameList:
                    #     exit_flag = False
                    #
                    #     for zz in zlist:
                    #         if zz in nnn:
                    #             exit_flag = True
                    #             break
                    #     if exit_flag:
                    #         continue
                    #     name = nnn
                    #     break

                    # if nameList:
                    #     for t in nameList:
                    #         if not t == name: #  排除姓名
                    #             find_creat_Tag(t, newP)

                    # if idlist: # 文件夹名字有数字
                    #     id = idlist[0]
                    #     # TODO 假设第一个是id
                    #     privDir = picDir +'/zdl/'+ name+'_'+id+'/' # 临时设置privDdir 为 名字加id
                    #
                    #     print("\n解析为 " + name + "  " + id)
                    #     pquery = Person.objects.filter(name__contains=name)
                    #     pnum = pquery.count()
                    #     if pnum == 0:
                    #         newP = Person.objects.create(name=name,  idnum=int(id), comment=post, doctor='zdl')
                    #         isNew =True
                    #         d =  name+ ' '+ str(id)+ ' '+str(newP.pk)+ ' '+root
                    #         created.append(d)
                    #     elif pnum == 1:
                    #         newP = pquery[0]
                    #         if not newP.idnum == idlist[0]:
                    #             newP = Person.objects.create(name=name, idnum=int(id), comment=post, doctor='zdl')
                    #             isNew = True
                    #             d = name + ' ' + str(id) + ' ' + str(newP.pk) + ' ' + root
                    #             created.append(d)
                    #
                    #
                    #     elif pnum > 1: #  查询出多个患者，只登记
                    #         query2 = pquery.filter(idnum__contains=id)
                    #         if query2.count()==1:
                    #             newP = query2[0]
                    #         else:
                    #             d = name + ' ' + str(id) + ' ' + root
                    #             repeated.append(d)
                    #             print("\n发现重复患者： %s" % post)
                    #             continue


                    # else:  # 无病历号, 则设置为0000
                    privDir = picDir + '/'+'zdl'+'/' + name + '_' + '0000' + '/'
                    print("\n解析为 " + name  )
                    pquery = Person.objects.filter(name__contains=name)
                    pnum = pquery.count()
                    if pnum == 0:
                        newP = Person.objects.create(name=name, idnum=0000, comment=post, doctor='zdl')
                        isNew =True
                        d = name+ ' '+str(newP.pk)+ ' '+root
                        created.append(d)
                    elif pnum == 1:
                        newP = Person.objects.get(name=name)
                        # d = {'name':name, 'id':'', 'pk':str(newP.pk), 'path':root}
                        # added.append(d)
                    elif pnum > 1:
                        d = name+ ' '+root
                        repeated.append(d)
                        print("\n发现重复患者： %s" % post)
                        continue

                    # 移动到新文件夹
                    if not os.path.exists(privDir):
                        os.makedirs(privDir)

                    if isNew:  # 是新建患者
                        newP.privateDir = privDir.replace(base+'/', '') # 相对地址 static/picture/zdl/xxx_123
                        newP.save()
                    elif not newP.privateDir:  # 不是新创建患者，但是该患者privDir是空的
                        newP.privateDir = privDir.replace(base+'/', '')
                        newP.save()
                    else:
                        privDir = base + '/' + newP.privateDir

                    # if nameList:
                    #     for t in nameList:
                    #         if not t == name:  # 排除姓名
                    #             find_creat_Tag(t, newP)
                    #
                    # # 提取名字+id ----默认人名文件夹中的数字只可能是id
                    # rootList = patternA.findall(root)  # 所有汉子
                    # if rootList:
                    #     for t in rootList:
                    #         if not t == name:  # 排除姓名
                    #             find_creat_Tag(t, newP)

                    #  开始处理post及图片
                    numPost = newP.posts.count()
                    path3 = privDir.replace(base, '')
                    newPost = Post.objects.create(name=post, person=newP, type=numPost+1, comment=post, dir=path3)
                    d = post+ ' '+newP.name+ ' '+str(newPost.pk)
                    posts.append(d)

                    # 开始处理图像，存储
                    for file in files:
                        ext = file.split('.')[-1]
                        if is_img(ext) and file[0] != '.' :
                            dt = datetime.now()
                            times = dt.strftime("%f")
                            datestr = dt.strftime("%Y%m%d")
                            # 新文件名
                            new_name = name + sep+ datestr + sep + 'S'+ str(numPost+1)+ sep +  times + '.' + ext
                            fpath = privDir+ new_name
                            old = root+'/'+file
                            shutil.move(old, fpath)
                            if os.path.exists(fpath):

                                path2 = fpath.replace(base, '')  # 图片相对地址 /static/picture/x/x/x/.jpg
                                newImg = Image.objects.create(name=file, post=newPost, person=newP, path=path2)
                                d = str(newPost.pk) + ' ' + path2
                                pics.append(d)
                                picpks.append(newImg.pk)
                                print("移动并创建image：%s   %s   患者：%s" % (file, new_name, post))

                    shutil.rmtree(root)
                    print("删除 %s" % (root))

                except:
                    err.append(root)
                    pass

    # 为新增的照片生成缩率图
    for pk in picpks:
        img = Image.objects.get(pk=pk)
        processImg(img, base=base)

    print('\n导入完成，正在生成log文件。。。。')

    dt = datetime.now()
    time2 = dt.strftime("%m%d-%H%M%S")
    fname2='log/log_readFoldrewithname' +time2+ '.txt'

    with open(fname2, 'w+') as f:

        f.write('\n\n\n多名重复患者**************************************\n')
        f.write('name' + ' ' +  'id'  + ' ' +  'path'  + '\n')
        f.write('总计：'+ str(len(repeated))+ '\n')
        for d in repeated:
            f.write(d + '\n')

        f.write('\n\n\n错误文件夹**************************************\n')
        for e in err:
            f.write(e+'\n')

        f.write('\n\n\n新建患者*******************************************\n')
        f.write('总计：'+ str(len(created) )+ '\n')
        f.write('name' + ' ' +  'id'  + ' ' + 'pk' +' '+  'path'  + '\n')
        for d in created:
            f.write(d+ '\n')

        # f.write('\n\n\n直接添加图片的患者*****************************\n')
        # f.write('name' + ' ' +  'id'  + ' ' + 'pk' +' '+  'path'  + '\n')
        # for d in added:
        #     f.write(d['name'] +' '+ d['id'] +' ' +d['pk']+' '+ d['path'] + '\n')

        f.write('\n\n\n直接添加 POSTs***********************************\n')
        f.write('总计：'+ str(len(posts))+ '\n')
        f.write('name' + ' ' +  'person'  + ' ' + 'pk' +' '+  'path'  + '\n')
        for d in posts:
            f.write(d+ '\n')

        f.write('\n\n\n添加图片*****************************************\n')
        f.write('总计：'+ str(len(pics))+ '\n')
        f.write('name' + ' ' +  'id'  + ' ' + 'pk' +' '+  'path'  + '\n')
        for d in pics:
            f.write(d+'\n')


    print("\nLog 保存完成")

    return fname2


if __name__=='__main__':
    start()
