# 🔰 黑客攻击平台 v2.0

这是一个面向安全测试与教育的网络攻击模拟平台，集成了 HTTP 洪水、漏洞扫描、端口扫描、网站爬取等多种功能。

## ✨ 功能亮点

- 📊 实时监控攻击数据
- 🔍 自动网站爬取与 URL 收集
- 🛡️ 端口扫描与漏洞检测
- 💻 支持代理设置
- 📱 多线程攻击模拟
- 💾 爬取结果自动保存
- 📡 WebSocket 实时日志

## 🚀 快速上手

### 源码运行

1. **安装依赖：**
    ```bash
    pip install requests beautifulsoup4 websocket-client shodan websockets
    ```

2. **分别启动两个组件：**
    - 启动 WebSocket 服务器：
      ```bash
      python websocket_server.py
      ```
    - 启动攻击平台界面：
      ```bash
      python http_flood_gui.py
      ```

## 🔧 打包指南

### 一键打包

运行打包脚本自动完成所有步骤：

```bash
python build.py
```

脚本会自动安装依赖、构建可执行文件，并整合到发布目录。

### 手动打包

如需手动操作，可用 .spec 文件：

```bash
pyinstaller websocket_server.spec
pyinstaller http_flood_gui.spec
```

### 运行打包版

在发布目录依次运行：
1. `WebSocket服务器.exe`（后台服务）
2. `HTTP攻击平台.exe`（图形界面）

## 📁 项目结构

- `websocket_server.py` — WebSocket 实时日志服务器
- `http_flood_gui.py` — 主 GUI 应用
- `build.py` — 自动打包脚本
- `爬取结果/` — 爬取数据存储目录
- `assets/` — 应用资源目录
- `.vscode/` — VS Code 配置

## ⚠️ 注意事项

- 仅限安全研究与教育，禁止非法用途
- 使用代理时请确保配置正确
- Shodan API 密钥为可选项
- 首次运行可能被杀毒软件拦截
- 爬取结果自动保存至指定目录

## 💻 系统要求

- Windows 7/10/11
- Python 3.6 及以上（源码运行）
- 网络连接
- 2GB+ 内存
- 100MB+ 磁盘空间
- 依赖库：requests, beautifulsoup4, websocket-client, shodan, websockets

## 📝 版本历史

- **v2.0** (2025.04.18) — 新增 WebSocket 实时日志，优化 UI，增强爬虫
- **v1.0** (2025.04.17) — 初始发布

## 📜 许可证

本项目仅供教育用途，禁止用于非法活动。

## 👥 贡献者

- 主要开发者：[Forrest]
- 图标设计：[ChatGPT]

## 📞 联系方式

如有建议或问题，欢迎联系：
- 邮箱：jin648862@gmail.com
- GitHub：[JiQingzhe2004](https://github.com/JiQingzhe2004/)
