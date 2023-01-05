from django.shortcuts import redirect, render
from app.models import Student, StudentMessage, LeaveReportStudent
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/')
def home(request):
    return render(request, 'Student/home.html')

@login_required(login_url='/')
def message(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        student_id = i.id
        studentMessage = StudentMessage.objects.filter(student_id = student_id)
        context = {
            'studentMessage': studentMessage,
        }
    return render(request, 'Student/messages.html', context)

@login_required(login_url='/')
def studentMessageMakeAsDone(request, status):
    messages = StudentMessage.objects.get(id = status)
    messages.status = 1
    messages.save()
    return redirect('student_messages')

@login_required(login_url='/')
@csrf_exempt
def studentApplyLeave(request):
    student_obj = Student.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id = student_obj)

    context = {
        'leave_data': leave_data,
    }
    
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_obj = Student.objects.get(admin=request.user.id)
        leave_report = LeaveReportStudent(
            student_id=student_obj, 
            leave_date=leave_date,
            leave_message=leave_message,
            leave_status=0,
            )
        leave_report.save()
        messages.success(request, "Applied for Leave.")
        return redirect('student_apply_leave')

    return render(request, 'Student/studentApplyLeave.html', context)







