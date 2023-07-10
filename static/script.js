// JavaScript code for calendar interaction

// Fetch events from the server and populate the calendar
function fetchEvents() {
  fetch('/get_events')
      .then(response => response.json())
      .then(data => {
          if (data.events) {
              data.events.forEach(event => {
                  const { date, title } = event;
                  const cell = document.querySelector(`[data-date="${date}"]`);
                  if (cell) {
                      const eventDiv = document.createElement('div');
                      eventDiv.classList.add('event');
                      eventDiv.textContent = title;
                      cell.appendChild(eventDiv);
                  }
              });
          }
      })
      .catch(error => console.log(error));
}

// Add an event to the calendar
function addEvent(event) {
  event.preventDefault();

  const title = document.getElementById('event-title').value;
  const date = document.getElementById('event-date').value;
  const time = document.getElementById('event-time').value;

  fetch('/add_event', {
      method: 'POST',
      body: JSON.stringify({ title, date, time }),
      headers: {
          'Content-Type': 'application/json'
      }
  })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              const cell = document.querySelector(`[data-date="${date}"]`);
              if (cell) {
                  const eventDiv = document.createElement('div');
                  eventDiv.classList.add('event');
                  eventDiv.textContent = title;
                  cell.appendChild(eventDiv);
              }

              document.getElementById('event-form').reset();
              document.getElementById('event-submit-button').disabled = true;
              document.getElementById('event-form-title').textContent = 'Add Event';
          }
      })
      .catch(error => console.log(error));
}

// Clear all events from the calendar
function clearEvents() {
  const events = document.querySelectorAll('.event');
  events.forEach(event => event.remove());
}

// Initialize the calendar and event form
document.addEventListener('DOMContentLoaded', () => {
  const currentDate = new Date();
  const currentMonth = currentDate.getMonth();
  const currentYear = currentDate.getFullYear();

  const calendarBody = document.getElementById('calendar-body');
  const currentMonthText = document.getElementById('current-month');
  const eventForm = document.getElementById('event-form');
  const eventSubmitButton = document.getElementById('event-submit-button');

  // Set the initial values
  currentMonthText.textContent = `${currentYear} - ${currentMonth + 1}`;

  // Render the calendar
  function renderCalendar(year, month) {
      const firstDay = new Date(year, month, 1).getDay();
      const lastDate = new Date(year, month + 1, 0).getDate();

      clearEvents();
      calendarBody.innerHTML = '';

      let date = 1;
      for (let week = 0; week < 6; week++) {
          const row = document.createElement('tr');

          for (let day = 0; day < 7; day++) {
              const cell = document.createElement('td');
              if (week === 0 && day < firstDay) {
                  cell.classList.add('disabled');
              } else if (date > lastDate) {
                  cell.classList.add('disabled');
              } else {
                  cell.textContent = date;
                  cell.dataset.date = `${year}-${month + 1}-${date}`;
                  date++;

                  cell.addEventListener('click', function () {
                      const selectedDate = this.dataset.date;
                      document.getElementById('event-date').value = selectedDate;
                      document.getElementById('event-submit-button').disabled = false;
                      document.getElementById('event-form-title').textContent = `Add Event on ${selectedDate}`;
                  });
              }

              row.appendChild(cell);
          }

          calendarBody.appendChild(row);
      }

      fetchEvents();
  }

  renderCalendar(currentYear, currentMonth);

  eventForm.addEventListener('submit', addEvent);
});


// Selecting the sidebar and buttons
const sidebar = document.querySelector(".sidebar");
const sidebarOpenBtn = document.querySelector("#sidebar-open");
const sidebarCloseBtn = document.querySelector("#sidebar-close");

// Function to hide the sidebar when the mouse leaves
const hideSidebar = () => {
  sidebar.classList.add("close");
};

// Function to show the sidebar when the mouse enters
const showSidebar = () => {
  sidebar.classList.remove("close");
};

// Function to show and hide the sidebar
const toggleSidebar = () => {
  sidebar.classList.toggle("close");
};

// If the window width is less than 800px, close the sidebar
if (window.innerWidth < 800) {
  sidebar.classList.add("close");
}

// Adding event listeners to buttons and sidebar for the corresponding actions
sidebar.addEventListener("mouseleave", hideSidebar);
sidebar.addEventListener("mouseenter", showSidebar);
sidebarOpenBtn.addEventListener("click", toggleSidebar);
sidebarCloseBtn.addEventListener("click", toggleSidebar);
