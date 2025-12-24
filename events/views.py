from django.shortcuts import render,redirect
from django.http import HttpResponse
from events.forms import EventModelForm,CategoryModelForm,ParticipantModelForm
from events.models import Event,Category,Participant
from datetime import date
from django.db.models import Q,Count,Max,Min,Avg
from django.contrib import messages

def home(request):
    type = request.GET.get('cat')
    events = Event.objects.select_related('category').all()
    today = Event.objects.filter(date=date.today())
    if type:
        events = events.filter(category__name=type)
    categories = Category.objects.all()
    return render(request, "dashboard/home.html",{'events':events,'categories':categories,'today':today})
def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")


def user_dashboard(request):
    type = request.GET.get('type', "Today's")
    
    search = request.GET.get('q')

    base_q = Event.objects.select_related('category').prefetch_related('participants')
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
    total_paricipants = Event.objects.aggregate(total=Count('participants', distinct=True))
    counts = Event.objects.aggregate(
        total=Count('id'),
        todays_event=Count('id', filter=Q(date=date.today())),
        previous_events=Count('id', filter=Q(date__lt=date.today())),
        upcoming_events=Count('id', filter=Q(date__gt=date.today()))
    )

    categorys = Category.objects.all()
    counts['total_participants'] = total_paricipants['total']
    context = {
        'events': events,
        # 'today': today,
        'type': type,
        'counts': counts,
        'categorys': categorys,
        'total_participants': total_paricipants
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
    

def event_create(request):
    particapnt = Participant.objects.all()
    form = EventModelForm()
    if request.method =='POST':
        form = EventModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Event Created Successfully")
            return redirect('home')

    context = {'form':form}
    return render(request,'event/form.html',context)

def show_Detail(request,id):
    event = Event.objects.select_related('category').prefetch_related('participants').get(id=id)
    context = {'event':event}
    return render(request,'event/detail.html',context)
    

def event_update(request,id):
    event = Event.objects.get(id=id)
    particapnt = Participant.objects.all()
    form = EventModelForm(instance = event)
    if request.method =='POST':
        form = EventModelForm(request.POST,instance=event)
        if form.is_valid():
            form.save()
            messages.success(request,"Event Updated Successfully")
            return redirect('user')

    context = {'form':form}
    return render(request,'event_form.html',context)

def event_delete(request,id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.error(request,"Event Deleted Successfully")
        return redirect('user')
    else:
        return redirect('user')
    


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
def create_participnat(request):
    form = ParticipantModelForm()
    if request.method =='POST':
        form = ParticipantModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Participant Created Successfully")
            return redirect('home')

    context = {'form':form}
    return render(request,'participant/form.html',context)

def all_participant(request):
    participants = Participant.objects.all()
    context = {'participants':participants}
    return render(request,'participant/list.html',context)

def participant_delete(request,id):
    if request.method == 'POST':
        participant = Participant.objects.get(id=id)
        participant.delete()
        messages.error(request,"Participant Deleted Successfully")
        return redirect('user')
    else:
        return redirect('user')
    
def participant_update(request,id):
    participant = Participant.objects.get(id=id)
    form = ParticipantModelForm(instance = participant)
    if request.method =='POST':
        form = ParticipantModelForm(request.POST,instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request,"Participant Updated Successfully")
            return redirect('user')

    context = {'form':form}
    return render(request,'participant/form.html',context)
def all_categories(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request,'category/list.html',context)

def category_delete(request,id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        messages.error(request,"Category Deleted Successfully")
        return redirect('user')
    else:
        return redirect('user')

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


