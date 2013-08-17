from django.contrib import admin
from launder.models import(
	WashFoldOrder,
	DryCleaning,
	LaundryShirtsOrder,
	DailyOperations,
)

admin.site.register(WashFoldOrder)
admin.site.register(DryCleaning)
admin.site.register(LaundryShirtsOrder)
admin.site.register(DailyOperations)
