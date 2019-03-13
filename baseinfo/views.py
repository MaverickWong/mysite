from django.shortcuts import render, redirect
from boards.models import Person
from django import forms
# Create your views here.


def home(request, pk):
	"""
	患者的基本信息
	:param request:
	:param pk:
	:return:
	"""
	p = Person.objects.get(pk=pk)
	return render(request, 'baseinfo/baseInfo.html', {'person': p})


class EditForm(forms.Form):
	status_choice = (
		(0, '无'),
		(1, '要做'),
		(2, '已发送'),
		(3, '已收到'),
		(4, '已戴走'),
	)


	name = forms.CharField(label='名称', required=True, max_length=100,
	                       widget=forms.TextInput(attrs={'class': 'form-control'}))
	idnum = forms.CharField(label='病历号', required=True, max_length=30)
	linkedcareId = forms.IntegerField(label='易看牙后台序号', required=False)
	comment = forms.CharField(label='备注', required=False, max_length=200)


def edit(request, pk):

	if request.method == 'POST':
		edit_form = EditForm(request.POST)

		message = '请检查填写内容'
		if edit_form.is_valid():
			comment = edit_form.cleaned_data['comment']
			name = edit_form.cleaned_data['name']
			linkedcareId = edit_form.cleaned_data['linkedcareId']

			# startTime = register_form.cleaned_data['startTime']
			idnum = edit_form.cleaned_data['idnum']

			p = Person.objects.get(pk=pk)
			p.name = name
			p.comment = comment
			p.idnum = idnum
			p.linkedcareId = linkedcareId
			# task.startTime=startTime

			p.save()
			message = '添加成功'

			return redirect('/detail/'+str(pk), {'msg': message})
	else:  # get
		p = Person.objects.get(pk=pk)
		form = EditForm(
			initial={
				'name': p.name,
				'comment': p.comment,
				'idnum': p.idnum,
				'linkedcareId': p.linkedcareId,
				# 'status': task.status,
				# 'endTime': task.endTime
			}
		)

		return render(request, 'baseinfo/edit.html', locals())

