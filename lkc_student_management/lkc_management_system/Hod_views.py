from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from app.models import Department ,CustomUser, LeaveReportOfficer, LeaveReportStudent, LeaveReportTeacher, Officer, SessionYearModel, Student, OfficerMessage, StudentMessage, TeacherMessage,Subject, Teacher
from django.contrib import auth, messages
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/')
def home(request):
    student_count = Student.objects.all().count()
    teacher_count = Teacher.objects.all().count()
    officer_count = Officer.objects.all().count()
    department_count = Department.objects.all().count()
    subject_count = Subject.objects.all().count()

    student_gender_male = Student.objects.filter(gender = 'Male').count()
    student_gender_female = Student.objects.filter(gender = 'Female').count()

    # Total Subjects and Students in Each Department
    students = Student.objects.all()

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

    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'officer_count': officer_count,
        'department_count': department_count,
        'subject_count': subject_count,
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female,
        'englishStudent_count': englishStudent_count,
        'KoreanStudent_count': KoreanStudent_count,
        'ChinesStudent_count': ChinesStudent_count,
        
    }

    return render(request, 'Hod/home.html', context)

# --------- For Student -----------
@login_required(login_url='/')
@csrf_exempt
def addStudent(request):
    department = Department.objects.all()
    sessionYear = SessionYearModel.objects.all()

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        studentID = request.POST.get('studentID')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department_id')
        session_year_id = request.POST.get('session_year_id')
    
        if Student.objects.filter(studentID=studentID).exists():
            messages.warning(request, 'This student ID is already exist!')
            return redirect('add_student')
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'This email is already exist!')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'This username is already exist!')
            return redirect('add_student')
        
        else:
            try:
                user = CustomUser(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    profile_pic = profile_pic,
                    user_type = 4
                )
                user.set_password(password)
                user.save()
                department = Department.objects.get(id=department_id)
                sessionYear = SessionYearModel.objects.get(id=session_year_id)
                student = Student(
                    admin = user,
                    studentID = studentID,
                    address = address,
                    department_id = department,
                    gender = gender,
                    session_year_id = sessionYear,
                )
                student.save()
                messages.success(request, user.first_name + " " + user.last_name + ' Are Successfully Added!')
                return redirect('add_student')
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect('add_student')

    context = {
        'department': department,
        'sessionYear': sessionYear
    }

    return render(request, 'Hod/addStudent.html', context)

@login_required(login_url='/')
def viewStudent(request):
    students = Student.objects.all()
    context = {
        'students': students
    }
    return render(request, 'Hod/viewStudent.html', context)

@login_required(login_url='/')
def editStudent(request, id):
    student = Student.objects.filter(id = id)
    department = Department.objects.all()
    sessionYear = SessionYearModel.objects.all()

    context = {
        'student':student,
        'department':department,
        'sessionYear': sessionYear,
    }
    return render(request,'Hod/editStudent.html',context)

@login_required(login_url='/')
@csrf_exempt
def updateStudent(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        studentID = request.POST.get('studentID')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department_id')
        session_year_id = request.POST.get('session_year_id')


        user = CustomUser.objects.get(id = student_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
            

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin = student_id)
        department = Department.objects.get(id = department_id)
        sessionYear = SessionYearModel.objects.get(id=session_year_id)

        student.studentID = studentID
        student.address = address
        student.gender = gender
        student.session_year_id = sessionYear
        student.department_id = department

        student.save()
        messages.success(request,'Record Are Successfully Updated !')
        return redirect('view_student')

    return render(request,'Hod/editStudent.html')

def deleteStudent(request, admin):
    student = CustomUser.objects.get(id = admin)
    student.delete()
    messages.success(request, 'Record Are Successfully Deleted!')
    return redirect('view_student')

# --------- For Teacher ---------
@login_required(login_url='/')
@csrf_exempt
def addTeacher(request):
    department = Department.objects.all()

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        teacherID = request.POST.get('teacherID')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department_id')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'This email is already exist!')
            return redirect('add_teacher')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'This username is already exist!')
            return redirect('add_teacher')

        user = CustomUser(
            first_name = first_name, 
            last_name = last_name, 
            email = email, 
            username = username,
            profile_pic = profile_pic,
            user_type = 3,
        )
        user.set_password(password)
        user.save()

        department = Department.objects.get(id = department_id)
        teacher = Teacher(
            teacherID = teacherID,
            department_id = department,
            admin = user,
            address = address,
            gender = gender,
        )
        teacher.save()
        messages.success(request, 'Teacher Are Successfully Added!')
        return redirect('add_teacher')

    context = {
        'department': department,
    }
    return render(request, 'Hod/addTeacher.html', context)

