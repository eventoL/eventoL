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

  createWebSocket(url){
    const websocket = new WebSocket(url);
    websocket.onopen = this.onOpen.bind(this);
    websocket.onmessage = this.onMessage.bind(this);
    websocket.onclose = this.onClose.bind(this);
    return websocket;
  }

  onMessage(data){
    const {onMessages} = this.state;
    onMessages.map(onMessageFunction => onMessageFunction && onMessageFunction(data));
  }

  onOpen(data){
    const {onOpens} = this.state;
    onOpens.map(onOpenFunction => onOpenFunction && onOpenFunction(data));
  }

  generateInterval(attempts){
    const seconds = Math.min(30, (Math.pow(2, attempts) - 1));
    return seconds * 1000;
  }

  onClose(data){
    /* eslint-disable react/no-direct-mutation-state */
    const {onCloses} = this.state;
    onCloses.map(onCloseFunction => onCloseFunction && onCloseFunction(data, this.props.reconnect));
    if (this.props.reconnect){
      const time = this.generateInterval(this.state.attempts);
      this.state.attempts += 1;
      setTimeout(() => {
        console.warn(`${gettext('Reconecting websocket, attemps')}: ${this.state.attempts}`);
        this.state.websocket = this.createWebSocket(this.props.ws_url);
      }, time);
    }
    /* eslint-enable react/no-direct-mutation-state */
  }

  handleNotSupportWs(){
    const {handlesNotSupportWs} = this.state;
    handlesNotSupportWs.map(hNotSupport => hNotSupport && hNotSupport());
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
    if (!WebSocket){
      const error = gettext('websocket not supported by your browser');
      if (this.props.handleNotSupportWs){
        return this.props.handleNotSupportWs(error);
      }
      throw error;
    }
  }
}
