# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),

    # 用户管理
    path('user-management/', views.user_management_view, name='user_management'),
    path('user-management/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('user-management/set-role/<int:user_id>/', views.set_user_role_view, name='set_user_role'),

    # 图书管理
    path('book-management/', views.book_management_view, name='book_management'),
    path('book-management/add/', views.add_book_view, name='add_book'),
    path('book-management/delete/<int:book_id>/', views.delete_book_view, name='delete_book'),

    # 借阅归还（管理员）
    path('borrow-return/', views.borrow_return_view, name='borrow_return'),
    path('borrow-return/borrow/', views.borrow_book_view, name='borrow_book'),
    path('borrow-return/return/', views.return_book_view, name='return_book'),

    # 学生借阅归还
    path('student/borrow-return/', views.student_borrow_return_view, name='student_borrow_return'),
    path('student/return/', views.student_return_book_view, name='student_return_book'),
    
    # 学生查看书籍
    path('books/', views.view_books_view, name='view_books'),  # 添加此行
]
