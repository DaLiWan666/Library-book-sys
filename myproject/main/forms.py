# main/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Book, BorrowReturn
from django.utils import timezone

class UserRegistrationForm(forms.ModelForm):
    """
    用户注册表单
    """
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password_confirm(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            raise forms.ValidationError("两次输入的密码不一致！")
        return cleaned_data.get('password_confirm')

class BookForm(forms.ModelForm):
    """
    图书添加表单
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BorrowFormAdmin(forms.Form):
    """
    管理员借阅图书表单
    """
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(available=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="选择图书"
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Student'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="选择借阅学生"
    )

class BorrowFormStudent(forms.Form):
    """
    学生借阅图书表单（不需要选择用户）
    """
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(available=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="选择图书"
    )

class ReturnForm(forms.Form):
    """
    归还图书表单
    """
    borrow_record = forms.ModelChoiceField(
        queryset=BorrowReturn.objects.none(),
        label="选择借阅记录",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReturnForm, self).__init__(*args, **kwargs)
        if user:
            # 如果传入了用户，显示该用户的未归还记录
            self.fields['borrow_record'].queryset = BorrowReturn.objects.filter(user=user, return_date__isnull=True)
            self.fields['borrow_record'].label_from_instance = lambda obj: f"{obj.book.title} - 借出日期: {obj.borrow_date}"
        else:
            # 否则，显示所有未归还的借阅记录（管理员视图）
            self.fields['borrow_record'].queryset = BorrowReturn.objects.filter(return_date__isnull=True)
            self.fields['borrow_record'].label_from_instance = lambda obj: f"{obj.book.title} - 借阅者: {obj.user.username} - 借出日期: {obj.borrow_date}"
