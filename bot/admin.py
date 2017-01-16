from django.contrib import admin
from .models import Recipe,RecomLog, Userinfo, Dialog
# Register your models here.

class RecomlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe', 'aprob', 'actual']

class DialogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'sent', 'get_recipe', 'get_actual']
    
    def get_recipe(self, obj):
        try:
            return obj.recom.recipe.name
        except:
            return "-"
    get_recipe.short_description = 'Recipe'
    get_recipe.admin_order_field = 'get_recipe'
    
    def get_actual(self, obj):
        try:
            return obj.recom.actual
        except:
            return "-"
    get_actual.short_description = 'Actual'
    get_actual.admin_order_field = 'get_actual'
    
admin.site.register(Recipe)
admin.site.register(Userinfo)
admin.site.register(RecomLog, RecomlogAdmin)
admin.site.register(Dialog, DialogAdmin)
