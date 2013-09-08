from django.contrib import admin
from launder.models import(
    WashFoldOrder,
    DryCleaning,
    LaundryShirtsOrder,
    DailyOperations,
    Product,
)


admin.site.register(WashFoldOrder)
admin.site.register(DryCleaning)
admin.site.register(LaundryShirtsOrder)
admin.site.register(DailyOperations)
admin.site.register(Product)
