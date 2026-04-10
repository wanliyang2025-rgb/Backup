#!/usr/bin/env python3
"""
QMD 语义搜索工具
用法: python3 qmd_search.py <搜索词>
"""
import subprocess
import json
import sys

def search(query, mode="vsearch", limit=10):
    """执行 QMD 搜索"""
    cmd = ["qmd", mode, query, "--json"]
    if limit:
        cmd.extend(["--limit", str(limit)])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return {"error": result.stderr or "搜索失败"}
        
        # 尝试解析 JSON
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"raw": result.stdout, "error": None}
    except subprocess.TimeoutExpired:
        return {"error": "搜索超时"}
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("用法: python3 qmd_search.py <搜索词> [模式: vsearch|search|query]")
        print("模式: vsearch=语义搜索, search=关键词, query=混合+重排序(最精准)")
        sys.exit(1)
    
    query = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "vsearch"
    
    print(f"🔍 搜索: {query} (模式: {mode})\n")
    
    results = search(query, mode)
    
    if "error" in results:
        print(f"❌ 错误: {results['error']}")
        sys.exit(1)
    
    if "results" in results:
        for i, r in enumerate(results["results"], 1):
            title = r.get("title", "无标题")
            path = r.get("path", "")
            score = r.get("score", 0)
            snippet = r.get("snippet", "")[:100]
            print(f"{i}. [{score:.2f}] {title}")
            print(f"   路径: {path}")
            if snippet:
                print(f"   摘要: {snippet}...")
            print()
    else:
        print(results)

if __name__ == "__main__":
    main()
