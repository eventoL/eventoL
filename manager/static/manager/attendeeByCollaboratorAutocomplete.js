$(document).ready(function () {
    $('body').on('change', '.autocomplete-light-widget select[name$=sede]', function () {
        var sedeSelectElement = $(this);
        var attendeeSelectElement = $('#' + $(this).attr('id').replace('sede', 'attendee'));
        var attendeeWidgetElement = attendeeSelectElement.parents('.autocomplete-light-widget');

        // When the Sede select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            attendeeWidgetElement.yourlabsWidget().autocomplete.data = {
                'sede_id': value[0],
            };
        } else {
            // If value is empty, empty autocomplete.data
            attendeeWidgetElement.yourlabsWidget().autocomplete.data = {}
        }
    })
});
