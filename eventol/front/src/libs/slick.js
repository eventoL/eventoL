import './slick.scss';

import 'slick';
import 'slick-carousel/slick/slick';

const startSlick = (id, autoplay = true, dots = true) => {
  const elementId = `#${id}`;
  const element = $(elementId);

  element.slick({
    autoplay,
    dots,
  });

  let isPlaying = autoplay;

  const onClick = () => {
    const action = isPlaying ? 'slickPause' : 'slickPlay';
    isPlaying = !isPlaying;
    element.slick('slickSetOption', 'autoplay', isPlaying).slick(action);
  };

  element.click(onClick);
};

if (!window.libs) {
  window.libs = {};
}
window.libs.slick = startSlick;
