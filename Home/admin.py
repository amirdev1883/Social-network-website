from django.contrib import admin
from .models import post


class PostAdmin(admin.ModelAdmin):
    list_diplay = ('user', 'slug', 'updated')
    search_fields = ('slug', 'body')
    list_filter = ('updated',)
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user', )


admin.site.register(post, PostAdmin)
