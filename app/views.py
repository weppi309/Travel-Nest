import json
from django.forms import ValidationError
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Avg, F, Prefetch
from django.shortcuts import redirect, render
from datetime import datetime, timedelta, date
from .models import *
from .forms import CreateUserForm, SearchForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Min
# Create your views here.

def dangky(request):
    form = CreateUserForm()
    if request.method == "POST":
        form =CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Gán quyền Staff status cho người dùng mới
            user.is_staff = True
            user.save()
            # form.save()
            return redirect('dangnhap')
    context={'form': form}
    return render(request,'app/dangky.html',context)
def dangnhap(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Your account is inactive. Please contact the admin.')
        else:
            messages.info(request, 'Username or password is not correct!')
           
    context={}    
    return render(request,'app/dangnhap.html',context)
def logoutPage(request):
    logout(request)
    return redirect("dangnhap")
def home(request):
    tinhs = Tinh.objects.all()
    # tinh_data = Tinh.objects.annotate(
    #     num_hotels=Count('khachsan', filter=Q(khachsan__active=True))
    # )
    active_hotels = KhachSan.objects.filter(active=True)
    tinh_data = Tinh.objects.prefetch_related(Prefetch('khachsan_set', queryset=active_hotels)).annotate(
        num_hotels=Count('khachsan', filter=Q(khachsan__active=True))
    )
    # Lấy hai hàng đầu hiển thị 2 ảnh
    top_2_tinhs = Tinh.objects.all()[:2]
    # Lấy hàng thứ hai hiển thị 3 ảnh kèm tên
    # second_tinh = Tinh.objects.all()[2]
    # top_3_tinhs = Tinh.objects.filter(id__gte=second_tinh.id)[:3]
    try:
        second_tinh = Tinh.objects.all()[2]
        top_3_tinhs = Tinh.objects.filter(id__gte=second_tinh.id)[:3]
    except IndexError:
        second_tinh = None
        top_3_tinhs = None

    context={'tinh_data': tinh_data, 'tinhs':tinhs,'top_2_tinhs':top_2_tinhs,'top_3_tinhs':top_3_tinhs} 
    return render(request,'app/home.html',context)

def update_huyen_list(request):
    tinh_id = request.GET.get('tinh_id')
    search = request.GET.get('tinh', '')
    if tinh_id:
        huyen_list = list(Huyen.objects.filter(tinh_id=tinh_id).values('id', 'tenhuyen'))
    elif search:
        tinh = Tinh.objects.filter(tentinh__icontains=search).first()
        if tinh:
            huyen_list = list(Huyen.objects.filter(tinh=tinh).values('id', 'tenhuyen'))
        else:
            huyen_list = []
    else:
        huyen_list = []

    return JsonResponse({'huyen_list': huyen_list})


def search(request):
    search = request.GET.get('tinh', '')
    tinh_id = request.GET.get('tinh_id')
    tinh_name = request.GET.get('tinh_name')
    khachsan_list = KhachSan.objects.filter(active=True).annotate(min_giaphong=Min('phong__giaphong'))
    form = SearchForm(request.GET, tinh_id=tinh_id, search=search)
    if tinh_id:
        tentinh = Tinh.objects.filter(id=tinh_id).first()
        if tentinh:
            search = tentinh.tentinh
    else:
        tentinh = Tinh.objects.filter(tentinh__icontains=search).first() if search else None
    if search:
        khachsan_list = khachsan_list.filter(
            Q(tinh__tentinh__icontains=search) |
            Q(diachi__icontains=search)
        )
    if tinh_id:
        khachsan_list = khachsan_list.filter(tinh_id=tinh_id)
    elif tentinh:
        khachsan_list = khachsan_list.filter(tinh=tentinh)
    else:
        khachsan_list = khachsan_list.filter(diachi__icontains=search)

    if form.is_valid():
        tiennghi = form.cleaned_data.get('tiennghi')
        diem_danhgia = form.cleaned_data.get('diem_danhgia')
        khu_vuc = form.cleaned_data.get('khu_vuc')
        sap_xep = form.cleaned_data.get('sap_xep')
        gia_min = form.cleaned_data.get('gia_min')
        gia_max = form.cleaned_data.get('gia_max')
        if tiennghi:
            khachsan_list = khachsan_list.filter(phong__tiennghi__in=tiennghi).distinct()
        # if diem_danhgia:
        # #     khachsan_list = khachsan_list.filter(diem_trung_binh__gte=diem_danhgia)
        #     diem_danhgia_int = int(diem_danhgia[0])
        #     khachsan_list = khachsan_list.annotate(
        #         diem_trung_binh=Avg('phong__chitiethoadon__hoadon__danhgia__diem')
        #     ).filter(diem_trung_binh__gte=diem_danhgia_int)
        if diem_danhgia:
            khachsan_list = khachsan_list.annotate(
                avg_rating=Avg('phong__chitiethoadon__hoadon__danhgia__diem')
            )
            rating_filters = Q()
            for rating in diem_danhgia:
                rating_filters |= Q(avg_rating__gte=int(rating))
            khachsan_list = khachsan_list.filter(rating_filters).distinct()

        if khu_vuc:
            huyen_names = list(khu_vuc.values_list('tenhuyen', flat=True))
            huyen_query = Q()
            for huyen in huyen_names:
                huyen_query |= Q(diachi__icontains=huyen)
            khachsan_list = khachsan_list.filter(huyen_query)
        if gia_min is not None:
            khachsan_list = khachsan_list.filter(min_giaphong__gte=gia_min)
        if gia_max is not None:
            khachsan_list = khachsan_list.filter(min_giaphong__lte=gia_max)
        if sap_xep and sap_xep != 'none':
            if sap_xep == 'giathap':
                khachsan_list = khachsan_list.order_by('min_giaphong')
            elif sap_xep == 'giacao':
                khachsan_list = khachsan_list.order_by('-min_giaphong')
    num_hotels_found = khachsan_list.count()
    context = {
        'form': form,
        'khachsan_list': khachsan_list,
        'search': search,
        'tentinh': tentinh,
        'tinh_id': tinh_id,
        'tinh_name': tinh_name,
        'num_hotels_found': num_hotels_found,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'html': render_to_string('app/search_results.html', context, request=request)
        })

    return render(request, 'app/searchtest.html', context)
