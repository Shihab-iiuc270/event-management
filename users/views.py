from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomRegistrationForm,CreateGroupForm,AssignRoleForm
from django.contrib import messages
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required,user_passes_test
from events.models import Event


def is_admin(user):
    return user.groups.filter(name = 'admin').exists()
# Create your views here.
def sign_up(request):
    form = CustomRegistrationForm()
    if request.method =='POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request,'A confirmation email has been sent to your email.Please check your email')
            return redirect('sign-in')
        else:
            print("Form is not valid")
    return render(request, 'registration/register.html',{'form':form})


def sign_in(request):
    form = LoginForm()
    if request.method =='POST':
        form = LoginForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    return render(request,'registration/login.html',{'form': form})

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    
@user_passes_test(is_admin,login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups',queryset=Group.objects.all(),to_attr='all_group')
    ).all()
    for user in users:
        if user.all_group:
            user.group_name = user.all_group[0].name
        else:
            user.group_name = 'No group assigned'
    return render (request,'admin/dashboard.html',{'users':users})

@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
            return redirect('assign-role',user.id)

    return render(request, 'admin/assign_role.html', {"form": form})

@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method =='POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request,f'group {group.name} is created succesfully')

            return redirect('create-group')
        
    return render(request,'admin/create_group.html',{'form':form})

@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request,'admin/group_list.html',{'groups':groups})


@login_required
def rsvp_ev(request):
    user = request.user
    rsvp_events = user.rsvp_events.all()  

    context = {
        'rsvp_events': rsvp_events
    }
    return render(request, 'user/click _dash.html', {'rsvp_events':rsvp_events})

@login_required
def rsvp_event(request, event_id):
    event = Event.objects.get(id=event_id)
    user = request.user

    if event.participant.filter(id=user.id).exists():
        messages.warning(request, "You have already RSVP'd for this event.")
    else:
        event.participant.add(user)
        messages.success(request, "You have successfully RSVP'd for the event!")

    return redirect('manager')
