# LLM-MapBook

## 项目活动

Datawhale AI 夏令营😀

## 项目介绍

LLM-MapBook 是一个利用LLM技术为故事讲述提供地图支持的项目。它通过大型语言模型（LLM）从书籍中提取地理信息和属性信息，结合地理编码得到地理坐标数据，并在交互式地图上进行可视化展示，为读者提供沉浸式的故事探索体验。该项目适用于故事创作者、教育工作者和地图爱好者，通过结合人工智能和地理空间技术，增强叙事效果。

## 应用场景

- 考古分析
- 地理历史学习
- 军事情报检索
- 社交网络分析

## 技术栈

- **后端**: FastAPI
- **前端**: Vue 2 + OpenLayers

## 主要思路

![image](https://github.com/user-attachments/assets/08ef18dc-7cac-4681-9558-d291b184c2c6)


1. **数据提取**: 使用LLM从故事书籍中提取地理坐标。
2. **数据处理**: 将提取的坐标数据进行处理，以便在前端进行展示。
3. **地图可视化**: 利用OpenLayers在前端展示交互式地图，并在地图上标记提取的坐标点。
4. **用户交互**: 提供用户界面，允许用户浏览和探索故事中的地理信息。

## 项目结构

```
LLM-MapBook/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── ...
│   ├── requirements.txt
│   └── utils
│       └── ...
│   ├── .env
│   └── ...
├── LICENSE
├── README.md
└── ...
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── ...
│   ├── package.json
│   └── ...
├── LICENSE
├── README.md
└── ...
```

## 安装与启动

### 后端

1. 进入后端目录：
   ```sh
   cd backend
   ```

2. 安装依赖：
   ```sh
   pip install -r requirements.txt
   ```

3. 启动后端服务：
   ```sh
   uvicorn app.main:app --reload
   ```

### 前端

- nodejs版本 16.20.2
- WebPack版本 @vue/cli 5.0.8

1. 进入前端目录：
   ```sh
   cd frontend/llm-mapbook/
   ```

2. 安装依赖：
   ```sh
   npm install
   ```

3. 启动前端服务：
   ```sh
   npm run serve
   ```

> 如果启动失败，可以`npm install @vue/cli 5.0.8` 后删除`nodeModule`再次`npm install`

## 使用说明

1. **后端服务**: 启动后端服务后，FastAPI 将在 `http://localhost:8000` 上运行。您可以通过访问 `http://localhost:8000/docs` 查看 API 文档。

2. **前端服务**: 启动前端服务后，Vue 应用将在 `http://localhost:8080` 上运行。您可以通过浏览器访问该地址，查看和交互地图应用。

## 贡献

我们欢迎任何形式的贡献，包括但不限于代码提交、问题反馈、功能建议等。

## 许可证

本项目采用 [GNU Affero General Public License (AGPL)](LICENSE)。请注意，AGPL 要求任何使用本项目的网络服务也必须开源。

---
