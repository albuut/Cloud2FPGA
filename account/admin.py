from django.contrib import admin
from account.models import User, Games
from account.forms import CustomUserForm
from django.contrib.auth.admin import UserAdmin



#Then add the feilds to the form
class CustomUserAdminPage(UserAdmin):
    model = User
    add_from = CustomUserForm
    list_display = ('username','email','birth_date','first_name','last_name','is_staff','date_joined')


    fieldsets = (
        *UserAdmin.fieldsets, #Add all previous default inputs from base model
        (
            'Birth Date',{'fields':('birth_date',)}
        ),
        (
            'Profile Picture',{'fields':('avatar',)}
        ),
    )


admin.site.register(User,CustomUserAdminPage)
admin.site.register(Games)