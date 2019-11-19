import 'html5-qrcode/lib/jsqrcode-combined.min';
import 'html5-qrcode/lib/html5-qrcode.min';

import Logger from '../utils/logger';

const qrcodeInit = readerId => {
  const element = $(`#${readerId}`);
  $.fn.extend({
    html5_qrcode(qrcodeSuccess, qrcodeError, videoError) {
      return element.each(() => {
        let height = element.height();
        let width = element.width();

        if (height == null) {
          height = 250;
        }

        if (width == null) {
          width = 300;
        }

        const vidElem = $(
          `<video width="${width}px" height="${height}px"></video>`
        ).appendTo(element);
        const canvasElem = $(
          `<canvas id="qr-canvas" width="${width - 2}px" height="${height -
            2}px" style="display:none;"></canvas>`
        ).appendTo(element);

        const video = vidElem[0];
        const canvas = canvasElem[0];
        const context = canvas.getContext('2d');
        let localMediaStream;

        const scan = () => {
          if (localMediaStream) {
            context.drawImage(video, 0, 0, 307, 250);

            try {
              qrcode.decode();
            } catch (e) {
              qrcodeError(e, localMediaStream);
            }

            $.data(element[0], 'timeout', setTimeout(scan, 500));
          } else {
            $.data(element[0], 'timeout', setTimeout(scan, 500));
          }
        };

        navigator.getUserMedia =
          navigator.getUserMedia ||
          navigator.webkitGetUserMedia ||
          navigator.mediaDevices.getUserMedia ||
          navigator.msGetUserMedia;

        const successCallback = stream => {
          video.srcObject = stream;
          video.mozSrcObject = stream;
          localMediaStream = stream;
          $.data(element[0], 'stream', stream);

          video.play();
          $.data(element[0], 'timeout', setTimeout(scan, 1000));
        };

        // Call the getUserMedia method with our callback functions
        const errorCallback = error => videoError(error, localMediaStream);
        const constraints = {video: true};
        if (navigator.getUserMedia) {
          if (navigator.getUserMedia !== navigator.mediaDevices.getUserMedia) {
            navigator.getUserMedia(constraints, successCallback, errorCallback);
          } else {
            navigator.mediaDevices
              .getUserMedia(constraints)
              .then(successCallback)
              .catch(errorCallback);
          }
        } else {
          Logger.log(
            'Native web camera streaming (getUserMedia) not supported in this browser.'
          );
        }

        qrcode.callback = result => qrcodeSuccess(result, localMediaStream);
      }); // end of html5_qrcode
    },

    html5_qrcode_stop() {
      return element.each(() => {
        // stop the stream and cancel timeouts
        element
          .data('stream')
          .getVideoTracks()
          .forEach(videoTrack => videoTrack.stop());

        clearTimeout(element.data('timeout'));
      });
    },
  });
};

const qrStart = (readerId, callback, errorMessage) => {
  qrcodeInit(readerId);
  $(`#${readerId}`).empty();
  $(`#${readerId}`).html5_qrcode(
    callback,
    () => {},
    () => $('#error').html(errorMessage)
  );
};

const startAutoQr = (readerId, url, eventRegistrationCode, errorMessage) => {
  const callback = data => {
    $(window.location).attr(
      'href',
      `${url}/?event_registration_code=${eventRegistrationCode}&ticket=${data}`
    );
  };
  qrStart(readerId, callback, errorMessage);
};

const registrationQr = (modalId, readerId, errorMessage) => {
  const callback = data => {
    const url = $(window.location).attr('href');
    $(window.location).attr('href', `${url}/${data}`);
  };
  qrStart(readerId, callback, errorMessage);
};

const stop = readerId => {
  $(`#${readerId}`).html5_qrcode_stop();
};

if (!window.libs) {
  window.libs = {};
}
window.libs.qrcode = {
  registrationQr,
  startAutoQr,
  qrStart,
  stop,
};
