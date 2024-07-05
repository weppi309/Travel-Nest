from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Các đường dẫn mà người dùng có thể truy cập mà không cần đăng nhập
        self.allowed_paths = [
            reverse('home'),
            reverse('ks'),
            reverse('ds'),
            reverse('dangky'),
            reverse('dangnhap'),
            reverse('logout'),
            reverse('admin:index'),  # Thêm đường dẫn admin
        ]
        # Đường dẫn bắt đầu với `/admin/` cũng cần cho phép
        self.admin_prefix = reverse('admin:index').rsplit('/', 2)[0]  # Lấy prefix /admin/
        
        # Đường dẫn tĩnh (static và media)
        self.static_prefix = settings.STATIC_URL
        self.media_prefix = settings.MEDIA_URL

    def __call__(self, request):
        # Cho phép truy cập nếu đường dẫn thuộc tài nguyên tĩnh hoặc media
        if (request.path.startswith(self.static_prefix) or
            request.path.startswith(self.media_prefix)):
            return self.get_response(request)
        
        # Cho phép truy cập nếu người dùng chưa xác thực và đường dẫn thuộc các đường dẫn cho phép
        if not request.user.is_authenticated:
            if request.path in self.allowed_paths or request.path.startswith(self.admin_prefix):
                return self.get_response(request)
            return redirect('home')

        # Cho phép truy cập nếu người dùng đã xác thực và có role user
        if request.user.role == 'user':
            return self.get_response(request)

        # Kiểm tra quyền truy cập của người dùng với role khác
        if request.user.role == 'admin':
            pass
        elif request.user.role == 'provider':
            if not request.path.startswith(reverse('admin:index')):
                return redirect('admin:index')

        response = self.get_response(request)
        return response

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.contrib.auth.models import Group

class JazzminSidebarMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Admin').exists():
                # Định nghĩa sidebar cho admin
                settings.JAZZMIN_SETTINGS["custom_links"] = {
                    "app": [
                        {"name": "User Role Stats", "url": "admin:user_role_stats", "icon": "fas fa-users"},
                        {"name": "Hotel by Tinh", "url": "admin:hotel_by_tinh", "icon": "fas fa-hotel"},
                        {"name": "Room by Hotel", "url": "admin:room_by_hotel", "icon": "fas fa-bed"},
                        {"name": "Invoice by Month", "url": "admin:invoice_by_month", "icon": "fas fa-file-invoice"},
                        {"name": "Revenue by Month", "url": "admin:revenue_by_month", "icon": "fas fa-dollar-sign"},
                        {"name": "Current Promotions", "url": "admin:current_promotions", "icon": "fas fa-tags"},
                    ]
                }
            else:
                # Định nghĩa sidebar cho các vai trò khác
                settings.JAZZMIN_SETTINGS["custom_links"] = {}

# class NoCacheMiddleware(MiddlewareMixin):
#     def process_response(self, request, response):
#         response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#         response['Pragma'] = 'no-cache'
#         response['Expires'] = '0'
#         return response