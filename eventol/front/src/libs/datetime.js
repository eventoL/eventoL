const start = () => {
  $('.timepicker').datetimepicker({
    format: 'HH:mm',
    icons: {
      time: 'fa fa-clock-o',
      date: 'fa fa-calendar',
      up: 'fa fa-arrow-up',
      down: 'fa fa-arrow-down',
    },
    stepping: 5,
  });
};

if (!window.libs) {
  window.libs = {};
}
window.libs.datetime = {
  start,
};
