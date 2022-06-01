from django.contrib import admin
from .models import *

class AdminSuit(admin.ModelAdmin):
    list_display = ('link', 'dress', 'color', 'fabric', 'design', 'photo')
    ordering = ['dress']
    # search_fields = ['dress__name']

class PerfumeAdmin(admin.ModelAdmin):
    list_display = ('link', 'perfume_type', 'scent', 'photo')

class HighlighterAdmin(admin.ModelAdmin):
    list_display = ('link', 'highlighter_type', 'photo')

class ShoeAdmin(admin.ModelAdmin):
    list_display = ('link', 'shoe_type', 'color', 'photo')

class BagAdmin(admin.ModelAdmin):
    list_display = ('link', 'bag_type', 'color', 'photo')

class GreetingAdmin(admin.ModelAdmin):
    list_display = ('query', 'response')

class FarewellAdmin(admin.ModelAdmin):
    list_display = ('query', 'response')

admin.site.register(Suit, AdminSuit)
admin.site.register(Perfume, PerfumeAdmin)
admin.site.register(Highlighter, HighlighterAdmin)
admin.site.register(Shoe, ShoeAdmin)
admin.site.register(Bag, BagAdmin)


admin.site.register(AddDressPiece)
admin.site.register(AddColor)
admin.site.register(AddDressFabric)
admin.site.register(AddDressDesign)
admin.site.register(AddFragranceType)
admin.site.register(AddScentType)
admin.site.register(AddFoundationType)
admin.site.register(AddHighlighterType)
admin.site.register(AddShoeType)
admin.site.register(AddBagType)


admin.site.register(AddGreeting, GreetingAdmin)
admin.site.register(AddFarewell, FarewellAdmin)