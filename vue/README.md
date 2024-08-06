# 项目前端介绍
本项目搭建vue框架作为前端，包含页面的样式设计，与后端交互的接口。

# 目录结构描述
	├── ReadMe.md           // 帮助文档

	├── __pycache__          // 项目运行生成类的包装文件夹

	├── node_modules         // vue框架导入库文件夹

	├── public          // vue运行静态资源（以及项目运行过程中生成图片example.jpg临时存放地址及调用地址）

	├── src

	│   ├── assets          // vue资源文件夹（包含网页图片资源以及字体资源

	│   ├── components             // vue组件文件夹

	│   │   ├── QuestionChoice.vue         // 网页首页组件

	│   │   ├── WritePage.vue        // 网页AI写诗页面组件

	│   │   ├── SearchPage.vue         // 网页查诗页面组件

	│   │   ├── DrawPage.vue         // 网页据诗画图页面组件

	│   │   ├── ReviewPage.vue          // 展示页面

	│   ├── router

	│   │   ├── index.js        // 网页页面跳转路径配置文件

	│   ├── font

	│   │   ├── font.css         // 字体配置

	│   ├── main.js         // vue项目总体配置文件

	├── App.vue           // vue项目运行文件

	├── vue.config.js          //跨域配置文件

	├── vite.config.js            // 导入scss库配置文件

	├── pnpm-lock.yaml           // 导入pnpm库配置文件
