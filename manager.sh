#!/bin/bash

# =================================================================
# XBot One-Click Manager (Standalone Version)
# Author: Legendary Master AI Assistant
# Version: 1.0 
# =================================================================

# --- 🎨 颜色与样式定义 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# --- 🖥️ 系统自动识别 ---
OS_TYPE="$(uname -s)"
case "${OS_TYPE}" in
    Linux*)     OS="Linux";;
    Darwin*)    OS="macOS";;
    CYGWIN*|MINGW*|MSYS*) OS="Windows";;
    *)          OS="UNKNOWN:${OS_TYPE}";;
esac

# --- 🔧 辅助函数 ---
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# --- 🐍 Python 环境检查与安装 ---
check_and_install_python() {
    echo -e "${CYAN}🔍 正在检查 Python 环境...${NC}"
    
    if ! command -v python3 &> /dev/null; then
        log_warn "⚠️ 未检测到 Python3，准备自动安装..."
        
        if [ "$OS" == "macOS" ]; then
            if command -v brew &> /dev/null; then
                log_info "检测到 Homebrew，正在安装 Python..."
                brew install python || brew upgrade python
            else
                log_error "❌ 未找到 Homebrew！无法自动安装 Python。"
                echo "👉 请先安装 Homebrew (https://brew.sh/) 或手动下载 Python3 安装包。"
                read -p "按回车键退出..."
                exit 1
            fi
        elif [ "$OS" == "Linux" ]; then
            log_info "正在尝试使用 apt 安装 Python3 及组件..."
            # 针对 Debian/Ubuntu 的自动安装
            sudo apt update
            sudo apt install -y python3 python3-venv python3-pip
        else
            log_error "❌ 无法在当前系统自动安装 Python，请手动安装后重试。"
            exit 1
        fi
    else
        VER=$(python3 --version)
        log_success "✅ 检测到 Python3 ($VER)"
    fi
}

check_screen() {
    if ! command -v screen &> /dev/null; then
        log_warn "⚠️ 未检测到 'screen' 工具，正在安装..."
        if [ "$OS" == "macOS" ]; then
            brew install screen
        elif [ "$OS" == "Linux" ]; then
            sudo apt install -y screen
        fi
    fi
}

# --- 🚀 菜单功能 ---

install_env() {
    echo -e "\n${CYAN}📦 开始一键部署 (${OS})...${NC}"
    
    # 1. 检查并安装 Python & Screen
    check_and_install_python
    check_screen

    # 2. 创建虚拟环境
    if [ ! -d "venv" ]; then
        log_info "正在创建独立虚拟环境 (venv)..."
        python3 -m venv venv
        if [ $? -ne 0 ]; then
             log_error "❌ 虚拟环境创建失败！请检查是否安装了 python3-venv"
             return
        fi
    else
        log_info "虚拟环境已存在，跳过创建。"
    fi

    # 3. 激活环境并安装依赖 (直接写死，无需 requirements.txt)
    source venv/bin/activate
    
    log_info "正在升级 pip..."
    pip install --upgrade pip
    
    log_info "正在安装项目核心依赖 (Playwright & Rich)..."
    pip install playwright rich
    
    log_info "正在安装 Playwright 浏览器内核..."
    playwright install chromium

    # === Linux 特供：系统级依赖补全 ===
    if [ "$OS" == "Linux" ]; then
        log_warn "🐧 检测到 Linux 系统，正在安装浏览器系统底层依赖 (需要 sudo 权限)..."
        sudo playwright install-deps
    fi

    log_success "✅ 所有环境配置完成！您现在可以删掉 requirements.txt 了。"
    read -p "按回车键返回菜单..."
}

generate_cookie() {
    echo -e "\n${YELLOW}🍪 生成 Cookie (核武器模式)${NC}"
    
    if [ ! -d "venv" ]; then
        log_error "请先执行 [1] 安装环境！"
        read -p "按回车键返回..."
        return
    fi
    
    source venv/bin/activate
    
    echo -e "${BLUE}ℹ️  如何获取 auth_token:${NC}"
    echo "  1. 打开浏览器 (Chrome/Edge) 并登录 X.com"
    echo "  2. 按 F12 打开开发者工具 -> 点击 'Application' (应用) 标签"
    echo "  3. 左侧栏展开 'Cookies' -> 点击 https://x.com"
    echo "  4. 在右侧列表中找到名为 'auth_token' 的项"
    echo "  5. 复制它的 'Value' (值)"
    echo "---------------------------------------------------"
    
    python auth.py
    
    read -p "按回车键返回菜单..."
}

