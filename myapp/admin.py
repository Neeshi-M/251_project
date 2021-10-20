from django.contrib import admin
from .models import EnrollRequest, Courses,Assignment,Submission

# Register your models here.
admin.site.register(EnrollRequest)
admin.site.register(Courses)
admin.site.register(Assignment)
admin.site.register(Submission)
