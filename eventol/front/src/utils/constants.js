export const MOBILE_WIDTH = 950;
export const LOGO_LANDING_DEFAULT = '/static/manager/img/logo.png';
export const BACKGROUND_DEFAULT = '/static/manager/img/background.png';
export const LOGO_HEADER_DEFAULT = '/static/manager/img/eventol-white.png';
export const REPORT_REQUIRED_FIELDS = 'name,event_slug,email,location,report,id,tags';
export const HOME_REQUIRED_FIELDS = 'event_slug,place,image,name,attendees_count,abstract,tags';

export const SLIDER_BASE_SETTINGS = {
  variableWidth: false,
  dots: true,
  infinite: false,
  speed: 500,
  slidesToShow: 4,
  slidesToScroll: 4,
  initialSlide: 0,
  responsive: [{
    breakpoint: 1290,
    settings: {
      slidesToShow: 3,
      slidesToScroll: 3,
      infinite: true,
      dots: true,
    },
  }, {
    breakpoint: 900,
    settings: {
      slidesToShow: 2,
      slidesToScroll: 2,
      initialSlide: 2,
    },
  }, {
    breakpoint: 610,
    settings: {
      slidesToShow: 1,
      slidesToScroll: 1,
    },
  }],
};
