const { defineConfig } = require("@vue/cli-service");
// const CompressionPlugin = require("compression-webpack-plugin");

module.exports = defineConfig({
  transpileDependencies: true,
});
const path = require("path");

module.exports = {
  devServer: {
    /* 自动打开浏览器 */
    open: true,
    /* 设置为0.0.0.0则所有的地址均能访问 */
    host: "0.0.0.0",
    https: false,
    // contentBase:path.join(__dirname,'public'),
    client: {
      overlay: false,
    },
    /* 配置代理，将 API 请求代理到后端服务器 */
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // 后端 API 地址
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''  // 将请求中的 '/api' 去掉，例如 '/api/user' -> '/user'
        }
      }
    }
  },
  configureWebpack: {
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src/"),
      },
    },
  },
  /* 部署生产环境和开发环境下的URL：可对当前环境进行区分，baseUrl 从 Vue CLI 3.3 起已弃用，要使用publicPath */
  /* baseUrl: process.env.NODE_ENV === 'production' ? './' : '/' */
  publicPath: process.env.NODE_ENV === "production" ? "/" : "/",
  /* 输出文件目录：在npm run build时，生成文件的目录名称 */
  outputDir: "dist",
  /* 放置生成的静态资源 (js、css、img、fonts) 的 (相对于 outputDir 的) 目录 */
  assetsDir: "",
  /* 是否在构建生产包时生成 sourceMap 文件，false将提高构建速度 */
  productionSourceMap: false,
  /* 默认情况下，生成的静态资源在它们的文件名中包含了 hash 以便更好的控制缓存，你可以通过将这个选项设为 false 来关闭文件名哈希。(false的时候就是让原来的文件名不改变) */
  filenameHashing: false,
  /* 代码保存时进行eslint监测 */
  lintOnSave: true,
  // 配置开启运行时编译功能，将模板字符串编译为渲染函数，使用这个功能，可以在不支持vue的浏览器中运行vue项目
  runtimeCompiler: true,
};
