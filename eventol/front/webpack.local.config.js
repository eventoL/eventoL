const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')

const config = require('./webpack.base.config.js')
const localSettings = require('./webpack.local-settings.js')

const port = 3000
const ip = localSettings.ip

const addDevVendors = module => [
  `webpack-dev-server/client?http://${ip}:${port}`,
  'webpack/hot/only-dev-server',
  module
];

config.devtool = "#eval-source-map"
config.ip = ip

// Use webpack dev server
config.entry = {
  Home: ['./src/views/Home'],
  vendors: ['react', 'babel-polyfill'],
}

// override django's STATIC_URL for webpack bundles
config.output.publicPath = `/static/bundles/local/`

// Add HotModuleReplacementPlugin and BundleTracker plugins
config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoErrorsPlugin(),
  new BundleTracker({filename: './webpack-stats-local.json'}),
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('development')
    }
  }),

])

// Add a loader for JSX files
config.module.loaders.push(
  { test: /\.jsx?$/, exclude: /node_modules/, loaders: ['babel'] }
)

module.exports = config
