from django.urls import path
from . import views
from events.views import manager_dashboard,user_dashboard,event_create,event_update,event_delete

urlpatterns = [
    path('manager-dashboard/', manager_dashboard,name='manager'),
    path('hello/',event_create,name = 'create'),
    path('user-dashboard/',user_dashboard,name='user'),
    # path("task-form/",hello),
    path("update-event/<int:id>/",event_update,name ='update'),
    path("delete-event/<int:id>/",event_delete,name ='delete'),


    # path('user-dashboard/', user_dashboard),
    # path('test/', test)
]