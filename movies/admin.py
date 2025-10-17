from django.contrib import admin
from .models import Movie, Review, Rating, Region, MovieRegionStat

class MovieRegionStatInline(admin.TabularInline):
    model = MovieRegionStat
    extra = 0
    fields = ("region", "views")
    readonly_fields = ("region", "views")

class MovieAdmin(admin.ModelAdmin): # controls how it looks and behaves
    ordering = ['name']
    search_fields = ['name']
    inlines = [MovieRegionStatInline]
    def get_readonly_fields(self, request, obj=None):
        ro = list(super().get_readonly_fields(request, obj))
        if obj and obj.amount_left <= 0:
            ro.append("amount_left")
        return ro
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Rating)
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    search_fields = ["name"]

@admin.register(MovieRegionStat)
class MovieRegionStatAdmin(admin.ModelAdmin):
    list_display = ("movie", "region", "views")
    search_fields = ("movie__name", "region__name")
    list_select_related = ("movie", "region")
