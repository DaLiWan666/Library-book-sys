# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import UserRegistrationForm, BookForm, BorrowFormAdmin, ReturnForm
from .models import Book, BorrowReturn
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .decorators import group_required

def get_user_role_flags(user):
    """
    辅助函数：返回用户是否为管理员和学生的布尔标识符。
    """
    is_admin = user.groups.filter(name='Administrator').exists()
    is_student = user.groups.filter(name='Student').exists()
    return is_admin, is_student

# 用户注册视图
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            student_group, created = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# 用户登录视图
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "用户名或密码不正确。"
    return render(request, 'login.html', {'error': error})

# 用户登出视图
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# 主页视图
@login_required
def home_view(request):
    top_books = BorrowReturn.objects.values('book__title').annotate(borrow_count=Count('book')).order_by('-borrow_count')[:100]
    is_admin, is_student = get_user_role_flags(request.user)

    context = {
        'is_admin': is_admin,
        'is_student': is_student,
        'top_books': top_books,
    }
    
    return render(request, 'home.html', context)

# 学生查看书籍视图
@login_required
def view_books_view(request):
    books = Book.objects.all()

    # 搜索功能
    query = request.GET.get('search', '')
    if query:
        books = books.filter(title__icontains=query)  # 根据书名搜索

    is_admin, is_student = get_user_role_flags(request.user)
    return render(request, 'view_books.html', {'books': books, 'is_admin': is_admin, 'is_student': is_student, 'query': query})


# 用户管理视图（仅限管理员）
@login_required
@group_required('Administrator')
def user_management_view(request):
    is_admin, is_student = get_user_role_flags(request.user)
    users = User.objects.all()
    return render(request, 'user_management.html', {'users': users, 'is_admin': is_admin, 'is_student': is_student})

# 删除用户视图（仅限管理员）
@login_required
@group_required('Administrator')
def delete_user_view(request, user_id):
    is_admin, is_student = get_user_role_flags(request.user)
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_management')
    return render(request, 'delete_user.html', {'user': user, 'is_admin': is_admin, 'is_student': is_student})

# 设置用户角色视图（仅限管理员）
@login_required
@group_required('Administrator')
def set_user_role_view(request, user_id):
    is_admin, is_student = get_user_role_flags(request.user)
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        role = request.POST.get('role')
        user.groups.clear()
        if role == 'Administrator':
            admin_group, created = Group.objects.get_or_create(name='Administrator')
            user.groups.add(admin_group)
        else:
            student_group, created = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)
        return redirect('user_management')
    return render(request, 'set_user_role.html', {'user': user, 'is_admin': is_admin, 'is_student': is_student})

# 图书管理视图（仅限管理员）
@login_required
@group_required('Administrator')
def book_management_view(request):
    is_admin, is_student = get_user_role_flags(request.user)
    books = Book.objects.all()

    # 搜索功能
    query = request.GET.get('search', '')
    if query:
        books = books.filter(title__icontains=query)  # 根据书名搜索

    return render(request, 'book_management.html', {'books': books, 'is_admin': is_admin, 'is_student': is_student, 'query': query})

# 添加图书视图（仅限管理员）
@login_required
@group_required('Administrator')
def add_book_view(request):
    is_admin, is_student = get_user_role_flags(request.user)
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_management')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form, 'is_admin': is_admin, 'is_student': is_student})

# 删除图书视图（仅限管理员）
@login_required
@group_required('Administrator')
def delete_book_view(request, book_id):
    is_admin, is_student = get_user_role_flags(request.user)
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_management')
    return render(request, 'delete_book.html', {'book': book, 'is_admin': is_admin, 'is_student': is_student})

# 借阅归还视图（仅限管理员）
@login_required
@group_required('Administrator')
def borrow_return_view(request):
    is_admin, is_student = get_user_role_flags(request.user)
    borrow_records = BorrowReturn.objects.all()
    return render(request, 'borrow_return.html', {'borrow_records': borrow_records, 'is_admin': is_admin, 'is_student': is_student})

# 学生用户查看借阅归还记录
@login_required
@group_required('Student')
def student_borrow_return_view(request):
    is_admin, is_student = get_user_role_flags(request.user)
    borrow_records = BorrowReturn.objects.filter(user=request.user)
    return render(request, 'borrow_return.html', {'borrow_records': borrow_records, 'is_admin': is_admin, 'is_student': is_student})

# 借阅图书视图（仅限管理员）
@login_required
@group_required('Administrator')
def borrow_book_view(request):
    is_admin, is_student = get_user_role_flags(request.user)
    if request.method == 'POST':
        form = BorrowFormAdmin(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            user = form.cleaned_data['user']  # 选择的学生
            if not book.available:
                return render(request, 'borrow_book.html', {'form': form, 'is_admin': is_admin, 'is_student': is_student, 'error': '该图书已被借出。'})
            borrow_record = BorrowReturn.objects.create(
                book=book,
                user=user,
                borrow_date=timezone.now().date()
            )
            book.available = False
            book.save()
            return redirect('borrow_return')
    else:
        form = BorrowFormAdmin()
    return render(request, 'borrow_book.html', {'form': form, 'is_admin': is_admin, 'is_student': is_student})


# 归还图书视图（仅限管理员）
@login_required
@group_required('Administrator')
def return_book_view(request):
    is_admin, is_student = get_user_role_flags(request.user)
    if request.method == 'POST':
        # 对于管理员，不传递 user 参数
        form = ReturnForm(request.POST)
        if form.is_valid():
            borrow_record = form.cleaned_data['borrow_record']
            if borrow_record.return_date:
                form.add_error('borrow_record', '该图书已归还。')
            else:
                borrow_record.return_date = timezone.now().date()
                borrow_record.save()
                book = borrow_record.book
                book.available = True
                book.save()
                return redirect('borrow_return')
        else:
            # 如果表单无效，重新设置查询集以重新渲染表单
            form.fields['borrow_record'].queryset = BorrowReturn.objects.filter(return_date__isnull=True)
    else:
        # GET 请求，初始化表单，不传递 user 参数
        form = ReturnForm()

    return render(request, 'return_book.html', {
        'form': form,
        'is_admin': is_admin,
        'is_student': is_student
    })

# 学生归还图书视图
@login_required
@group_required('Student')
def student_return_book_view(request):
    is_admin, is_student = get_user_role_flags(request.user)
    if request.method == 'POST':
        form = ReturnForm(request.POST, user=request.user)
        if form.is_valid():
            borrow_record = form.cleaned_data['borrow_record']
            if borrow_record.return_date:
                return render(request, 'student_return_book.html', {'form': form, 'is_admin': is_admin, 'is_student': is_student, 'error': '该图书已归还。'})
            borrow_record.return_date = timezone.now().date()
            borrow_record.save()
            book = borrow_record.book
            book.available = True
            book.save()
            return redirect('student_borrow_return')
    else:
        form = ReturnForm(user=request.user)
    return render(request, 'student_return_book.html', {'form': form, 'is_admin': is_admin, 'is_student': is_student})
