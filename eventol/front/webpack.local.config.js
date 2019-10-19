/* eslint-disable import/no-extraneous-dependencies */
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const config = require('./webpack.base.config.js');
const localSettings = require('./webpack.local-settings.js');

const {ip} = localSettings;
const port = 3000;

config.devServer = {
  historyApiFallback: true,
  noInfo: true,
  overlay: true,
  port,
  host: ip,
  disableHostCheck: true,
  public: `${ip}:${port}`,
  publicPath: `http://${ip}:${port}`,
};

const addDevVendors = module => [
  `webpack-dev-server/client?http://${ip}:${port}`,
  'webpack/hot/only-dev-server',
  module,
];

config.devtool = '#eval-source-map';

// Use webpack dev server
config.entry = {
  Home: addDevVendors('./src/views/Home'),
  EventHome: addDevVendors('./src/views/EventHome'),
  Report: addDevVendors('./src/views/Report'),
  slick: addDevVendors('./src/libs/slick'),
  form: addDevVendors('./src/libs/form'),
  base: addDevVendors('./src/libs/base'),
  map: addDevVendors('./src/libs/map'),
  vendors: ['react', '@babel/polyfill'],
};

config.mode = 'development';

// override django's STATIC_URL for webpack bundles
config.output.publicPath = `http://${ip}:${port}/assets/bundles/`;

// Add HotModuleReplacementPlugin and BundleTracker plugins
config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoEmitOnErrorsPlugin(),
  new BundleTracker({filename: './webpack-stats-local.json'}),
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify('development'),
    },
  }),
]);

module.exports = config;
