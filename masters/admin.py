from django.contrib import admin
from django.utils.html import mark_safe
from .models import Site, Area, Location

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'active')

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'site')
    list_filter = ('site',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    # 🌟 Notice I removed 'site' and replaced it with 'get_site'
    list_display = ('name', 'area', 'get_site', 'floor', 'qr_enabled', 'qr_preview')
    
    # 🌟 Removed 'site' from the filter since it belongs to Area now
    list_filter = ('area', 'qr_enabled') 
    search_fields = ('name', 'qr_token')
    readonly_fields = ('qr_preview',)

    # 🌟 This custom helper fetches the site name through the Area!
    def get_site(self, obj):
        if obj.area and obj.area.site:
            return obj.area.site.name
        return "-"
    get_site.short_description = 'Building'

    # The magic thumbnail preview
    def qr_preview(self, obj):
        if obj.qr_image:
            return mark_safe(f'<a href="{obj.qr_image.url}" target="_blank"><img src="{obj.qr_image.url}" width="50" height="50" style="border-radius: 5px;"/></a>')
        return "-"
    qr_preview.short_description = 'QR Code'