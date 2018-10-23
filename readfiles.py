#!/usr/bin/python
# -*- coding:utf8 -*-
# 这个一定要，不然会报错，但是错误很明显，容易定位。
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
# django版本大于1.7时需要这两句

# ssh://zdl@192.168.3.104:22/usr/bin/python3 -u /home/zdl/.pycharm_helpers/pydev/pydevd.py --multiproc --qt-support=auto --client '0.0.0.0' --port 33557 --file /home/zdl/mysite2/readfiles.py


from boards.models import *
import re
from PIL  import Image as Image2
from pathlib import PurePosixPath
from datetime import date, time, datetime
import threading


def is_img(ext):
    ext = ext.lower()
    if ext in ['jpg', 'png', 'jpeg', 'bmp']:
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



base = "/Users/wcy/Documents/mysite2"
# /Volumes/张栋梁病例照片/正畸患者照片/唇侧正畸/A/
dir = "/static/picture/老硬盘照片"
path = base+ dir
# base = "\Users\Wang\mysite2/static/老硬盘照片"

allpatients = []
repeated = []
# repeatedDic = {'name':'', 'id':'', 'path':''}
added = []
# addedDic = {'name':'', 'id':'', 'pk':'', 'path':''}
created = []
# createdDic = {'name':'', 'id':'', 'pk':'', 'path':''}
pics =[]
posts = []

err = []
d = u"[\u4e00-\u9fa5]+"  # 中文 匹配
d2 = u"[d]+"  # 匹配 数字
patternDigt = re.compile(r'\d+')   # 查找数字
patternA = re.compile(d)


