from django import get_version
from django.apps import AppConfig
from django.conf import settings
from django.contrib.admin import options
from django.contrib.admin.options import ModelAdmin
from django.db import models
from . import VERSION
from django import forms
from widgets import SuitDateWidget, SuitDateTimeWidget


class DjangoSuitConfig(AppConfig):
    name = 'suit'
    verbose_name = 'Django Suit'
    version = VERSION
    django_version = get_version()
    menu_position = 'horizontal'
    list_per_page = 18
    list_filters_position = 'right'
    form_size = 'col-sm-2:col-sm-9'
    admin_name = 'Django Suit'

    # not used yet
    theme = 'dark'
    header_date_format = 'l, jS F Y'
    header_time_format = 'H:i'

    # form
    show_required_asterisk = True
    confirm_unsaved_changes = True

    # menu
    search_url = '/admin/auth/user/'
    menu_open_first_child = True


    def __init__(self, app_name, app_module):

        self.override_datepickers()
        self.setup_model_admin()

        if 'filer' in settings.INSTALLED_APPS:
            try:
                self.setup_filer_app()
            except Exception:
                pass

        super(DjangoSuitConfig, self).__init__(app_name, app_module)

    def override_datepickers(self):
        # options.FORMFIELD_FOR_DBFIELD_DEFAULTS = {
        # models.DateTimeField: {
        # 'form_class': forms.SplitDateTimeField,
        # 'widget': widgets.AdminSplitDateTime
        # },
        # models.DateField: {'widget': widgets.AdminDateWidget},
        # models.TimeField: {'widget': widgets.AdminTimeWidget},
        # }

        options.FORMFIELD_FOR_DBFIELD_DEFAULTS[models.DateField].update({
            'widget': SuitDateWidget
        })
        options.FORMFIELD_FOR_DBFIELD_DEFAULTS[models.DateTimeField].update({
            'form_class': forms.DateTimeField,
            'widget': SuitDateTimeWidget
        })

    def setup_model_admin(self):
        """
        Override some ModelAdmin defaults
        """
        ModelAdmin.actions_on_top = False
        ModelAdmin.actions_on_bottom = True
        ModelAdmin.list_per_page = self.list_per_page

    def setup_filer_app(self):
        """
        Override filer app defaults
        """
        from suit.widgets import AutosizedTextarea
        from filer.admin.imageadmin import ImageAdminForm
        from filer.admin.fileadmin import FileAdminChangeFrom
        # from filer.admin import FolderAdmin

        def ensure_meta_widgets(meta_cls):
            if not hasattr(meta_cls, 'widgets'):
                meta_cls.widgets = {}
            meta_cls.widgets['description'] = AutosizedTextarea

        ensure_meta_widgets(ImageAdminForm.Meta)
        ensure_meta_widgets(FileAdminChangeFrom.Meta)
        # FolderAdmin.actions_on_top = False
        # FolderAdmin.actions_on_bottom = True
