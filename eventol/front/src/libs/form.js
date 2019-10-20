import 'bootstrap-datepicker/dist/css/bootstrap-datepicker3.css';

require('bootstrap-datepicker/js/bootstrap-datepicker');
require('bootstrap-datepicker/js/locales/bootstrap-datepicker.es');
require('geocomplete/jquery.geocomplete.min');
require('./jquery.formset');

const loadForm = (placeLabel, limitProposalLabel) => {
  $('#geocomplete').geocomplete({
    map: '.map_canvas',
    types: ['geocode', 'establishment'],
  });

  $('#geocomplete').bind('geocode:result', (_, result) => {
    $(`#${placeLabel}`).val(JSON.stringify(result));
  });

  let place = $(`#${placeLabel}`).val();

  if (place !== '') {
    place = JSON.parse(place);
    $('#geocomplete').geocomplete('find', place.formatted_address);
  }

  $('.limit-proposal-picker')
    .datepicker({
      format: 'yyyy-mm-dd',
    })
    .on('changeDate', () => {
      $(`#${limitProposalLabel}`).val(
        $('.limit-proposal-picker').datepicker('getFormattedDate')
      );
    });

  const limitProposalDate = $(`#${limitProposalLabel}`).val();
  if (limitProposalDate !== '') {
    $('.limit-proposal-picker').datepicker('setDate', limitProposalDate);
  }

  $('#event-date-formset').formset({
    animateForms: true,
  });

  $('#event-date-formset').on('formAdded', event => {
    const inputs = $(event.target).find(':input');
    $.each(inputs, (_, input) => {
      const $input = $(input);
      if ($input.attr('type') !== 'button') {
        $(input).addClass('form-control');
      }
    });
  });

  $('#contacts-formset').formset({
    animateForms: true,
  });

  $('#contacts-formset').on('formAdded', event => {
    const inputs = $(event.target).find(':input');
    $.each(inputs, (_, input) => {
      const $input = $(input);
      if ($input.attr('type') !== 'button') {
        $(input).addClass('form-control');
      }
    });
  });
};

if (!window.libs) {
  window.libs = {};
}
window.libs.form = loadForm;
