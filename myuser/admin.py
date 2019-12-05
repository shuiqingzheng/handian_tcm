from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import MyUser


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("密码"),
                                         help_text=(
        '忘记密码 --> <a href={} '
        'style="padding: 5px;font-size: 14px;color:white;background: #84adc6;"'
        '>修改密码</a>'.format('../password/')
    ),)

    class Meta:
        model = MyUser
        fields = ('email', 'username', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    form = UserChangeForm

    list_display = ('id', 'email', 'username')
    ordering = ('-pk',)
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('信息', {'fields': ('username', )}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')}),
        ('日期', {'fields': ('last_login', )}),
    )


admin.site.site_header = '中医知识系统'
admin.site.site_title = '中医知识系统'
