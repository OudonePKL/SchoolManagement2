"""lkc_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import Hod_views, Officer_views, views, Student_views, Teacher_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Base/', views.base, name='base'),

    # Profile
    path('Profile/', views.profile, name='profile'),
    path('Profile/Update/', views.profile_update, name='profile_update'),

    # Login path
    path('', views.login, name='login'),
    path('dologin/', views.dologin, name='dologin'),
    path('dologout/', views.dologout, name='dologout'),

    # ----- For Hod panel url -----
    path('Hod/Home/', Hod_views.home, name='hold_home'),
    # For Student Path
    path('Hod/Student/Add/', Hod_views.addStudent, name='add_student'),
    path('Hod/Student/View/', Hod_views.viewStudent, name='view_student'),
    path('Hod/Student/Edit/<str:id>/', Hod_views.editStudent, name='edit_student'),
    path('Hod/Student/Update/', Hod_views.updateStudent,name='update_student'),
    path('Hod/Student/Delete/<str:admin>', Hod_views.deleteStudent,name='delete_student'),
    path('Hod/Student/Apply_Leave/', Hod_views.studentLeaveView, name='student_leave_view'),
    path('Hod/Student/Apply_Leave_Approve/<leave_id>/', Hod_views.studentLeaveApprove, name='student_leave_approve'),
    path('Hod/Student/Apply_Leave_Reject/<leave_id>/', Hod_views.studentLeaveReject, name='student_leave_reject'),

    # For Teacher Path
    path('Hod/Teacher/Add/', Hod_views.addTeacher, name='add_teacher'),
    path('Hod/Teacher/View/', Hod_views.viewTeacher, name='view_teacher'),
    path('Hod/Teacher/Edit/<str:id>/', Hod_views.editTeacher, name='edit_teacher'),
    path('Hod/Teacher/Update/', Hod_views.updateTeacher,name='update_teacher'),
    path('Hod/Teacher/Delete/<str:admin>', Hod_views.deleteTeacher,name='delete_teacher'),
    path('Hod/Teacher/Apply_Leave/', Hod_views.teacherLeaveView, name='teacher_leave_view'),
    path('Hod/Teacher/Apply_Leave_Approve/<leave_id>/', Hod_views.teacherLeaveApprove, name='teacher_leave_approve'),
    path('Hod/Teacher/Apply_Leave_Reject/<leave_id>/', Hod_views.teacherLeaveReject, name='teacher_leave_reject'),
   


    # For Officer Path
    path('Hod/Officer/Add/', Hod_views.addOfficer, name="add_officer"),
    path('Hod/Officer/View/', Hod_views.viewOfficer, name="view_officer"),
    path('Hod/Officer/Edit/<str:id>/', Hod_views.editOfficer, name="edit_officer"),
    path('Hod/Officer/Update/', Hod_views.updateOfficer,name='update_officer'),
    path('Hod/Officer/Delete/<str:admin>/', Hod_views.deleteOfficer, name="delete_officer"),
    path('Hod/Officer/Apply_Leave/', Hod_views.officerLeaveView, name='officer_leave_view'),
    path('Hod/Officer/Apply_Leave_Approve/<leave_id>/', Hod_views.officerLeaveApprove, name='officer_leave_approve'),
    path('Hod/Officer/Apply_Leave_Reject/<leave_id>/', Hod_views.officerLeaveReject, name='officer_leave_reject'),

    # For Officer Message path
    path('Hod/Officer/send_message/', Hod_views.officerSendMessage, name='officer_send_message'),
    path('Hod/Officer/save_message/', Hod_views.saveOfficerMessage, name='save_officer_message'),

    # For Student Message path
    path('Hod/Student/send_message/', Hod_views.studentSendMessage, name='student_send_message'),
    path('Hod/Student/save_message/', Hod_views.saveStudentMessage, name='save_student_message'),

    # For Teacher Message path
    path('Hod/Teacher/send_message/', Hod_views.teacherSendMessage, name='teacher_send_message'),
    path('Hod/Teacher/save_message/', Hod_views.saveTeacherMessage, name='save_teacher_message'),



    # ----- For Student panel url -----
    path('Student/Home/', Student_views.home, name='student_home'),
    path('Student/Messages/', Student_views.message, name='student_messages'),
    path('Student/make_as_done/<str:status>/', Student_views.studentMessageMakeAsDone, name='student_message_make_as_done'),
    path('Student/Apply_Leave/', Student_views.studentApplyLeave, name='student_apply_leave'),



    # ----- For Officer panel url -----\
    path('Officer/Home/', Officer_views.home, name='officer_home'),
    path('Officer/Messages/', Officer_views.message, name='officer_messages'),
    path('Officer/make_as_done/<str:status>/', Officer_views.officerMessageMakeAsDone, name='officer_message_make_as_done'),
    path('Officer/Apply_Leave/', Officer_views.officerApplyLeave, name='officer_apply_leave'),



    # ----- For Teacher panel url -----\
    path('Teacher/Home/', Teacher_views.home, name='teacher_home'),
    path('Teacher/Messages/', Teacher_views.message, name='teacher_messages'),
    path('Teacher/make_as_done/<str:status>/', Teacher_views.teacherMessageMakeAsDone, name='teacher_message_make_as_done'),
    path('Teacher/Apply_Leave/', Teacher_views.teacherApplyLeave, name='teacher_apply_leave'),



    # For Department Path
    path('Hod/Department/Add/', Hod_views.addDepartment, name='add_department'),
    path('Hod/Department/View/', Hod_views.viewDepartment, name='view_department'),
    path('Hod/Department/Edit/<str:id>/', Hod_views.editDepartment, name='edit_department'),
    path('Hod/Department/Update/', Hod_views.updateDepartment, name='update_department'),
    path('Hod/Department/Delete/<str:id>/', Hod_views.deleteDepartment, name='delete_department'),

    # For Subject Path
    path('Hod/Subject/Add/', Hod_views.addSubject, name='add_subject'),
    path('Hod/Subject/View/', Hod_views.viewSubject, name='view_subject'),
    path('Hod/Subject/Edit/<str:id>/', Hod_views.editSubject, name='edit_subject'),
    path('Hod/Subject/Update/', Hod_views.updateSubject, name='update_subject'),
    path('Hod/Subject/View/Delete/<str:id>', Hod_views.deleteSubject, name='delete_subject'),

    # For Session Year Path
    path('Hod/SessionYear/Add/', Hod_views.addSessionYear, name='add_sessionYear'),
    path('Hod/SessionYear/View/', Hod_views.viewSessionYear, name='view_sessionYear'),
    path('Hod/SessionYear/Edit/<str:id>/', Hod_views.editSessionYear, name='edit_sessionYear'),
    path('Hod/SessionYear/Update/', Hod_views.updateSessionYear, name='update_sessionYear'),
    path('Hod/SessionYear/View/Delete/<str:id>', Hod_views.deleteSessionYear, name='delete_sessionYear'),




    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
