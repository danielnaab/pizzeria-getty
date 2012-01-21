from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db.models import get_models

import models

admin.site.register(models.Size)
admin.site.register(models.Topping)

# Register every model.
#for model in get_models(models):
#    try:
#        admin.site.register(model)
#    except AlreadyRegistered:
#        pass
