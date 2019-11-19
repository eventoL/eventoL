const webpack = require('webpack');
const config = require('./webpack.base.config.js');
const BundleTracker = require('webpack-bundle-tracker');
const localSettings = require('./webpack.local-settings.js');

const ip = localSettings.ip;
const port = 3000;

const addDevVendors = module => [
  `webpack-dev-server/client?http://${ip}:${port}`,
  'webpack/hot/only-dev-server',
  module
];

config.devtool = '#eval-source-map';
config.ip = ip;

// Use webpack dev server
config.entry = {
  Home: addDevVendors('./src/views/Home'),
  EventHome: addDevVendors('./src/views/EventHome'),
  Report: addDevVendors('./src/views/Report'),
  vendors: ['react', 'babel-polyfill']
};

// override django's STATIC_URL for webpack bundles
config.output.publicPath = `http://${ip}:${port}/assets/bundles/`;

// Add HotModuleReplacementPlugin and BundleTracker plugins
config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoErrorsPlugin(),
  new BundleTracker({filename: './webpack-stats-local.json'}),
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify('development')
    }
  })
]);

// Add a loader for JSX files
config.module.loaders.push(
  {test: /\.jsx?$/, exclude: /node_modules/, loaders: ['babel']}
);

module.exports = config;
