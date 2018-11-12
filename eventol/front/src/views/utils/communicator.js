import {getWsUrl} from '../../utils/urls';
import WsCommunicator from '../../utils/WsCommunicator';


/* eslint-disable-next-line import/prefer-default-export */
export const getCommunicator = properties => new WsCommunicator({
  wsUrl: getWsUrl(properties.ws_protocol),
  reconnect: true,
});
