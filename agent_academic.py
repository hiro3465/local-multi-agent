# -*- coding: utf-8 -*-
import time
import os
import urllib.request
import json

SHARED_FILE = "shared_memo.txt"
MY_ROLE = "Academic"

def call_ollama(prompt):
    # Ollama（ローカルLLM）を呼び出す関数
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "hf.co/elyza/Llama-3-ELYZA-JP-8B-GGUF",  # またはお使いのローカルモデル名（qwenなど）
        "prompt": f"あなたは放送大学の学術的背景に精通した研究者です。以下の共有ノートを読み、学術的な視点や理論的な裏付けを加えて200字程度で返答を追記してください。\n\n{prompt}",
        "stream": False
    }
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode("utf-8"), 
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            return res.get("response", "")
    except Exception as e:
        return f"[Error connecting to Ollama: {e}]"

def main():
    print(f"[{MY_ROLE}] 起動しました。相手の書き込みを待ちます...")
    last_content = ""
    
    while True:
        if os.path.exists(SHARED_FILE):
            with open(SHARED_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            
            # ファイルが更新されており、直近の書き込みが自分以外の場合に反応
            if content != last_content and f"[{MY_ROLE}]" not in content[-100:]:
                print(f"[{MY_ROLE}] 新しいメッセージを検知しました。思考中...")
                time.sleep(2) # 落ち着いて読むためのウェイト
                
                # Ollamaに考えさせる
                reply = call_ollama(content)
                
                # 共有ファイルに追記
                new_entry = f"\n\n--- [{MY_ROLE}の意見] ---\n{reply}"
                with open(SHARED_FILE, "a", encoding="utf-8") as f:
                    f.write(new_entry)
                
                with open(SHARED_FILE, "r", encoding="utf-8") as f:
                    last_content = f.read()
                print(f"[{MY_ROLE}] 返信を書き込みました。")
                
        time.sleep(3) # 3秒ごとにファイルをチェック

if __name__ == "__main__":
    main()