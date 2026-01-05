from django.urls import path
from  events.views import home,event_create,create_category,show_Detail,user_dashboard,event_delete,event_update,all_categories,category_update,category_delete,search_events,manager_dashboard,dashboard
urlpatterns = [
    path('manager-dashboard/', manager_dashboard,name='manager'),
    path('event-create/',event_create,name = 'create'),
    path('category-create/',create_category,name = 'create-category'),
    # path('create-participant/',create_participnat,name = 'create-participant'),
    # path('create-participant/',paricipant_create,name = 'create-participant'),
    path('user-dashboard/',user_dashboard,name='user'),
    # path("participant/",participant,name='participant'),
    path("update-event/<int:id>/",event_update,name ='update'),
    path("delete-event/<int:id>/",event_delete,name ='delete'),
    path("",home, name="home"),
    path("event-detail/<int:id>/",show_Detail, name="show-Detail"),
    # path("participants/",all_participant, name="list-participant"),
    # path("participants/update/<int:id>/",participant_update, name="participant_update"),
    # path("participants/delete/<int:id>/",participant_delete, name="participant_delete"),
    path("categories/",all_categories, name="list-category"),
    path("categories/update/<int:id>/",category_update, name="category_update"),
    path("categories/delete/<int:id>/",category_delete, name="category_delete"),
    path("search-events/",search_events, name="search_events"),
    path('dashboard/',dashboard,name='dashboard'),
    # path('rsvp/<int:event_id>/',rsvp_event,name='rsvp')

   
]