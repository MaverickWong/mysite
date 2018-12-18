#!/usr/bin/python
# -*- coding:utf8 -*-
# 这个一定要
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
# django版本大于1.7时需要这两句

# 针对单个文件夹的导入
# 要求：文件夹名包含姓名

# python3 -u /home/zdl/mysite2/readfiles.py

from boards.models import *
import re,shutil
from PIL  import Image as Image2
from pathlib import PurePosixPath
from datetime import date, time, datetime


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

base = "/home/zdl/mysite2"
inputDir='/static/a待导入图片'
picDir = base + '/static/picture'
# /Volumes/张栋梁病例照片/正畸患者照片/唇侧正畸/A/
# dir = "/static/picture/老硬盘照片"
# dir = "/static/picture/a正畸患者照片"

# path = base+ dir
path = base + inputDir
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
patternA = re.compile(d)  # 中文

dt = datetime.now()
sep = '_'
# def start():
for root, dirs, files in os.walk(path):
    have_file = False
    for file in files:
        # print("File:%s,  %s" %(file, root))fro
        ext = file.split('.')[-1]
        if is_img(ext):
            have_file = True
            break

    if have_file:
        post = root.split('/')[-1]  # 患者文件夹名
        if not post=='small':
            try:
                # pfull = root.split('/')[-2]  # 患者文件夹名
                print("\n读取。。" +"  " + post)
                newP = Person.objects.get(pk=1) # 先随便取出一个人

                # 提取名字+id ----默认人名文件夹中的数字只可能是id
                nameList = patternA.findall(post)  # 名字
                idlist = patternDigt.findall(post) # 数字

                #  创建或者提取患者 newPerson
                name = None
                zlist = ['张', '栋', '梁']
                exit_flag =False
                for nnn in nameList:
                    exit_flag = False

                    for zz in zlist:
                        if zz in nnn:
                            exit_flag = True
                            break
                    if exit_flag:
                        continue
                    name = nnn
                    break

                if nameList:
                    for t in nameList:
                        if not t == name: #  排除姓名
                            find_creat_Tag(t, newP)

                if idlist: #有数字
                    id = idlist[0]

                    privDir = picDir + '/'+ name+'_'+id+'/'
                    print("\n解析为 " + name + "  " + id)
                    pquery = Person.objects.filter(name__contains=name)
                    pnum = pquery.count()
                    if pnum == 0:
                        newP = Person.objects.create(name=name,  comment=post, doctor='zdl')
                        d =  name+ ' '+ str(id)+ ' '+str(newP.pk)+ ' '+root
                        created.append(d)
                    elif pnum == 1:
                        newP = pquery[0]
                    elif pnum > 1: #  查询出多个患者，只登记
                        d =  name+ ' '+ str(id)+ ' '+ root
                        repeated.append(d)
                        print("\n发现重复患者： %s" % post)
                        continue

                else:  # 无病历号, 则设置为0000
                    privDir = picDir + '/' + name + '_' + '0000' + '/'
                    print("\n解析为 " + name  )
                    pquery = Person.objects.filter(name__contains=name)
                    pnum = pquery.count()
                    if pnum == 0:
                        newP = Person.objects.create(name=name, comment=post, doctor='zdl')
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
                    os.mkdir(privDir)
                newP.privateDir = privDir.replace(base, '') # 图片相对地址 /static/picture/xxx/xxx
                newP.save()

                if nameList:
                    for t in nameList:
                        if not t == name: #  排除姓名
                            find_creat_Tag(t, newP)

                biglist = ['唇侧', '舌侧', '隐适美', 'Invislign']
                for t in biglist:
                    if t in root:
                        find_creat_Tag(t, newP)

                # 提取名字+id ----默认人名文件夹中的数字只可能是id
                rootList = patternA.findall(root)  # 所有汉子
                if rootList:
                    for t in rootList:
                        if not t == name: #  排除姓名
                            find_creat_Tag(t, newP)

                #  开始处理post及图片
                path3 = privDir.replace(base, '')
                newPost = Post.objects.create(name=post, person=newP, type=1, comment=post, dir=path3)
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
                        new_name = name+ '_'+ sep+ datestr + sep + 'S'+ str(1)+ sep +  times + '.' + ext
                        fpath = privDir+'/'+ new_name
                        old = root+'/'+file
                        shutil.move(old, fpath)
                        if os.path.exists(fpath):

                            path2 = fpath.replace(base, '')  # 图片相对地址 /static/picture/x/x/x/.jpg
                            newImg = Image.objects.create(name=file, post=newPost, person=newP, path=path2)
                            d = str(newPost.pk) + ' ' + path2
                            pics.append(d)
                            print("移动并创建image：%s   %s   患者：%s" % (file, new_name, post))

                shutil.rmtree(root)
                print("删除 %s" % (root))



            except:
                err.append(root)
                pass


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



