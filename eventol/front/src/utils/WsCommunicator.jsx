import React from 'react';
import PropTypes from 'prop-types';


export default class WsCommunicator extends React.Component {
  static propTypes = {
    handleNotSupportWs: PropTypes.func,
    onClose: PropTypes.func,
    onMessage: PropTypes.func,
    onOpen: PropTypes.func,
    reconnect: PropTypes.bool,
    wsUrl: PropTypes.string.isRequired,
  }

  static defaultProps = {
    onOpen: evt => console.log('open', evt),
    onMessage: evt => console.log('message', evt),
    onClose: evt => console.warn('close', evt),
    handleNotSupportWs: evt => console.warn('close', evt),
    reconnect: true,
  }

  constructor(props){
    super(props);
    this.checkWebSocketSupport();
    const websocket = this.createWebSocket(props.wsUrl);
    this.state = {
      attempts: 1,
      onOpens: [props.onOpen],
      onMessages: [props.onMessage],
      onCloses: [props.onClose],
      handlesNotSupportWs: [props.handleNotSupportWs],
      websocket,
    };
  }

  onMessage = data => {
    const {onMessages} = this.state;
    onMessages.map(onMessageFunction => onMessageFunction && onMessageFunction(data));
  }

  onOpen = data => {
    const {onOpens} = this.state;
    onOpens.map(onOpenFunction => onOpenFunction && onOpenFunction(data));
  }

  onClose = data => {
    /* eslint-disable react/no-direct-mutation-state no-console */
    const {onCloses, attempts} = this.state;
    const {reconnect, wsUrl} = this.props;
    onCloses.map(onCloseFunction => onCloseFunction && onCloseFunction(data, reconnect));
    if (reconnect){
      const time = this.generateInterval(attempts);
      this.state.attempts += 1;
      setTimeout(() => {
        console.warn(`${gettext('Reconecting websocket, attemps')}: ${attempts}`);
        this.state.websocket = this.createWebSocket(wsUrl);
      }, time);
    }
    /* eslint-enable react/no-direct-mutation-state no-console */
  }

  generateInterval = attempts => {
    const seconds = Math.min(30, (2 ** attempts) - 1);
    return seconds * 1000;
  }

  handleNotSupportWs = () => {
    const {handlesNotSupportWs} = this.state;
    handlesNotSupportWs.map(hNotSupport => hNotSupport && hNotSupport());
  }

  createWebSocket(url){
    const websocket = new WebSocket(url);
    websocket.onopen = this.onOpen;
    websocket.onmessage = this.onMessage;
    websocket.onclose = this.onClose;
    return websocket;
  }

  addOnMessage(onMessageFunction){
    const {onMessages} = this.state;
    onMessages.push(onMessageFunction);
  }

  addOnOpen(onOpenFunction){
    const {onOpens} = this.state;
    onOpens.push(onOpenFunction);
  }

  addOnClose(onCloseFunction){
    const {onCloses} = this.state;
    onCloses.push(onCloseFunction);
  }

  addHandleNotSupportWs(hNotSupport){
    const {handlesNotSupportWs} = this.state;
    handlesNotSupportWs.push(hNotSupport);
  }

  checkWebSocketSupport(){
    const {handleNotSupportWs} = this.props;
    if (!WebSocket){
      const error = gettext('websocket not supported by your browser');
      if (handleNotSupportWs){
        return handleNotSupportWs(error);
      }
      throw error;
    }
    return null;
  }
}
