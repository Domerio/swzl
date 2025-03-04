const path = require('path')

module.exports = {
    outputDir: path.resolve(__dirname, '../static/frontend'),
    assetsDir: '',
    // indexPath: path.resolve(__dirname, '../templates/frontend/login.html'), // 改为统一的入口模板
    indexPath: path.resolve(__dirname, '../templates/frontend/index.html'), // 改为统一的入口模板
    publicPath: process.env.NODE_ENV === 'production'
    ? '/static/frontend/'
    : '/static/frontend/', // 确保静态资源路径正确
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                pathRewrite: {'^/api': ''}
            }
        },
        historyApiFallback: true
    },

    configureWebpack: {
        output: {
            filename: 'js/[name].[hash:8].js',
            chunkFilename: 'js/[name].[hash:8].chunk.js'
        }
    },
    css: {
        extract: {
            filename: 'css/[name].[hash:8].css',
            chunkFilename: 'css/[name].[hash:8].chunk.css'
        }
    }
}
