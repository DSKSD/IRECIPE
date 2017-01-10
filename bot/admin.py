from django.contrib import admin
from .models import Recipe,RecomLog, Userinfo, Dialog
# Register your models here.

class RecomlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe', 'aprob', 'actual']

class DialogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'sent']

admin.site.register(Recipe)
admin.site.register(Userinfo)
admin.site.register(RecomLog, RecomlogAdmin)
admin.site.register(Dialog, DialogAdmin)
