from django.contrib import admin
from .models import Profile, FriendRequest
from .forms import ProfileAdminForm
from django.contrib.auth.models import User

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = ('user',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'friends':
            kwargs['queryset'] = User.objects.exclude(pk=request.user.pk)  # Exclude current user
        return super().formfield_for_manytomany(db_field, request, **kwargs)


    def change_view(self, request, object_id, form_url='', extra_context=None):
        profile = self.get_object(request, object_id)
        if profile:
            if not profile.friends.exists():
                self.message_user(request, f"{profile.user.username} has no friends yet.", level='info')
        return super().change_view(request, object_id, form_url, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

admin.site.register(Profile, ProfileAdmin)

admin.site.register(FriendRequest)
