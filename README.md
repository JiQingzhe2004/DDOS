黑客攻击平台 v2.0
这是一个用于安全测试和教育目的的网络攻击模拟平台。该工具包含HTTP洪水攻击、漏洞扫描、端口扫描和网站爬取等功能。

功能特点
📊 实时攻击数据监控
🔍 自动网站爬取与URL收集
🛡️ 端口扫描和漏洞检测
💻 支持代理设置
📱 多线程攻击模拟
💾 自动保存爬取结果
📡 WebSocket服务器实时日志

使用方法
直接运行源代码
安装依赖：

使用启动器同时运行界面和WebSocket服务器：

或分别运行两个组件：

运行WebSocket服务器：python websocket_server.py
运行攻击平台界面：python http_flood_gui.py

运行打包后的可执行文件
运行发布版本目录中的两个组件：
先运行 WebSocket服务器.exe 启动后台服务
再运行 HTTP攻击平台.exe 启动图形界面应用

## 自动打包
运行打包脚本以自动完成所有步骤：

```bash
python build.py
```

打包脚本将自动执行以下操作：

- 安装所需依赖和PyInstaller（如果尚未安装）
- 构建WebSocket服务器的可执行文件
- 构建HTTP攻击平台GUI的可执行文件
- 将生成的可执行文件整合到发布版本目录中

## 手动打包
也可以使用已经准备好的.spec文件手动打包：

```bash
pyinstaller websocket_server.spec
pyinstaller http_flood_gui.spec
```

## 项目结构
- `websocket_server.py` - WebSocket服务器，用于实时日志和数据传输
- `http_flood_gui.py` - 主GUI应用，包含攻击功能实现
- `build.py` - 自动打包脚本
- `爬取结果/` - 保存网站爬取的URL结果
- `assets/` - 存放应用图标等资源

## 注意事项
- 本工具仅用于安全研究和教育目的，请勿用于非法活动
- 使用代理功能时，请确保代理服务器配置正确
- Shodan API密钥为可选项，使用时需要提供有效的API密钥
- 首次运行可能会被杀毒软件拦截，需要添加到信任列表
- 爬取结果会自动保存，可在爬取结果目录中查看

## 系统要求
- Windows 7/10/11
- Python 3.6或更高版本（仅源码运行需要）
- 网络连接

## 版本历史
- v2.0 (2025.04) - 添加WebSocket实时日志，优化UI界面，增强爬虫功能
- v1.0 (2025.01) - 初始版本