def ds(request): #view danh sách khách sạn theo tỉnh
    tinh_id = request.GET.get('tinh_id')
    tinh_name = request.GET.get('tinh_name')
   # Kiểm tra xem có tinh_id nào được truyền không
    if tinh_id is not None:
        khachsans = KhachSan.objects.filter(tinh_id=tinh_id, active=True)
    else:
        khachsans = KhachSan.objects.filter(active=True)
    context={'khachsans':khachsans, 'tinh_id':tinh_id,'tinh_name':tinh_name}
    return render(request,'app/listkhachsan.html',context)
def ks(request):
    khachsan_id = request.GET.get('khachsan_id')
    khachsan = KhachSan.objects.get(pk=khachsan_id)
    listanhks =AnhKhachSan.objects.filter(khachsan=khachsan)
    listdichvu = DichVu.objects.filter(khachsan=khachsan)
    khachsan_name = khachsan.tenkhachsan
    listphong = Phong.objects.filter(khachsan=khachsan, active=True)
    for phong in listphong:
         number_of_rooms = phong.soluong
         phong.range_soluong = range(phong.soluong+1)
    
    first_room = Phong.objects.first()
    price_per_room = first_room.giaphong if first_room else 0
    
    first_room = Phong.objects.first()
    price_per_room = first_room.giaphong
    tinh_name = khachsan.tinh.tentinh
    tinh_id = khachsan.tinh.id
    danhgias= Danhgia.objects.filter(hoadon__chitiethoadon__phong__khachsan__id=khachsan_id)
    diemtb_danhgia = khachsan.diem_trung_binh    
    tendiem_tb= khachsan.get_danh_gia_tb
    tong_danhgia=khachsan.sum_danh_gia
    context={'listdichvu':listdichvu,'tendiem_tb':tendiem_tb,'diemtb_danhgia':diemtb_danhgia,'tong_danhgia':tong_danhgia,'danhgias':danhgias,'range': range,'numberOfRoomsFromServer': number_of_rooms, 'pricePerRoomFromServer': price_per_room,'khachsan':khachsan,'khachsan_id':khachsan_id, 'khachsan_name':khachsan_name,'listanhks':listanhks,'listphong':listphong,'tinh_name':tinh_name,'tinh_id':tinh_id}
    return render(request, 'app/khachsan.html', context)
