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
      dots: true
    }
  }, {
    breakpoint: 900,
    settings: {
      slidesToShow: 2,
      slidesToScroll: 2,
      initialSlide: 2
    }
  }, {
    breakpoint: 610,
    settings: {
      slidesToShow: 1,
      slidesToScroll: 1
    }
  }]
};
