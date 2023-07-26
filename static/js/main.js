var eventId = null;

document.addEventListener('DOMContentLoaded', function () {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: '/calendar/api/events/',
    editable: true,
    selectable: true,
    dayMaxEvents: true,
    displayEventEnd: true,
    dateClick: function (info) {
      $('#addEventModal').modal('show');
      $('#id_start_date').val(info.dateStr + 'T00:00');
      $('#id_end_date').val(info.dateStr + 'T00:00');
    },
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    titleFormat: {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    },

    select: function (info) {
      $('#addEventModal').modal('show');
      $('#addEventForm #id_start_date').val(formatDateForDatetimeLocal(info.startStr));
      $('#addEventForm #id_end_date').val(formatDateForDatetimeLocal(info.startStr));
      $('#addEventForm #id_duration_days').val(1);
    },

    eventClick: function (info) {
      $('#editEventModal').modal('show');
      eventId = info.event.id;
      var timezoneValue = info.event.timezone;
      $('#editEventForm #event_id').val(eventId);
      $('#editEventForm #id_title').val(info.event.title);
      $('#editEventForm #id_start_date').val(formatDateForDatetimeLocal(info.event.start));
      $('#editEventForm #id_end_date').val(formatDateForDatetimeLocal(info.event.end));
      $('#editEventForm #id_timezone').val(timezoneValue).trigger('change');
    },

  });

  // Send form
  $('#addEventForm').submit(function (e) {
    e.preventDefault();
    var form_data = new FormData(this);
    fetch('/calendar/api/events/add/', {
      method: 'POST',
      body: form_data,
      credentials: 'same-origin',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
      .then(response => {
        if (response.ok) {
          // Clean form
          $('#addEventForm')[0].reset();
          $('#addEventModal').modal('hide');
          calendar.refetchEvents();
        } else {
          console.log('Error:', response.statusText);
        }
      })
      .catch(error => {
        console.log('Error:', error);
      });
  });

  $('#editEventForm').submit(function (e) {
    e.preventDefault();
    var form_data = new FormData(this);
    var id = eventId;

    fetch(`/calendar/api/events/edit/${id}/`, {
      method: 'POST',
      body: form_data,
      credentials: 'same-origin',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
      .then(response => {
        if (response.ok) {
          // Clean form
          $('#editEventForm')[0].reset();
          $('#editEventModal').modal('hide');
          calendar.refetchEvents();
        } else {
          console.log('Error:', response.statusText);
        }
      })
      .catch(error => {
        console.log('Error:', error);
      });
  });

  $('#deleteEventButton').click(function () {
    if (confirm("Tem certeza de que deseja excluir este evento?")) {
      var id = eventId;

      fetch(`/calendar/api/events/delete/${id}/`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': getCookie('csrftoken')
        }
      })
        .then(response => {
          if (response.ok) {
            alert("Evento excluído com sucesso!");
            $('#editEventModal').modal('hide');
            calendar.refetchEvents();
          } else {
            console.log('Error:', response.statusText);
          }
        })
        .catch(error => {
          console.log('Error:', error);
        });
    }
  });

  // Get 'csrftoken'
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Verificar se o cookie começa com o nome 'csrftoken'
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  calendar.render();
});

function toggleRecurrenceFields() {
  if ($('#id_recurring').prop('checked')) {
    $('#recurrence_fields').show();
  } else {
    $('#recurrence_fields').hide();
  }
}

$('#id_recurring').on('change', function() {
  toggleRecurrenceFields();
});

toggleRecurrenceFields();

function formatDateForDatetimeLocal(dateStr) {
  let dateObj = new Date(dateStr);
  let year = dateObj.getUTCFullYear();
  let month = (dateObj.getUTCMonth() + 1).toString().padStart(2, '0');
  let day = dateObj.getUTCDate().toString().padStart(2, '0');
  let hours = dateObj.getUTCHours().toString().padStart(2, '0');
  let minutes = dateObj.getUTCMinutes().toString().padStart(2, '0');
  return `${year}-${month}-${day}T${hours}:${minutes}`;
}