# def start():
for root, dirs, files in os.walk(path):
    have_file = False
    for file in files:
        # print("File:%s,  %s" %(file, root))fro
        ext = file.split('.')[-1]
        if is_img(ext):
            have_file = True

    # if not have_file:  # 空文件夹
    #     continue
    # else:  # 文件夹内有文件
    if have_file:
        post = root.split('/')[-1]  # post文件夹名称
        if not post=='small':
            try:
                pfull = root.split('/')[-2]  # 患者文件夹名
                print("\n读取。。" + pfull + "  " + post)

                newP = Person.objects.get(pk=1) # 先随便取出一个人

                # 提取名字+id ----默认人名文件夹中的数字只可能是id
                nameList = patternA.findall(pfull)  # 名字
                idlist = patternDigt.findall(pfull) # id

                #  创建或者提取患者 newPerson
                name = nameList[0]
                if idlist: #有病历号
                    id = idlist[0]
                    print("\n解析为 " + name + "  " + id)
                    pquery = Person.objects.filter(name__contains=name, idnum__contains=id)
                    pnum = pquery.count()
                    if pnum == 0:
                        newP = Person.objects.create(name=name, idnum=id, comment=pfull, doctor='zdl')
                        d = {'name':name, 'id':str(id), 'pk':str(newP.pk), 'path':root}
                        created.append(d)
                    elif pnum == 1:
                        newP = pquery[0]
                    elif pnum > 1: #  查询出多个患者，只登记
                        d = {'name':name, 'id':str(id), 'path':root}
                        repeated.append(d)
                        print("\n发现重复患者： %s" % pfull)
                        continue

                else:  # 无病历号
                    print("\n解析为 " + name + "  无id " )
                    pquery = Person.objects.filter(name__contains=name)
                    pnum = pquery.count()
                    if pnum == 0:
                        newP = Person.objects.create(name=name, comment=pfull, doctor='zdl')
                        d = {'name':name, 'id':'', 'pk':str(newP.pk), 'path':root}
                        created.append(d)
                    elif pnum == 1:
                        newP = Person.objects.get(name=name)
                        # d = {'name':name, 'id':'', 'pk':str(newP.pk), 'path':root}
                        # added.append(d)
                    elif pnum > 1:
                        d = {'name':name, 'id':'',  'path':root}
                        repeated.append(d)
                        print("\n发现重复患者： %s" % pfull)
                        continue

                # 设定privateDir
                p= PurePosixPath(root)
                priv = str(p.parents[0]).replace(base, '')
                priv = priv.replace('/', '', 1) # 图片相对地址 static/picture     x/x/x/.jpg
                newP.privateDir = priv
                newP.save()

                # 增加tag
                # 从患者名字文件夹中提取
                if nameList:
                    for t in nameList:
                        if not t == name: #  排除姓名
                            find_creat_Tag(t, newP)
                            # tags = Tag.objects.filter(name__contains=t)
                            # if tags.count() == 1:  # 查到一个，则往该tag增加person
                            #     tags[0].persons.add(newP)
                            #     tags[0].save()
                            # elif tags.count() == 0:  # 未查到则新建tag
                            #     tag2 = Tag.objects.create(name=t)
                            #     tag2.persons.add(newP)
                            #     tag2.save()
                # 从post文件夹名字中提取
                postlist = patternA.findall(post)  # post中含有的汉子
                for t in postlist:
                    if not t == name:  # 排除姓名
                        find_creat_Tag(t, newP)

                biglist = ['唇侧', '舌侧', '隐适美', 'Invislign']
                for t in biglist:
                    if t in root:
                        find_creat_Tag(t, newP)


                #  开始处理post及图片
                n = newP.posts.count()
                #  处理post名称，取出所有数字
                dd = patternDigt.findall(post)
                post_re = ''  # 存储post名字中的所有数字，如果未找到数字，则存储post文件夹名
                if dd:
                    for d in dd:
                        post_re = post_re + str(d)
                else:
                    post_re = post

                # 如果post已经存在，则跳出循环，不处理内部的照片
                if Post.objects.filter(comment__contains=post, person=newP).count()>0:
                    continue
                else:  # 不存在则新建post
                    dir = root.replace(base, '') # 图片相对地址 /static/picture/xxx/xxx
                    newPost = Post.objects.create(name=post_re, person=newP, type=n+1, comment=post, dir=dir)
                    d = {'name':post, 'person':newP.name, 'pk':str(newPost.pk)}
                    posts.append(d)

                    # 开始处理图像，存储
                    for file in files:
                        ext = file.split('.')[-1]
                        if is_img(ext):
                            fpath = root+'/'+file
                            path2 = fpath.replace(base, '')  # 图片相对地址 /static/picture/x/x/x/.jpg
                            newImg = Image.objects.create(name=file, post=newPost, person=newP, path=path2)
                            d = {'pk':str(newPost.pk), 'path':path2}
                            pics.append(d)
                            print("创建image：%s post：%s 患者：%s" % (file, post, pfull))


                        # ext = file.split('.')[-1]
                        # if is_img(ext):  # 是图像
                        #     # dir = 'static/picture/' + person.name + sep + str(person.idnum) + '/'
                        #     icondir = root + '/small' + '/'
                        #     iconpath = icondir+file
                        #     if not os.path.exists(icondir):
                        #         os.mkdir(icondir)
                        #     # 制作缩略图函数
                        #     fpath = root+'/'+file
                        #     if os.path.exists(fpath):
                        #         im = Image2.open(fpath)
                        #         size = (400, 400)
                        #         if im:
                        #             try:
                        #                 # im = Image.open(infile)
                        #                 im.thumbnail(size)
                        #                 im.save(iconpath, "JPEG")
                        #             except IOError:
                        #                 print("cannot create thumbnail")
                        #
                        #     path2 =   fpath.replace(base, '')  # 图片相对地址 /static/picture/x/x/x/.jpg
                        #     iconpath2 = iconpath.replace(base, '')
                        #     newImg = Image.objects.create(name=file, post=newPost, person=newP, path=path2, thumbnail=iconpath2)
                        #     d = {'pk':str(newPost.pk), 'path':path2}
                        #     pics.append(d)
                        #     print("创建image：%s post：%s 患者：%s" % (file, post, pfull))
            except:
                err.append(root)
                pass


print('\n导入完成，正在生成log文件。。。。')

dt = datetime.now()
time2 = dt.strftime("%m%d-%H%M%S")
fname2='log/log_readfile' +time2+ '.txt'