def dondatphong(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if 'huyphong' in request.POST:
                hoadon_id = request.POST.get('hoadon_id')
                
                phong_id = request.POST.get('phong_id')
                print(f"HoaDon ID: {hoadon_id}, Phong ID: {phong_id}")  # Log để kiểm tra giá trị nhận được

                try:
                    hoadon = HoaDon.objects.get(id=hoadon_id)
                    phong = Phong.objects.get(id=phong_id)
                    chitiethoadon = hoadon.chitiethoadon_set.get(phong_id=phong_id)

                    if chitiethoadon.ngay_gio_nhan > timezone.now() + timezone.timedelta(days=1):
                        hoadon.huy_don_hang()
                        phong.soluong += chitiethoadon.soluong_phong
                        phong.save()
                        messages.success(request, 'Đã hủy phòng thành công.')
                    else:
                        messages.error(request, 'Không thể hủy phòng trong vòng 1 ngày trước khi nhận phòng.')

                except HoaDon.DoesNotExist:
                    messages.error(request, 'Hóa đơn không tồn tại.')

                except ChiTietHoaDon.DoesNotExist:
                    messages.error(request, 'Chi tiết hóa đơn không tồn tại.')

                except ValidationError as e:
                    messages.error(request, str(e))

                return redirect('dondatphong')

            if 'danhgia' in request.POST:
                diem = request.POST.get("exampleRadios")
                binhluan = request.POST.get("binhluan")
                hoadon_id = request.POST.get("hoadon_id")
                hoadon = HoaDon.objects.get(id=hoadon_id)
                print("Hóa đơn ID:", hoadon_id)
                # Kiểm tra xem hóa đơn đã được đánh giá chưa
                if Danhgia.objects.filter(hoadon=hoadon).exists():
                    messages.error(request, 'Hóa đơn này đã được đánh giá trước đó.')
                else:
                    # Tạo đối tượng đánh giá mới và lưu vào cơ sở dữ liệu
                    Danhgia.objects.create(
                        hoadon=hoadon,
                        diem=diem,
                        binhluan=binhluan
                    )
                    messages.success(request, 'Đánh giá của bạn đã được lưu.')
                return redirect('dondatphong')

        customer = request.user
        hoadons = HoaDon.objects.filter(user=customer)
    else:
        hoadons = []

    context = {'hoadons': hoadons}
    return render(request, 'app/dondatphong.html', context)


@login_required
def datphong(request):
    if request.method == 'GET':
        slphong = request.GET.get("quantity")
        quantity_float = float(slphong)
        ngay_gio_nhan = request.GET.get("ngay_nhan")
        ngay_gio_tra = request.GET.get("ngay_tra")
        phong_id = request.GET.get("phong_id")
        phong = Phong.objects.get(id=phong_id)
        khuyenmai_list = phong.khuyenmai.all()
        ten_ks = phong.khachsan.tenkhachsan
        ten_tinh = phong.khachsan.tinh.tentinh
        tenphong = phong.tenphong
        giagoc = phong.giaphong_vnd
        if phong.khuyenmai.exists:
            
            giakm= phong.get_discounted_price()
            gia=giakm.replace(",", "")
            dongia=float(gia)
        else:
            dongia = phong.giaphong
        anh_phong = AnhPhong.objects.filter(phong=phong)
        ngay_gio_nhan_str = datetime.strptime(ngay_gio_nhan, "%Y-%m-%dT%H:%M")
        ngay_gio_tra_str = datetime.strptime(ngay_gio_tra, "%Y-%m-%dT%H:%M")
        so_dem = (ngay_gio_tra_str - ngay_gio_nhan_str).days
        total = so_dem * dongia * quantity_float
        formatted_total = "{:,.0f}".format(total) 
        diemtb_danhgia = phong.khachsan.diem_trung_binh    
        tendiem_tb= phong.khachsan.get_danh_gia_tb
        tong_danhgia=phong.khachsan.sum_danh_gia
        context = {
            'formatted_total':formatted_total,
            'giagoc':giagoc,
            'khuyenmai_list':khuyenmai_list,
            'phong_id': phong_id,
            'ten_tinh': ten_tinh,
            'ngay_gio_nhan': ngay_gio_nhan,
            'ngay_gio_tra': ngay_gio_tra,
            'ten_ks': ten_ks,
            'anh_phong': anh_phong,
            'slphong': slphong,
            'so_dem': so_dem,
            'total': total,
            'tenphong': tenphong,
            'dongia': dongia,
            'diemtb_danhgia':diemtb_danhgia,
            'tendiem_tb':tendiem_tb,
            'tong_danhgia':tong_danhgia
        }
        return render(request, 'app/datphong.html', context)
    
    elif request.method == 'POST':
        ngay_nhan = request.POST.get("ngay_nhan")
        ngay_tra = request.POST.get("ngay_tra")
        so_luong_dem = request.POST.get("so_luong_dem")
        phong_id = request.POST.get("phong_id")
        payment_method = request.POST.get("payment_method")
        sldem = float(so_luong_dem)
        slphong = request.POST.get("slphong")
        # Kiểm tra xem giá trị từ phiên đã tồn tại hay chưa
        phong = Phong.objects.get(id=phong_id)
        don_gia = phong.giaphong
        quantity_float = float(slphong)
        total = sldem * don_gia * quantity_float
        customer = request.user
        payment_status = True if payment_method == 'bank' else False
        if slphong:
            slphong = int(slphong)
        
        if slphong is not None:
            phong = Phong.objects.get(id=phong_id)
            don_gia = phong.giaphong
            customer = request.user
            
            if phong.soluong >= slphong:
                phong.soluong -= slphong
                if phong.soluong > 0:
                    phong.active = True
                elif phong.soluong == 0:
                    phong.active = False
                phong.save()
                
                hoadon = HoaDon.objects.create(user=customer,payment_method=payment_method, payment_status=payment_status)
                chitiethoadon = ChiTietHoaDon.objects.create(phong=phong,hoadon=hoadon,ngay_gio_nhan=ngay_nhan,ngay_gio_tra=ngay_tra,soluong_dem=so_luong_dem,soluong_phong=slphong,dongia=don_gia,tongtien=total)
                
        return redirect('dondatphong')
    
    return render(request, 'app/datphong.html')

def index(request):
    # Xác định ngày hiện tại
    today = datetime.now()

    # Tìm ngày thứ 2 gần nhất
    monday = today - timedelta(days=today.weekday())

    # Xác định ngày chủ nhật trong tuần
    sunday = monday + timedelta(days=6)

    # Kiểm tra nếu hôm nay là chủ nhật và nếu vậy, giảm đi 1 tuần
    if today.weekday() == 6:
        monday -= timedelta(days=7)
        sunday -= timedelta(days=7)

    group_name = 'khachhang'
    group = Group.objects.get(name=group_name)  # Lấy đối tượng nhóm từ tên
    users_count = User.objects.filter(
    Q(groups=group),
    Q(date_joined__gte=monday),
    Q(date_joined__lte=sunday)
    ).count()
    # ... (Các bước trước để tính số lượng người dùng trong tuần hiện tại)

    # Tính số lượng người dùng trong tuần trước
    last_monday = monday - timedelta(days=7)
    last_sunday = sunday - timedelta(days=7)

    last_week_users_count = User.objects.filter(
        Q(groups=group),
        Q(date_joined__gte=last_monday),
        Q(date_joined__lte=last_sunday)
    ).count()
    if last_week_users_count == 0:
    # Tránh chia cho 0
        percentage_change = 0
    else:
        percentage_change = ((users_count - last_week_users_count) / last_week_users_count) * 100
     # Lấy năm hiện tại
    current_year = datetime.now().year

    # Xác định quý hiện tại
    current_quarter = (datetime.now().month - 1) // 3 + 1
    # Lấy số lượng khách sạn hiện tại từ quý trước
    khach_san_hien_tai = KhachSan.objects.filter(
        ngay_them__year=current_year,
        ngay_them__quarter=current_quarter
    ).count()
    tinh_data = []
    tinh_list = Tinh.objects.all()
    for tinh in tinh_list:
        khachsan_count = KhachSan.objects.filter(tinh=tinh).count()
        phong_count = Phong.objects.filter(khachsan__tinh=tinh).count()
        tinh_data.append({
            'ten_tinh': tinh.tentinh,
            'so_luong_khach_san': khachsan_count,
            'tong_so_phong': phong_count
        })

    context = {'users_count':users_count,'percentage_change':percentage_change,'khach_san_hien_tai':khach_san_hien_tai, 'tinh_data': tinh_data}
    return render(request, 'admin/index.html', context)

def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        
        # Lấy các giá trị từ POST request
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')

        # Chỉ cập nhật thông tin nếu có sự thay đổi
        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        if new_first_name:
            user.first_name = new_first_name
        if new_last_name:
            user.last_name = new_last_name

        # Xử lý tải lên hình ảnh mới
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            # Lưu hình ảnh vào hệ thống lưu trữ (ví dụ: media/uploads/)
            user.avatar = 'uploads/' + avatar.name
            default_storage.save(user.avatar, ContentFile(avatar.read()))

        user.save()
        return redirect('edit_profile')
    context ={'user':request.user}
    return render(request, 'pages/profile.html', context)
def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        danhgia_list = Danhgia.objects.filter(user=user)       
        hoadons= HoaDon.objects.filter(user=user)
        danhgia_hoadon = None
        if request.method == 'POST':
            diem = request.POST.get("exampleRadios")
            binhluan = request.POST.get("binhluan")
            phong_id = request.POST.get("phong_id")  # Lấy phong_id từ biểu mẫu đánh giá
            hoadon = HoaDon.objects.get(chitiethoadon__phong_id=phong_id, user=user)  # Lấy hóa đơn dựa trên phong_id
            danhgia_hoadon = Danhgia.objects.filter(user=user, phong=hoadon.chitiethoadon_set.get(phong_id=phong_id).phong)
            if not danhgia_hoadon:
                danhgia = Danhgia.objects.create(user=user, phong=hoadon.chitiethoadon_set.get(phong_id=phong_id).phong, diem=diem, binhluan=binhluan)
            else:
                pass
            return redirect('customer_dashboard')  # Chuyển hướng trở lại trang danh sách hóa đơn sau khi đánh giá
    else:
        hoadon =[]
    context = {
        'hoadons': hoadons,
        'danhgia_hoadon': danhgia_hoadon,
        'danhgia_list':danhgia_list,
    }
    
    return render(request, 'pages/dashboard.html', context)


import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import random
import requests
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
# from django.utils.http import urlquote
from urllib.parse import quote
from app.models import PaymentForm
from app.vnpay import vnpay


def index_payment(request):
    return render(request, "payment/index.html", {"title": "Danh sách demo"})


def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()

@login_required
def payment(request):
    if request.method == 'POST':
        # Process input data and build url payment
        form = PaymentForm(request.POST)
        if form.is_valid():
            order_type = form.cleaned_data['order_type']
            order_id = form.cleaned_data['order_id']
            amount = form.cleaned_data['amount']
            order_desc = form.cleaned_data['order_desc']
            bank_code = form.cleaned_data['bank_code']
            language = form.cleaned_data['language']
            ipaddr = get_client_ip(request)
            # Build URL Payment
            vnp = vnpay()
            vnp.requestData['vnp_Version'] = '2.1.0'
            vnp.requestData['vnp_Command'] = 'pay'
            vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
            vnp.requestData['vnp_Amount'] = amount * 100
            vnp.requestData['vnp_CurrCode'] = 'VND'
            vnp.requestData['vnp_TxnRef'] = order_id
            vnp.requestData['vnp_OrderInfo'] = order_desc
            vnp.requestData['vnp_OrderType'] = order_type
            # Check language, default: vn
            if language and language != '':
                vnp.requestData['vnp_Locale'] = language
            else:
                vnp.requestData['vnp_Locale'] = 'vn'
                # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
            if bank_code and bank_code != "":
                vnp.requestData['vnp_BankCode'] = bank_code

            vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
            vnp.requestData['vnp_IpAddr'] = ipaddr
            vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
            vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
            print(vnpay_payment_url)
            return redirect(vnpay_payment_url)
        else:
            print("Form input not validate")
    else:
        return render(request, "payment/payment.html", {"title": "Thanh toán"})


def payment_ipn(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = inputData['vnp_Amount']
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            # Check & Update Order Status in your Database
            # Your code here
            firstTimeUpdate = True
            totalamount = True
            if totalamount:
                if firstTimeUpdate:
                    if vnp_ResponseCode == '00':
                        print('Payment Success. Your code implement here')
                    else:
                        print('Payment Error. Your code implement here')

                    # Return VNPAY: Merchant update success
                    result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
                else:
                    # Already Update
                    result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})
            else:
                # invalid amount
                result = JsonResponse({'RspCode': '04', 'Message': 'invalid amount'})
        else:
            # Invalid Signature
            result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
    else:
        result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

    return result


