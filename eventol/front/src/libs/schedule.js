import 'fullcalendar/dist/fullcalendar.css';
import 'fullcalendar-scheduler/dist/scheduler.css';

import 'moment';
import 'fullcalendar/dist/fullcalendar';
import 'fullcalendar-scheduler/dist/scheduler';

import './schedule.scss';

const DEFAULT_CALENDAR_OPTIONS = {
  schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
  defaultView: 'agendaDay',
  header: false,
  height: 'auto',
  timeFormat: 'H:mm',
  slotLabelFormat: ['H:mm'],
  eventColor: '#0288d1',
  slotDuration: '00:10',
  allDaySlot: false,
};

const loadSchedule = (rooms, activities) => {
  Object.keys(activities).forEach(date => {
    const activitiesPerDay = JSON.parse(activities[date]);
    const calendarOptions = {
      ...DEFAULT_CALENDAR_OPTIONS,
      resources: rooms,
      defaultDate: activitiesPerDay.date,
      scrollTime: activitiesPerDay.min_time,
      minTime: activitiesPerDay.min_time,
      maxTime: activitiesPerDay.max_time,
      events: activitiesPerDay.activities,
    };
    $(`#calendar-${date}`).fullCalendar(calendarOptions);
  });
};

if (!window.libs) {
  window.libs = {};
}
window.libs.schedule = loadSchedule;
