'use strict';

const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TaserJSPlugin = require("terser-webpack-plugin");
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const BrowserSyncPlugin = require('browser-sync-webpack-plugin');
const FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin');
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const path = require('path');

const paths = {
  appSrc: path.join(__dirname, 'static/src/'),
  appBuild: path.join(__dirname, 'static/build/'),
};

const DEV = process.env.NODE_ENV === 'development';

module.exports = {
  mode: DEV ? 'development' : 'production',
  target: 'web',
  devtool: DEV ? 'source-map' : false,
  performance: {
    maxEntrypointSize: 1024000,
    maxAssetSize: 1024000,
  },
  entry: [
    path.join(__dirname, 'static/src/sass/main.scss'),
    path.join(__dirname, 'static/src/js/main.js')
  ],
  output: {
    path: paths.appBuild,
    filename: 'main.js'
  },
  module: {
    rules: [
      // Disable require.ensure as it's not a standard language feature.
      { parser: { requireEnsure: false } },
      // Transform ES6 with Babel
      {
        test: /\.js?$/,
        loader: 'babel-loader',
        include: paths.appSrc,
      },
      {
        test: /\.(png|jpg|jpe?g|gif|svg)$/i,
        loader: 'file-loader',
        options: {
          outputPath: 'images',
        }
      },

      {
          // Apply rule for fonts files
          test: /\.(woff|woff2|ttf|otf|eot)$/,
          use: [
                 {
                   // Using file-loader too
                   loader: "file-loader",
                   options: {
                     name: '[name].[ext]',
                     outputPath: 'fonts'
                   }
                 }
               ]
     },


      {
        test: /\.s[ac]ss$/i,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              publicPath: ''
            }
          },
          {
            loader: "css-loader",
          },
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: [
                  [
                    "autoprefixer",
                  ]
                ],
              },
            }
          },
          {
            loader: 'resolve-url-loader',
            options: {
              sourceMap: true,
              removeCR: true,
            }
          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true,
            }
          }
        ],
      }
    ],
  },
  optimization: {
    minimize: !Boolean(DEV),
    minimizer: [
      new OptimizeCSSAssetsPlugin({
        cssProcessorOptions: {
          map: {
            inline: false,
            annotation: true,
          }
        }
      }),
      new TaserJSPlugin({
        terserOptions: {
          keep_fnames: true
        }
      })
    ]
  },
  plugins: [
    new webpack.ProvidePlugin({
       $: "jquery",
       jQuery: "jquery"
      }),
    !DEV && new CleanWebpackPlugin({
      cleanAfterEveryBuildPatterns: 'build/**/*'
    }),
    new MiniCssExtractPlugin({
      filename: 'main.css'
    }),
    new webpack.EnvironmentPlugin({
      NODE_ENV: 'development', // use 'development' unless process.env.NODE_ENV is defined
      DEBUG: false,
    }),
    DEV &&
      new FriendlyErrorsPlugin({
        clearConsole: false,
      }),
    DEV &&
      new BrowserSyncPlugin({
        notify: false,
        host: 'localhost',
        port: 4000,
        logLevel: 'info',
        proxy: `http://127.0.0.1:8000/`
      }),
  ].filter(Boolean),
}
