# Generated by Django 4.2.6 on 2024-07-04 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_chitiethoadon_tongtien'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='khuyenmai',
            name='phong',
        ),
        migrations.AddField(
            model_name='phong',
            name='khuyenmai',
            field=models.ManyToManyField(blank=True, to='app.khuyenmai'),
        ),
    ]
