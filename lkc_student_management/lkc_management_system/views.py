from django.shortcuts import redirect, render, HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib import auth, messages
from app.models import CustomUser, Teacher
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



def base(request):
    return render(request, 'base.html')

def login(request):
    return render(request, 'login.html')

@login_required(login_url='/')
def profile(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/')
@csrf_exempt
def profile_update(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            customuser = CustomUser.objects.get(id = request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name

            if password != None and password != '':
                customuser.set_password(password)
            if profile_pic != None and profile_pic != '':
                customuser.profile_pic = profile_pic
            if email != None and email != '':
                customuser.email = email
            if username != None and username != '':
                customuser.username = username
            customuser.save()
            messages.success(request, 'Your Profile Updated Successfully!')
            return redirect('profile')
        except:
            messages.error(request, 'Failed To Update Your Profile!')

    return render(request, 'profile.html')

# Authentications
@csrf_exempt
def dologin(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request, 
                username=request.POST.get('username'),
                password=request.POST.get('password'),)
        if user!=None:
            auth.login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('hold_home')
            elif user_type == '2':
                return redirect('officer_home')
            elif user_type == '3':
                return redirect('teacher_home')
            elif user_type == '4':
                return redirect('student_home')
            else:
                messages.error(request, 'Email and Password are invalid!')
                return redirect('login')
        else:
            messages.error(request, 'Email and Password are invalid!')
            return redirect('login')

def dologout(request):
    auth.logout(request)
    return redirect('login')

