from django.utils import timezone
from datetime import timedelta
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

    class Meta:
        verbose_name_plural = 'Quản lý người dùng'

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
    class Meta:
        verbose_name_plural = 'Quản lý tỉnh thành'
    def __str__(self):
        return self.tentinh
class Huyen(ModelBase):
    tenhuyen= models.CharField(max_length=200,null=True)
    tinh = models.ForeignKey(Tinh,on_delete=models.SET_NULL,blank=True,null=True)
    class Meta:
        verbose_name_plural = 'Quản lý quận huyện'
    def __str__(self):
        return self.tenhuyen
class Xa(ModelBase):
    tenXa = models.CharField(max_length=200,null=True)
    huyen = models.ForeignKey(Huyen,on_delete=models.SET_NULL,blank=True,null=True)
    class Meta:
        verbose_name_plural = 'Quản lý xã phường'
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
    class Meta:
        verbose_name_plural = 'Quản lý khách sạn'
    def __str__(self):
        return self.tenkhachsan
    @property
    def diem_trung_binh(self):
        danhgia_list = Danhgia.objects.filter(hoadon__chitiethoadon__phong__khachsan=self)
        # Tính tổng điểm từ tất cả các đánh giá
        tong_diem = sum([danhgia.diem for danhgia in danhgia_list])
        # Đếm số lượng đánh giá
        so_luong_danh_gia = danhgia_list.count()
        # Tính điểm trung bình hoặc đặt điểm mặc định là 10 nếu chưa có đánh giá
        diem_trung_binh = (tong_diem / so_luong_danh_gia) if so_luong_danh_gia > 0 else 10
        diem_tb= int(diem_trung_binh)
        return diem_tb
    @property
    def get_danh_gia_tb(self):
        if 9 <= self.diem_trung_binh<= 10:
            return "Tuyệt vời"
        elif 7 <= self.diem_trung_binh < 9:
            return "Tốt"
        elif 5 <= self.diem_trung_binh < 7:
            return "Bình thường"
        elif self.diem_trung_binh < 5:
            return "Tệ"
    @property
    def sum_danh_gia(self):
         danhgia_list = Danhgia.objects.filter(hoadon__chitiethoadon__phong__khachsan=self)
         so_luong_danh_gia = danhgia_list.count()
         return so_luong_danh_gia
class Phong(ModelBase):
    tenphong = models.CharField(max_length=200,null=True)
    dientich = models.CharField(max_length=200,null=True)
    phongtam = models.CharField(max_length=200,null=True)
    soluongnguoi = models.IntegerField()
    giaphong = models.FloatField()
    soluong= models.IntegerField()
    khachsan = models.ForeignKey(KhachSan,on_delete=models.SET_NULL,blank=True,null=True)
    tiennghi = models.ManyToManyField('TienNghi',blank=True)
    class Meta:
        verbose_name_plural = 'Quản lý phòng'
    def __str__(self):
        return self.tenphong
class AnhPhong(ModelBase):
    anhphong = models.ImageField(upload_to='anhphong/%Y/%m',null=True,blank=True)
    phong = models.ForeignKey(Phong,on_delete=models.SET_NULL,blank=True,null=True )
    class Meta:
        verbose_name_plural = 'Quản lý ảnh phòng'
class AnhKhachSan(ModelBase):
    anhks = models.ImageField(upload_to='anhks/%Y/%m',null=True,blank=True)
    khachsan = models.ForeignKey(KhachSan,on_delete=models.SET_NULL,blank=True,null=True)
    class Meta:
        verbose_name_plural = 'Quản lý ảnh khách sạn'
class TienNghi(ModelBase):
    icon = models.ImageField(upload_to='icon/%Y/%m',null=True,blank=True)
    tentiennghi = models.CharField(max_length=200,null=True)
    mota_tiennghi = models.TextField(blank=True,null=True)
    
    class Meta:
        verbose_name_plural = 'Quản lý tiện nghi'
    def __str__(self):
        return self.tentiennghi
class DichVu(ModelBase):
    tendichvu= models.CharField(max_length=200,null=True)
    mota_dichvu= models.TextField(blank=True,null=True)
    gia_dichvu = models.FloatField()
    class Meta:
        verbose_name_plural = 'Quản lý dịch vụ'
    def __str__(self):
        return self.tendichvu
    
class HoaDon(ModelBase):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    thanh_toan = models.ForeignKey('Payment_VNPay', on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=[('bank', 'Bank'), ('on_arrival', 'On Arrival')], default='on_arrival')
    payment_status = models.BooleanField(default=False)
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
    class Meta:
        verbose_name_plural = 'Quản lý hóa đơn'
    def huy_don_hang(self):
        if self.payment_status:
            raise forms.ValidationError("Đơn hàng đã thanh toán, không thể hủy.")
        
        chi_tiet_hoa_don = ChiTietHoaDon.objects.filter(hoadon=self)
        for chi_tiet in chi_tiet_hoa_don:
            if chi_tiet.ngay_gio_nhan <= timezone.now() + timedelta(days=1):
                raise forms.ValidationError("Không thể hủy đơn hàng vì đã quá thời gian nhận phòng.")
        
        chi_tiet_hoa_don.delete()
        self.delete()
class ChiTietHoaDon(ModelBase):
    phong = models.ForeignKey(Phong,on_delete=models.SET_NULL,blank=True,null=True)
    hoadon = models.ForeignKey(HoaDon,on_delete=models.SET_NULL,blank=True,null=True)
    ngay_gio_nhan = models.DateTimeField()
    ngay_gio_tra = models.DateTimeField()
    soluong_phong = models.IntegerField()
    soluong_dem = models.IntegerField()
    dongia = models.FloatField()
    class Meta:
        verbose_name_plural = 'Quản lý chi tiết hóa đơn'
class Danhgia(ModelBase):
    hoadon = models.OneToOneField(HoaDon,on_delete=models.CASCADE,blank=True,null=True)
    diem = models.IntegerField()
    binhluan = models.CharField(max_length=200,null=True)
    class Meta:
        verbose_name_plural = 'Quản lý đánh giá'
    @property
    def get_danh_gia(self):
        if 9 <= self.diem <= 10:
            return "Xuất sắc"
        elif 7 <= self.diem < 9:
            return "Tốt"
        elif 5 <= self.diem < 7:
            return "Bình thường"
        elif self.diem < 5:
            return "Tệ"
        else:
            return "Chưa được đánh giá"
class KhuyenMai(ModelBase):
    tenkhuyenmai= models.CharField(max_length=200,null=True)
    thoigian_bd = models.DateTimeField()
    thoigian_kt = models.DateTimeField()
    giatri_km = models.FloatField()
    phong = models.ManyToManyField(Phong, blank=True)
    class Meta:
        verbose_name_plural = 'Quản lý khuyến mãi'
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