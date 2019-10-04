/* eslint-disable import/no-extraneous-dependencies,no-unused-vars,no-useless-escape */
const path = require('path');
const webpack = require('webpack');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

module.exports = {
  context: __dirname,

  entry: {
    Home: './src/views/Home',
    EventHome: './src/views/EventHome',
    Report: './src/views/Report',
    vendors: ['react', 'react-dom', 'redux', '@babel/polyfill'],
  },

  output: {
    path: path.resolve('./eventol/static/bundles/local/'),
    filename: '[name]-[hash].js',
  },

  externals: [], // add all vendor libs

  plugins: [],

  performance: {
    hints: process.env.NODE_ENV === 'production' ? 'warning' : false,
  },

  optimization: {
    removeEmptyChunks: true,
    mergeDuplicateChunks: true,
    minimizer: [
      new UglifyJsPlugin({
        cache: true,
        parallel: true,
        uglifyOptions: {
          compress: false,
          ecma: 6,
          mangle: true,
        },
        sourceMap: true,
      }),
    ],
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.scss$/,
        use: ['style-loader', 'css-loader', 'sass-loader'],
      },
      {
        test: /\.(gif|png|jpe?g|svg)$/i,
        use: [
          'file-loader',
          {
            loader: 'image-webpack-loader',
            options: {
              mozjpeg: {
                progressive: true,
                quality: 65,
              },
              optipng: {
                enabled: false,
              },
              pngquant: {
                quality: '65-90',
                speed: 4,
              },
              gifsicle: {
                interlaced: false,
              },
              webp: {
                quality: 75,
              },
              svgo: {
                enabled: true,
              },
            },
          },
        ],
      },
      {
        test: /\.(eot|woff2|woff|ttf)$/,
        use: 'file-loader',
      },
      {test: /\.jsx?$/, exclude: /node_modules/, loaders: ['babel-loader']},
      {
        include: [{test: /\Toggle.js?$/}, {test: /\effects.js?$/}],
        use: ['babel-loader'],
      },
    ],
  },

  resolve: {
    modules: ['node_modules', 'bower_components'],
    extensions: ['.js', '.jsx'],
  },
};
