from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('provider', 'Provider'),
        ('user', 'User'),
    )
    phone_number = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    avatar = models.ImageField(upload_to='avatar/%Y/%m', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username
    
    
class ModelBase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        abstract = True
        # ordering = ['-id'] # sắp giảm theo id
 
class Tinh(ModelBase):
    tentinh = models.CharField(max_length=200,null=True)
    anhtinh = models.ImageField(upload_to='tinh/%Y/%m',null=True,blank=True)
    def __str__(self):
        return self.tentinh
class Huyen(ModelBase):
    tenhuyen= models.CharField(max_length=200,null=True)
    tinh = models.ForeignKey(Tinh,on_delete=models.SET_NULL,blank=True,null=True)
   
    def __str__(self):
        return self.tenhuyen
class Xa(ModelBase):
    tenXa = models.CharField(max_length=200,null=True)
    huyen = models.ForeignKey(Huyen,on_delete=models.SET_NULL,blank=True,null=True)
    def __str__(self):
        return self.tenXa

class KhachSan(ModelBase):
    tenkhachsan = models.CharField(max_length=200,null=True)
    diachi = models.CharField(max_length=200,null=True)
    xa= models.ForeignKey(Xa,on_delete=models.SET_NULL,blank=True,null=True)
    tinh = models.ForeignKey(Tinh,on_delete=models.SET_NULL,blank=True,null=True )
    sdt = models.CharField(max_length=11,null=True)
    mota = models.CharField(max_length=200,null=True)
    email_ks = models.CharField(max_length=200,null=True)    
    dichvu = models.ManyToManyField('DichVu',blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True,null=True)
    def __str__(self):
        return self.tenkhachsan

class Phong(ModelBase):
    tenphong = models.CharField(max_length=200,null=True)
    dientich = models.CharField(max_length=200,null=True)
    phongtam = models.CharField(max_length=200,null=True)
    soluongnguoi = models.IntegerField()
    giaphong = models.FloatField()
    soluong= models.IntegerField()
    khachsan = models.ForeignKey(KhachSan,on_delete=models.SET_NULL,blank=True,null=True)
    tiennghi = models.ManyToManyField('TienNghi',blank=True)
    

class AnhPhong(ModelBase):
    anhphong = models.ImageField(upload_to='anhphong/%Y/%m',null=True,blank=True)
    phong = models.ForeignKey(Phong,on_delete=models.SET_NULL,blank=True,null=True )

class AnhKhachSan(ModelBase):
    anhks = models.ImageField(upload_to='anhks/%Y/%m',null=True,blank=True)
    khachsan = models.ForeignKey(KhachSan,on_delete=models.SET_NULL,blank=True,null=True)

class TienNghi(ModelBase):
    khachsan = models.ForeignKey(KhachSan, on_delete=models.CASCADE,blank=True,null=True)
    icon = models.ImageField(upload_to='icon/%Y/%m',null=True,blank=True)
    tentiennghi = models.CharField(max_length=200,null=True)
    mota_tiennghi = models.TextField(blank=True,null=True)
    loai_tiennghi = models.ForeignKey('LoaiTienNghi',on_delete=models.SET_NULL,blank=True,null=True)
    def __str__(self):
        return self.tentiennghi
class LoaiTienNghi(ModelBase):
    tenloai = models.CharField(max_length=200,null=True)
class DichVu(ModelBase):
    tendichvu= models.CharField(max_length=200,null=True)
    mota_dichvu= models.TextField(blank=True,null=True)
    gia_dichvu = models.FloatField()
    def __str__(self):
        return self.tendichvu
    
class HoaDon(ModelBase):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    thanh_toan = models.ForeignKey('Payment_VNPay', on_delete=models.SET_NULL, null=True, blank=True)
    CHUA_THANH_TOAN = 'CTT'
    DA_NHAN_PHONG = 'DNP'
    DA_HUY = 'DH'
    
    TRANGTHAI_CHOICES = [
        (CHUA_THANH_TOAN, 'Chưa thanh toán'),
        (DA_NHAN_PHONG, 'Đã nhận phòng'),
        (DA_HUY, 'Đã hủy'),
    ]
    
    trangthai = models.CharField(
        max_length=3,
        choices=TRANGTHAI_CHOICES,
        default=CHUA_THANH_TOAN,
    )

class ChiTietHoaDon(ModelBase):
    phong = models.ForeignKey(Phong,on_delete=models.SET_NULL,blank=True,null=True)
    hoadon = models.ForeignKey(HoaDon,on_delete=models.SET_NULL,blank=True,null=True)
    ngay_gio_nhan = models.DateTimeField()
    ngay_gio_tra = models.DateTimeField()
    soluong = models.IntegerField()
    dongia = models.FloatField()
class Danhgia(ModelBase):
    hoadon = models.OneToOneField(HoaDon,on_delete=models.CASCADE,blank=True,null=True)
    diem = models.IntegerField()
    binhluan = models.CharField(max_length=200,null=True)

class KhuyenMai(ModelBase):
    tenkhuyenmai= models.CharField(max_length=200,null=True)
    thoigian_bd = models.DateTimeField()
    thoigian_kt = models.DateTimeField()
    giatri_km = models.FloatField()
    phong = models.ManyToManyField(Phong, blank=True)

class Payment_VNPay(models.Model):
    order_id = models.BigIntegerField(default=0, null=True, blank=True)
    amount = models.FloatField(default=0.0, null=True, blank=True)
    order_desc = models.CharField(max_length=200,null=True, blank=True)
    vnp_TransactionNo = models.CharField(max_length=200,null=True, blank=True)
    vnp_ResponseCode = models.CharField(max_length=200,null=True, blank=True)

class PaymentForm(forms.Form):
    order_id = forms.CharField(max_length=250)
    order_type = forms.CharField(max_length=20)
    amount = forms.IntegerField()
    order_desc = forms.CharField(max_length=100)
    bank_code = forms.CharField(max_length=20, required=False)
    language = forms.CharField(max_length=2)