def payment_return(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']

        # Lấy giá trị từ cookie
        # totalPrice = request.COOKIES.get('totalPrice')
        user = request.COOKIES.get('user')
        cutomer= User.objects.get(username=user)
        phong_id = request.COOKIES.get('phong_id')
        ngay_gio_nhan = request.COOKIES.get('ngay_gio_nhan')
        ngay_gio_tra = request.COOKIES.get('ngay_gio_tra')
        soluong_dem = request.COOKIES.get('soluong_dem')
        soluong_phong = request.COOKIES.get('soluong_phong')
        payment_method = request.COOKIES.get('payment_method')
        giaphong = request.COOKIES.get('giaphong')


        # cutomer = request.user
        payment = Payment_VNPay.objects.create(
            order_id = order_id,
            amount = amount,
            order_desc = order_desc,
            vnp_TransactionNo = vnp_TransactionNo,
            vnp_ResponseCode = vnp_ResponseCode
        )
        if soluong_phong:
                soluong_phong = int(soluong_phong)
        if soluong_phong is not None:
            phong = Phong.objects.get(id=phong_id)
            
            if phong.soluong >= soluong_phong:
                phong.soluong -= soluong_phong
                if phong.soluong > 0:
                    phong.active = True
                elif phong.soluong == 0:
                    phong.active = False
                phong.save()
                # Tạo đơn đặt phòng 
                payment_status = True if payment_method == 'bank' else False
                hoa_don = HoaDon.objects.create(
                    id=payment.order_id,
                    user=cutomer,
                    payment_method=payment_method, 
                    payment_status=payment_status# Giả sử user là một ID, cập nhật nếu cần thi
                    # thanhtoan= payment.id
                )

                # Tạo đối tượng ChiTietHoaDon
                chi_tiet_hoa_don = ChiTietHoaDon.objects.create(
                    hoadon=hoa_don,
                    phong_id=phong_id,
                    ngay_gio_nhan =ngay_gio_nhan ,
                    ngay_gio_tra =ngay_gio_tra,
                    soluong_dem=soluong_dem,
                    soluong_phong=soluong_phong,
                    tongtien=amount,
                    dongia = giaphong,
                )

        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                return render(request, "payment/payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Thành công", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
            else:
                return render(request, "payment/payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Lỗi", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
        else:
            return render(request, "payment/payment_return.html",
                          {"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
                           "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
                           "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum"})
    else:
        return render(request, "payment/payment_return.html", {"title": "Kết quả thanh toán", "result": ""})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

n = random.randint(10**11, 10**12 - 1)
n_str = str(n)
while len(n_str) < 12:
    n_str = '0' + n_str


def query(request):
    if request.method == 'GET':
        return render(request, "payment/query.html", {"title": "Kiểm tra kết quả giao dịch"})

    url = settings.VNPAY_API_URL
    secret_key = settings.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_Version = '2.1.0'

    vnp_RequestId = n_str
    vnp_Command = 'querydr'
    vnp_TxnRef = request.POST['order_id']
    vnp_OrderInfo = 'kiem tra gd'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_IpAddr = get_client_ip(request)

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode,
        vnp_TxnRef, vnp_TransactionDate, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render(request, "payment/query.html", {"title": "Kiểm tra kết quả giao dịch", "response_json": response_json})

def refund(request):
    if request.method == 'GET':
        return render(request, "payment/refund.html", {"title": "Hoàn tiền giao dịch"})

    url = settings.VNPAY_API_URL
    secret_key = settings.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_RequestId = n_str
    vnp_Version = '2.1.0'
    vnp_Command = 'refund'
    vnp_TransactionType = request.POST['TransactionType']
    vnp_TxnRef = request.POST['order_id']
    vnp_Amount = request.POST['amount']
    vnp_OrderInfo = request.POST['order_desc']
    vnp_TransactionNo = '0'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_CreateBy = 'user01'
    vnp_IpAddr = get_client_ip(request)

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode, vnp_TransactionType, vnp_TxnRef,
        vnp_Amount, vnp_TransactionNo, vnp_TransactionDate, vnp_CreateBy, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_Amount": vnp_Amount,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_TransactionType": vnp_TransactionType,
        "vnp_TransactionNo": vnp_TransactionNo,
        "vnp_CreateBy": vnp_CreateBy,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render(request, "payment/refund.html", {"title": "Kết quả hoàn tiền giao dịch", "response_json": response_json})


from django.db.models import Count, Avg, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def user_role_stats_view(request):
    role_stats = User.objects.values('role').annotate(count=Count('id'))
    context = {'role_stats': role_stats}
    return render(request, 'admin/user_role_stats.html', context)
@staff_member_required
def hotel_by_tinh_view(request):
    hotel_stats = KhachSan.objects.values('tinh__tentinh').annotate(count=Count('id'))
    context = {'hotel_stats': hotel_stats}
    return render(request, 'admin/hotel_by_tinh.html', context)
@staff_member_required
def room_by_hotel_view(request):
    room_stats = Phong.objects.values('khachsan__tenkhachsan').annotate(count=Count('id'))
    context = {'room_stats': room_stats}
    return render(request, 'admin/room_by_hotel.html', context)
@staff_member_required
def invoice_by_month_view(request):
    invoice_stats = HoaDon.objects.annotate(month=TruncMonth('created_date')).values('month').annotate(count=Count('id'))
    context = {'invoice_stats': invoice_stats}
    return render(request, 'admin/invoice_by_month.html', context)
@staff_member_required
def revenue_by_month_view(request):
    revenue_stats = ChiTietHoaDon.objects.annotate(month=TruncMonth('created_date')).values('month').annotate(revenue=Sum('dongia'))
    context = {'revenue_stats': revenue_stats}
    return render(request, 'admin/revenue_by_month.html', context)
@staff_member_required
def hotel_rating_view(request):
    rating_stats = Danhgia.objects.values('hoadon__khachsan__tenkhachsan').annotate(avg_rating=Avg('diem'))
    context = {'rating_stats': rating_stats}
    return render(request, 'admin/hotel_rating.html', context)
@staff_member_required
def current_promotions_view(request):
    current_date = timezone.now()
    promotions = KhuyenMai.objects.filter(thoigian_bd__lte=current_date, thoigian_kt__gte=current_date)
    context = {'promotions': promotions}
    return render(request, 'admin/current_promotions.html', context)
@staff_member_required
def admin_view(request):
    role = request.user.role
    return render(request, 'admin/custom_admin.html', {'role': role})