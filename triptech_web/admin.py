from django.contrib import admin
from .models import Filenames, Data


# Register your models here.
class ChoiceInLineData(admin.TabularInline):
    model = Data
    extra = 3


class FilenamesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['filename']}),
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInLineData]
    list_display = ('filename', 'pub_date',)
    list_filter = ['pub_date']
    search_fields = ['filename']


admin.site.register(Filenames, FilenamesAdmin)

