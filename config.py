# config.py
# -*- coding: utf-8 -*-

class Config:
    # --- 基础设置 ---
    HEADLESS = True       # True=后台静默模式(VPS用), False=能看到浏览器(Mac调试用)
    Target_URL = "https://x.com/home"  # 推荐页

    # --- 筛选漏斗 (核心逻辑) ---
    MAX_TIME_HOURS = 6     # 只要 6 小时内的推文
    MIN_LIKES = 100        # 点赞数大于 100
    MAX_REPLIES = 20       # 评论数小于 20 (抢占前排)
    MIN_VIEWS = 10000     # 【新增】最低展现量 (少于1万的没人看，不回)
    
    # --- 频率控制 (安全第一) ---
    MAX_REPLIES_PER_HOUR = 99  # 建议蓝V初期不要超过50，逐步增加
    DAILY_LIMIT = 2400          # 单日最大回复数
    
    # --- 冷却时间 (秒) ---
    # 模拟真人：发完一条后，休息多久
    MIN_SLEEP = 20         
    MAX_SLEEP = 59        
    
    # --- 关键词黑名单 ---
    # 如果推文包含这些词，绝对不回（避坑政治、负面、成人）
    BLACKLIST = [
        "死", "殺", "引退", "炎上", "悲報", "緊急", 
        "政治", "宗教", "crypto scam", "giveaway",
        "エロ", "nft", "promo", "bot", "裏垢", "募集"
    ]
