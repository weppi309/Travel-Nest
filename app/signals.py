from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import User
from django.db.models.signals import post_save
@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # Admin group
    admin_group, created = Group.objects.get_or_create(name='Admin')
    if created:
        permissions = Permission.objects.all()
        admin_group.permissions.set(permissions)
        admin_group.save()

    # Provider group
    provider_group, created = Group.objects.get_or_create(name='Provider')
    if created:
        # Add specific permissions for providers
        provider_permissions = Permission.objects.filter(
            content_type__app_label='app', 
            content_type__model__in=['khachsan', 'phong', 'dichvu', 'anhphong', 'anhkhachsan', 'tiennghi', 'hoadon', 'chitiethoadon']  
        )
        provider_group.permissions.set(provider_permissions)
        provider_group.save()

    # User group
    user_group, created = Group.objects.get_or_create(name='User')
    if created:
        # Add specific permissions for users
        user_permissions = Permission.objects.filter(
            content_type__app_label='app', 
            content_type__model__in=['hoadon', 'chitiethoadon', 'danhgia', 'anhphong', 'anhkhachsan']
        )
        user_group.permissions.set(user_permissions)
        user_group.save()

@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'admin':
            group, created = Group.objects.get_or_create(name='Admin')
        elif instance.role == 'provider':
            group, created = Group.objects.get_or_create(name='Provider')
        elif instance.role == 'user':
            group, created = Group.objects.get_or_create(name='User')
        instance.groups.add(group)

