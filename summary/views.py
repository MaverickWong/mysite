from django.shortcuts import render, redirect
from django.http import HttpResponse

from boards.models import Person, Post, Image, Tag
from record.models import Record
from mysite.views import get_client_ip

# Create your views here.


def home(request):
	get_client_ip(request)  # 记录ip地址

	docname = request.user.username
	if request.user.is_authenticated:
		if docname == 'zdl':  # 用户名为zdl时，可以查看所有患者[:16]
			persons = Person.objects.order_by('pk').reverse()
			total_person_num = Person.objects.all().count()

		else:  # 只能看该医生的患者
			persons = Person.objects.filter(doctor=docname).order_by('pk')
			total_person_num = Person.objects.filter(doctor=docname).count()

		# tags = Tag.objects.all()

		# # 分页
		# page = request.GET.get('page', 1)
		# paginator = Paginator(persons, 6)
		# try:
		# 	topics = paginator.page(page)
		# except PageNotAnInteger:
		# 	# fallback to the first page
		# 	topics = paginator.page(1)
		# except EmptyPage:
		# 	# probably the user tried to add a page number
		# 	# in the url, so we fallback to the last page
		# 	topics = paginator.page(paginator.num_pages)
		#
		# tgroups = []
		# for i in range(10):
		# 	tgroup = Tag.objects.filter(type=i)
		# 	tgroups.append(tgroup)
		# # tgroups.append(Tag.objects.filter(type=101)) # 添加101其他
		# tags = Tag.objects.filter(type=101)

		persons = Person.objects.all().order_by('last_updated').reverse()[:20]

		total_posts_num = Post.objects.all().count()
		total_img_num = Image.objects.all().count()
		tag_count = Tag.objects.all().count()
		total_record_num = Record.objects.all().count()
		total_person_newly_updated = persons.count()

		contx = {'persons': persons,
		         'total_person_num': total_person_num, 'total_posts_num': total_posts_num,
		         'total_img_num': total_img_num, 'total_record_num': total_record_num,
		         'total_person_newly_updated': total_person_newly_updated
		         }

		return render(request, 'summary/index.html', contx)
	else:
		return redirect('login')
