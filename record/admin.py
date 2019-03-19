from django.contrib import admin
from record.models import Record
# Register your models here.


class RecordAdmin(admin.ModelAdmin):
    list_display = ('person', 'pk', 'treatmentPlan', 'medicalRecordId', 'createdAt',)


admin.site.register(Record, RecordAdmin)