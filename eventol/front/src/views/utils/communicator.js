import {getWsUrl} from '../../utils/urls';
import WsCommunicator from '../../utils/WsCommunicator';

export const getCommunicator = properties =>
  new WsCommunicator(getWsUrl(properties.ws_protocol));

export default {
  getCommunicator,
};
