
from import_export.admin import \
    ImportExportModelAdmin as BaseImportExportModelAdmin


class ImportExportModelAdmin(BaseImportExportModelAdmin):
    change_list_template = 'admin/change_list_import_export.html'
