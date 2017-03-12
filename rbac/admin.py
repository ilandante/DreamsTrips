from django.contrib import admin

from .models import\
    Object, Operation, PermissonAssignment, Role, UserRole


admin.site.register(Object)
admin.site.register(Operation)
admin.site.register(PermissonAssignment)
admin.site.register(Role)
admin.site.register(UserRole)
