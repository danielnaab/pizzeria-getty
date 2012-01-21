from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db.models import get_models

import models

# Register every model.
for model in get_models(models):
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
