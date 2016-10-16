
from django.contrib import admin

from .models import Metric, Server, ServerProperty


admin.site.register(Server)
admin.site.register(ServerProperty)
admin.site.register(Metric)
