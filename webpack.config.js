const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.jsx', // Точка входа
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    clean: true,
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/, // Для JavaScript/JSX файлов
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
      {
        test: /\.css$/, // Для CSS файлов
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'], // Поддержка JSX
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html', // HTML-шаблон
    }),
  ],
  devServer: {
    static: './dist',
    proxy: {
      '/api': 'http://localhost:5000', // Проксирование запросов к Flask
    },
    port: 3000,
  },
};
