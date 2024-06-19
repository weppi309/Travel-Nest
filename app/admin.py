from django.contrib import admin
from .models import *
# Register your models here.
class KhachSanInline(admin.TabularInline):
    model = KhachSan
    extra = 1
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'date_joined', 'phone_number', 'address', 'custom_method')
    inlines = [KhachSanInline]

    def custom_method(self, obj):
        return ', '.join([str(group) for group in obj.groups.all()])
    custom_method.short_description = 'Groups'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'provider':
            return qs.filter(id=request.user.id)
        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None and obj.id != request.user.id:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None and obj.id != request.user.id:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.role == 'provider':
            return False
        return super().has_add_permission(request)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            fieldsets = tuple(
                (name, {'fields': [f for f in data['fields'] if f not in ('groups', 'user_permissions', 'role', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login', 'password')]})
                for name, data in fieldsets
            )
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            readonly_fields.extend(['groups', 'user_permissions', 'role', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login', 'password'])
        return readonly_fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            # Prevent non-superusers from changing 'role', 'groups', 'is_superuser', 'is_staff', 'is_active', 'date_joined'
            if 'role' in form.changed_data:
                form.cleaned_data['role'] = obj.role
            if 'groups' in form.changed_data:
                form.cleaned_data['groups'] = obj.groups
            if 'is_superuser' in form.changed_data:
                form.cleaned_data['is_superuser'] = obj.is_superuser
            if 'is_staff' in form.changed_data:
                form.cleaned_data['is_staff'] = obj.is_staff
            if 'is_active' in form.changed_data:
                form.cleaned_data['is_active'] = obj.is_active
            if 'date_joined' in form.changed_data:
                form.cleaned_data['date_joined'] = obj.date_joined
            if 'last_login' in form.changed_data:
                form.cleaned_data['last_login'] = obj.last_login
            if 'password' in form.changed_data:
                form.cleaned_data['password'] = obj.password
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)
admin.site.register(User, UserAdmin)
class AnhPhongInline(admin.TabularInline):
    model = AnhPhong
class PhongAdmin(admin.ModelAdmin):
    list_display=('id','tenphong','khachsan','created_date','active')
    inlines = [AnhPhongInline]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'provider':
            return qs.filter(khachsan__owner=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None and obj.khachsan.owner != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None and obj.khachsan.owner != request.user:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.role == 'provider':
            return True
        return super().has_add_permission(request)

class AnhKhachSanInline(admin.TabularInline):
    model = AnhKhachSan

class PhongInline(admin.TabularInline):
    model = Phong
class KhachSanAdmin(admin.ModelAdmin):
    list_display=('id','tenkhachsan','sdt','email_ks','created_date','active')
    inlines = [AnhKhachSanInline, PhongInline]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'provider':
            return qs.filter(owner=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None and obj.owner != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None and obj.owner != request.user:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.role == 'provider':
            return True
        return super().has_add_permission(request)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            kwargs['initial'] = request.user.id  # Thiết lập owner mặc định là provider đang đăng nhập
            kwargs['queryset'] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is not None:
            form.base_fields['owner'].queryset = User.objects.filter(id=request.user.id)
        return form

class TinhAdmin(admin.ModelAdmin):
    list_display=('id','tentinh','created_date','active')
class HuyenAdmin(admin.ModelAdmin):
    list_display=('id','tenhuyen','tinh','created_date','active')
class XaAdmin(admin.ModelAdmin):
    list_display=('id','tenXa','huyen','created_date','active')
    
class AnhPhongAdmin(admin.ModelAdmin):
    list_display=('id','anhphong','phong','created_date','active')
class AnhKhachSanAdmin(admin.ModelAdmin):
    list_display=('id','anhks','khachsan','created_date','active')
class LoaiTienNghiAdmin(admin.ModelAdmin):
    list_display=('id','tenloai','created_date','active')
class TienNghiAdmin(admin.ModelAdmin):
    list_display=('id','tentiennghi','loai_tiennghi','created_date','active')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'provider':
            return qs.filter(khachsan__owner=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None and obj.khachsan.owner != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None and obj.khachsan.owner != request.user:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.role == 'provider':
            return True
        return super().has_add_permission(request)
class DichVuAdmin(admin.ModelAdmin):
    list_display=('id','tendichvu','gia_dichvu','created_date','active') 
class ChiTietHoaDonInline(admin.TabularInline):
    model = ChiTietHoaDon
    extra = 1
# class HoaDonAdmin(admin.ModelAdmin):
#     list_display=('id','user','created_date','active')
#     inlines = [ChiTietHoaDonInline]
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.role == 'provider':
#             # Lấy tất cả ChiTietHoaDon liên quan đến phong thuộc nhà cung cấp
#             chi_tiet_hoa_don_ids = ChiTietHoaDon.objects.filter(phong__khachsan__owner=request.user).values_list('hoadon_id', flat=True)
#             return qs.filter(id__in=chi_tiet_hoa_don_ids)
#         return qs

#     def has_change_permission(self, request, obj=None):
#         if request.user.role == 'provider' and obj is not None:
#             chi_tiet_hoa_dons = ChiTietHoaDon.objects.filter(hoadon=obj)
#             if not chi_tiet_hoa_dons.filter(phong__khachsan__owner=request.user).exists():
#                 return False
#         return super().has_change_permission(request, obj)

#     def has_delete_permission(self, request, obj=None):
#         if request.user.role == 'provider' and obj is not None:
#             chi_tiet_hoa_dons = ChiTietHoaDon.objects.filter(hoadon=obj)
#             if not chi_tiet_hoa_dons.filter(phong__khachsan__owner=request.user).exists():
#                 return False
#         return super().has_delete_permission(request, obj)

#     def has_add_permission(self, request):
#         if request.user.role == 'provider':
#             return True
#         return super().has_add_permission(request)
# class ChiTietHoaDonAdmin(admin.ModelAdmin):
#     list_display=('id','hoadon','phong','created_date','active')
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.role == 'provider':
#             # Filter ChiTietHoaDon objects by Phong's owner which is associated with the current user's HoaDon
#             return qs.filter(phong__owner=request.user.hoadon_set.first().user)
#         return qs

#     def has_change_permission(self, request, obj=None):
#         if request.user.role == 'provider' and obj is not None and obj.phong.owner != request.user.hoadon_set.first().user:
#             return False
#         return super().has_change_permission(request, obj)

#     def has_delete_permission(self, request, obj=None):
#         if request.user.role == 'provider' and obj is not None and obj.phong.owner != request.user.hoadon_set.first().user:
#             return False
#         return super().has_delete_permission(request, obj)

#     def has_add_permission(self, request):
#         if request.user.role == 'provider':
#             return True
#         return super().has_add_permission(request)

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == 'phong':
#             # Filter Phong objects by the owner associated with the current user's HoaDon
#             kwargs['queryset'] = Phong.objects.filter(owner=request.user.hoadon_set.first().user)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
class HoaDonAdmin(admin.ModelAdmin):
    list_display=('id','user','created_date','active')
    inlines = [ChiTietHoaDonInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'provider':
            # Lọc các hóa đơn mà provider đó có quyền xem
            return qs.filter(chitiethoadon__phong__khachsan__owner=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None:
            chi_tiet_hoa_dons = obj.chitiethoadon_set.filter(phong__khachsan__owner=request.user)
            if not chi_tiet_hoa_dons.exists():
                return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None:
            chi_tiet_hoa_dons = obj.chitiethoadon_set.filter(phong__khachsan__owner=request.user)
            if not chi_tiet_hoa_dons.exists():
                return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.role == 'provider':
            return True
        return super().has_add_permission(request)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'phong':
            # Lọc các phòng thuộc khách sạn của `HoaDon` của provider
            hoa_don = request.user.hoadon_set.first()
            if hoa_don:
                kwargs['queryset'] = Phong.objects.filter(khachsan__owner=hoa_don.user)
            else:
                kwargs['queryset'] = Phong.objects.none()  # Trả về queryset rỗng nếu không tìm thấy `HoaDon`
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
class ChiTietHoaDonAdmin(admin.ModelAdmin):
    list_display=('id','hoadon','phong','created_date','active')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'provider':
            # Lọc chi tiết hóa đơn dựa trên phòng thuộc khách sạn của `HoaDon` của provider
            hoa_don = request.user.hoadon_set.first()
            if hoa_don:
                return qs.filter(phong__khachsan__owner=hoa_don.user)
            else:
                return qs.none()  # Trả về queryset rỗng nếu không tìm thấy `HoaDon`
        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None:
            hoa_don = request.user.hoadon_set.first()
            if hoa_don and obj.phong.khachsan.owner != hoa_don.user:
                return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None:
            hoa_don = request.user.hoadon_set.first()
            if hoa_don and obj.phong.khachsan.owner != hoa_don.user:
                return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.role == 'provider':
            return True
        return super().has_add_permission(request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'phong':
            # Lọc các phòng thuộc khách sạn của `HoaDon` của provider
            hoa_don = request.user.hoadon_set.first()
            if hoa_don:
                kwargs['queryset'] = Phong.objects.filter(khachsan__owner=hoa_don.user)
            else:
                kwargs['queryset'] = Phong.objects.none()  # Trả về queryset rỗng nếu không tìm thấy `HoaDon`
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
class DanhGiaAdmin(admin.ModelAdmin):
    list_display=('id','hoadon','diem','created_date','active')
class KhuyenMaiAdmin(admin.ModelAdmin):
    list_display=('id','tenkhuyenmai','thoigian_bd','thoigian_kt','giatri_km','created_date','active')

admin.site.register(Tinh,TinhAdmin)
admin.site.register(Huyen,HuyenAdmin)
admin.site.register(Xa,XaAdmin)
admin.site.register(KhachSan,KhachSanAdmin)
admin.site.register(Phong,PhongAdmin)
admin.site.register(AnhPhong,AnhPhongAdmin)
admin.site.register(AnhKhachSan,AnhKhachSanAdmin)
admin.site.register(TienNghi,TienNghiAdmin)
admin.site.register(LoaiTienNghi,LoaiTienNghiAdmin)
admin.site.register(DichVu,DichVuAdmin)
admin.site.register(HoaDon,HoaDonAdmin)
# admin.site.register(ChiTietHoaDon,ChiTietHoaDonAdmin)
admin.site.register(Danhgia,DanhGiaAdmin)
admin.site.register(KhuyenMai,KhuyenMaiAdmin)