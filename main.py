# main.py (V1.0: X平台日区自动回复)
# -*- coding: utf-8 -*-
import time
import random
import re
import os
import datetime
from rich.console import Console
from playwright.sync_api import sync_playwright
from config import Config
from replies_data import ReplyLibrary

console = Console()

class XBot:
    def __init__(self):
        self.replied_count = 0
        self.processed_tweets = set()
        self.recent_replies = []
        self.scroll_steps = 0
        self.empty_scan_count = 0
        self.last_hunt_time = time.time()
        
        with open("xbot_run.log", "a", encoding="utf-8") as f:
            f.write(f"\n\n{'='*20} V1.0 X平台日区自动回复 {time.strftime('%Y-%m-%d %H:%M:%S')} {'='*20}\n")

    def log(self, msg, style="white"):
        timestamp = time.strftime('%H:%M:%S')
        console.print(f"[{timestamp}] {msg}", style=style)
        try:
            with open("xbot_run.log", "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {msg}\n")
        except: pass

    def parse_number(self, text):
        if not text: return 0
        text = str(text).upper().replace(',', '').strip()
        try:
            if '萬' in text: return int(float(text.replace('萬', '')) * 10000)
            if '万' in text: return int(float(text.replace('万', '')) * 10000)
            if 'K' in text: return int(float(text.replace('K', '')) * 1000)
            if 'M' in text: return int(float(text.replace('M', '')) * 1000000)
            match = re.search(r'(\d+(\.\d+)?)', text)
            return int(float(match.group(1))) if match else 0
        except: return 0

    def is_time_valid(self, time_text):
        if not time_text: return False
        if any(bad in time_text for bad in ['d', '日', 'y', '年', '月', 'Feb', 'Jan', 'Dec']): return False
        if any(unit in time_text for unit in ['m', 's', '分', '秒']): return True 
        if any(unit in time_text for unit in ['h', '小时', '時間']):
            try:
                match = re.search(r'\d+', time_text)
                return int(match.group()) <= Config.MAX_TIME_HOURS if match else False
            except: return False
        return False

    def get_unique_reply(self, text_content, has_media):
        for _ in range(5):
            reply = ReplyLibrary.get_smart_reply(text_content, has_media)
            clean_new = re.sub(r'[^\w]', '', reply)[:5]
            is_duplicate = False
            for old in self.recent_replies:
                clean_old = re.sub(r'[^\w]', '', old)[:5]
                if clean_new == clean_old:
                    is_duplicate = True; break
            if not is_duplicate:
                self.recent_replies.append(reply)
                if len(self.recent_replies) > 30: self.recent_replies.pop(0)
                return reply
        return reply

    # === 猎杀Lite (只点赞) ===
    def perform_hunt_lite(self, page):
        self.log("⚔️ 启动『猎杀点赞』(Lite)...", "bold magenta")
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        search_query = f"lang:ja min_faves:1000 -filter:retweets -filter:replies since:{today}"
        search_url = f"https://x.com/search?q={search_query}&src=typed_query&f=top"
        
        try:
            page.goto(search_url, timeout=60000)
            time.sleep(5)
            
            liked_count = 0
            target_likes = random.randint(1, 3)
            
            for _ in range(3):
                if liked_count >= target_likes: break
                
                tweets = page.locator('article[data-testid="tweet"]').all()
                for tweet in tweets:
                    if liked_count >= target_likes: break
                    try:
                        like_btn = tweet.locator('[data-testid="like"]').first
                        aria_label = like_btn.get_attribute("aria-label") or ""
                        if "Unlike" in aria_label or "取消" in aria_label: continue

                        like_btn.scroll_into_view_if_needed()
                        time.sleep(0.5)
                        like_btn.click(force=True)
                        self.log(f"❤️ 猎杀点赞 ({liked_count+1}/{target_likes})", "magenta")
                        
                        liked_count += 1
                        time.sleep(random.uniform(1, 2))
                    except: continue
                
                page.keyboard.press("PageDown")
                time.sleep(2)
            
            self.log("⚔️ 猎杀结束，秒回主页。", "dim")

        except Exception as e:
            self.log(f"⚠️ 猎杀异常: {e}", "yellow")
        
        try: page.goto(Config.Target_URL, timeout=60000)
        except: pass
        time.sleep(5)

    # === 主页处理逻辑 ===
    def process_home_tweet(self, page, tweet, text, time_val, metrics):
        likes, replies, views = metrics
        
        has_media = False
        if tweet.locator('[data-testid="tweetPhoto"]').count() > 0: has_media = True
        elif tweet.locator('[data-testid="videoPlayer"]').count() > 0: has_media = True
        
        media_tag = "🖼️" if has_media else "📄"
        view_str = f"{views/10000:.1f}万" if views >= 10000 else str(views)
        
        self.log(f"🎯 锁定: {media_tag} 赞{likes} 回{replies} 阅{view_str} | {time_val}", "cyan")

        if has_media: time.sleep(random.uniform(2, 4))

        if random.random() < 0.3:
            try: tweet.locator('[data-testid="like"]').first.click(timeout=2000, force=True)
            except: pass

        reply_btn = tweet.locator('[data-testid="reply"]').first
        try:
            reply_btn.scroll_into_view_if_needed(timeout=3000)
            time.sleep(0.5)
            reply_btn.click(timeout=3000, force=True)
        except: pass
        
        time.sleep(2.5)

        all_editors = page.locator('div[role="textbox"][contenteditable="true"]')
        if all_editors.count() < 2:
            try: reply_btn.evaluate("element => element.click()")
            except: pass
            time.sleep(3)
            all_editors = page.locator('div[role="textbox"][contenteditable="true"]')
            if all_editors.count() < 2:
                page.keyboard.press("Escape"); return

        target_editor = all_editors.last
        
        try:
            target_editor.click(timeout=3000, force=True)
            time.sleep(0.5)
            
            content = self.get_unique_reply(text, has_media)
            self.log(f"🧠 输入: {content}", "cyan")

            page.keyboard.insert_text(content)
            time.sleep(0.5)
            page.keyboard.press("Space"); time.sleep(0.1); page.keyboard.press("Backspace")
            time.sleep(1)
            
            clicked = False
            send_btns = page.locator('[data-testid="tweetButton"], [data-testid="tweetButtonInline"]').filter(has_text="Reply").or_(page.locator('[data-testid="tweetButton"]'))
            
            for i in range(send_btns.count()):
                btn = send_btns.nth(i)
                if btn.is_enabled():
                    btn.click()
                    clicked = True
                    self.replied_count += 1
                    self.log(f"✅ 发送成功 ({self.replied_count})", "bold green")
                    sleep_time = random.randint(Config.MIN_SLEEP, Config.MAX_SLEEP)
                    self.log(f"💤 休息 {sleep_time} 秒...", "dim")
                    time.sleep(sleep_time)
                    break
            
            if not clicked:
                target_editor.press("Control+A"); target_editor.press("Control+X")
                time.sleep(0.5); target_editor.press("Control+V"); time.sleep(1)
                
                for i in range(send_btns.count()):
                    btn = send_btns.nth(i)
                    if btn.is_enabled():
                        btn.click(); clicked = True
                        self.replied_count += 1
                        self.log(f"✅ 唤醒发送 ({self.replied_count})", "bold green")
                        time.sleep(60); break
                
                if not clicked:
                    page.keyboard.press("Escape")

        except Exception:
            page.keyboard.press("Escape")

    def run(self):
        if not os.path.exists("cookies.json"):
            self.log("❌ 未找到 cookies.json", "red"); return

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=Config.HEADLESS)
                context = browser.new_context(
                    storage_state="cookies.json",
                    viewport={'width': 1920, 'height': 1080},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                page = context.new_page()
            except Exception as e:
                self.log(f"❌ 启动失败: {e}", "red"); return

            self.log("🚀 V10.2 引擎启动 (繁中修复版)...", "bold green")
            try: page.goto(Config.Target_URL, timeout=60000)
            except: pass
            time.sleep(8)

            while True:
                if self.replied_count >= Config.DAILY_LIMIT:
                    self.log("🛑 任务完成", "red"); break

                # 猎杀 Lite
                if time.time() - self.last_hunt_time > 3600:
                    self.perform_hunt_lite(page)
                    self.last_hunt_time = time.time()
                    self.scroll_steps = 0
                    continue

                tweets = page.locator('article[data-testid="tweet"]').all()
                
                if len(tweets) == 0:
                    self.empty_scan_count += 1
                    
                    # === 核心修复：繁简中英 全面兼容 ===
                    # 增加了：開始、解鎖、認證、Verify、Continue
                    unlock_patterns = re.compile(r'Start|Unlock|Authenticate|Verify|Yes|Continue|開始|解鎖|認證|开始|解锁|认证', re.IGNORECASE)
                    
                    # 查找包含这些关键词的按钮
                    unlock_btns = page.locator('div[role="button"]').filter(has_text=unlock_patterns)
                    
                    if unlock_btns.count() > 0:
                        btn_text = unlock_btns.first.inner_text()
                        self.log(f"🔓 检测到锁定按钮 [{btn_text}]，尝试点击...", "bold magenta")
                        try: 
                            unlock_btns.first.click(timeout=5000)
                            time.sleep(5)
                            # 点完后刷新页面看是否解开
                            page.goto(Config.Target_URL)
                            continue
                        except Exception as e: 
                            self.log(f"❌ 点击失败: {e}", "red")
                    
                    retry = page.locator('div[role="button"]').filter(has_text="Retry")
                    if retry.count() > 0: retry.click()

                    if self.empty_scan_count >= 3:
                        try: page.goto(Config.Target_URL); self.empty_scan_count=0; time.sleep(10); continue
                        except: pass
                else:
                    self.empty_scan_count = 0

                for tweet in tweets:
                    try:
                        text = tweet.inner_text()
                        time_node = tweet.locator('time').first
                        if not time_node.count(): continue
                        time_val = time_node.inner_text()

                        try:
                            reply_val = tweet.locator('[data-testid="reply"]').get_attribute("aria-label") or "0"
                            like_val = tweet.locator('[data-testid="like"]').get_attribute("aria-label") or "0"
                            
                            views = 0
                            analytics_link = tweet.locator('a[href*="/analytics"]').first
                            if analytics_link.count() > 0:
                                view_val = analytics_link.get_attribute("aria-label") or "0"
                                views = self.parse_number(view_val)

                            replies = self.parse_number(reply_val)
                            likes = self.parse_number(like_val)
                        except: continue

                        tid = f"{text[:20]}_{time_val}"
                        if tid in self.processed_tweets: continue
                        self.processed_tweets.add(tid)

                        if any(b in text for b in Config.BLACKLIST): continue
                        if not self.is_time_valid(time_val): continue
                        
                        if likes < Config.MIN_LIKES: continue
                        if replies > Config.MAX_REPLIES: continue
                        # 展现量限制已移除

                        self.process_home_tweet(page, tweet, text, time_val, (likes, replies, views))

                    except: continue

                self.log("🔄 滚动...", "dim")
                page.keyboard.press("PageDown")
                self.scroll_steps += 1
                
                if self.scroll_steps >= 7:
                    self.log("🔄 刷新主页...", "magenta")
                    try: page.goto(Config.Target_URL); self.scroll_steps=0; time.sleep(8)
                    except: pass
                
                time.sleep(random.uniform(3, 6))

if __name__ == "__main__":
    bot = XBot()
    bot.run()
