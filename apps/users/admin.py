from django.contrib import admin

from apps.users.models import User, UserVerification, Role


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'created_time')
    search_fields = ('username', 'email', 'phone')
    readonly_fields = ('password', 'created_time', 'updated_time')


@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'time_limit', 'is_confirmed')
    search_fields = ('user_username',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
