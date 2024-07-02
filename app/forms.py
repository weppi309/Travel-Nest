from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Tinh

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

class SearchForm(forms.Form):
    tinh = forms.ModelChoiceField(queryset=Tinh.objects.all(), required=False, label='Tỉnh')
    tenkhachsan = forms.CharField(max_length=200, required=False, label='Tên khách sạn')
    diachi = forms.CharField(max_length=200, required=False, label='Địa chỉ')
    giaphong_min = forms.FloatField(required=False, label='Giá phòng tối thiểu')
    giaphong_max = forms.FloatField(required=False, label='Giá phòng tối đa')
    soluongnguoi = forms.IntegerField(required=False, label='Số lượng người')
    ngay_nhan = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Ngày nhận')
    ngay_tra = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Ngày trả')

