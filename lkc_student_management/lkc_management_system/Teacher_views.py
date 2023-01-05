from django.shortcuts import redirect, render
from app.models import SessionYearModel, Student, Subject, Teacher, TeacherMessage, LeaveReportTeacher
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/')
def home(request):
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()

    englishStudent = []
    KoreanStudent = []
    ChinesStudent = []
    
    for i in students:
        if i.department_id.name == 'English':
            englishStudent.append(i)
        elif i.department_id.name == 'Korean':
            KoreanStudent.append(i)
        else:
            ChinesStudent.append(i)

    englishStudent_count = len(englishStudent)
    KoreanStudent_count = len(KoreanStudent)
    ChinesStudent_count = len(ChinesStudent)

    print(englishStudent)

    context = {
        'englishStudent_count': englishStudent_count,
        'KoreanStudent_count': KoreanStudent_count,
        'ChinesStudent_count': ChinesStudent_count,
        'subjects': subjects,
        'teachers': teachers,
        'students': students,
    }
    return render(request, 'Teacher/home.html', context)

@login_required(login_url='/')
def message(request):
    teacher = Teacher.objects.filter(admin = request.user.id)
    for i in teacher:
        teacher_id = i.id
        teacherMessage = TeacherMessage.objects.filter(teacher_id = teacher_id)
        context = {
            'teacherMessage': teacherMessage,
        }
    return render(request, 'Teacher/messages.html', context)

@login_required(login_url='/')
def teacherMessageMakeAsDone(request, status):
    message = TeacherMessage.objects.get(id = status)
    message.status = 1
    message.save()
    return redirect('teacher_message')

@login_required(login_url='/')
@csrf_exempt
def teacherApplyLeave(request):
    teacher_obj = Teacher.objects.get(admin=request.user.id)
    leave_data = LeaveReportTeacher.objects.filter(teacher_id = teacher_obj)

    context = {
        'leave_data': leave_data,
    }
    
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        teacher_obj = Teacher.objects.get(admin=request.user.id)
        leave_report = LeaveReportTeacher(
            teacher_id=teacher_obj, 
            leave_date=leave_date,
            leave_message=leave_message,
            leave_status=0,
            )
        leave_report.save()
        messages.success(request, "Applied for Leave.")
        return redirect('teacher_apply_leave')

    return render(request, 'Teacher/teacherApplyLeave.html', context)







