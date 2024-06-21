import {MOBILE_WIDTH} from './constants';

export const focusOn = id => {
  document.getElementById(id).focus();
};

export const mapSizesToProps = ({width}) => ({
  isMobile: width < MOBILE_WIDTH,
});
