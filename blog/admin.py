from django.contrib import admin
from .models import Post, Category, Tag
from .models import PostImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields =("name",)


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 3

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "user", "published_date")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('tags',)
    inlines = [PostImageInline]


from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)





