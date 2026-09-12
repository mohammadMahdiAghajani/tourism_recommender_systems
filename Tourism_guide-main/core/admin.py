from django.contrib import admin
from .models import (
    Countries, Cities, Attractions, AttractionImages, AttractionProfiles,
    Tags, AttractionTags, Users, UserProfiles, UserTags, Interactions
)

# ثبت مدل در پنل مدیریت جنگو
@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# ثبت مدل در پنل مدیریت جنگو
@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    list_filter = ('country',)
    search_fields = ('name',)


class AttractionImagesInline(admin.TabularInline):
    model = AttractionImages
    extra = 0


class AttractionProfilesInline(admin.StackedInline):
    model = AttractionProfiles
    extra = 0

# ثبت مدل در پنل مدیریت جنگو
@admin.register(Attractions)
class AttractionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'latitude', 'longitude', 'created_at')
    list_filter = ('city',)
    search_fields = ('name', 'short_description')
    inlines = [AttractionImagesInline, AttractionProfilesInline]
    readonly_fields = ('public_id', 'created_at', 'updated_at')

# ثبت مدل در پنل مدیریت جنگو
@admin.register(AttractionImages)
class AttractionImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'attraction', 'caption', 'display_order')
    list_filter = ('attraction',)

# ثبت مدل در پنل مدیریت جنگو
@admin.register(AttractionProfiles)
class AttractionProfilesAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'attraction_type', 'environment', 'cost_band', 'best_season')
    list_filter = ('attraction_type', 'environment', 'best_season')

# ثبت مدل در پنل مدیریت جنگو
@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# ثبت مدل در پنل مدیریت جنگو
@admin.register(AttractionTags)
class AttractionTagsAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'tag')

# ثبت مدل در پنل مدیریت جنگو
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'created_at')
    search_fields = ('username', 'email')

# ثبت مدل در پنل مدیریت جنگو
@admin.register(UserProfiles)
class UserProfilesAdmin(admin.ModelAdmin):
    list_display = ('user', 'nationality', 'language', 'age_band', 'travel_style', 'budget_band')
    list_filter = ('nationality', 'travel_style', 'age_band')

# ثبت مدل در پنل مدیریت جنگو
@admin.register(UserTags)
class UserTagsAdmin(admin.ModelAdmin):
    list_display = ('user', 'tag', 'weight')

# ثبت مدل در پنل مدیریت جنگو
@admin.register(Interactions)
class InteractionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'attraction', 'action_type', 'score', 'created_at')
    list_filter = ('action_type',)
    search_fields = ('user__username', 'attraction__name')