# 取出所有Image后，检查image的path，及thumbnail，size_m，如果none，则制作缩略图



# error=[]
# imgAddIcon =[]
#

# def makeIconfor(imgs, d):
#     # imgs = Image.objects.all()
#     total = imgs.count()
#     i = 0
#     for img in imgs:
#         i=i+1
#         try:
#             # 图像名
#             img_path= base +  img.path
#             if os.path.exists(img_path):
#
#                 imgName= img_path.split('/')[-1]  # 赵云.p0.0186202.jpg
#                 if imgName[0] == '.':
#                     img.delete()
#                     continue
#                 # 图像的目录
#                 img_post  = img.post # TODO warnning 默认img已经有post信息，此处可能出错
#                 post_path = base + img_post.dir
#
#                 small_path = post_path+'/'+ 'small'+ '_'+ imgName
#                 medium_path = post_path+'/'+ 'medium'+ '_'+ imgName
#
#                 # 制作缩略图函数
#
#                 if not img.thumbnail:
#                     im = Image2.open(img_path)
#                     size = (400, 400)
#                     if im:
#                     # im = Image.open(infile)
#                         im.thumbnail(size)
#                         im.save(small_path, "JPEG")
#                         img.thumbnail = small_path.replace(base, '')
#                         img.save()
#                         imgAddIcon.append(img.pk)
#
#                 if not img.size_m:
#                     im = Image2.open(img_path)
#                     sizem = (1200, 1200)
#                     if im:
#                         im.thumbnail(sizem)
#                         im.save(medium_path, "JPEG")
#                         img.size_m = medium_path.replace(base, '')
#                         img.save()
#                         print('成功制作缩略图：' + img.path + '\n')
#
#         except:
#             error.append(img.pk)
#
#         try:
#             print('进度：' + str(i*100/total) + '%\n')
#         except:
#             pass
#
# lasti = Image.objects.all().last()
# biggestpk = lasti.pk
# # 0 - 1/4 2/4 3/4  1
# threads = []
# for ii in range(1, 5):
#     start = int( biggestpk * (ii-1)/4)
#     stop = int( biggestpk * ii/4 -1)
#     img2s = Image.objects.filter(pk__range=(start, stop))
#     t=threading.Thread(target=makeIconfor, args=(img2s, 1))
#     threads.append(t)
#
# for t in threads:
#     t.start()  # 开启新线程
#     t.join()  # 等待所有线程完成
#
#

# dt = datetime.now()
# time2 = dt.strftime("%m%d-%H%M%S")
#
# error=[]
# imgAddIcon =[]
# dels =[]
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
#             if imgName[0] == '.':
#                     dels.append(str(img.pk))
#                     print("删除 "+ str(img.pk))
#
#                     img.delete()
#                     continue
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
#
#
# print('\n缩略图完成，正在生成log文件。。。。')
#
#
# fname3 = 'log/log_iconMake' + time2 + '.txt'
# with open(fname3, 'w+') as f:
#
#     f.write('\n错误********************************************\n')
#     # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
#     f.write('总计：' + str(len(error)) + '\n')
#     for d in error:
#         f.write(d + '\n')
#
#     f.write('\n\n\n成功添加******************************************\n')
#     # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
#     f.write('总计：' + str(len(imgAddIcon)) + '\n')
#     for d in imgAddIcon:
#         f.write(str(d) + '\n')
#
#     f.write('\n\n\n删除******************************************\n')
#     # f.write('name' + ' ' + 'id' + ' ' + 'path' + '\n')
#     f.write('总计：' + str(len(dels)) + '\n')
#     for d in dels:
#         f.write(str(d) + '\n')
#
# print('\n完成。。。。')

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
