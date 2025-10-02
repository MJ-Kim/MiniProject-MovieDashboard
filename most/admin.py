from django.contrib import admin
from most.models import MostMovie

# Register your models here.
@admin.register(MostMovie)
class MostMovieAdmin(admin.ModelAdmin):
    pass
