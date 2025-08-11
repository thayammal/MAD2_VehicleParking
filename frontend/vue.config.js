const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})


module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:5000', // your backend URL
        changeOrigin: true,
        secure: false,
        pathRewrite: { '^/api': '/api' }
      }
    }
  }
};
