import Logger from './logger';

export default class WsCommunicator {
  constructor(
    wsUrl,
    handleNotSupportWs = evt => Logger.warning('close', evt),
    onClose = evt => Logger.warning('close', evt),
    onMessage = evt => Logger.log('message', evt),
    onOpen = evt => Logger.log('open', evt),
    reconnect = true
  ) {
    this.checkWebSocketSupport();
    this.websocket = this.createWebSocket(wsUrl);
    this.attempts = 1;
    this.reconnect = reconnect;
    this.onOpens = [onOpen];
    this.onMessages = [onMessage];
    this.onCloses = [onClose];
    this.handlesNotSupportWs = [handleNotSupportWs];
  }

  onMessage = data => {
    this.onMessages.map(
      onMessageFunction => onMessageFunction && onMessageFunction(data)
    );
  };

  onOpen = data => {
    this.onOpens.map(onOpenFunction => onOpenFunction && onOpenFunction(data));
  };

  onClose = data => {
    this.onCloses.map(
      onCloseFunction =>
        onCloseFunction && onCloseFunction(data, this.reconnect)
    );
    if (this.reconnect) {
      const time = this.generateInterval(this.attempts);
      this.attempts += 1;
      setTimeout(() => {
        Logger.warning(
          `${gettext('Reconecting websocket, attemps')}: ${this.attempts}`
        );
        this.websocket = this.createWebSocket(this.wsUrl);
      }, time);
    }
  };

  generateInterval = attempts => {
    const seconds = Math.min(30, 2 ** attempts - 1);
    return seconds * 1000;
  };

  handleNotSupportWs = () => {
    this.handlesNotSupportWs.map(hNotSupport => hNotSupport && hNotSupport());
  };

  createWebSocket = url => {
    const websocket = new WebSocket(url);
    websocket.onopen = this.onOpen;
    websocket.onmessage = this.onMessage;
    websocket.onclose = this.onClose;
    return websocket;
  };

  addOnMessage = onMessageFunction => {
    this.onMessages.push(onMessageFunction);
  };

  addOnOpen = onOpenFunction => {
    this.onOpens.push(onOpenFunction);
  };

  addOnClose = onCloseFunction => {
    this.onCloses.push(onCloseFunction);
  };

  addHandleNotSupportWs = hNotSupport => {
    this.handlesNotSupportWs.push(hNotSupport);
  };

  checkWebSocketSupport = () => {
    if (!WebSocket) {
      const error = gettext('websocket not supported by your browser');
      if (this.handleNotSupportWs) {
        return this.handleNotSupportWs(error);
      }
      throw error;
    }
    return null;
  };
}
