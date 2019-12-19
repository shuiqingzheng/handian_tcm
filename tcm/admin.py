from django.contrib import admin
from tcm.models import (
    TCM, Literature, HandianProduct, Term,
    XingWei, Prescription,
)


@admin.register(TCM)
class TCMAdmin(admin.ModelAdmin):
    list_display = ('neo_id', 'name')


@admin.register(Literature)
class LiteratureAdmin(admin.ModelAdmin):
    list_display = ('neo_id', 'name')


@admin.register(HandianProduct)
class HandianProductAdmin(admin.ModelAdmin):
    list_display = ('neo_id', 'name')


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('neo_id', 'name')


@admin.register(XingWei)
class XingWeiAdmin(admin.ModelAdmin):
    list_display = ('neo_id', 'name')


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('neo_id', 'name')
