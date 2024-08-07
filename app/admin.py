from django.contrib import admin
from django.utils.html import mark_safe
from app.views import current_promotions_view, hotel_by_tinh_view, hotel_rating_view, invoice_by_month_view, revenue_by_month_view, room_by_hotel_view, user_role_stats_view
from .models import *
# from django.urls import reverse
# from django.utils.html import format_html

class CustomAdminSite(admin.AdminSite):
    site_header = 'Travel Nest AdminSite'
    site_title = 'Admin'
    index_title = 'Welcome to Travel Nest Admin Site'

    def get_urls(self):
        from django.urls import path
        from django.contrib.auth.decorators import user_passes_test
        
        # Custom decorator to check if user is an admin
        def is_admin(user):
            return user.is_superuser

        # Define the URLs with the custom decorator
        custom_urls = [
            path('user-role-stats/', self.admin_view(user_passes_test(is_admin)(user_role_stats_view)), name='user_role_stats'),
            path('hotel-by-tinh/', self.admin_view(user_passes_test(is_admin)(hotel_by_tinh_view)), name='hotel_by_tinh'),
            path('room-by-hotel/', self.admin_view(user_passes_test(is_admin)(room_by_hotel_view)), name='room_by_hotel'),
            path('invoice-by-month/', self.admin_view(user_passes_test(is_admin)(invoice_by_month_view)), name='invoice_by_month'),
            path('revenue-by-month/', self.admin_view(user_passes_test(is_admin)(revenue_by_month_view)), name='revenue_by_month'),
            path('hotel-rating/', self.admin_view(user_passes_test(is_admin)(hotel_rating_view)), name='hotel_rating'),
            path('current-promotions/', self.admin_view(user_passes_test(is_admin)(current_promotions_view)), name='current_promotions'),
        ]
        # Add the custom URLs to the default admin URLs
        urls = super().get_urls()
        return custom_urls + urls

admin_site = CustomAdminSite(name='custom_admin')
class KhachSanInline(admin.TabularInline):
    model = KhachSan
    extra = 1
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'date_joined', 'phone_number', 'address', 'custom_method')
    # inlines = [KhachSanInline]
    list_display_links = list_display
    list_filter = ('is_active', 'date_joined')
    search_fields = ('first_name', 'username', 'last_name', 'email', 'phone_number')
    readonly_fields = ['image_view']

    def image_view(self, user):
        return mark_safe(
            "<img src='/static/{url}' alt='test' width='120' />".format(url=user.avatar.name)
        )
    def get_inlines(self, request, obj=None):
        if request.user.role != 'admin':
            return [KhachSanInline]
        return super().get_inlines(request, obj)
    def custom_method(self, obj):
        return ', '.join([str(group) for group in obj.groups.all()])
    custom_method.short_description = 'Groups'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role in ['user', 'provider']:
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
admin_site.register(User, UserAdmin)
class AnhPhongInline(admin.TabularInline):
    model = AnhPhong
class PhongAdmin(admin.ModelAdmin):
    list_display=('id','tenphong','khachsan','created_date','active')
    inlines = [AnhPhongInline]
    list_display_links = list_display
    list_filter = ('khachsan', 'active')
    search_fields = ('tenphong',)
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
    list_display=('id','tenkhachsan','sdt','email_ks','owner','created_date','active')
    inlines = [AnhKhachSanInline, PhongInline]
    list_display_links = list_display
    list_filter = ('created_date', 'owner', 'active')
    search_fields = ('tenkhachsan',)
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
            if request.user.role == 'provider':
                kwargs['initial'] = request.user.id  # Thiết lập owner mặc định là provider đang đăng nhập
                kwargs['queryset'] = User.objects.filter(id=request.user.id)
            else:
                # Lọc danh sách owner chỉ bao gồm những người dùng có vai trò 'provider'
                kwargs['queryset'] = User.objects.filter(role='provider')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.role == 'provider':
            form.base_fields['owner'].queryset = User.objects.filter(id=request.user.id)
            if obj is None:  # Khi thêm mới
                form.base_fields['owner'].initial = request.user
            form.base_fields['owner'].disabled = True
        else:
            form.base_fields['owner'].queryset = User.objects.filter(role='provider')
        return form
class TinhAdmin(admin.ModelAdmin):
    list_display=('id','tentinh','created_date','active')
    list_display_links = list_display
    list_filter = ('active',)
    search_fields = ('tentinh',)
class HuyenAdmin(admin.ModelAdmin):
    list_display=('id','tenhuyen','tinh','created_date','active')
    list_display_links = list_display
    list_filter = ('tinh', 'active')
    search_fields = ('tenhuyen',)
class XaAdmin(admin.ModelAdmin):
    list_display=('id','tenXa','huyen','created_date','active')
    list_display_links = list_display
    list_filter = ('huyen', 'active')
    search_fields = ('tenXa',)
class AnhPhongAdmin(admin.ModelAdmin):
    list_display=('id','anhphong','phong','created_date','active')
class AnhKhachSanAdmin(admin.ModelAdmin):
    list_display=('id','anhks','khachsan','created_date','active')
class TienNghiAdmin(admin.ModelAdmin):
    list_display=('id','tentiennghi','created_date','active')
    list_display_links = list_display
    list_filter = ('active',)
    search_fields = ('tentiennghi',)
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
    list_display_links = list_display
    list_filter = ('active', 'gia_dichvu')
    search_fields = ('tendichvu',)
class ChiTietHoaDonInline(admin.TabularInline):
    model = ChiTietHoaDon
    extra = 1
class HoaDonAdmin(admin.ModelAdmin):
    list_display=('id','user', 'trangthai', 'thanh_toan','created_date','active')
    inlines = [ChiTietHoaDonInline]
    list_display_links = list_display
    list_filter = ('user', 'trangthai', 'active')
    search_fields = ('user__username',)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'provider':
            # Lọc các hóa đơn mà provider đó có quyền xem
            return qs.filter(chitiethoadon__phong__khachsan__owner=request.user)
        if request.user.role == 'user':
            return qs.filter(user=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None:
            chi_tiet_hoa_dons = obj.chitiethoadon_set.filter(phong__khachsan__owner=request.user)
            if not chi_tiet_hoa_dons.exists():
                return False
        if request.user.role == 'user' and obj is not None and obj.user != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.role == 'provider' and obj is not None:
            chi_tiet_hoa_dons = obj.chitiethoadon_set.filter(phong__khachsan__owner=request.user)
            if not chi_tiet_hoa_dons.exists():
                return False
        if request.user.role == 'user' and obj is not None and obj.user != request.user:
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
    list_display_links = list_display
    list_filter = ('hoadon', 'phong', 'active')
    search_fields = ('hoadon__id', 'phong__tenphong')
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

admin_site.register(Tinh,TinhAdmin)
admin_site.register(Huyen,HuyenAdmin)
admin_site.register(Xa,XaAdmin)
admin_site.register(KhachSan,KhachSanAdmin)
admin_site.register(Phong,PhongAdmin)
admin_site.register(AnhPhong,AnhPhongAdmin)
admin_site.register(AnhKhachSan,AnhKhachSanAdmin)
admin_site.register(TienNghi,TienNghiAdmin)
admin_site.register(DichVu,DichVuAdmin)
admin_site.register(HoaDon,HoaDonAdmin)
# admin.site.register(ChiTietHoaDon,ChiTietHoaDonAdmin)
admin_site.register(Danhgia,DanhGiaAdmin)
admin_site.register(KhuyenMai,KhuyenMaiAdmin)