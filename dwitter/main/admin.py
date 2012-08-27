# -*- coding: utf-8 -*- 
from django.contrib import admin
from dwitter.main.models import *

class MemberAdmin(admin.ModelAdmin):
    list_display = ('user','nick')

class DwitAdmin(admin.ModelAdmin):
     list_display = ('content','member','stamp')

class DPFAdmin(admin.ModelAdmin):
    pass
admin.site.register(DPF, DPFAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Dwit, DwitAdmin)

