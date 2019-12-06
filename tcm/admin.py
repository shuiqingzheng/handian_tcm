from django.contrib import admin
from tcm.models import TCM, Literature, HandianProduct


@admin.register(TCM)
class TCMAdmin(admin.ModelAdmin):
    list_display = ('neo_id', 'name')


@admin.register(Literature)
class LiteratureAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(HandianProduct)
class HandianProductAdmin(admin.ModelAdmin):
    list_display = ('id', )
