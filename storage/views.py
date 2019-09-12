from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, reverse
from django.shortcuts import HttpResponse
from django import forms
from .models import *
from django.contrib.auth.decorators import permission_required


# Create your views here.


# @permission_required('tasklist.view_task')
def home(request):
	tasks = DrugItem.objects.order_by('-pk')
	group_dict = dict(DrugItem.big_group_choice)
	# return  HttpResponse('good')
	msg = '欢迎，测试版'
	ctx = {'tasks': tasks, 'group_dict': group_dict, 'msg': msg}
	return render(request, 'storage/index.html', ctx)


class AddForm(forms.Form):
	name = forms.CharField(label='物品名称', required=True, max_length=100,
	                       widget=forms.TextInput(attrs={'class': 'form-control'}))
	shortname = forms.CharField(label='名称首字母', required=True, max_length=10, widget=forms.TextInput(attrs={}))
	count = forms.IntegerField(label='数量', required=True)
	min_count = forms.IntegerField(label='报警数量', required=True, help_text='库存低于报警数量时，自动红色标记')
	comment = forms.CharField(label='备注', required=False, max_length=200)
	group = forms.ChoiceField(label='分组', required=False, choices=DrugItem.big_group_choice)
	status = forms.ChoiceField(label='状态', required=False, choices=DrugItem.status_choice)

	# person = forms.ForeignKey(Person, related_name='tasks', null=True, blank=True, on_delete=models.SET_NULL)
	# doc = forms.CharField(max_length=20, null=True, blank=True)
	# startTime = forms.DateTimeFieldField(label='开始时间',  widget=forms.TextInput(attrs={'class': 'form-control'}))
	endTime = forms.DateField(label='结束时间', required=False,
	                          widget=forms.TextInput(attrs={'id': 'datetimepicker1', 'class': 'form-control'}))
	# timeLength = forms.CharField(max_length=10, null=True, blank=True)  'id':'datetimepicker1',


def add(request):
	if request.method == 'POST':
		register_form = AddForm(request.POST)

		# register_form = forms.RegisterForm(request.POST)
		message = '请检查填写内容'
		if register_form.is_valid():
			name = register_form.cleaned_data['name']
			shortname = register_form.cleaned_data['shortname']
			count = register_form.cleaned_data['count']
			min_count = register_form.cleaned_data['min_count']
			comment = register_form.cleaned_data['comment']

			group = register_form.cleaned_data['group']
			# startTime = register_form.cleaned_data['startTime']
			status = register_form.cleaned_data['status']
			endTime = register_form.cleaned_data['endTime']

			task = DrugItem.objects.create(name=name)
			task.shortname = shortname
			task.count = count
			task.min_count = min_count
			task.comment = comment
			task.group = group
			# task.startTime=startTime
			task.status = status
			task.endTime = endTime
			task.save()

			# 创建时即增加初始记录
			if count > 0:
				detail = InOutDetail.objects.create(prop='+', count=count, comment=comment, drugitem=task)
				detail.save()

			# 标签
			# tag_list = request.POST['newTags']
			# new_tag_list = tag_list.split(' ')
			# if new_tag_list:
			#     for t in new_tag_list:
			#         tags = Task_tags.objects.filter(name=t)
			#         if tags.count() == 1:  # 查到一个
			#             tags[0].tasks.add(task)
			#             tags[0].save()
			#         elif tags.count() == 0:  # 未查到
			#             tag2 = Task_tags.objects.create(name=t)
			#             tag2.tasks.add(task)
			#             tag2.save()

			message = '添加成功'

			return redirect(reverse('storage:home'), {'msg': message})
	else:
		form = AddForm()
		# tags = Task_tags.objects.all()

		return render(request, 'storage/add_task.html', locals())


class EditForm(forms.Form):
	name = forms.CharField(label='物品名称', required=True, max_length=100,
	                       widget=forms.TextInput(attrs={'class': 'form-control'}))
	shortname = forms.CharField(label='名称首字母', required=True, max_length=10, widget=forms.TextInput(attrs={}))
	count = forms.IntegerField(label='数量', required=True)
	group = forms.ChoiceField(label='分组', required=False, choices=DrugItem.big_group_choice)
	status = forms.ChoiceField(label='状态', required=False, choices=DrugItem.status_choice)
	comment = forms.CharField(label='备注', required=False, max_length=200)

	# person = forms.ForeignKey(Person, related_name='tasks', null=True, blank=True, on_delete=models.SET_NULL)
	# doc = forms.CharField(max_length=20, null=True, blank=True)
	# startTime = forms.DateField(label='开始时间',  widget=forms.TextInput(attrs={'class': 'form-control'}))
	endTime = forms.DateField(label='结束时间', required=False,
	                          widget=forms.TextInput(attrs={'id': 'datetimepicker2', 'class': 'form-control'}))
	# timeLength = forms.CharField(max_length=10, null=True, blank=True)


