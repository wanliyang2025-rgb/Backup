#!/bin/bash
# 极空间 NAS WebDAV 便捷工具
# 用法:
#   ./nas.sh list <path>          # 列出目录
#   ./nas.sh get <path> <outfile> # 下载文件
#   ./nas.sh put <local> <path>    # 上传文件

HOST="192.168.3.134"
PORT="5005"
USER="18664974664"
PASS="Wly19940728"

CMD=$1
shift

case $CMD in
  list)
    curl -s -X PROPFIND -u "$USER:$PASS" -H "Depth: 1" \
      "http://$HOST:$PORT/$1" | python3 -c "
import sys, re
content = sys.stdin.read()
hrefs = re.findall(r'<D:href>([^<]+)</D:href>', content)
for h in hrefs:
    import urllib.parse
    print(urllib.parse.unquote(h))
"
    ;;
  get)
    curl -s -u "$USER:$PASS" "http://$HOST:$PORT/$1" -o "$2"
    echo "Downloaded to $2"
    ;;
  put)
    curl -s -u "$USER:$PASS" -T "$1" "http://$HOST:$PORT/$2"
    echo "Uploaded to $2"
    ;;
  *)
    echo "Usage: nas.sh {list|get|put} <args...>"
    ;;
esac