@login_required(login_url='/')
def viewTeacher(request):
    teacher = Teacher.objects.all()
    context = {
        'teacher': teacher
    }
    return render(request, 'Hod/viewTeacher.html', context)

@login_required(login_url='/')
def editTeacher(request, id):
    teacher = Teacher.objects.get(id = id)
    department = Department.objects.all()

    context = {
        'teacher':teacher,
        'department': department,
    }
    return render(request,'Hod/editTeacher.html',context)

@login_required(login_url='/')
@csrf_exempt
def updateTeacher(request):
    if request.method == "POST":
        teacher_id = request.POST.get('teacher_id')
        profile_pic = request.FILES.get('profile_pic')
        teacherID = request.POST.get('teacherID')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department_id')


        user = CustomUser.objects.get(id = teacher_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic   
        
        user.save()

        teacher = Teacher.objects.get(admin = teacher_id)
        department = Department.objects.get(id = department_id)

        teacher.teacherID = teacherID
        teacher.address = address
        teacher.gender = gender
        teacher.department_id = department

        teacher.save()
        messages.success(request,'Record Are Successfully Updated !')
        return redirect('view_teacher')

    return render(request,'Hod/editTeacher.html')

def deleteTeacher(request, admin):
    teacher = CustomUser.objects.get(id = admin)
    teacher.delete()
    messages.success(request, 'Record Are Successfully Deleted!')
    return redirect('view_teacher')

# --------- For Officer -----------
@login_required(login_url='/')
@csrf_exempt
def addOfficer(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        officerID = request.POST.get('officerID')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
    
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'This email is already exist!')
            return redirect('add_officer')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'This username is already exist!')
            return redirect('add_officer')

        if gender == 'Select Gender':
            messages.error(request, 'Choice The Gender Please!')
            return redirect('add_officer')

        user = CustomUser(
            first_name = first_name, 
            last_name = last_name, 
            email = email, 
            username = username,
            profile_pic = profile_pic,
            user_type = 2,
        )
        user.set_password(password)
        user.save()

        officer = Officer(
            officerID = officerID,
            admin = user,
            address = address,
            gender = gender,
        )
        officer.save()
        messages.success(request, 'Officer Are Successfully Added!')
        return redirect('add_officer')

    return render(request, 'Hod/addOfficer.html')

@login_required(login_url='/')
def viewOfficer(request):
    officer = Officer.objects.all()
    context = {
        'officer': officer,
    }
    return render(request, 'Hod/viewOfficer.html', context)

@login_required(login_url='/')
def editOfficer(request, id):
    officer = Officer.objects.get(id = id)
    context = {
        'officer': officer
    }
    return render(request, 'Hod/editOfficer.html', context )

