# Generated by Django 4.2.6 on 2024-06-21 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_payment_vnpay_hoadon_thanh_toan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment_vnpay',
            name='order_id',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]