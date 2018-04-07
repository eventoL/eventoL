const path = require('path')
const webpack = require('webpack')

module.exports = {
  context: __dirname,

  entry: {
    // Add as many entry points as you have container-react-components here
    Home: './src/views/Home',
    EventHome: './src/views/EventHome',
    vendors: ['react', 'babel-polyfill'],
  },

  output: {
      path: path.resolve('./eventol/static/bundles/local/'),
      filename: '[name]-[hash].js'
  },

  externals: [
  ], // add all vendor libs

  plugins: [
    new webpack.optimize.CommonsChunkPlugin('vendors', 'vendors.js'),
  ], // add all common plugins here

  module: {
    loaders: [
      {
        test: /\.css$/,
        loader: 'style-loader!css-loader'
      },
      {
        test: /\.scss$/,
        loader: 'style-loader!css-loader!sass-loader'
      },
      {
        test: /\.(gif|png|jpe?g|svg)$/i,
        loader: 'file-loader!image-webpack-loader',
        options: {
          optipng: {
            enabled: true,
          },
          svgo: {
            enabled: true,
          },
        }
      },
      {
        test: /\.(eot|woff2|woff|ttf)$/,
        loader: 'file-loader'
      }
    ]
  },

  resolve: {
    modulesDirectories: ['node_modules', 'bower_components'],
    extensions: ['', '.js', '.jsx']
  },
}
