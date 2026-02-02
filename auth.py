# make_cookie.py
import json

def create_cookie_file():
    print("="*50)
    print("🔑 核武器模式：手动注入 Cookie")
    print("="*50)
    
    # 1. 让用户粘贴 auth_token
    token = input("👉 请粘贴你的 auth_token 值 (按回车确认): ").strip()
    
    if not token:
        print("❌ 不能为空！")
        return

    # 2. 构造 Playwright 格式的 Cookie
    # 我们只需要这一个核心 Cookie，其他的 X 会自动补全
    cookies = [
        {
            "name": "auth_token",
            "value": token,
            "domain": ".x.com",
            "path": "/",
            "httpOnly": True,
            "secure": True,
            "sameSite": "None"
        }
    ]

    state = {"cookies": cookies, "origins": []}

    # 3. 写入文件
    with open("cookies.json", "w") as f:
        json.dump(state, f)
        
    print("\n✅ 成功！cookies.json 已生成。")
    print("🚀 你现在可以直接运行 main.py 了（它会跳过登录页，直接进入主页）。")

if __name__ == "__main__":
    create_cookie_file()
