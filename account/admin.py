from django.contrib import admin
from account.models import User
from account.forms import CustomUserForm
from django.contrib.auth.admin import UserAdmin



#Then add the feilds to the form
class CustomUserAdminPage(UserAdmin):
    model = User
    add_from = CustomUserForm
    list_display = ('username','email','birth_date','last_name','is_staff','date_joined','account_id')
    filter_horizontal =('game',)

    fieldsets = (
        *UserAdmin.fieldsets, #Add all previous default inputs from base model
        (
            'Birth Date',{'fields':('birth_date',)}
        ),
        (
            'Profile Picture',{'fields':('avatar',)}
        ),
        (
            'Games',{'fields':('game',)}
        ),
        (
            'Storage',{'fields':('current_storage','total_storage',)}
        ),
        (
            'Syncing Variables',{'fields':('play_flag','sync_flag','sync_done_flag','updated',)}
        ),
    )


admin.site.register(User,CustomUserAdminPage)