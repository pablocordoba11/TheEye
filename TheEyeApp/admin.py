from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session as SessionDjango
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
    readonly_fields=('app_secret',)

class EventTypeAdministration(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class EventTypeInline(admin.TabularInline):
    model = EventType

class EventAdministration(admin.ModelAdmin):
    list_display = ('name', 'get_type', 'get_application', 'get_session', 'data', 'get_time_stamp')
    search_fields = ('name',)

    def get_type(self, obj):
        if hasattr(obj, 'type') and obj.type.name is not None:
            return obj.type.name
        else:
            return  ""

    get_type.short_description = 'Type'
    get_type.admin_order_field = 'Type'

    def get_application(self, obj):
        if hasattr(obj, 'application') and obj.application is not None:
            return obj.application.name
        else:
            return  ""

    get_application.short_description = 'Application'
    get_application.admin_order_field = 'Application'

    def get_session(self, obj):
        if hasattr(obj, 'session_django') and obj.session_django is not None:
            return obj.session_django.session_key
        else:
            return  ""

    get_session.short_description = 'Session'
    get_session.admin_order_field = 'Session'

    def get_time_stamp(self, obj):
        if hasattr(obj, 'timestampbase_ptr') and obj.timestampbase_ptr is not None:
            return obj.timestampbase_ptr.created_at
        else:
            return  ""

    get_time_stamp.short_description = 'Created at'
    get_time_stamp.admin_order_field = 'Created at'

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

# Register your models here.

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Application, ApplicationAdministration)
admin.site.register(EventType, EventTypeAdministration)
admin.site.register(Event, EventAdministration)
admin.site.register(SessionDjango, SessionAdmin)


