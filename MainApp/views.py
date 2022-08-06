from django.shortcuts import render, get_object_or_404, redirect
from .models import *


# Create your views here.

def index(request):
    if request.session.get('is_login', None) is not True:
        return redirect('MainApp:login')
    name = request.session.get('user_name')
    return render(request, 'index.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect('MainApp:index')
    if request.method == 'POST':
        login_id = request.POST.get('login_id')
        login_pwd = request.POST.get('login_pwd')
        print(login_id)
        if login_pwd and login_id:
            print('yes')
            try:
                user = User.objects.get(student_id=login_id)
            except:
                message = '用户不存在！'
                return render(request, 'login.html', {'message': message})
            if user.password == login_pwd:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('MainApp:index')
            else:
                message = '学号或密码不正确！'
                return render(request, 'login.html', {'message': message})
        else:
            re_id = request.POST.get('re_id')
            re_name = request.POST.get('re_name')
            re_email = request.POST.get('re_email')
            re_phone = request.POST.get('re_phone')
            re_supervisor = request.POST.get('re_supervisor')
            re_pwd = request.POST.get('re_pwd')
            re_confirm_pwd = request.POST.get('re_confirm_pwd')
            if re_pwd != re_confirm_pwd:
                message = '两次输入的密码不同！'
                return render(request, 'login.html',
                              {'re_name': re_name, 're_id': re_id, 're_email': re_email, 're_pwd': re_pwd,
                               're_phone': re_phone, 're_supervisor': re_supervisor, 'message': message})
            else:
                same_student_id_user = User.objects.filter(student_id=re_id)
                if same_student_id_user:
                    message = '学号已经被注册了！'
                    return render(request, 'login.html',
                                  {'re_name': re_name, 're_confirm_pwd': re_confirm_pwd, 're_email': re_email,
                                   're_pwd': re_pwd, 're_phone': re_phone, 're_supervisor': re_supervisor,
                                   'message': message})
                same_email_user = User.objects.filter(email=re_email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login.html',
                                  {'re_name': re_name, 're_confirm_pwd': re_confirm_pwd, 're_id': re_id,
                                   're_pwd': re_pwd, 're_phone': re_phone, 're_supervisor': re_supervisor,
                                   'message': message})
                same_phone_user = User.objects.filter(phone=re_phone)
                if same_phone_user:
                    message = '该手机号已经被注册了！'
                    return render(request, 'login.html',
                                  {'re_name': re_name, 're_confirm_pwd': re_confirm_pwd, 're_id': re_id,
                                   're_pwd': re_pwd, 're_email': re_email, 're_supervisor': re_supervisor,
                                   'message': message})
                new_user = User()
                new_user.name = re_name
                new_user.email = re_email
                new_user.phone = re_phone
                new_user.student_id = re_id
                new_user.supervisor = re_supervisor
                new_user.password = re_pwd
                new_user.save()
                return redirect('MainApp:index')
    return render(request, 'login.html')


def logout(request):
    request.session.clear()
    return render(request, 'login.html')


def forget(request):
    return render(request, 'index.html', locals())


def cycle_protocol(request):
    return render(request, 'cycle_protocol.html', locals())


def centrifuge(request):
    return render(request, 'centrifuge.html', locals())


def comments(request):
    return render(request, 'comments.html', locals())


def commitment(request):
    return render(request, 'commitment.html', locals())


def cultured_basic(request):
    return render(request, 'cultured_basic.html', locals())


def cylinder(request):
    return render(request, 'cylinder.html', locals())


def incubator(request):
    return render(request, 'incubator.html', locals())


def note(request):
    return render(request, 'note.html', locals())


def safe(request):
    return render(request, 'safe.html', locals())


def sterilizer(request):
    return render(request, 'sterilizer.html', locals())


def tank(request):
    return render(request, 'tank.html', locals())


def manage_rule(request):
    return render(request, 'manage_rule.html', locals())


def star_cell_cultured(request):
    return render(request, 'star_cell_cultured.html', locals())
