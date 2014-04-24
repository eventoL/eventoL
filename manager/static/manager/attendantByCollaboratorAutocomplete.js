$(document).ready(function() {
    $('body').on('change', '.autocomplete-light-widget select[name$=sede]', function() {
        var sedeSelectElement = $(this);
        var attendantSelectElement = $('#' + $(this).attr('id').replace('sede', 'attendant'));
        var attendantWidgetElement = attendantSelectElement.parents('.autocomplete-light-widget');

        // When the Sede select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            attendantWidgetElement.yourlabsWidget().autocomplete.data = {
                'sede_id': value[0],
            };
        } else {
            // If value is empty, empty autocomplete.data
            attendantWidgetElement.yourlabsWidget().autocomplete.data = {}
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(attendantWidgetElement, 'data is', attendantWidgetElement.yourlabsWidget().autocomplete.data)
    })
});
