import datetime
import hashlib
from django.http import Http404, FileResponse
from django.shortcuts import render, redirect

from .models import *


# Create your views here.

def index(request):
    unit_groups = UnitGroup.objects.all()
    groups = []
    for group in unit_groups:
        groups.append({
            'group': group,
            'units': Unit.objects.filter(group=group)
        })
    if request.session.get('is_login', None) is not True:
        return redirect('MainApp:login')
    name = request.session.get('user_name')
    return render(request, 'index.html', locals())


def login(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        user_id = ''
    if request.session.get('is_login', None):
        return redirect('MainApp:index')
    if request.method == 'POST':
        login_id = request.POST.get('login_id')
        login_pwd = request.POST.get('login_pwd')
        if login_pwd and login_id:
            try:
                user = User.objects.get(student_id=login_id)
            except:
                message = '用户不存在！'
                return render(request, 'login.html', {'message': message, 'user_id': user_id})
            if user.password == hash_code(login_pwd):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('MainApp:index')
            else:
                message = '学号或密码不正确！'
                return render(request, 'login.html', {'message': message, 'user_id': user_id})
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
                               're_phone': re_phone, 're_supervisor': re_supervisor, 'message': message,
                               'user_id': user_id})
            else:
                same_student_id_user = User.objects.filter(student_id=re_id)
                if same_student_id_user:
                    message = '学号已经被注册了！'
                    return render(request, 'login.html',
                                  {'re_name': re_name, 're_confirm_pwd': re_confirm_pwd, 're_email': re_email,
                                   're_pwd': re_pwd, 're_phone': re_phone, 're_supervisor': re_supervisor,
                                   'message': message, 'user_id': user_id})
                same_email_user = User.objects.filter(email=re_email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login.html',
                                  {'re_name': re_name, 're_confirm_pwd': re_confirm_pwd, 're_id': re_id,
                                   're_pwd': re_pwd, 're_phone': re_phone, 're_supervisor': re_supervisor,
                                   'message': message, 'user_id': user_id})
                same_phone_user = User.objects.filter(phone=re_phone)
                if same_phone_user:
                    message = '该手机号已经被注册了！'
                    return render(request, 'login.html',
                                  {'re_name': re_name, 're_confirm_pwd': re_confirm_pwd, 're_id': re_id,
                                   're_pwd': re_pwd, 're_email': re_email, 're_supervisor': re_supervisor,
                                   'message': message, 'user_id': user_id})
                new_user = User()
                new_user.name = re_name
                new_user.email = re_email
                new_user.phone = re_phone
                new_user.student_id = re_id
                new_user.supervisor = re_supervisor
                new_user.password = hash_code(re_pwd)
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
        User.objects.filter(student_id=student_id).update(password=hash_code(password))
        return redirect('MainApp:index')
    return render(request, 'forget.html')


def comments(request):
    if request.session.get('is_login', None) is not True:
        return redirect('MainApp:login')
    unit_groups = UnitGroup.objects.all()
    groups = []
    for group in unit_groups:
        groups.append({
            'group': group,
            'units': Unit.objects.filter(group=group)
        })
    user_name = request.session.get('user_name')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    comment_list = Comment.objects.order_by('-date')
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if not comment_text:
            message = '评论内容不能为空！'
        else:
            new_comment = Comment()
            new_comment.user_id = request.session.get('user_id')
            new_comment.text = comment_text
            new_comment.save()
            return redirect('MainApp:comments')
    return render(request, 'comments.html', locals())


def download(request, file_id):
    if request.session.get('is_login', None) is not True:
        return redirect('MainApp:login')
    file = File.objects.get(id=file_id)
    download_file = open(str(file.path), 'rb')
    file_name = str(file.path).split('/')[-1]
    file_type = str(file.path).split('.')[-1]
    try:
        if file_type == 'doc':
            response = FileResponse(download_file)
            response['Content-Type'] = 'application/msword'
            response['Content-Disposition'] = 'attachment;filename="{}"'.format(
                file_name.encode('utf-8').decode('ISO-8859-1'))
            return response
        if file_type == 'docx':
            response = FileResponse(download_file)
            response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            response['Content-Disposition'] = 'attachment;filename="{}"'.format(
                file_name.encode('utf-8').decode('ISO-8859-1'))
            return response
        if file_type == 'pdf':
            response = FileResponse(download_file)
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment;filename="{}"'.format(
                file_name.encode('utf-8').decode('ISO-8859-1'))
            return response
    except:
        return Http404