with open(fname2, 'w+') as f:

    f.write('\n\n\n多名重复患者**************************************\n')
    f.write('name' + ' ' +  'id'  + ' ' +  'path'  + '\n')
    f.write('总计：'+ str(len(repeated))+ '\n')
    for d in repeated:
        f.write(d['name'] +' '+ d['id'] +' '+ d['path'] + '\n')

    f.write('\n\n\n错误文件夹**************************************\n')
    for e in err:
        f.write(e+'\n')

    f.write('\n\n\n新建患者*******************************************\n')
    f.write('总计：'+ str(len(created) )+ '\n')
    f.write('name' + ' ' +  'id'  + ' ' + 'pk' +' '+  'path'  + '\n')
    for d in created:
        f.write(d['name'] +' '+ d['id'] +' ' +d['pk']+' '+ d['path'] + '\n')

    # f.write('\n\n\n直接添加图片的患者*****************************\n')
    # f.write('name' + ' ' +  'id'  + ' ' + 'pk' +' '+  'path'  + '\n')
    # for d in added:
    #     f.write(d['name'] +' '+ d['id'] +' ' +d['pk']+' '+ d['path'] + '\n')

    f.write('\n\n\n直接添加 POSTs***********************************\n')
    f.write('总计：'+ str(len(posts))+ '\n')
    f.write('name' + ' ' +  'person'  + ' ' + 'pk' +' '+  'path'  + '\n')
    for d in posts:
        f.write(d['name'] +' '+ d['person'] +' ' +d['pk']+ '\n')

    f.write('\n\n\n添加图片*****************************************\n')
    f.write('总计：'+ str(len(pics))+ '\n')
    f.write('name' + ' ' +  'id'  + ' ' + 'pk' +' '+  'path'  + '\n')
    for d in pics:
        f.write(d['pk']+ d['path']+'\n')






print("\nLog 保存完成，开始创建缩略图。。。")

# 取出所有Image后，检查image的path，及thumbnail，size_m，如果none，则制作缩略图



error=[]
imgAddIcon =[]


def makeIconfor(imgs, d):
    # imgs = Image.objects.all()
    total = imgs.count()
    i = 0
    for img in imgs:
        i=i+1
        try:
            # 图像名
            img_path= base +  img.path
            if os.path.exists(img_path):

                imgName= img_path.split('/')[-1]  # 赵云.p0.0186202.jpg
                # 图像的目录
                img_post  = img.post # TODO warnning 默认img已经有post信息，此处可能出错
                post_path = base + img_post.dir

                small_path = post_path+'/'+ 'small'+ '_'+ imgName
                medium_path = post_path+'/'+ 'medium'+ '_'+ imgName

                # 制作缩略图函数

                if not img.thumbnail:
                    im = Image2.open(img_path)
                    size = (400, 400)
                    if im:
                    # im = Image.open(infile)
                        im.thumbnail(size)
                        im.save(small_path, "JPEG")
                        img.thumbnail = small_path.replace(base, '')
                        img.save()
                        imgAddIcon.append(img.pk)

                if not img.size_m:
                    im = Image2.open(img_path)
                    sizem = (1200, 1200)
                    if im:
                        im.thumbnail(sizem)
                        im.save(medium_path, "JPEG")
                        img.size_m = medium_path.replace(base, '')
                        img.save()
                        print('成功制作缩略图：' + img.path + '\n')

        except:
            error.append(img.pk)

        try:
            print('进度：' + str(i*100/total) + '%\n')
        except:
            pass

lasti = Image.objects.all().last()
biggestpk = lasti.pk
# 0 - 1/4 2/4 3/4  1
threads = []
for ii in range(1, 5):
    start = int( biggestpk * (ii-1)/4)
    stop = int( biggestpk * ii/4 -1)
    img2s = Image.objects.filter(pk__range=(start, stop))
    t=threading.Thread(target=makeIconfor, args=(img2s, 1))
    threads.append(t)
    t.start()  # 开启新线程
    t.join()  # 等待所有线程完成



# error=[]
# imgAddIcon =[]
#
# imgs = Image.objects.all()
# total = imgs.count()
# i = 0
# for img in imgs:
#     i=i+1
#     try:
#         # 图像名
#         img_path= base +  img.path
#         if os.path.exists(img_path):
#
#             imgName= img_path.split('/')[-1]  # 赵云.p0.0186202.jpg
#             # 图像的目录
#             img_post  = img.post # TODO warnning 默认img已经有post信息，此处可能出错
#             post_path = base + img_post.dir
#
#             small_path = post_path+'/'+ 'small'+ '_'+ imgName
#             medium_path = post_path+'/'+ 'medium'+ '_'+ imgName
#
#             # 制作缩略图函数
#
#             if not img.thumbnail:
#                 im = Image2.open(img_path)
#                 size = (400, 400)
#                 if im:
#                 # im = Image.open(infile)
#                     im.thumbnail(size)
#                     im.save(small_path, "JPEG")
#                     img.thumbnail = small_path.replace(base, '')
#                     img.save()
#                     imgAddIcon.append(img.pk)
#             if not img.size_m:
#                 im = Image2.open(img_path)
#                 sizem = (1200, 1200)
#                 if im:
#                     im.thumbnail(sizem)
#                     im.save(medium_path, "JPEG")
#                     img.size_m = medium_path.replace(base, '')
#                     img.save()
#                     print('成功制作缩略图：' + img.path + '\n')
#
#     except:
#         error.append(img.pk)
#
#     try:
#         print('进度：' + str(i*100/total) + '%\n')
#     except:
#         pass
#


