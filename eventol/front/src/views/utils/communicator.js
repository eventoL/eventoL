import {getWsUrl} from '../../utils/urls';
import WsCommunicator from '../../utils/WsCommunicator';

export const getCommunicator = properties =>
  new WsCommunicator({
    wsUrl: getWsUrl(properties.ws_protocol),
    reconnect: true,
  });

export default {
  getCommunicator,
};
