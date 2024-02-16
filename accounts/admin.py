from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):

	list_display = ('email', 'is_staff')
	list_filter = ('is_staff',)
	readonly_fields = ('last_login',)

	fieldsets = (
		('Main', {'fields':('email', 'name', 'password')}),
		('Permissions', {'fields':('is_active', 'is_staff', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
	)

	search_fields = ('email', 'name')
	ordering = ('name',)
	filter_horizontal = ('groups', 'user_permissions')
	
	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		is_superuser = request.user.is_superuser
		if not is_superuser:
			form.base_fields['is_superuser'].disabled = True
		return form

admin.site.register(User, UserAdmin)
