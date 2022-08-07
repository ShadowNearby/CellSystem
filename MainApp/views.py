from django.shortcuts import render, get_object_or_404, redirect
from .models import *
import os
from django.http import HttpResponse, Http404, StreamingHttpResponse, FileResponse


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
    request.session.flush()
    return redirect('MainApp:index')


def forget(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password_check = request.POST.get('password_check')
        user = User.objects.get(student_id=student_id)
        if not user:
            message = '用户不存在！'
            return render(request, 'forget.html', {'message': message})
        user_phone = user.phone
        if user_phone != phone:
            message = '手机号码不正确！'
            return render(request, 'forget.html', {'message': message, 'student_id': student_id})
        if password != password_check:
            message = '两次输入密码不同！'
            return render(request, 'forget.html',
                          {'message': message, 'student_id': student_id, 'password': password, 'phone': phone})
        User.objects.filter(student_id=student_id).update(password=password)
        return redirect('MainApp:index')
    return render(request, 'forget.html')


def cycle_protocol(request):
    name = request.session.get('user_name')
    return render(request, 'cycle_protocol.html', locals())


def centrifuge(request):
    name = request.session.get('user_name')
    return render(request, 'centrifuge.html', locals())


def comments(request):
    user_name = request.session.get('user_name')
    comment_list = Comment.objects.all().reverse()
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        print('yes')
        if not comment_text:
            message = '评论内容不能为空！'
        else:
            new_comment = Comment()
            new_comment.user_id = request.session.get('user_id')
            new_comment.text = comment_text
            new_comment.save()
    return render(request, 'comments.html', locals())


def commitment(request):
    name = request.session.get('user_name')
    return render(request, 'commitment.html', locals())


def cultured_basic(request):
    name = request.session.get('user_name')
    return render(request, 'cultured_basic.html', locals())


def cylinder(request):
    name = request.session.get('user_name')
    return render(request, 'cylinder.html', locals())


def incubator(request):
    name = request.session.get('user_name')
    return render(request, 'incubator.html', locals())


def note(request):
    name = request.session.get('user_name')
    return render(request, 'note.html', locals())


def safe(request):
    name = request.session.get('user_name')
    return render(request, 'safe.html', locals())


def sterilizer(request):
    name = request.session.get('user_name')
    return render(request, 'sterilizer.html', locals())


def tank(request):
    name = request.session.get('user_name')
    return render(request, 'tank.html', locals())


def manage_rule(request):
    name = request.session.get('user_name')
    return render(request, 'manage_rule.html', locals())


def star_cell_cultured(request):
    name = request.session.get('user_name')
    return render(request, 'star_cell_cultured.html', locals())


def download(request, file_id):
    file = File.objects.get(id=file_id)
    download_file = open(str(file.path), 'rb')
    file_name = str(file.path).split('/')[1]
    print(file_name)

    def file_iterator(file_path, chunk_size=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
        """
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    try:
        response = FileResponse(file_iterator(download_file))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format("1.docx")
    except:
        return Http404
    return response


def setting(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        new_phone = request.POST.get('phone')
        new_email = request.POST.get('email')
        new_supervisor = request.POST.get('supervisor')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        new_password_check = request.POST.get('new_password_check')
        if new_phone != user.phone:
            same_phone_user = User.objects.filter(phone=new_phone)
            if same_phone_user:
                message = '该电话已被注册！'
                return render(request, 'setting.html', {'user': user, 'message': message})
            User.objects.filter(id=user_id).update(phone=new_phone)
            user.phone = new_phone
        if new_email != user.email:
            same_email_user = User.objects.filter(email=new_email)
            if same_email_user:
                message = '该邮箱已被注册！'
                return render(request, 'setting.html', {'user': user, 'message': message})
            User.objects.filter(id=user_id).update(email=new_email)
            user.email = new_email
        if new_supervisor != user.supervisor:
            User.objects.filter(id=user_id).update(supervisor=new_supervisor)
            user.supervisor = new_supervisor
        if password:
            if password != user.password:
                pwd_message = '原密码输入错误！'
                return render(request, 'setting.html', {'user': user, 'pwd_message': pwd_message})
            if new_password != new_password_check:
                pwd_message = '两次输入密码不同！'
                return render(request, 'setting.html', {'user': user, 'pwd_message': pwd_message})
            User.objects.filter(id=user_id).update(password=new_password)
            user.password = new_password
        return render(request, 'setting.html', {'user': user})
    return render(request, 'setting.html', {'user': user})
