# -*- coding: utf-8 -*-
import time
import os

SHARED_FILE = "shared_memo.txt"

def main():
    print("=== shared_memo.txt リアルタイムモニター開始 ===")
    last_content = ""
    
    while True:
        if os.path.exists(SHARED_FILE):
            with open(SHARED_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            
            if content != last_content:
                # 画面を綺麗にして最新の内容を表示
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"=== shared_memo.txt リアルタイムモニター ({time.strftime('%H:%M:%S')}) ===")
                print(content)
                last_content = content
                
        time.sleep(1)

if __name__ == "__main__":
    main()