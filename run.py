#!/usr/bin/env python3
"""
启动脚本 - 从项目根目录运行
支持一键启动 Whisper + GPT-SoVITS 服务
"""
import sys
import os
import subprocess
import threading
import time
import codecs
from backend.app.core.model_paths import configure_hf_env

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
configure_hf_env()

def check_gpt_sovits_running():
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 9880))
        sock.close()
        return result == 0
    except:
        return False

def start_gpt_sovits():
    gpt_sovits_dir = os.path.dirname(os.path.abspath(__file__))
    gpt_sovits_dir = os.path.join(gpt_sovits_dir, "models", "GPT-SoVITS")
    gpt_sovits_py = os.path.join(gpt_sovits_dir, "api.py")
    
    if not os.path.exists(gpt_sovits_py):
        print("[WARNING] 未找到 GPT-SoVITS，跳过")
        return None
    
    print("[BOOT] 正在启动 GPT-SoVITS (端口 9880)...")
    print("      首次启动需要加载模型，请耐心等待...")
    print()
    
    env = os.environ.copy()
    env['PYTHONPATH'] = gpt_sovits_dir + os.pathsep + env.get('PYTHONPATH', '')
    
    device = "cpu"
    try:
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            print("[OK] 检测到 CUDA 显卡，使用 GPU 加速")
        else:
            print("[!] 未检测到 CUDA，使用 CPU 模式")
    except:
        print("[!] 无法检测 CUDA，使用 CPU 模式")
    
    process = subprocess.Popen(
        [sys.executable, gpt_sovits_py, "-d", device, "-p", "9880"],
        cwd=gpt_sovits_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1
    )
    
    def log_output():
        for line in iter(process.stdout.readline, b''):
            if line:
                try:
                    decoded = line.decode('utf-8', errors='replace').strip()
                    if decoded:
                        clean_line = ''.join(c if ord(c) < 128 else '?' for c in decoded)
                        if clean_line.strip():
                            print(f"   [GPT-SoVITS] {clean_line}")
                except:
                    pass
    
    log_thread = threading.Thread(target=log_output, daemon=True)
    log_thread.start()
    
    max_wait = 180
    waited = 0
    while waited < max_wait:
        if check_gpt_sovits_running():
            print()
            print("[OK] GPT-SoVITS 启动成功！")
            print()
            return process
        
        if process.poll() is not None:
            print()
            print("[WARNING] GPT-SoVITS 进程异常，将使用模拟音频")
            print()
            return None
            
        time.sleep(1)
        waited += 1
        if waited % 30 == 0 and waited < max_wait:
            print(f"   加载中... ({waited}秒)")
    
    print()
    print("[WARNING] GPT-SoVITS 启动中，使用模拟音频")
    print()
    return process

if __name__ == "__main__":
    from backend.main import app
    import uvicorn
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=" * 50)
    print("       YuNi AI 语音系统")
    print("=" * 50)
    print()
    
    gpt_process = None
    if check_gpt_sovits_running():
        print("[OK] GPT-SoVITS 已运行")
        print()
    else:
        gpt_process = start_gpt_sovits()
    
    print("[INFO] 主服务运行中: http://127.0.0.1:8003")
    print("       语音识别: http://127.0.0.1:8003/whisper")
    print("       API 文档: http://127.0.0.1:8003/docs")
    print()
    
    try:
        uvicorn.run(app, host="127.0.0.1", port=8003, reload=False)
    except KeyboardInterrupt:
        print("\n正在关闭服务...")
    finally:
        if gpt_process and gpt_process.poll() is None:
            gpt_process.terminate()
            try:
                gpt_process.wait(timeout=5)
            except:
                gpt_process.kill()
        print("服务已关闭")
