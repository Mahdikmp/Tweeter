from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, Tweet, Comment


# Do not show groups in admin panel
admin.site.unregister(Group)
admin.site.unregister(User)


# Define a model we want to be inilined
class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = True


# Meka the defined model to be inlined in user model
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInLine]


    def delete_model(self, request, obj):
        if hasattr(obj, 'profile'):
            obj.profile.delete()


    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if hasattr(obj, 'profile'):
                obj.profile.delete()



# To show tweets more clean
admin.site.register(Tweet)
admin.site.register(Comment)