@login_required(login_url='/')
@csrf_exempt
def updateOfficer(request):
    if request.method == "POST":
        officer_id = request.POST.get('officer_id')
        profile_pic = request.FILES.get('profile_pic')
        officerID = request.POST.get('officerID')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = CustomUser.objects.get(id = officer_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic   
        
        user.save()

        officer = Officer.objects.get(admin = officer_id)
        officer.officerID = officerID
        officer.address = address
        officer.gender = gender

        officer.save()
        messages.success(request,'Record Are Successfully Updated !')
        return redirect('view_officer')

    return render(request,'Hod/editOfficer.html')

def deleteOfficer(request, admin):
    officer = CustomUser.objects.get(id = admin)
    officer.delete()
    messages.success(request, 'Record Are Successfully Deleted!')
    return redirect('view_officer')


# --------- For Department or Department -----------
@login_required(login_url='/')
@csrf_exempt
def addDepartment(request):
    if request.method == 'POST':
        department_name = request.POST.get('department_name')

        department = Department(
            name = department_name
        )
        department.save()
        messages.success(request, 'Department Is Successfully Created!')
        return redirect('add_department')
        
    return render(request, 'Hod/addDepartment.html')

@login_required(login_url='/')
def viewDepartment(request):
    department = Department.objects.all()
    context = {
        'department': department,
    }
    return render(request, 'Hod/viewDepartment.html', context)

@login_required(login_url='/')
def editDepartment(request, id):
    department = Department.objects.get(id = id)

    context = {
        'department': department,
    }

    return render(request, 'Hod/editDepartment.html', context)

@login_required(login_url='/')
@csrf_exempt
def updateDepartment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        department_id = request.POST.get('department_id')

        department = Department.objects.get(id = department_id)
        department.name = name
        department.save()
        messages.success(request, 'Department Are Successfully Updated!')
        return redirect('view_department')

    return render(request, 'Hod/editDepartment.html')

def deleteDepartment(request, id):
    department = Department.objects.get(id = id)
    department.delete()
    messages.success(request, 'Department are Successfully Deleted!')

    return redirect('view_department')

# For Session Year
@login_required(login_url='/')
@csrf_exempt
def addSessionYear(request):
    if request.method == 'POST':
        sessionYear = request.POST.get('sessionYear')

        sessionYear = SessionYearModel(
            sessionYear=sessionYear, 
        )
        sessionYear.save()
        messages.success(request, "Session Year added Successfully!")
        return redirect("add_sessionYear")

    return render(request, 'Hod/addSessionYear.html')

@login_required(login_url='/')
def viewSessionYear(request):
    sessionYear = SessionYearModel.objects.all()
    context = {
        'sessionYear': sessionYear,
    }
    return render(request, 'Hod/viewSessionYear.html', context)

@login_required(login_url='/')
def editSessionYear(request, id):
    sessionYear = SessionYearModel.objects.get(id = id)
    context = {
        'sessionYear': sessionYear,
    }
    return render(request, 'Hod/editSessionYear.html', context)

@login_required(login_url='/')
@csrf_exempt
def updateSessionYear(request):
    if request.method == 'POST':
        sessionYear = request.POST.get('sessionYear')
        sessionYear_id = request.POST.get('sessionYear_id')

        sessionYearModel = SessionYearModel.objects.get(id = sessionYear_id)
        sessionYearModel.sessionYear = sessionYear
        sessionYearModel.save()
        
        messages.success(request, 'Session Year Are Successfully Updated!')
        # return redirect('/Hod/SessionYear/Edit/'+sessionYear_id+'/')
        return redirect('view_sessionYear')

    return render(request, 'Hod/editSessionYear.html')

def deleteSessionYear(request, id):
    sessionYear = SessionYearModel.objects.get(id = id)
    sessionYear.delete()
    messages.success(request, 'Session Year Are Successfully Deleted!')

    return redirect('view_sessionYear')


# For Subjects
@login_required(login_url='/')
@csrf_exempt
def addSubject(request):
    department = Department.objects.all()
    sessionYear = SessionYearModel.objects.all()
    teacher = Teacher.objects.all()

    if request.method == 'POST':
        department_id = request.POST.get('department_id')
        teacher_id = request.POST.get('teacher_id')
        session_year_id = request.POST.get('session_year_id')
        subject_name = request.POST.get('subject_name')

        department = Department.objects.get(id=department_id)
        sessionStartYear = SessionYearModel.objects.get(id=session_year_id)
        teacher = Teacher.objects.get(id=teacher_id)
        subject = Subject(
            department_id= department,
            teacher_id = teacher,
            session_year_id = sessionStartYear,
            name = subject_name,
        )
        subject.save()
        messages.success(request, 'Subject Is Successfully Created!')
        return redirect('add_subject') 

    context = {
        'department': department,
        'sessionYear': sessionYear,
        'teacher':teacher,
    }
    return render(request, 'Hod/addSubject.html', context)

@login_required(login_url='/')
def viewSubject(request):
    subject = Subject.objects.all()
    context = {
        'subject': subject,
    }
    return render(request, 'Hod/viewSubject.html', context)

def editSubject(request, id):
    subject = Subject.objects.get(id = id)
    department = Department.objects.all()
    sessionYear = SessionYearModel.objects.all()
    teacher = Teacher.objects.all()

    context = {
        'subject':subject,
        'department':department,
        'sessionYear':sessionYear,
        'teacher':teacher,
    }
    
    return render(request, 'Hod/editSubject.html', context )

@login_required(login_url='/')
@csrf_exempt
def updateSubject(request):
    if request.method == 'POST':
        department_id = request.POST.get('department_id')
        subject_id = request.POST.get('subject_id')
        teacher_id = request.POST.get('teacher_id')
        session_year_id = request.POST.get('session_year_id')
        subject_name = request.POST.get('subject_name')

        if department_id == "Select Department":
            messages.error(request,'Please Choose The Department!')
        else:
            subject = Subject.objects.get(id = subject_id)
            department = Department.objects.get(id = department_id)
            teacher = Teacher.objects.get(id = teacher_id)
            session_year = SessionYearModel.objects.get(id = session_year_id)

            subject.session_year_id = session_year
            subject.teacher_id = teacher
            subject.department_id = department
            subject.subject_name = subject_name

            subject.save()
            messages.success(request, 'Subject Are Successfully Updated!')
            return redirect('view_subject')

    return render(request, 'Hod/editSubject.html')

def deleteSubject(request, id):
    subject = Subject.objects.get(id = id)
    subject.delete()
    messages.success(request, 'Subject Are Successfully Deleted!')

    return redirect('view_subject')

# For Officer Message 
@login_required(login_url='/')
def officerSendMessage(request):
    officer = Officer.objects.all()
    see_message = OfficerMessage.objects.all().order_by('-id')
    context = {
        'officer': officer,
        'see_message': see_message,
    }
    return render(request, 'Hod/officerSendMessage.html', context)

@login_required(login_url='/')
@csrf_exempt
def saveOfficerMessage(request):
    if request.method == 'POST':
        officer_id = request.POST.get('officer_id')
        message = request.POST.get('message')

        officer = Officer.objects.get(admin = officer_id)
        officerMessage = OfficerMessage(
            officer_id = officer,
            message = message,
        )
        officerMessage.save()
        messages.success(request, 'Message Are Successfully Sent')
        return redirect('officer_send_message')

# For Student Message 
@login_required(login_url='/')
def studentSendMessage(request):
    student = Student.objects.all()
    see_message = StudentMessage.objects.all().order_by('-id')
    context = {
        'student': student,
        'see_message': see_message,
    }
    return render(request, 'Hod/studentSentMessage.html', context)

@login_required(login_url='/')
@csrf_exempt
def saveStudentMessage(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        message = request.POST.get('message')

        student = Student.objects.get(admin = student_id)
        studentMessage = StudentMessage(
            student_id = student,
            message = message,
        )
        studentMessage.save()
        messages.success(request, 'Message Are Successfully Sent')
        return redirect('student_send_message')

# For Teacher Message
@login_required(login_url='/')
def teacherSendMessage(request):
    teacher = Teacher.objects.all()
    see_message = TeacherMessage.objects.all().order_by('-id')
    context = {
        'teacher': teacher,
        'see_message': see_message,
    }
    return render(request, 'Hod/teacherSendMessage.html', context)

@login_required(login_url='/')
@csrf_exempt
def saveTeacherMessage(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        message = request.POST.get('message')

        teacher = Teacher.objects.get(admin = teacher_id)
        teacherMessage = TeacherMessage(
            teacher_id = teacher,
            message = message,
        )
        teacherMessage.save()
        messages.success(request, 'Message Are Successfully Sent')
        return redirect('teacher_send_message')

# View All Applies
@login_required(login_url='/')
def officerLeaveView(request):
    leaves = LeaveReportOfficer.objects.all()
    context = {
        'leaves': leaves
    }
    return render(request, 'Hod/officerLeaveView.html', context)

def officerLeaveApprove(request, leave_id):
    leave = LeaveReportOfficer.objects.get(id = leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('officer_leave_view')

def officerLeaveReject(request, leave_id):
    leave = LeaveReportOfficer.objects.get(id = leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('officer_leave_view')

@login_required(login_url='/')
def teacherLeaveView(request):
    leaves = LeaveReportTeacher.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'Hod/teacherLeaveView.html', context)

def teacherLeaveApprove(request, leave_id):
    leave = LeaveReportTeacher.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('teacher_leave_view')

def teacherLeaveReject(request, leave_id):
    leave = LeaveReportTeacher.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('teacher_leave_view') 

@login_required(login_url='/')
def studentLeaveView(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        'leaves': leaves
    }
    return render(request, 'Hod/studentLeaveView.html', context)

def studentLeaveApprove(request, leave_id):
    leave = LeaveReportStudent.objects.get(id = leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')

def studentLeaveReject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id = leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')





