from django.contrib import admin
from .models import (
    Countries, Cities, Attractions, AttractionImages, AttractionProfiles,
    Tags, AttractionTags, Users, UserProfiles, UserTags, Interactions
)


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


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


@admin.register(Attractions)
class AttractionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'latitude', 'longitude', 'created_at')
    list_filter = ('city',)
    search_fields = ('name', 'short_description')
    inlines = [AttractionImagesInline, AttractionProfilesInline]
    readonly_fields = ('public_id', 'created_at', 'updated_at')


@admin.register(AttractionImages)
class AttractionImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'attraction', 'caption', 'display_order')
    list_filter = ('attraction',)


@admin.register(AttractionProfiles)
class AttractionProfilesAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'attraction_type', 'environment', 'cost_band', 'best_season')
    list_filter = ('attraction_type', 'environment', 'best_season')


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(AttractionTags)
class AttractionTagsAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'tag')


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'created_at')
    search_fields = ('username', 'email')


@admin.register(UserProfiles)
class UserProfilesAdmin(admin.ModelAdmin):
    list_display = ('user', 'nationality', 'language', 'age_band', 'travel_style', 'budget_band')
    list_filter = ('nationality', 'travel_style', 'age_band')


@admin.register(UserTags)
class UserTagsAdmin(admin.ModelAdmin):
    list_display = ('user', 'tag', 'weight')


@admin.register(Interactions)
class InteractionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'attraction', 'action_type', 'score', 'created_at')
    list_filter = ('action_type',)
    search_fields = ('user__username', 'attraction__name')
