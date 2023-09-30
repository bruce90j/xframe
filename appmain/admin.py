from django.contrib import admin

from appmain.models import NFT


# Register your models here.
@admin.register(NFT)
class NFTAdmin(admin.ModelAdmin):
    list_display = ['xid', 'name', 'description']