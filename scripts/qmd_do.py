#!/usr/bin/env python3
"""
QMD 语义搜索 - LeonWan Obsidian Vault 专用
用法: python3 qmd_do.py <search|list|status> [args]
"""
import subprocess
import json
import sys
import os

VAULT_PATH = os.path.expanduser("~/obsidian-vault")

def cmd(*args):
    return subprocess.run(args, capture_output=True, text=True)

def do_search(query, mode="vsearch", limit=8):
    """执行搜索并美化输出"""
    result = cmd("qmd", mode, query, "--limit", str(limit), "--json")
    
    if result.returncode != 0:
        return False, result.stderr or "搜索失败"
    
    try:
        data = json.loads(result.stdout)
    except:
        return False, f"解析失败: {result.stdout[:200]}"
    
    if "results" not in data or not data["results"]:
        return True, f"没有找到与 '{query}' 相关的内容"
    
    lines = []
    lines.append(f"🔍 搜索: {query} (模式: {mode})\n")
    lines.append(f"📚 Obsidian Vault: {VAULT_PATH}")
    lines.append(f"📊 找到 {len(data['results'])} 条结果:\n")
    lines.append("─" * 50)
    
    for i, r in enumerate(data["results"], 1):
        title = r.get("title", "无标题")
        path = r.get("path", "")
        score = r.get("score", 0)
        snippet = r.get("snippet", "")
        
        # 相对路径
        if "obsidian-vault/" in path:
            rel_path = path.split("obsidian-vault/")[-1]
        else:
            rel_path = path
        
        lines.append(f"\n{i}. {title}")
        lines.append(f"   📁 {rel_path}  (相关度: {score:.2f})")
        if snippet:
            lines.append(f"   💬 {snippet[:150]}{'...' if len(snippet) > 150 else ''}")
    
    return True, "\n".join(lines)

def do_list():
    """列出已索引的笔记"""
    result = cmd("qmd", "collection", "list")
    if result.returncode != 0:
        return False, result.stderr
    
    out = []
    out.append("📚 QMD 已索引的集合:\n")
    out.append("─" * 40)
    
    try:
        data = json.loads(result.stdout)
        for coll in data.get("collections", []):
            name = coll.get("name", "?")
            path = coll.get("path", "")
            count = coll.get("count", 0)
            out.append(f"\n• {name}: {count} 条笔记")
            out.append(f"  路径: {path}")
    except:
        out.append(result.stdout)
    
    return True, "\n".join(out)

def do_status():
    """检查 QMD embed 状态"""
    # 检查进程
    p = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    embeding = "qmd" in p.stdout and "embed" in p.stdout
    
    result = cmd("qmd", "collection", "list")
    
    lines = ["📊 QMD 状态检查"]
    lines.append("─" * 40)
    
    if embeding:
        lines.append("⏳ embed 正在运行中（下载模型ing）...")
    else:
        lines.append("✅ embed 未在运行")
    
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            cols = data.get("collections", [])
            lines.append(f"✅ 已配置 {len(cols)} 个集合")
            for c in cols:
                lines.append(f"  • {c.get('name')} ({c.get('count', 0)} 条)")
        except:
            lines.append(f"⚠️ 集合列表解析异常: {result.stdout[:200]}")
    else:
        lines.append(f"❌ QMD 未配置: {result.stderr}")
    
    return True, "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print("用法: qmd_do.py <search|list|status> [query]")
        print("示例: qmd_do.py search 知识管理")
        print("      qmd_do.py status")
        print("      qmd_do.py list")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "search":
        if len(sys.argv) < 3:
            print("请提供搜索词: qmd_do.py search <查询>")
            sys.exit(1)
        query = sys.argv[2]
        mode = sys.argv[3] if len(sys.argv) > 3 else "vsearch"
        ok, msg = do_search(query, mode)
        print(msg)
        
    elif action == "list":
        ok, msg = do_list()
        print(msg)
        
    elif action == "status":
        ok, msg = do_status()
        print(msg)
    else:
        print(f"未知操作: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
