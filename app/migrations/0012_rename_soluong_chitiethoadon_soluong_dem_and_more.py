# Generated by Django 5.0.6 on 2024-07-04 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_tiennghi_loai_tiennghi_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chitiethoadon',
            old_name='soluong',
            new_name='soluong_dem',
        ),
        migrations.RemoveField(
            model_name='khuyenmai',
            name='phong',
        ),
        migrations.AddField(
            model_name='chitiethoadon',
            name='soluong_phong',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chitiethoadon',
            name='tongtien',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hoadon',
            name='payment_method',
            field=models.CharField(choices=[('bank', 'Bank'), ('on_arrival', 'On Arrival')], default='on_arrival', max_length=50),
        ),
        migrations.AddField(
            model_name='hoadon',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='phong',
            name='khuyenmai',
            field=models.ManyToManyField(blank=True, to='app.khuyenmai'),
        ),
    ]
