const path = require('path');

module.exports = {
  outputDir: path.resolve(__dirname, './static/frontend'),
  indexPath: path.resolve(__dirname, './templates/frontend/index.html'),
  publicPath: '/static/frontend/',
};