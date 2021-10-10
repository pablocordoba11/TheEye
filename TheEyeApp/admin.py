from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class UserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'get_token', 'email', 'get_groups')
    search_fields = ('first_name', 'last_name', 'username')
    list_filter = ('groups', 'is_active')
    fieldsets_top = (
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    )
    normaluser_fieldsets = (
        (('Permissions'), {'fields': ('is_active', 'is_staff',
                                      'groups')}),
    )
    superuser_fieldsets = (
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
    )
    admin_fieldsets = (
        (('Permissions'), {'fields': ('is_active', 'is_staff',
                                      'groups')}),
    )
    fieldsets_bottom = (
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def get_groups(self, obj):
        if obj.groups is not None:
            groups_output = []
            groups = obj.groups.all()
            for p in groups:
                groups_output.append(p.name)
            return ", ".join(groups_output)
        else:
            return ""

    get_groups.short_description = 'Groups'
    get_groups.admin_order_field = 'groups'


    def get_token(self, obj):
        if hasattr(obj, 'UserExtension') and obj.UserExtension.token is not None:
            return obj.UserExtension.token
        else:
            return  ""

    get_token.short_description = 'Token'
    get_token.admin_order_field = 'Token'

class ApplicationAdministration(admin.ModelAdmin):
    list_display = ('name', 'url', 'description', 'type')
    search_fields = ('name',)

class EventTypeAdministration(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class EventTypeInline(admin.TabularInline):
    model = EventType

class EventAdministration(admin.ModelAdmin):
    list_display = ('name', 'get_type', 'data')
    search_fields = ('name',)

    def get_type(self, obj):
        if hasattr(obj, 'type') and obj.type.name is not None:
            return obj.type.name
        else:
            return  ""

    get_type.short_description = 'Type'
    get_type.admin_order_field = 'Type'

# Register your models here.

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Application, ApplicationAdministration)
admin.site.register(EventType, EventTypeAdministration)
admin.site.register(Event, EventAdministration)


