from django.contrib import admin
from .models import Wine, Producer, Variety, BennelongWineList


class WineAdmin(admin.ModelAdmin):
    list_filter = (
        "producer__name",
        "variety__name",
    )
    search_fields = ("producer__name", "variety__name")


class ProducerAdmin(admin.ModelAdmin):
    list_filter = ("name", "region")
    search_fields = ("name", "region")


class VarietyAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    search_fields = ("name",)


class BennelongWineListAdmin(admin.ModelAdmin):
    pass


admin.site.register(Wine, WineAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Variety, VarietyAdmin)
admin.site.register(BennelongWineList, BennelongWineListAdmin)
