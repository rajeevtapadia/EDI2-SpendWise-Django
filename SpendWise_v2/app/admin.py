from django.contrib import admin
from django.contrib.auth.models import Group, User
from . models import Profile, Expense
# from .models import Expense

# Register your models here.

# unregister groups
admin.site.unregister(Group)

# mix profile info into user info
class ProfileInline(admin.StackedInline):
    model = Profile
    
class ExpensesInline(admin.StackedInline):
    model = Expense

# extend user model
class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline, ExpensesInline]

# admin.site.register(Expense)

# unregister and register user again
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



# register profile
# admin.site.register(Profile)

