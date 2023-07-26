from ..models import Event
from datetime import timedelta


class EventService:
    def calculate_duration_in_hours(self, duration_days, duration_hours):
        return duration_days * 24 + duration_hours
      
    def create_event(self, user, title, start_date, duration_days, duration_hours=None, recurring=False, **kwargs):
        if not duration_hours:
            duration_hours = 0

        event = Event.objects.create(
            user=user,
            title=title,
            start_date=start_date,
            duration_days=duration_days,
            duration_hours=duration_hours,
            recurring=recurring,
            **kwargs
        )
        return event

    def update_event(self, event, title, start_date, duration_days, duration_hours=None, recurring=False, **kwargs):
        event.title = title
        event.start_date = start_date
        event.duration_days = duration_days
        event.duration_hours = duration_hours
        event.recurring = recurring
        for key, value in kwargs.items():
            setattr(event, key, value)
        event.save()
        return event

    def delete_event(self, event):
        event.delete()

    def get_event_by_id(self, event_id):
        try:
            event = Event.objects.get(pk=event_id)
            return event
        except Event.DoesNotExist:
            return None

    def get_all_events(self, user):
        events = Event.objects.filter(user=user)
        return events
    
    def create_recurring_events(self, event, end_date, recurrence_frequency):
        duration_in_hours = self.calculate_duration_in_hours(event.duration_days, event.duration_hours)

        current_date = event.start_date + timedelta(days=1)
        while current_date <= end_date:
            new_event = Event.objects.create(
                user=event.user,
                title=event.title,
                start_date=current_date,
                duration_days=event.duration_days,
                duration_hours=event.duration_hours,
                recurring=False,
                **{
                    'recurrence_frequency': recurrence_frequency,
                    'timezone': event.timezone,
                }
            )
            current_date += timedelta(days=1) if recurrence_frequency == 'daily' else timedelta(weeks=1) if recurrence_frequency == 'weekly' else timedelta(days=30)

        return event