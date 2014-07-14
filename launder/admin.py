from django.contrib import admin
from launder.models import(
    WashFoldOrder,
    DryCleaning,
    LaundryShirtsOrder,
    Transaction,
    Product,
)


admin.site.register(WashFoldOrder)
admin.site.register(DryCleaning)
admin.site.register(LaundryShirtsOrder)
admin.site.register(Transaction)
admin.site.register(Product)
