# Generated by Django 5.0.6 on 2024-06-24 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_payment_vnpay_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoadon',
            name='trangthai',
            field=models.CharField(choices=[('CTT', 'Chưa thanh toán'), ('DNP', 'Đã nhận phòng'), ('DH', 'Đã hủy')], default='CTT', max_length=3),
        ),
    ]