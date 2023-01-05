from django.shortcuts import redirect, render
from app.models import LeaveReportOfficer, Officer, OfficerMessage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/')
def home(request):
    return render(request, 'Officer/home.html')

@login_required(login_url='/')
def message(request):
    officer = Officer.objects.filter(admin = request.user.id)
    for i in officer:
        officer_id = i.id
        officerMessage = OfficerMessage.objects.filter(officer_id = officer_id)
        context = {
            'officerMessage': officerMessage,
        }
    return render(request, 'Officer/message.html', context)

@login_required(login_url='/')
def officerMessageMakeAsDone(request, status):
    messages = OfficerMessage.objects.get(id = status)
    messages.status = 1
    messages.save()
    return redirect('officer_messages')

@login_required(login_url='/')
@csrf_exempt
def officerApplyLeave(request):
    officer_obj = Officer.objects.get(admin=request.user.id)
    leave_data = LeaveReportOfficer.objects.filter(officer_id = officer_obj)

    context = {
        'leave_data': leave_data,
    }
    
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        officer_obj = Officer.objects.get(admin=request.user.id)
        leave_report = LeaveReportOfficer(
            officer_id=officer_obj, 
            leave_date=leave_date,
            leave_message=leave_message,
            leave_status=0,
            )
        leave_report.save()
        messages.success(request, "Applied for Leave.")
        return redirect('officer_apply_leave')

    return render(request, 'Officer/officerApplyLeave.html', context)




