#!/usr/bin/env python3
"""
🏓 Pickleball Master - 匹克球挑戰遊戲
A fun terminal game about pickleball!

Usage:
    python3 pickleball_game.py
"""

import random
import time
import sys

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def c(text, color):
    return f"{color}{text}{Colors.RESET}"

def print_slow(text, delay=0.03):
    """Print text with typing effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_header(title):
    """Print game header"""
    print()
    print(c("═" * 70, Colors.CYAN))
    print(c(f"  {title}", Colors.BOLD + Colors.CYAN))
    print(c("═" * 70, Colors.CYAN))
    print()

def welcome():
    """Welcome screen"""
    print_header("🏓 PICKLEBALL MASTER 匹克球挑戰")
    print_slow("歡迎來到匹克球挑戰遊戲！", 0.05)
    print()
    print("目標：成為匹克球大師！通過各種挑戰提升你的等級。")
    print()
    print("遊戲規則：")
    print("  1. 回答問題 / 完成挑戰")
    print("  2. 贏取積分")
    print("  3. 提升等級")
    print("  4. 成為大師！")
    print()

def get_player_name():
    """Get player name"""
    print(c("請輸入你的名字：", Colors.YELLOW), end=" ")
    name = input().strip()
    if not name:
        name = "匹克球手"
    print()
    print_slow(f"好！{name}，讓我哋開始啦！🚀", 0.03)
    print()
    return name

class Game:
    def __init__(self, player_name):
        self.player_name = player_name
        self.score = 0
        self.level = 1
        self.streak = 0
        self.games_played = 0
        self.title = "🌱 新手"
        self.update_level()
        
    def update_level(self):
        """Update player level based on score"""
        if self.score >= 100:
            self.level = 5
            self.title = "🏆 匹克球大師"
        elif self.score >= 70:
            self.level = 4
            self.title = "⭐ 高級玩家"
        elif self.score >= 40:
            self.level = 3
            self.title = "🎯 中級玩家"
        elif self.score >= 20:
            self.level = 2
            self.title = "🎾 初學者"
        else:
            self.level = 1
            self.title = "🌱 新手"
    
    def show_status(self):
        """Show player status"""
        print()
        print(c("┌" + "─" * 68 + "┐", Colors.DIM))
        print(c(f"│  玩家：{self.player_name:<50} │", Colors.DIM))
        print(c(f"│  等級：Lv.{self.level} - {self.title:<43} │", Colors.DIM))
        print(c(f"│  積分：{self.score:<55} │", Colors.DIM))
        print(c(f"│  連勝：{self.streak:<55} │", Colors.DIM))
        print(c("└" + "─" * 68 + "┘", Colors.DIM))
        print()
    
    def quiz_game(self):
        """Pickleball quiz game"""
        print_header(f"📝 知識挑戰 - 第 {self.games_played + 1} 關")
        
        questions = [
            {
                "q": "匹克球嘅英文係咩？",
                "options": ["A) Tennis", "B) Pickleball", "C) Badminton", "D) Squash"],
                "answer": "B",
                "points": 10
            },
            {
                "q": "一個標準匹克球場有幾呎長？",
                "options": ["A) 20 呎", "B) 30 呎", "C) 44 呎", "D) 60 呎"],
                "answer": "C",
                "points": 15
            },
            {
                "q": "匹克球比賽通常係幾分制？",
                "options": ["A) 11 分", "B) 15 分", "C) 21 分", "D) 25 分"],
                "answer": "A",
                "points": 10
            },
            {
                "q": "\"Kitchen\" 在匹克球中指的是什麼？",
                "options": ["A) 休息區", "B) 發球區", "C) 非截擊區", "D) 觀眾區"],
                "answer": "C",
                "points": 15
            },
            {
                "q": "匹克球拍通常用咩材料做？",
                "options": ["A) 木", "B) 金屬", "C) 複合材料", "D) 塑料"],
                "answer": "C",
                "points": 10
            },
            {
                "q": "雙打比賽有幾多人參與？",
                "options": ["A) 2 人", "B) 3 人", "C) 4 人", "D) 6 人"],
                "answer": "C",
                "points": 5
            },
            {
                "q": "發球時要打過幾多個區？",
                "options": ["A) 1 個", "B) 2 個", "C) 3 個", "D) 4 個"],
                "answer": "A",
                "points": 10
            },
            {
                "q": "匹克球起源於哪個國家？",
                "options": ["A) 英國", "B) 美國", "C) 中國", "D) 澳洲"],
                "answer": "B",
                "points": 10
            }
        ]
        
        # Select 3 random questions
        selected = random.sample(questions, min(3, len(questions)))
        
        correct = 0
        for i, q in enumerate(selected, 1):
            print(f"\n{c(f'問題 {i}:', Colors.YELLOW)} {c(q['q'], Colors.BOLD)}")
            for opt in q['options']:
                print(f"  {opt}")
            
            print()
            print(c("你的答案 (A/B/C/D): ", Colors.YELLOW), end="")
            answer = input().strip().upper()
            
            if answer == q['answer']:
                print(c("✅ 正確！", Colors.GREEN))
                self.score += q['points']
                self.streak += 1
                correct += 1
                # Bonus for streak
                if self.streak >= 3:
                    bonus = 5
                    self.score += bonus
                    print(c(f"🔥 連勝獎勵 +{bonus}!", Colors.YELLOW))
            else:
                print(c(f"❌ 錯誤！正確答案係 {q['answer']}", Colors.RED))
                self.streak = 0
            
            time.sleep(1)
        
        self.games_played += 1
        print()
        print(c(f"📊 本輪成績：{correct}/{len(selected)} 正確", Colors.CYAN))
        self.update_level()
    
    def reflex_game(self):
        """Simple reflex/reaction game"""
        print_header(f"⚡ 反應挑戰 - 第 {self.games_played + 1} 關")
        
        print("規則：當見到「🏓」時，立即按 Enter！")
        print("準備好未？...")
        print()
        
        time.sleep(2)
        
        # Random delay 2-5 seconds
        delay = random.uniform(2, 5)
        time.sleep(delay)
        
        print(c("🏓 按 Enter!", Colors.BOLD + Colors.GREEN))
        
        start = time.time()
        input()
        reaction = time.time() - start
        
        print()
        print(f"你的反應時間：{c(f'{reaction:.3f} 秒', Colors.CYAN)}")
        
        # Scoring based on reaction time
        if reaction < 0.2:
            points = 30
            msg = "🏆 世界級反應！"
        elif reaction < 0.3:
            points = 20
            msg = "⭐ 非常好！"
        elif reaction < 0.4:
            points = 15
            msg = "👍 不錯！"
        elif reaction < 0.5:
            points = 10
            msg = "🙂 平均"
        else:
            points = 5
            msg = "💪 繼續練習！"
        
        print(c(msg, Colors.GREEN))
        print(c(f"+{points} 積分！", Colors.YELLOW))
        
        self.score += points
        self.games_played += 1
        self.update_level()
    
    def serve_challenge(self):
        """Serving accuracy challenge"""
        print_header(f"🎯 發球準確度挑戰 - 第 {self.games_played + 1} 關")
        
        print("目標：發球入區！")
        print("你會見到一個移動嘅目標，喺啱嘅時機按 Enter 發球！")
        print()
        print("準備...")
        time.sleep(1)
        
        successful = 0
        attempts = 5
        
        for i in range(attempts):
            print(f"\n發球 {i+1}/{attempts}")
            print("目標移動中...", end="")
            
            # Random timing challenge
            target_pos = random.randint(1, 10)
            time.sleep(random.uniform(0.5, 1.5))
            print(" 現在！")
            
            start = time.time()
            input()
            reaction = time.time() - start
            
            # Success if reaction is close to target timing
            if 0.3 < reaction < 0.7:
                print(c("✅ 好球！入區！", Colors.GREEN))
                successful += 1
            else:
                print(c("❌ 出界！", Colors.RED))
        
        # Calculate score
        accuracy = (successful / attempts) * 100
        points = int(accuracy * 0.5)
        
        print()
        print(c(f"📊 準確度：{successful}/{attempts} ({accuracy:.0f}%)", Colors.CYAN))
        print(c(f"+{points} 積分！", Colors.YELLOW))
        
        self.score += points
        self.games_played += 1
        self.update_level()
    
    def show_menu(self):
        """Show game menu"""
        print()
        print(c("╔" + "═" * 68 + "╗", Colors.BLUE))
        print(c("║  選擇挑戰：", Colors.BOLD + Colors.BLUE) + " " * 54 + "║")
        print(c("╠" + "═" * 68 + "╣", Colors.BLUE))
        print(c("║  1. 📝 知識挑戰 (回答問題)", Colors.CYAN) + " " * 35 + "║")
        print(c("║  2. ⚡ 反應挑戰 (測試反應)", Colors.CYAN) + " " * 35 + "║")
        print(c("║  3. 🎯 發球挑戰 (準確度)", Colors.CYAN) + " " * 36 + "║")
        print(c("║  4. 📊 查看進度", Colors.CYAN) + " " * 48 + "║")
        print(c("║  5. 🚪 退出遊戲", Colors.CYAN) + " " * 48 + "║")
        print(c("╚" + "═" * 68 + "╝", Colors.BLUE))
        print()
    
    def play(self):
        """Main game loop"""
        welcome()
        name = get_player_name()
        
        while True:
            self.show_status()
            self.show_menu()
            
            print(c("請選擇 (1-5): ", Colors.YELLOW), end="")
            choice = input().strip()
            
            if choice == "1":
                self.quiz_game()
            elif choice == "2":
                self.reflex_game()
            elif choice == "3":
                self.serve_challenge()
            elif choice == "4":
                self.show_status()
                print("繼續加油！你可以做到！💪")
            elif choice == "5":
                print()
                print(c("多謝你玩 Pickleball Master!", Colors.CYAN))
                print(c(f"最終成績:", Colors.YELLOW))
                print(f"  等級：Lv.{self.level} - {self.title}")
                print(f"  積分：{self.score}")
                print(f"  遊戲次數：{self.games_played}")
                print()
                print(c("下次見！👋", Colors.GREEN))
                print()
                break
            else:
                print(c("無效選擇，請再試！", Colors.RED))
            
            time.sleep(1)

if __name__ == '__main__':
    try:
        game = Game("")
        game.play()
    except KeyboardInterrupt:
        print()
        print(c("\n遊戲中斷！下次見！👋", Colors.YELLOW))
        print()
