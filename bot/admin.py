from django.contrib import admin
from .models import Recipe,RecomLog, Userinfo
# Register your models here.

class RecomlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe', 'aprob', 'actual']


admin.site.register(Recipe)
admin.site.register(Userinfo)
admin.site.register(RecomLog, RecomlogAdmin)
