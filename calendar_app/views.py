from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .forms import EventForm
from .services.event_service import EventService


from .models import Event


class CalendarHomeView(View):
    def get(self, request, *args, **kwargs):
        event_form = EventForm()
        return render(request, 'calendar_app/calendar_home.html', {'event_form': event_form})


class AddEventView(View):
    def post(self, request, *args, **kwargs):
        try:
            event_form = EventForm(request.POST)
            if event_form.is_valid():
                event_service = EventService()

                # Extract form data
                title = event_form.cleaned_data['title']
                start_date = event_form.cleaned_data['start_date']
                end_date = event_form.cleaned_data['end_date']
                duration_days = event_form.cleaned_data['duration_days']
                duration_hours = event_form.cleaned_data['duration_hours']
                recurring = event_form.cleaned_data['recurring']
                recurrence_frequency = event_form.cleaned_data['recurrence_frequency']

                # Calculate duration in hours
                duration_in_hours = event_service.calculate_duration_in_hours(duration_days, duration_hours)

                # Create the event
                event = event_service.create_event(
                    user=request.user,
                    title=title,
                    start_date=start_date,
                    end_date=end_date,
                    duration_days=duration_days,
                    duration_hours=duration_hours,
                    recurring=recurring,
                    recurrence_frequency=recurrence_frequency,
                    timezone=event_form.cleaned_data['timezone'],
                )

                # If recurring, create recurring events
                if recurring:
                    event_service.create_recurring_events(event, end_date, recurrence_frequency)

                return JsonResponse({'message': 'Event created successfully'}, status=201)
            else:
                return JsonResponse({'errors': event_form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class EventListView(View):
    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(user=request.user)
        data = [{'id': event.id, 'title': event.title, 'start': event.start_date.isoformat(), 'end': event.end_date.isoformat(), 'timezone': event.timezone,} for event in events]
        return JsonResponse(data, safe=False)
    

class EditEventView(View):
    def post(self, request, *args, **kwargs):
        try:
            event_id = kwargs.get('event_id')
            event = Event.objects.get(id=event_id, user=request.user)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found or does not belong to the current user'}, status=404)

        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_service = EventService()
            event_service.update_event(
                event=event,
                title=event_form.cleaned_data['title'],
                start_date=event_form.cleaned_data['start_date'],
                end_date=event_form.cleaned_data['end_date'],
                duration_days=event_form.cleaned_data['duration_days'],
                duration_hours=event_form.cleaned_data['duration_hours'],
            )
            return JsonResponse({'message': 'Event updated successfully'}, status=200)
        else:
            return JsonResponse({'errors': event_form.errors}, status=400)


class DeleteEventView(View):
    def post(self, request, *args, **kwargs):
        try:
            event_id = kwargs.get('event_id')
            event = Event.objects.get(id=event_id, user=request.user)
            event.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
