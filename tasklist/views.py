from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django import forms
from tasklist.models import *
from django.contrib.auth.decorators import permission_required

# Create your views here.


# @permission_required('tasklist.view_task')
def home(request):
    tasks = Task.objects.order_by('-pk')
    group_dict = dict(Task.group_choice)
    # return  HttpResponse('good')
    msg = '欢迎，测试版'
    ctx ={'tasks': tasks, 'group_dict': group_dict, 'msg': msg}
    return render(request, 'task/index.html', ctx)


class AddForm(forms.Form):

    name = forms.CharField(label='项目名称', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    comment = forms.CharField(label='备注', required=False, max_length=200)
    group = forms.ChoiceField(label='分组', required=False, choices=Task.group_choice)
    status = forms.ChoiceField(label='状态', required=False, choices=Task.status_choice)

    # person = forms.ForeignKey(Person, related_name='tasks', null=True, blank=True, on_delete=models.SET_NULL)
    # doc = forms.CharField(max_length=20, null=True, blank=True)

    # startTime = forms.DateTimeFieldField(label='开始时间',  widget=forms.TextInput(attrs={'class': 'form-control'}))
    endTime = forms.DateField(label='结束时间',  required=False, widget=forms.TextInput(attrs={'id':'datetimepicker1', 'class': 'form-control'}))
    # timeLength = forms.CharField(max_length=10, null=True, blank=True)  'id':'datetimepicker1',


def add(request):
    if request.method == 'POST':
        register_form = AddForm(request.POST)

        # register_form = forms.RegisterForm(request.POST)
        message = '请检查填写内容'
        if register_form.is_valid():
            comment = register_form.cleaned_data['comment']
            name = register_form.cleaned_data['name']
            group = register_form.cleaned_data['group']
            # startTime = register_form.cleaned_data['startTime']
            status = register_form.cleaned_data['status']
            endTime = register_form.cleaned_data['endTime']

            task = Task.objects.create(name=name)
            task.comment = comment
            task.group = group
            # task.startTime=startTime
            task.status = status
            task.endTime = endTime
            task.save()

            # 标签
            tag_list = request.POST['newTags']
            new_tag_list = tag_list.split(' ')
            if new_tag_list:
                for t in new_tag_list:
                    tags = Task_tags.objects.filter(name=t)
                    if tags.count() == 1:  # 查到一个
                        tags[0].tasks.add(task)
                        tags[0].save()
                    elif tags.count() == 0:  # 未查到
                        tag2 = Task_tags.objects.create(name=t)
                        tag2.tasks.add(task)
                        tag2.save()

            message = '添加成功'

            return redirect('/task/', {'msg': message})
    else:
        form = AddForm()
        tags = Task_tags.objects.all()

        return render(request, 'task/add_task.html', locals())


class EditForm(forms.Form):

    name = forms.CharField(label='项目名称', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    comment = forms.CharField(label='备注', required=False, max_length=200)
    group = forms.ChoiceField(label='分组', required=False, choices=Task.group_choice)
    status = forms.ChoiceField(label='状态', required=False, choices=Task.status_choice)

    # person = forms.ForeignKey(Person, related_name='tasks', null=True, blank=True, on_delete=models.SET_NULL)
    # doc = forms.CharField(max_length=20, null=True, blank=True)

    # startTime = forms.DateField(label='开始时间',  widget=forms.TextInput(attrs={'class': 'form-control'}))
    endTime = forms.DateField(label='结束时间',  required=False, widget=forms.TextInput(attrs={'id':'datetimepicker2', 'class': 'form-control'}))
    # timeLength = forms.CharField(max_length=10, null=True, blank=True)


def edit(request, pk):
    edit_form = EditForm(request.POST)
    if request.method == 'POST':
        # register_form = AddForm(request.POST)

        message = '请检查填写内容'
        if edit_form.is_valid():
            comment = edit_form.cleaned_data['comment']
            name = edit_form.cleaned_data['name']
            group = edit_form.cleaned_data['group']
            # startTime = register_form.cleaned_data['startTime']
            status = edit_form.cleaned_data['status']
            endTime = edit_form.cleaned_data['endTime']

            task = Task.objects.get(pk=pk)
            task.name = name
            task.comment = comment
            task.group = group
            # task.startTime=startTime
            task.status = status
            task.endTime = endTime
            task.save()
            message = '添加成功'

            return redirect('/task/', {'msg': message})
    else:  # get
        task = Task.objects.get(pk=pk)
        form = EditForm(
            initial={
                'name': task.name,
                'comment': task.comment,
                'group': task.group,
                'status': task.status,
                'endTime': task.endTime
            }
        )

        return render(request, 'task/edit.html', locals())


def del_task(request,pk):
    t = Task.objects.get(pk=pk)
    t.delete()
    message = '删除成功'

    return redirect('/task/', {'msg': message})


def search_task(request):
    s= request.GET['s']
    if s:
        s = s.replace(' ', '')
        tasks = Task.objects.filter(name__contains=s)
        msg = '搜索到 %d 条' % (tasks.count())
        return render(request, 'task/index.html', {'tasks': tasks, 'msg':msg})
    else:
        tasks = Task.objects.all()
        msg = '请检查输入'
        return render(request, 'task/index.html', {'tasks': tasks, 'msg': msg})


class EditForm2(forms.Form):
    group = forms.ChoiceField(label='分组', required=False, choices=Task.group_choice)


def search_group(request):
    grp = request.GET['s']
    tasks = Task.objects.filter(group=grp   )
    msg = 'hh'
    return render(request, 'task/index.html', {'tasks': tasks, 'msg': msg})
