# 项目后端介绍
本项目搭建vue框架作为后端，包含LLM调用大模型，fastapi连接前端。

# 目录结构描述
	├── ReadMe.md           // 帮助文档

	├── __pycache__         // 项目运行生成类的包装文件夹

	├── .idea           // git相关文件

	├── fastapi-backend              // fastapi库

	├── model

	│   ├── m3e-base               // 文本向量化嵌入模型

	├── node_moudules               // 前后端连接基础库

	├── web-video              // 存放项目运行中生成音频文件

	├── main.py               // 后端主程序文件及接口文件

	├── work.py               // 调用大模型实现主要功能函数

	├── database.py            // 连接数据库函数

	├── build_vector             // 生成检索工具函数

	├── model.py            // 音频转文本模型

	├── demo.py           // 音频转文本函数库
