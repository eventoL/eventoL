const place1 = {
  address_components: [
    {long_name: '1667', short_name: '1667', types: ['street_number']},
    {long_name: 'Ayacucho', short_name: 'Ayacucho', types: ['route']},
    {
      long_name: 'Centro',
      short_name: 'Centro',
      types: ['neighborhood', 'political'],
    },
    {
      long_name: 'Rosario',
      short_name: 'Rosario',
      types: ['locality', 'political'],
    },
    {
      long_name: 'Departamento Rosario',
      short_name: 'Departamento Rosario',
      types: ['administrative_area_level_2', 'political'],
    },
    {
      long_name: 'Santa Fe',
      short_name: 'Santa Fe',
      types: ['administrative_area_level_1', 'political'],
    },
    {long_name: 'Argentina', short_name: 'AR', types: ['country', 'political']},
    {long_name: 'S2000', short_name: 'S2000', types: ['postal_code']},
    {long_name: 'BYS', short_name: 'BYS', types: ['postal_code_suffix']},
  ],
  formatted_address: 'Ayacucho 1667, S2000BYS Rosario, Santa Fe, Argentina',
  geometry: {
    location: {lat: -32.9586923, lng: -60.629729},
    location_type: 'ROOFTOP',
    viewport: {
      south: -32.9600412802915,
      west: -60.63107798029148,
      north: -32.9573433197085,
      east: -60.628380019708516,
    },
  },
  place_id: 'ChIJ7QvrMwCrt5URpyBml6doLnY',
  plus_code: {
    compound_code: '29RC+G4 Rosario, Santa Fe, Argentina',
    global_code: '47VX29RC+G4',
  },
  types: ['street_address'],
};

const place2 = {
  address_components: [
    {long_name: '1551', short_name: '1551', types: ['street_number']},
    {long_name: 'Sarmiento', short_name: 'Sarmiento', types: ['route']},
    {
      long_name: 'San Nicolás',
      short_name: 'San Nicolás',
      types: ['political', 'sublocality', 'sublocality_level_1'],
    },
    {
      long_name: 'Comuna 1',
      short_name: 'Comuna 1',
      types: ['administrative_area_level_2', 'political'],
    },
    {
      long_name: 'Buenos Aires',
      short_name: 'CABA',
      types: ['administrative_area_level_1', 'political'],
    },
    {long_name: 'Argentina', short_name: 'AR', types: ['country', 'political']},
    {long_name: 'C1042', short_name: 'C1042', types: ['postal_code']},
    {long_name: 'ABC', short_name: 'ABC', types: ['postal_code_suffix']},
  ],
  formatted_address: 'Sarmiento 1551, C1042ABC CABA, Argentina',
  geometry: {
    location: {lat: -34.6052436, lng: -58.388569700000005},
    location_type: 'ROOFTOP',
    viewport: {
      south: -34.6065925802915,
      west: -58.38991868029149,
      north: -34.60389461970851,
      east: -58.387220719708466,
    },
  },
  place_id: 'ChIJbXpzCcTKvJURbeIVAyh6SnU',
  plus_code: {
    compound_code: '9JV6+WH Buenos Aires, Argentina',
    global_code: '48Q39JV6+WH',
  },
  types: ['street_address'],
};

export const event1 = {
  attendees: 10,
  backdrop: 'event1backdrop',
  eventSlug: 'event1slug',
  overview: 'event1overview',
  place: JSON.stringify(place1),
  tags: [
    {
      name: 'slug-name',
      slug: 'slug-slug',
    },
  ],
  title: 'event 1',
  url: 'event1Url',
  id: 1,
};

export const event2 = {
  attendees: 25,
  backdrop: 'event2backdrop',
  eventSlug: 'event2slug',
  overview: 'event2overview',
  place: JSON.stringify(place2),
  tags: [
    {
      name: 'slug-name',
      slug: 'slug-slug',
    },
  ],
  title: 'event 2',
  url: 'event2Url',
  id: 2,
};

export const events = [event1, event2];

export default {
  event1,
  event2,
  events,
};
