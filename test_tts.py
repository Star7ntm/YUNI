"""
TTS 功能测试脚本
用于验证 Whisper 页面的 TTS 功能是否正常工作
"""
import requests
import base64
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 测试配置
API_URL = "http://127.0.0.1:8003"
TEST_TOKEN = None

def login_test_user():
    """登录测试用户"""
    print("1. 登录测试用户...")
    response = requests.post(f"{API_URL}/api/login", json={
        "username": "testuser",
        "password": "Test123"
    })
    
    if response.status_code == 200:
        data = response.json()
        global TEST_TOKEN
        TEST_TOKEN = data.get('token')
        print(f"   ✅ 登录成功，Token: {TEST_TOKEN[:20]}...")
        return True
    else:
        print(f"   ❌ 登录失败: {response.text}")
        return False

def test_tts_api():
    """测试 TTS API"""
    print("2. 测试 TTS API...")
    
    if not TEST_TOKEN:
        print("   ❌ 没有有效的 Token")
        return False
    
    response = requests.post(
        f"{API_URL}/api/tts",
        headers={
            "Authorization": f"Bearer {TEST_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "text": "你好，这是一个测试语音合成",
            "speaker": "default",
            "speed": 1.0
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ TTS API 返回成功")
        print(f"   - sample_rate: {data.get('sample_rate')}")
        print(f"   - duration: {data.get('duration')}")
        print(f"   - audio_base64 长度: {len(data.get('audio_base64', ''))}")
        return True
    else:
        print(f"   ❌ TTS API 失败: {response.status_code} - {response.text}")
        return False

def test_without_login():
    """测试未登录状态"""
    print("3. 测试未登录状态...")
    
    response = requests.post(
        f"{API_URL}/api/tts",
        json={
            "text": "测试文字",
            "speaker": "default",
            "speed": 1.0
        }
    )
    
    if response.status_code == 401:
        print("   ✅ 未登录正确返回 401")
        return True
    else:
        print(f"   ❌ 预期 401，实际: {response.status_code}")
        return False

def main():
    print("=" * 50)
    print("TTS 功能测试")
    print("=" * 50)
    print()
    
    # 先测试未登录
    test_without_login()
    print()
    
    # 登录测试用户
    if not login_test_user():
        print()
        print("请先创建测试用户或使用已有账户登录")
        return
    
    print()
    
    # 测试 TTS API
    if test_tts_api():
        print()
        print("🎉 所有测试通过！")
        print()
        print("功能验证完成，可以正常使用 TTS 功能")
    else:
        print()
        print("⚠️  测试失败，请检查:")
        print("   1. GPT-SoVITS 服务是否已启动 (端口 9880)")
        print("   2. 后端服务是否正常运行")
        print("   3. 测试用户是否有权限")

if __name__ == "__main__":
    main()
