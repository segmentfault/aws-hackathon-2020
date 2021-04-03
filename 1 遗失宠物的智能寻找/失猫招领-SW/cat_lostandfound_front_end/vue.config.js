module.exports = {
  outputDir: 'static',

  chainWebpack: (config) => {
    config.plugin('html').tap((args) => {
      args[0].title = '失猫招领'
      return args
    })
  },

  devServer: {
    proxy: {
      '/api': {
        target:
          'http://lostandfound-env.eba-ftezekhq.ap-northeast-1.elasticbeanstalk.com',
        changeOrigin: true,
        pathRewrite: {
          '^/api/': '',
        },
      },

      '/classify': {
        target: 'http://18.181.212.95:5000',
        changeOrigin: true,
      },
    },
  },
}