def setting(request):
    if request.session.get('is_login', None) is not True:
        return redirect('MainApp:login')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    unit_groups = UnitGroup.objects.all()
    groups = []
    for group in unit_groups:
        groups.append({
            'group': group,
            'units': Unit.objects.filter(group=group)
        })
    if request.method == 'POST':
        new_phone = request.POST.get('phone')
        new_email = request.POST.get('email')
        new_supervisor = request.POST.get('supervisor')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        new_password_check = request.POST.get('new_password_check')
        if new_phone and new_phone != user.phone:
            same_phone_user = User.objects.filter(phone=new_phone)
            if same_phone_user:
                message = '该电话已被注册！'
                return render(request, 'setting.html', {'user': user, 'message': message, 'groups': groups})
            User.objects.filter(id=user_id).update(phone=new_phone)
            user.phone = new_phone
        if new_email and new_email != user.email:
            same_email_user = User.objects.filter(email=new_email)
            if same_email_user:
                message = '该邮箱已被注册！'
                return render(request, 'setting.html', {'user': user, 'message': message, 'groups': groups})
            User.objects.filter(id=user_id).update(email=new_email)
            user.email = new_email
        if new_supervisor and new_supervisor != user.supervisor:
            User.objects.filter(id=user_id).update(supervisor=new_supervisor)
            user.supervisor = new_supervisor
        if password:
            if hash_code(password) != user.password:
                pwd_message = '原密码输入错误！'
                return render(request, 'setting.html', {'user': user, 'pwd_message': pwd_message, 'groups': groups})
            if new_password != new_password_check:
                pwd_message = '两次输入密码不同！'
                return render(request, 'setting.html', {'user': user, 'pwd_message': pwd_message, 'groups': groups})
            User.objects.filter(id=user_id).update(password=hash_code(new_password))
        return render(request, 'setting.html', {'user': user, 'groups': groups})
    return render(request, 'setting.html', {'user': user, 'groups': groups})


def hash_code(s, salt='login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def ln_index(request):
    if request.session.get('is_login', None) is not True:
        return redirect('MainApp:login')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    sum_cell = 2916
    query_result = TankCell.objects.filter(state='占用')
    time_now = datetime.date.today()
    red = yellow = blue = 0
    for cell in query_result:
        cell_time = cell.date.date()
        span_days = (cell_time - time_now).days
        if span_days >= 365:
            red += 1
        elif 183 <= span_days < 365:
            yellow += 1
        else:
            blue += 1
    green = sum_cell - red - yellow - blue
    return render(request, 'ln_index.html', locals())


def ln_query(request):
    if request.session.get('is_login', None) is not True:
        return redirect('MainApp:login')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        basket = request.POST.get('basket')
        floor = request.POST.get('floor')
        row = request.POST.get('row')
        column = request.POST.get('column')
        query_result = TankCell.objects.filter(basket=basket, floor=floor, row=row, column=column).first()
        if query_result:
            cell_time = query_result.date.date()
            time_now = datetime.date.today()
            span_days = (cell_time - time_now).days
            if span_days >= 365:
                color = 'red'
            elif 183 <= span_days < 365:
                color = 'yellow'
            else:
                color = 'blue'
            if query_result.state == '空闲':
                color = 'green'
            return render(request, 'ln_query.html', {'cell': query_result, 'user': user, 'color': color})
        else:
            query_result = TankCell(name='无', state='空闲', date=None)
            return render(request, 'ln_query.html', {'cell': query_result, 'user': user, 'color': 'green'})
    return render(request, 'ln_query.html', {'user': user})


def ln_my(request):
    if request.session.get('is_login', None) is not True:
        return redirect('MainApp:login')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    cells = TankCell.objects.filter(user=user)
    time_now = datetime.date.today()
    cell_span_days = []
    A = ['A', 'B', 'C', 'D']
    a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    for cell in cells:
        cell.basket = A[int(cell.basket) - 1]
        cell.column = a[int(cell.column) - 1]
        cell_span_days.append({
            'cell': cell,
            'span_days': (cell.date.date() - time_now).days
        })

    return render(request, 'ln_my.html', locals())


def ln_modify(request):
    if request.session.get('is_login', None) is not True:
        return redirect('MainApp:login')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        action = request.POST.get('action')
        special = request.POST.get('special')
        basket = request.POST.get('basket')
        floor = request.POST.get('floor')
        row = request.POST.get('row')
        column = request.POST.get('column')
        query_result = TankCell.objects.filter(basket=basket, floor=floor, row=row, column=column).first()
        if action == 'take':
            action = '空闲'
        else:
            action = '占用'
        if query_result is None:
            new_Cell = TankCell(basket=basket, floor=floor, row=row, column=column, user=user, state=action,
                                name=name,
                                special_attr=special)
            new_Cell.save()
            TankCellHistory(tankCell=new_Cell).save()
        else:
            query_result.state = action
            query_result.name = name
            query_result.special_attr = special
            query_result.save()
            TankCellHistory(tankCell=query_result).save()

        return render(request, 'ln_modify.html', {'user': user})
    return render(request, 'ln_modify.html', {'user': user})


def unit(request, unit_id: int):
    if request.session.get('is_login', None) is not True:
        return redirect('MainApp:login')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    query_unit = Unit.objects.get(id=unit_id)
    unit_groups = UnitGroup.objects.all()
    groups = []
    for group in unit_groups:
        groups.append({
            'group': group,
            'units': Unit.objects.filter(group=group)
        })
    return render(request, 'unit.html', {'user': user, 'unit': query_unit, 'groups': groups})


def comment(request, comment_id: int):
    if request.session.get('is_login', None) is not True:
        return redirect('MainApp:login')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    query_comment = Comment.objects.get(id=comment_id)
    return render(request, 'comment.html', {'user': user})
