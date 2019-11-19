/* eslint-disable import/no-extraneous-dependencies */
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const TerserPlugin = require('terser-webpack-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const safePostCssParser = require('postcss-safe-parser');
const config = require('./webpack.base.config.js');

config.output.path = require('path').resolve('./eventol/static/bundles/prod/');

config.optimization.minimize = true;
config.optimization.nodeEnv = 'production';
config.optimization.minimizer = [
  new TerserPlugin({
    terserOptions: {
      parse: {
        ecma: 8,
      },
      compress: {
        ecma: 5,
        warnings: false,
        comparisons: false,
        inline: 2,
      },
      mangle: {
        safari10: true,
      },
      output: {
        ecma: 5,
        comments: false,
        ascii_only: true,
      },
    },
    parallel: true,
    cache: true,
    sourceMap: false,
  }),
  new OptimizeCSSAssetsPlugin({
    cssProcessorOptions: {
      parser: safePostCssParser,
      map: false,
    },
  }),
];

config.mode = 'production';

config.plugins = config.plugins.concat([
  new BundleTracker({filename: './webpack-stats-prod.json'}),

  // removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify('production'),
    },
  }),

  // keeps hashes consistent between compilations
  new webpack.optimize.OccurrenceOrderPlugin(),
]);

module.exports = config;
