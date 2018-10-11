const webpack = require('webpack');
const WebpackDevServer = require('webpack-dev-server');
const config = require('./webpack.local.config');
const host = '0.0.0.0';
const port = 3000;

new WebpackDevServer(webpack(config), {
  publicPath: config.output.publicPath,
  hot: true,
  inline: true,
  historyApiFallback: true,
  headers: {'Access-Control-Allow-Origin': '*'},
}).listen(port, host, err => {
  if (err) console.log(err);
  console.log(`Listening at ${host}:${port}`);
});
