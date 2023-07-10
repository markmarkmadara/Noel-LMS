$(document).ready(function() {
    var eventColors = {};
    var uniqueEventIds = [];

    $('#calendar').fullCalendar({
        header:{
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        defaultView: 'month',
        events: '/events',
        eventRender: function(event, element) {
            var eventId = event.id;
            var eventTitle = event.title;
            var eventStart = moment(event.start).format('YYYY-MM-DD HH:mmA');
            var eventEnd = moment(event.end).format('YYYY-MM-DD HH:mmA');
            var eventStartTime = moment(event.start).format('hh:mmA');
            var eventEndTime = moment(event.end).format('hh:mmA');

            if (!eventColors[eventTitle]) {
                var colorCount = Object.keys(eventColors).length % 6;
                eventColors[eventTitle] = 'event-color-' + (colorCount + 1);
            }
            element.addClass(eventColors[eventTitle]);

            var maxTitleLength = 12;
            var truncatedTitle = eventTitle.length > maxTitleLength ? eventTitle.substr(0, maxTitleLength) + '...' : eventTitle;
            element.find('.fc-title').text(truncatedTitle);
            element.find('.fc-title').attr('title', eventTitle);
            element.find('.fc-time').text(eventStartTime);

            element.find('.fc-title').css({
                'font-weight': 'bold',
                'font-family': 'Tahoma, Verdana, Segoe, sans-serif',
                'color': '#000'
            });
            element.find('span.fc-time').css({
                'font-weight': 'bold',
                'font-family': 'Tahoma, Verdana, Segoe, sans-serif',
                'color': '#000'
            });

            if (!uniqueEventIds.includes(eventId)) {
                uniqueEventIds.push(eventId);
                var eventListItem = '<li id="event-' + eventId + '" class="' + eventColors[eventTitle] +  '">' +
                    '<h3><strong>' + eventTitle + '</h3><br>' +
                    'Start: ' + eventStart + '<br><br>' +
                    'End: ' + eventEnd +
                    '</li></strong>';
                $('#eventList').append(eventListItem);
            }


            var currentDate = moment().format('YYYY-MM-DD HH:mm');
            var eventEndDate = moment(event.end).format('YYYY-MM-DD HH:mm');
            if (eventEndDate < currentDate) {
                element.css('opacity', '0.6');
            }

                        // Check if event end date has passed and delete the event if necessary
                        var currentDate = moment().format('YYYY-MM-DD HH:mm');
                        if (currentDate > eventEnd) {
                            $('#calendar').fullCalendar('removeEvents', eventId);
                            $('#event-' + eventId).remove();
                        }
        }
    });
});