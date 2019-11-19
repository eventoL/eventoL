import ClipboardJS from 'clipboard';

const start = () => {
  // eslint-disable-next-line no-new
  new ClipboardJS('.dropdown-item');
};

if (!window.libs) {
  window.libs = {};
}
window.libs.clipboard = {
  start,
};
