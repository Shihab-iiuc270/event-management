from django.shortcuts import render,redirect
from django.http import HttpResponse
from events.forms import EventModelForm,CategoryModelForm,ParticipantModelForm
from events.models import Event,Category,Participant
from datetime import date
from django.db.models import Q,Count,Max,Min,Avg
from django.contrib import messages


def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")


def user_dashboard(request):
    type = request.GET.get('type', 'all')
    cat = request.GET.get('cat')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    search = request.GET.get('q')

    base_q = Event.objects.select_related('category').prefetch_related('assign_to')
    events = base_q.all()

    today = base_q.filter(date=date.today())
    if search :
        events = events.filter(
            Q(name__icontains=search) | 
            Q(location__icontains=search)
        )
    if cat:
        events = events.filter(category__name=cat)

    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])


    if type == 'todays_event':
        events = today
    elif type == 'upcoming_event':
        events = base_q.filter(date__gt=date.today())
    elif type == 'past_event':
        events = base_q.filter(date__lt=date.today())
    total_paricipants = Event.objects.aggregate(total=Count('assign_to', distinct=True))
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
        'today': today,
        'counts': counts,
        'categorys': categorys,
        'total_participants': total_paricipants
    }

    return render(request, "dashboard/user_dashboard.html", context)



def event_create(request):
    particapnt = Participant.objects.all()
    form = EventModelForm()
    if request.method =='POST':
        form = EventModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Event Created Successfully")
            return redirect('user')

    context = {'form':form}
    return render(request,'event_form.html',context)



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