print('\n缩略图完成，正在生成log文件。。。。')


fname3 = 'log/log_iconMake' + time2 + '.txt'
with open(fname3, 'w+') as f:

    f.write('\n错误********************************************\n')
    # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
    f.write('总计：' + str(len(error)) + '\n')
    for d in error:
        f.write(d + '\n')

    f.write('\n\n\n成功添加******************************************\n')
    # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
    f.write('总计：' + str(len(imgAddIcon)) + '\n')
    for d in imgAddIcon:
        f.write(str(d) + '\n')

print('\n完成。。。。')

# ext = file.split('.')[-1]
# if is_img(ext):  # 是图像
#     # dir = 'static/picture/' + person.name + sep + str(person.idnum) + '/'
#     icondir = root + '/small' + '/'
#     iconpath = icondir+file
#     if not os.path.exists(icondir):
#         os.mkdir(icondir)
#     # 制作缩略图函数
#     fpath = root+'/'+file
#     if os.path.exists(fpath):
#         im = Image2.open(fpath)
#         size = (400, 400)
#         if im:
#             try:
#                 # im = Image.open(infile)
#                 im.thumbnail(size)
#                 im.save(iconpath, "JPEG")
#             except IOError:
#                 print("cannot create thumbnail")
#
#     path2 =   fpath.replace(base, '')  # 图片相对地址 /static/picture/x/x/x/.jpg
#     iconpath2 = iconpath.replace(base, '')
#     newImg = Image.objects.create(name=file, post=newPost, person=newP, path=path2, thumbnail=iconpath2)
#     d = {'pk':str(newPost.pk), 'path':path2}
#     pics.append(d)
#     print("创建image：%s post：%s 患者：%s" % (file, post, pfull))



# start()



#  walk的结果：root， dirs， filenames
# 假设根据阶段分文件夹，则将第一个抛弃后，新建post，image，加到person
#
# az = [] # a-z 所有字母文件夹
# for a, b, c in os.walk(base):
# 	az.append(b)
# azdir = az[0]
# # print(az[0])

# for az1 in azdir:
# 	azpath= base +'/' +az1
# 	allP= [] # 所有患者文件夹
# 	for a, b, c in os.walk(azpath):
# 		allP.append(b)
# 	persons = allP[0]
# 	print(allP[0])
#
# 	for p in persons:
# 		# 创建新person的model
# 		# personM = Person.models.create(name=p)
# 		print("\n\n\n患者：%s \n" %p)
# 		t = [] # 所有posts文件夹
# 		personDir = azpath+ '/' + p # 患者文件夹全路径
# 		for a, b, c in os.walk(personDir):
# 			# print(b)
# 			t.append(b)
# 		posts = t[0]
# 		# print(posts)
#
# 		for po in posts:
# 			podir = personDir + '/' +po
# 			# postM = Post.models.creat(name=po, person=personM)
# 			print("post：%s" %po)
# 			print(os.path.getctime(podir))
# 			files = [] # post文件夹内部所有图像文件
# 			for a, b, c in os.walk(podir):
# 				files.append(c)
# 			files = files[0]
# 			for file in files:
# 				# print(img)
# 				ext = file.split('.')[-1]
# 				if is_img(ext): # 验证是否图像文件
# 					imgpath = podir + '/' +file
# 					# 缩略图
# 					# imgM = Images.models.creat(name=img, path=imgpath, person=personM)
# 					print("创建image：%s post：%s 患者：%s" %(file, po, p))
# 					# print(os.path.getctime(imgpath))
#
