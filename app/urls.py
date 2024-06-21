from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dangky/', views.dangky, name = "dangky"),
    path('dangnhap/', views.dangnhap, name = "dangnhap"),
    path('logout/', views.logoutPage, name = "logout"),
    path('', views.home, name = "home"),
    # # path('', views.index, name='index'),
    path('ds/', views.ds, name = "ds"),
    path('ks/', views.ks, name = 'ks'),
    path('search/', views.search, name = 'search'),
    path('datphong/', views.datphong, name = "datphong"),
    path('dondatphong/', views.dondatphong, name = "dondatphong"),
    # path('custom-dashboard/', views.index, name='custom_dashboard'),
    # # path('custom-profile/', views.profile, name='custom_profile'),
    # path('customer-dashboard/', views.dashboard, name='customer_dashboard'),
    # path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('pay', views.index_payment, name='index'),
    path('payment', views.payment, name='payment'),
    path('payment_ipn', views.payment_ipn, name='payment_ipn'),
    path('payment_return', views.payment_return, name='payment_return'),
    path('query', views.query, name='query'),
    path('refund', views.refund, name='refund'),
]

urlpatterns +=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)