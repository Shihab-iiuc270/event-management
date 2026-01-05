from django.shortcuts import render,redirect
from django.http import HttpResponse
from events.forms import EventModelForm,CategoryModelForm
from events.models import Event,Category
from datetime import date
from django.db.models import Q,Count,Max,Min,Avg
from django.contrib import messages
from users.views import is_admin
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.core.mail import send_mail
from django.conf import settings


# def is_organiser(user):
#     return user.groups.filter(name = 'organiser').exists() or user.groups.filter(name = 'admin').exists()
def is_organiser(user):
    return user.groups.filter(name = 'organiser').exists()

def home(request):
    type = request.GET.get('cat')
    events = Event.objects.select_related('category').all()
    today = Event.objects.filter(date=date.today())
    if type:
        events = events.filter(category__name=type)
    categories = Category.objects.all()
    return render(request, "dashboard/home.html",{'events':events,'categories':categories,'today':today})

@login_required
def manager_dashboard(request):
    base_q = Event.objects.select_related('category')
    events = base_q.all()
    return render(request, "dashboard/manager_dashboard.html",{'events':events})

@user_passes_test(is_organiser,login_url='no-permission')
def user_dashboard(request):
    type = request.GET.get('type', "All")
    
    search = request.GET.get('q')

    base_q = Event.objects.select_related('category')
    events = base_q.all()

    today = base_q.filter(date=date.today())
   
    # if cat:
    #     events = events.filter(category__name=cat)

    


    if type == "Today's":
        events = today
    elif type == 'Upcoming':
        events = base_q.filter(date__gt=date.today())
    elif type == 'Past':
        events = base_q.filter(date__lt=date.today())
    # total_paricipants = Event.objects.aggregate(total=Count('participants', distinct=True))
    counts = Event.objects.aggregate(
        total=Count('id'),
        todays_event=Count('id', filter=Q(date=date.today())),
        previous_events=Count('id', filter=Q(date__lt=date.today())),
        upcoming_events=Count('id', filter=Q(date__gt=date.today()))
    )

    categorys = Category.objects.all()
    # counts['total_participants'] = total_paricipants['total']
    context = {
        'events': events,
        # 'today': today,
        'type': type,
        'counts': counts,
        'categorys': categorys,
        # 'total_participants': total_paricipants
    }

    return render(request, "dashboard/user_dashboard.html", context)

def search_events(request):
    search = request.GET.get('q')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    base_q = Event.objects.select_related('category').prefetch_related('participants')
    events = base_q.all()
    if search :
        events = events.filter(
            Q(name__icontains=search) | 
            Q(location__icontains=search)
        )
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    return render(request, "dashboard/home.html", {'events': events})

@login_required
@permission_required('events.add_event',login_url='no-permission')
def event_create(request):
    # particapnt = Participant.objects.all()
    form = EventModelForm()
    if request.method =='POST':
        form = EventModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Event Created Successfully")
            return redirect('user')

    context = {'form':form}
    return render(request,'event/form.html',{'form':form})

@login_required
@permission_required('events.view_event',login_url='no-permission')
def show_Detail(request,id):
    event = Event.objects.select_related('category').prefetch_related('participants').get(id=id)
    context = {'event':event}
    return render(request,'event/detail.html',context)

@login_required
@permission_required('events.change_event',login_url='no-permission')
def event_update(request,id):
    event = Event.objects.get(id=id)
    # particapnt = Participant.objects.all()
    form = EventModelForm(instance = event)
    if request.method =='POST':
        form = EventModelForm(request.POST,instance=event)
        if form.is_valid():
            form.save()
            messages.success(request,"Event Updated Successfully")
            return redirect('user')

    context = {'form':form}
    return render(request,'event_form.html',context)

@login_required
@permission_required('events.delete_event',login_url='no-permission')
def event_delete(request,id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.error(request,"Event Deleted Successfully")
        return redirect('user')
    else:
        return redirect('user')
    

@login_required
@permission_required('events.add_category',login_url='no-permission')
def create_category(request):
    form = CategoryModelForm()
    if request.method =='POST':
        form = CategoryModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Category Created Successfully")
            return redirect('home')

    context = {'form':form}
    return render(request,'category/form.html',context)
# def create_participnat(request):
#     form = ParticipantModelForm()
#     if request.method =='POST':
#         form = ParticipantModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Participant Created Successfully")
#             return redirect('home')

    context = {'form':form}
    return render(request,'participant/form.html',context)

# def all_participant(request):
#     participants = Participant.objects.all()
#     context = {'participants':participants}
#     return render(request,'participant/list.html',context)

# def participant_delete(request,id):
#     if request.method == 'POST':
#         participant = Participant.objects.get(id=id)
#         participant.delete()
#         messages.error(request,"Participant Deleted Successfully")
#         return redirect('user')
#     else:
#         return redirect('user')
    
# def participant_update(request,id):
#     participant = Participant.objects.get(id=id)
#     form = ParticipantModelForm(instance = participant)
#     if request.method =='POST':
#         form = ParticipantModelForm(request.POST,instance=participant)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Participant Updated Successfully")
#             return redirect('user')

    context = {'form':form}
    return render(request,'participant/form.html',context)

@login_required
@permission_required('events.view_category',login_url='no-permission')
def all_categories(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request,'category/list.html',context)

@login_required
@permission_required('events.delete_category',login_url='no-permission')
def category_delete(request,id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        messages.error(request,"Category Deleted Successfully")
        return redirect('user')
    else:
        return redirect('user')
    
@login_required
@permission_required('events.change_category',login_url='no-permission')
def category_update(request,id):
    category = Category.objects.get(id=id)
    form = CategoryModelForm(instance = category)
    if request.method =='POST':
        form = CategoryModelForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.success(request,"Category Updated Successfully")
            return redirect('user')

    context = {'form':form}
    return render(request,'category/form.html',context)


@login_required
def dashboard(request):
    # if is_organiser(request.user):
    #     return redirect('user')
    # elif is_admin(request.user):
    #     return redirect('admin-dashboard')
    # else:
    #     return redirect('manager')
    pass

# @login_required
# def rsvp_event(request, event_id):
#     event = Event.objects.get(id=event_id)
#     user = request.user 

#     if event.participant.filter(id=user.id).exists():
#         messages.warning(request, "You have already RSVP'd for this event.")
#     else:
#         event.participant.add(user)
#         messages.success(request, "You have successfully RSVP'd for the event!")

#         subject = "Event RSVP Confirmation"
#         message = (
#             f"Hi {user.username} You have successfully RSVP’d for the event: {event.name}"
#         )

#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             [user.email],
#             fail_silently=False
#         )

#     return redirect('manager')
