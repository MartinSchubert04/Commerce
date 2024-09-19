from django.contrib import admin
from .models import User, Categories, Listing, Comments, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Listing)
admin.site.register(Comments)
admin.site.register(Bid)