from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'password',
        'is_staff',
        'is_superuser',
        'bio',
        'role'
    )
    list_display_links = ('username',)
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
