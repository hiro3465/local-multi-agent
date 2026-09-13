# -*- coding: utf-8 -*-
import time
import os
import urllib.request
import json

SHARED_FILE = "shared_memo.txt"
MY_ROLE = "Business"
MAX_ROUNDS = 2  # 終了とする往復回数

def call_ollama(prompt, is_final=False):
    url = "http://localhost:11434/api/generate"
    if is_final:
        system_prompt = "あなたは実務に精通したビジネスパーソンです。ここまでの議論を踏まえ、最終的な結論と成果を200字程度でまとめてください。"
    else:
        system_prompt = "あなたは実務に精通したビジネスパーソンです。以下の共有ノートの学術的意見に対して、実際の仕事での活用法やツッコミ、具体例を200字程度で返答を追記してください。"

    data = {
        "model": "hf.co/elyza/Llama-3-ELYZA-JP-8B-GGUF",
        "prompt": f"{system_prompt}\n\n{prompt}",
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
    print(f"[{MY_ROLE}] 起動しました。")
    last_content = ""
    
    while True:
        if os.path.exists(SHARED_FILE):
            with open(SHARED_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 発言回数をカウント
            Business_count = content.count("[Businessの意見]")
            
            # 上限に達していたら最終まとめて終了
            if Business_count >= MAX_ROUNDS:
                if f"[{MY_ROLE} 最終結論]" not in content:
                    print(f"[{MY_ROLE}] 規定のラウンド数に達しました。最終結論をまとめます...")
                    reply = call_ollama(content, is_final=True)
                    new_entry = f"\n\n--- [{MY_ROLE} 最終結論] ---\n{reply}"
                    with open(SHARED_FILE, "a", encoding="utf-8") as f:
                        f.write(new_entry)
                print(f"[{MY_ROLE}] 処理を終了します。")
                break

            if content != last_content and f"[{MY_ROLE}]" not in content[-100:]:
                print(f"[{MY_ROLE}] 新しいメッセージを検知しました。思考中...")
                time.sleep(2)
                
                reply = call_ollama(content)
                new_entry = f"\n\n--- [{MY_ROLE}の意見] ---\n{reply}"
                with open(SHARED_FILE, "a", encoding="utf-8") as f:
                    f.write(new_entry)
                
                with open(SHARED_FILE, "r", encoding="utf-8") as f:
                    last_content = f.read()
                print(f"[{MY_ROLE}] 返信を書き込みました。")
                
        time.sleep(3)

if __name__ == "__main__":
    main()