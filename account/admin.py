from django.contrib import admin
from account.models import User
from account.forms import CustomUserForm
from django.contrib.auth.admin import UserAdmin



#Then add the feilds to the form
class CustomUserAdminPage(UserAdmin):
    model = User
    add_from = CustomUserForm
    list_display = ('username','email','birth_date','last_name','is_staff','date_joined','account_id')


    fieldsets = (
        *UserAdmin.fieldsets, #Add all previous default inputs from base model
        (
            'Birth Date',{'fields':('birth_date',)}
        ),
        (
            'Profile Picture',{'fields':('avatar',)}
        ),
        (
            'Add Games',{'fields':('add_games',)}
        ),
        (
            'Added Games',{'fields':('added_games',)}
        ),
        (
            'Remove Games',{'fields':('remove_games',)}
        ),
    )


admin.site.register(User,CustomUserAdminPage)