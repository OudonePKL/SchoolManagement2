from django.contrib import admin
from .models import CustomUser, Department, Student, Officer, OfficerMessage, StudentMessage, Subject, Teacher, LeaveReportTeacher, LeaveReportOfficer, LeaveReportStudent
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserModle(UserAdmin):
    list_display = ['username', 'user_type']

admin.site.register(CustomUser, UserModle)
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Officer)
admin.site.register(OfficerMessage)
admin.site.register(StudentMessage)
admin.site.register(Subject)
admin.site.register(LeaveReportOfficer)
admin.site.register(LeaveReportTeacher)
admin.site.register(LeaveReportStudent)