import os
import sys
import subprocess
import shutil
import importlib

def install_pyinstaller():
    """安装PyInstaller（如果尚未安装）"""
    try:
        import PyInstaller
        print("PyInstaller已安装")
    except ImportError:
        print("正在安装PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller安装完成")

def install_dependencies():
    """安装必要的依赖项"""
    dependencies = ["requests", "beautifulsoup4", "websocket-client", "shodan", "websockets"]
    
    for dep in dependencies:
        try:
            importlib.import_module(dep.replace("-", "_"))
            print(f"{dep} 已安装")
        except ImportError:
            print(f"正在安装 {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"{dep} 安装完成")

def build_executables():
    """分别构建各个可执行文件"""
    print("正在打包应用程序...")
    
    # 创建图标目录（如果尚未存在）
    icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    os.makedirs(icon_dir, exist_ok=True)
    
    # 创建爬取结果目录（如果尚未存在）
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "爬取结果")
    os.makedirs(results_dir, exist_ok=True)
    print(f"已创建或确认爬取结果目录: {results_dir}")
    
    # 获取图标路径
    icon_path = os.path.join(icon_dir, "icon.ico")
    
    # ...其余代码保持不变...
    
    # 构建WebSocket服务器
    print("\n1. 正在打包WebSocket服务器...")
    ws_cmd = [
        "pyinstaller",
        "--name=WebSocket服务器",
        "--console",  # 显示控制台窗口，便于查看日志
        "--onefile",
        "--clean",
        "--hidden-import=websockets",
        "--hidden-import=asyncio",
        "websocket_server.py"
    ]
    # 只有在图标存在时才添加图标参数
    if os.path.exists(icon_path):
        ws_cmd.insert(2, f"--icon={icon_path}")
    
    subprocess.check_call(ws_cmd)
    
    # 构建HTTP攻击平台GUI
    print("\n2. 正在打包HTTP攻击平台GUI...")
    gui_cmd = [
        "pyinstaller",
        "--name=HTTP攻击平台",
        "--windowed",  # 不显示控制台窗口
        "--onefile",
        "--clean",
        "--add-data=爬取结果;爬取结果",  # 包含爬取结果目录
        "--hidden-import=websocket-client",
        "--hidden-import=shodan",
        "http_flood_gui.py"
    ]
    # 只有在图标存在时才添加图标参数
    if os.path.exists(icon_path):
        gui_cmd.insert(2, f"--icon={icon_path}")
    
    subprocess.check_call(gui_cmd)
    
    # 将所有可执行文件复制到同一目录
    print("\n正在整合可执行文件...")
    dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
    final_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "发布版本")
    os.makedirs(final_dir, exist_ok=True)
    
    # 复制所有可执行文件
    for exe_name in ["WebSocket服务器.exe", "HTTP攻击平台.exe"]:
        src = os.path.join(dist_dir, exe_name)
        dst = os.path.join(final_dir, exe_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"已复制: {exe_name} -> {final_dir}")
    
    print(f"\n打包完成！所有可执行文件位于 {final_dir} 目录中")
    print("使用方法：")
    print("1. 先运行「WebSocket服务器.exe」启动WebSocket服务")
    print("2. 然后运行「HTTP攻击平台.exe」启动攻击平台界面")

def create_sample_icon():
    """创建一个示例图标文件"""
    icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    icon_path = os.path.join(icon_dir, "icon.ico")
    
    if not os.path.exists(icon_path):
        print("提示: 您可以将自定义图标放在assets/icon.ico，用于应用程序图标。")

if __name__ == "__main__":
    # 确保当前目录是脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 安装PyInstaller（如果需要）
    install_pyinstaller()
    
    # 安装依赖
    install_dependencies()
    
    # 检查图标
    create_sample_icon()
    
    # 构建可执行文件
    build_executables()
    
    print("\n注意事项:")
    print("1. 生成的可执行文件位于'发布版本'目录中")
    print("2. 首次运行可能会被杀毒软件拦截，需要添加信任")
    print("3. 如需自定义图标，请将.ico格式图标放入assets目录并命名为icon.ico")
    print("4. 运行「WebSocket服务器.exe」和「HTTP攻击平台.exe」分别启动服务和界面")