def edit(request, pk):
	edit_form = EditForm(request.POST)
	if request.method == 'POST':
		# register_form = AddForm(request.POST)
		message = '请检查填写内容'
		if edit_form.is_valid():
			comment = edit_form.cleaned_data['comment']
			name = edit_form.cleaned_data['name']
			shortname = edit_form.cleaned_data['shortname']
			count = edit_form.cleaned_data['count']
			# startTime = register_form.cleaned_data['startTime']
			status = edit_form.cleaned_data['status']
			# endTime = edit_form.cleaned_data['endTime']

			task = DrugItem.objects.get(pk=pk)
			task.name = name
			task.shortname = shortname
			task.comment = comment
			task.count = count
			# task.startTime=startTime
			task.status = status
			# task.endTime = endTime
			task.save()
			message = '添加成功'

			return redirect(reverse('storage:home'), {'msg': message})

	else:  # get
		task = DrugItem.objects.get(pk=pk)
		form = EditForm(
			initial={
				'name': task.name,
				'comment': task.comment,
				'count': task.count,
				'status': task.status,
				# 'endTime': task.endTime
			}
		)

		return render(request, 'storage/edit.html', locals())


class InoutForm(forms.Form):
	prop = forms.ChoiceField(label='出入库操作', required=True, choices=InOutDetail.PROP)
	# name = forms.CharField(label='物品名称', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	count = forms.IntegerField(label='数量', required=True)
	# group = forms.ChoiceField(label='分组', required=False, choices=DrugItem.big_group_choice)
	# status = forms.ChoiceField(label='状态', required=False, choices=DrugItem.status_choice)
	comment = forms.CharField(label='备注', required=False, max_length=64)
	user = forms.CharField(label='操作人', required=False, max_length=12)

	# person = forms.ForeignKey(Person, related_name='tasks', null=True, blank=True, on_delete=models.SET_NULL)
	# doc = forms.CharField(max_length=20, null=True, blank=True)
	# startTime = forms.DateField(label='开始时间',  widget=forms.TextInput(attrs={'class': 'form-control'}))
	endTime = forms.DateField(label='购入时间', required=False,
	                          widget=forms.TextInput(attrs={'id': 'datetimepicker2', 'class': 'form-control'}))
	# timeLength = forms.CharField(max_length=10, null=True, blank=True)


def inout(request, drugpk):
	edit_form = InoutForm(request.POST)
	if request.method == 'POST':
		# register_form = AddForm(request.POST)

		message = '请检查填写内容'
		if edit_form.is_valid():
			comment = edit_form.cleaned_data['comment']
			user = edit_form.cleaned_data['user']
			count = edit_form.cleaned_data['count']
			# startTime = register_form.cleaned_data['startTime']
			prop = edit_form.cleaned_data['prop']
			# endTime = edit_form.cleaned_data['endTime']

			drugitem = DrugItem.objects.get(pk=drugpk)
			task = InOutDetail.objects.create(user=user, count=count, drugitem=drugitem, comment=comment, prop=prop)
			# task.user = user
			# task.comment = comment
			if prop == '+':
				drugitem.count += count
				drugitem.save()
			else:
				drugitem.count -= count
				drugitem.save()
			# task.startTime=startTime
			# task.prop = prop
			# task.drugitem = drugitem
			# task.endTime = endTime
			# task.save()
			message = '添加成功'

			return redirect(reverse('storage:home'), {'msg': message})

	else:  # get
		drugitem = DrugItem.objects.get(pk=drugpk)
		form = InoutForm(
			initial={
				# 'name': task.name,
				# 'comment': task.comment,
				# 'count': task.count,
				# 'status': task.status,
				# 'endTime': task.endTime
			}
		)

		return render(request, 'storage/in_out.html', locals())


def inout_detail(request, drugpk):
	drugitem = DrugItem.objects.get(pk=drugpk)
	details = drugitem.inout_details.all()
	ctx = {'details': details, 'drug': drugitem}
	return render(request, 'storage/inout_details.html', ctx)


def del_task(request, pk):
	t = DrugItem.objects.get(pk=pk)
	t.delete()
	message = '删除成功'

	return redirect(reverse('storage:home'), {'msg': message})


def search_task(request):
	s = request.GET['s']
	if s:
		s = s.replace(' ', '')
		tasks = DrugItem.objects.filter(name__contains=s)
		msg = '搜索到 %d 条' % (tasks.count())
		return render(request, 'storage/index.html', {'tasks': tasks, 'msg': msg})
	else:
		tasks = DrugItem.objects.all()
		msg = '请检查输入'
		return render(request, 'storage/index.html', {'tasks': tasks, 'msg': msg})


class EditForm2(forms.Form):
	group = forms.ChoiceField(label='分组', required=False, choices=DrugItem.big_group_choice)


def search_group(request):
	grp = request.GET['s']
	tasks = DrugItem.objects.filter(group=grp)
	msg = 'hh'
	return render(request, 'storage/index.html', {'tasks': tasks, 'msg': msg})
