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
        selectable: true,
        editable: true,
        select: function(start, end) {
            $('#eventModal').css('display', 'block');
            $('#start').val(start.format());
            $('#end').val(end.format());

            $('.close').click(function() {
                $('#eventModal').css('display', 'none');
            });

            $('#eventForm').off('submit').on('submit', function(e) {
                e.preventDefault();
                var title = $('#title').val();
                var start = $('#start').val();
                var end = $('#end').val();

                // Disable the submit button to prevent multiple submissions
                $('#submitBtn').prop('disabled', true);

                $.ajax({
                    url: '/events',
                    type: 'POST',
                    data: {
                        title: title,
                        start: start,
                        end: end
                    },
                    success: function(response) {
                        console.log(response.message);
                        $('#calendar').fullCalendar('refetchEvents');
                        $('#eventModal').css('display', 'none');
                        // Enable the submit button after successful submission
                        $('#submitBtn').prop('disabled', false);
                    },
                    error: function(xhr, status, error) {
                        console.log(error);
                        alert('An error occurred. Please try again.');
                        // Enable the submit button after an error occurs
                        $('#submitBtn').prop('disabled', false);
                    }
                });
            });
        },
        eventClick: function(calEvent, jsEvent, view) {
            var eventTitle = calEvent.title;
            if (confirm('Are you sure you want to delete the event "' + eventTitle + '"?')) {
                $.ajax({
                    url: '/events/' + calEvent.id,
                    type: 'DELETE',
                    success: function(response) {
                        console.log(response.message);
                        $('#calendar').fullCalendar('refetchEvents');
                        // Remove the event from the running events list
                        $('#event-' + calEvent.id).remove();
                    },
                    error: function(xhr, status, error) {
                        console.log(error);
                        alert('An error occurred. Please try again.');
                    }
                });
            }
        },
        events: '/events',
        eventRender: function(event, element) {
            var eventId = event.id;
            var eventTitle = event.title;
            var eventStart = moment(event.start).format('YYYY-MM-DD HH:mmA');
            var eventEnd = moment(event.end).format('YYYY-MM-DD HH:mmA');
            var eventStartTime = moment(event.start).format('hh:mmA');
            var eventEndTime = moment(event.end).format('hh:mmA');

            // Add the event unique colors to the event element
            if (!eventColors[eventTitle]) {
                var colorCount = Object.keys(eventColors).length % 6; // Change the number 6 to the desired number of colors
                eventColors[eventTitle] = 'event-color-' + (colorCount + 1);
            }
            element.addClass(eventColors[eventTitle]);

            // Truncate the event title if it exceeds the maximum length
            var maxTitleLength = 12; // Define the maximum length of the event title
            var truncatedTitle = eventTitle.length > maxTitleLength ? eventTitle.substr(0, maxTitleLength) + '...' : eventTitle;
            element.find('.fc-title').text(truncatedTitle);

            // Add a tooltip to display the full event title on hover
            element.find('.fc-title').attr('title', eventTitle);
            
            // Customize the display of the event title 
            //element.find('.fc-title').text(eventTitle);
            element.find('.fc-time').text(eventStartTime);

            element.find('.fc-title').css({
                'font-weight': 'bold',
                'font-family': 'Tahoma, Verdana, Segoe, sans-serif',
                'color': '#000' // Update font color here
            });   
            element.find('span.fc-time').css({
                'font-weight': 'bold',
                'font-family': 'Tahoma, Verdana, Segoe, sans-serif',
                'color': '#000' // Update font color here
            });                    

            // Add event to the running events list
            if (!uniqueEventIds.includes(eventId)) {
                uniqueEventIds.push(eventId);
                var eventListItem = '<li id="event-' + eventId + '" class="' + eventColors[eventTitle] +  '">' +
                    '<h3><strong>' + eventTitle + '</h3><br>' +
                    'Start: ' + eventStart + '<br><br>' +
                    'End: ' + eventEnd +
                    '</li></strong>';
                $('#eventList').append(eventListItem);
            }

            // Check if event end date has passed and delete the event if necessary
            var currentDate = moment().format('YYYY-MM-DD HH:mm');
            if (currentDate > eventEnd) {
                $('#calendar').fullCalendar('removeEvents', eventId);
                $('#event-' + eventId).remove();
            }

        },
        eventAfterAllRender: function(view) {
            $('.event-group').click(function() {
                $(this).toggleClass('show-more');
            });
        }
    });
});