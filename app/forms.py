from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Huyen, KhachSan, TienNghi, User, Tinh

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

# class SearchForm(forms.Form):
#     # tinh = forms.ModelChoiceField(
#     #     queryset=Tinh.objects.all(), 
#     #     required=False, label='Tỉnh',
#     #     widget=forms.Select(attrs={'id': 'id_tinh', 'onchange': 'updateHuyenList()'})
#     # )
#     # tenkhachsan = forms.CharField(max_length=200, required=False, label='Tên khách sạn')
#     # diachi = forms.CharField(max_length=200, required=False, label='Địa chỉ')
#     # sao_khachsan = forms.MultipleChoiceField(
#     #     choices=[(i, f'{i} sao') for i in range(1, 6)],
#     #     required=False,
#     #     widget=forms.CheckboxSelectMultiple,
#     #     label='Sao khách sạn'
#     # )
#     tiennghi = forms.ModelMultipleChoiceField(
#         queryset=TienNghi.objects.all(),
#         required=False,
#         widget=forms.CheckboxSelectMultiple,
#         label='Tiện nghi'
#     )
#     diem_danhgia = forms.ChoiceField(
#         choices=[('9', 'Tuyệt hảo: 9 điểm trở lên'), ('8', 'Rất tốt: 8 điểm trở lên'), ('7', 'Tốt: 7 điểm trở lên'), ('6', 'Dễ chịu: 6 điểm trở lên')],
#         required=False,
#         widget=forms.CheckboxSelectMultiple,
#         label='Điểm đánh giá của khách'
#     )
#     khu_vuc = forms.ModelMultipleChoiceField(
#         queryset=Huyen.objects.none(),
#         required=False,
#         widget=forms.CheckboxSelectMultiple,
#         label='Khu vực'
#     )

#     def __init__(self, *args, **kwargs):
#         tinh_id = kwargs.pop('tinh_id', None)
#         super(SearchForm, self).__init__(*args, **kwargs)
#         if tinh_id:
#             self.fields['khu_vuc'].queryset = Huyen.objects.filter(tinh_id=tinh_id)
    # khu_vuc = forms.ModelMultipleChoiceField(
    #     # choices=[('Quan 1', 'Quận 1'), ('Quan 4', 'Quận 4'), ('Quan 7', 'Quận 7')],
    #     queryset = Huyen.objects.all(),
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     label='Khu vực'
    # )
    # khachsan_addresses = KhachSan.objects.values_list('diachi', flat=True).distinct()
    # HUYEN_CHOICES = list(set((address.split(", ")[-2], address.split(", ")[-2]) for address in khachsan_addresses))
    # khu_vuc = forms.MultipleChoiceField(required=False, choices=HUYEN_CHOICES, widget=forms.CheckboxSelectMultiple, label='Khu vực')
class SearchForm(forms.Form):
    tiennghi = forms.ModelMultipleChoiceField(
        queryset=TienNghi.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Tiện nghi'
    )
    diem_danhgia = forms.MultipleChoiceField(
        choices=[('9', 'Tuyệt hảo: 9 điểm trở lên'), ('8', 'Rất tốt: 8 điểm trở lên'), ('7', 'Tốt: 7 điểm trở lên'), ('6', 'Dễ chịu: 6 điểm trở lên')],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Điểm đánh giá của khách'
    )
    tinh = forms.CharField(max_length=200, required=False, widget=forms.HiddenInput())
    tinh_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    tinh_name = forms.CharField(max_length=200, required=False, widget=forms.HiddenInput())
    search = forms.CharField(max_length=200, required=False, widget=forms.HiddenInput())
    khu_vuc = forms.ModelMultipleChoiceField(
        queryset=Huyen.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Khu vực'
    )

    def __init__(self, *args, **kwargs):
        tinh_id = kwargs.pop('tinh_id', None)
        search = kwargs.pop('search', None)  # Lấy giá trị search từ dữ liệu form
        super(SearchForm, self).__init__(*args, **kwargs)
        
        if tinh_id:
            self.fields['khu_vuc'].queryset = Huyen.objects.filter(tinh_id=tinh_id)
        elif search:
            tinh = Tinh.objects.filter(tentinh__icontains=search).first()
            if tinh:
                self.fields['khu_vuc'].queryset = Huyen.objects.filter(tinh=tinh)
    sap_xep = forms.ChoiceField(choices=[('none', 'Không sắp xếp'), ('giathap', 'Giá thấp đến cao'), ('giacao', 'Giá cao đến thấp')], required=False)
    gia_min = forms.IntegerField(
        required=False, 
        widget=forms.TextInput(attrs={'oninput': "this.value = this.value.replace(/[^0-9]/g, '').replace(/^0+/, '');", 'placeholder': 'Giá tối thiểu'})
    )
    gia_max = forms.IntegerField(
        required=False, 
        widget=forms.TextInput(attrs={'oninput': "this.value = this.value.replace(/[^0-9]/g, '').replace(/^0+/, '');", 'placeholder': 'Giá tối đa'})
    )