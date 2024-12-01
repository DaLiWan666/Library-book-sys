# main/models.py
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    """
    图书模型
    """
    title = models.CharField(max_length=200, verbose_name="书名")
    author = models.CharField(max_length=100, verbose_name="作者")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    available = models.BooleanField(default=True, verbose_name="是否可借")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="入库时间")  # 新增字段

    def __str__(self):
        return self.title


class BorrowReturn(models.Model):
    """
    借阅归还模型
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="图书")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="借阅者")
    borrow_date = models.DateField(auto_now_add=True, verbose_name="借出日期")
    return_date = models.DateField(null=True, blank=True, verbose_name="归还日期")

    def __str__(self):
        return f"{self.book.title} 借阅者: {self.user.username}"
