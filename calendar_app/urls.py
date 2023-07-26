from django.urls import path
from .views import CalendarHomeView, AddEventView, EventListView, EditEventView, DeleteEventView
from calendar_app.utils.utils import custom_authentication_required


app_name = 'calendar_app'


urlpatterns = [
    path('calendar/', custom_authentication_required(CalendarHomeView.as_view()), name='calendar_home'),
    path('calendar/api/events/add/', custom_authentication_required(AddEventView.as_view()), name='add_event'),
    path('calendar/api/events/edit/<int:event_id>/', custom_authentication_required(EditEventView.as_view()), name='edit_event'),
    path('calendar/api/events/delete/<int:event_id>/', custom_authentication_required(DeleteEventView.as_view()), name='delete_event'),
    path('calendar/api/events/', custom_authentication_required(EventListView.as_view()), name='event_list'),
]