start_bot() {
    echo -e "\n${GREEN}🚀 启动 XBot 任务...${NC}"
    
    if [ ! -f "cookies.json" ]; then
        log_error "❌ 未找到 cookies.json！请先执行 [2] 生成 Cookie。"
        read -p "按回车键返回..."
        return
    fi

    if screen -list | grep -q "xbot_session"; then
        log_warn "⚠️ 任务已经在后台运行中！"
        read -p "按回车键返回..."
        return
    fi

    # 使用 screen 后台启动
    screen -dmS xbot_session bash -c 'source venv/bin/activate; python main.py'
    
    log_success "✅ XBot 已在后台启动！(Session: xbot_session)"
    log_info "您可以选择 [4] 查看运行日志。"
    read -p "按回车键返回..."
}

view_log() {
    echo -e "\n${CYAN}📜 实时运行日志 (按 Ctrl+C 退出查看，不影响后台任务)${NC}"
    if [ -f "xbot_run.log" ]; then
        tail -f xbot_run.log
    else
        log_warn "暂无日志文件，任务可能尚未启动或刚启动。"
        read -p "按回车键返回..."
    fi
}

stop_bot() {
    echo -e "\n${RED}🛑 停止 XBot 任务...${NC}"
    if screen -list | grep -q "xbot_session"; then
        screen -X -S xbot_session quit
        log_success "✅ 已成功终止后台任务。"
    else
        log_warn "没有检测到正在运行的任务。"
    fi
    read -p "按回车键返回..."
}

uninstall() {
    echo -e "\n${RED}🗑️  卸载与清理...${NC}"
    read -p "⚠️  确定要删除虚拟环境和 Cookie 吗？(y/n): " confirm
    if [ "$confirm" == "y" ]; then
        rm -rf venv
        rm -f cookies.json
        log_success "✅ 已清理环境文件 (venv, cookies.json)。"
        echo "提示：再见👋。"
    else
        log_info "已取消。"
    fi
    read -p "按回车键返回..."
}

update_lib() {
    echo -e "\n${CYAN}🔄 更新语料词库...${NC}"
    echo "当前为本地模式。项目托管至 GitHub 后，此处将执行 git pull。"
    read -p "按回车键返回..."
}

# --- 🖥️ 主循环 ---
while true; do
    clear
    echo -e "=========================================================="
    echo -e "   🤖 XBot 自动回复截流系统 - 管理面板 (v1.0 Standalone)"
    echo -e "   👤 用户: X先生 | 💻 系统: $OS"
    echo -e "=========================================================="
    echo -e "${GREEN}1.${NC} 🛠️  一键安装与配置 (含 Python/环境/依赖)"
    echo -e "${GREEN}2.${NC} 🍪 生成 Cookie (Auth Token)"
    echo -e "${GREEN}3.${NC} 🚀 启动任务 (Start Main)"
    echo -e "${GREEN}4.${NC} 📜 查看运行日志 (Log)"
    echo -e "${RED}5.${NC} 🗑️  卸载/清理环境 (Uninstall)"
    echo -e "${RED}6.${NC} 🛑 停止后台回复 (Stop)"
    echo -e "${YELLOW}7.${NC} 🔄 更新语料词库 (Update)"
    echo -e "${BLUE}8.${NC} 🚪 退出菜单 (Exit)"
    echo -e "=========================================================="
    
    read -p "👉 请输入选项 [1-8]: " choice

    case $choice in
        1) install_env ;;
        2) generate_cookie ;;
        3) start_bot ;;
        4) view_log ;;
        5) uninstall ;;
        6) stop_bot ;;
        7) update_lib ;;
        8) echo "👋 再见，X先生！"; exit 0 ;;
        *) echo "❌ 无效选项，请重试。" ; sleep 1 ;;
    esac
done
