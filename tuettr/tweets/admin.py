from django.contrib import admin

# Register your models here.
from django.apps import apps
"""
admin.py
Auto-register admin classes with fields and links to linked model classes
based on http://djangosnippets.org/snippets/997/
"""

from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.db import models as dmodels
from django.db.models import Field, ForeignKey, OneToOneField
from types import ModuleType


def add_link_field(admin_class, field):
    field_name = field.name + '_link'

    def link(self, instance):
        # import pdb; pdb.set_trace()
        app_name = field.related_model._meta.app_label# field.related.parent_model._meta.app_label
        reverse_path = "admin:%s_%s_change" % (
            app_name,
            field.related_model._meta.model_name
        )
        related_instance = getattr(instance, field.name)
        if related_instance:
            url = reverse(reverse_path, args=(related_instance.id,))
            return mark_safe("<a href='%s'>%s</a>" % (
                url,
                str(related_instance))
            )
        else:
            return str(related_instance)
    link.allow_tags = True
    link.short_description = field.name + ' link'
    setattr(admin_class, field_name, link)
    admin_class.readonly_fields = list(
        getattr(admin_class, 'readonly_fields', [])) + [field_name]
    return admin_class, field_name


def register_admin_module(module, exclude=None, new_fields=None):
    """
    @param module: module containing django.db.models classes
    @type module: str or __module__
    @param exclude: list of classes to exclude from auto-register
    @type exclude: iterable of str or None
    @param new_fields: dictionary of additional fields:
        {'model name': ('field_name', callable)}
    @type new_fields: dict or None
    If you are providing str, use absolute path
    """
    exclude = exclude or []
    new_fields = new_fields or {}

    mods = []
    mods.append(module)


    admins = []
    #for each model prepare an admin class (Admin<model_name>, model)
    for c in mods:
        admins.append(("%sAdmin" % c.__name__, c))

    #create the admin class and register it
    for (ac, c) in admins:
        admin_class = type(ac, (admin.ModelAdmin,), dict())
        admin_class.list_display = []
        for field in c._meta.fields:
            field_name = field.name
            # create link for relations
            if issubclass(type(field), (ForeignKey, OneToOneField)):
                admin_class, field_name = add_link_field(admin_class, field)
            if issubclass(type(field), (ForeignKey, OneToOneField, Field)):
                admin_class.list_display.append(field_name)

        # add user defined custom fields
        for new_field in new_fields:
            if c.__name__ == new_field:
                setattr(admin_class, new_fields[new_field][0],
                        new_fields[new_field][1])
                admin_class.list_display.append(new_fields[new_field][0])

        try:  # pass gracefully on duplicate registration errors
            admin.site.register(c, admin_class)
        except Exception:
            pass


models = apps.get_models()
for model in models:
    try:
        register_admin_module(model)
    except admin.sites.AlreadyRegistered:
        print('error')