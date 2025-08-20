from django.contrib import admin

from blog.models import Post, Commentaire, Follow


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', '')


admin.site.register(Post)
admin.site.register(Commentaire)
admin.site.register(Follow)
