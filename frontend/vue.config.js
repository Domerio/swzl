const path = require('path')

module.exports = {
    outputDir: path.resolve(__dirname, '../static/frontend'),
    assetsDir: '', // 资源文件直接放在outputDir下，而非子目录
    // indexPath: path.resolve(__dirname, '../templates/frontend/login.html'), // 改为统一的入口模板
    indexPath: path.resolve(__dirname, '../templates/frontend/index.html'), // 改为统一的入口模板
    publicPath: '/static/frontend/', // 资源路径需与Django的STATIC_URL匹配
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true
            }
        },
        historyApiFallback: true
    },

    configureWebpack: {
        output: {
            filename: 'js/[name].[fullhash:8].js',
            chunkFilename: 'js/[name].[fullhash:8].chunk.js',
        }
    },
    css: {
        extract: {
            filename: 'css/[name].[fullhash:8].css',
            chunkFilename: 'css/[name].[fullhash:8].chunk.css'
        }
    }
}
