# 飞书文档 API 参考

## 认证

```bash
# 获取 tenant_access_token
curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_a93b3aa665789cc2","app_secret":"d4lvhry3RZcCtDfGekHbyeNTy00TXjv0"}'
```

响应：
```json
{"code":0,"tenant_access_token":"t-xxx...","msg":"ok"}
```

## 创建文档

```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"title":"文档标题"}'
```

## 获取文档块

```bash
curl "https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks?document_revision_id=-1&page_size=50" \
  -H "Authorization: Bearer {TOKEN}"
```

根块 ID = 文档 ID

## 添加块

```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{parent_id}/children" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"children":[{"block_type":2,"text":{"elements":[{"text_run":{"content":"文本内容"}}],"style":{"align":1}}}],"index":-1}'
```

## Block Type 速查

| type | 说明 |
|------|------|
| 1 | 页面（根） |
| 2 | 文本段落 |
| 3 | 标题1 (h1) |
| 4 | 标题2 (h2) |
| 5 | 标题3 (h3) |
| 12 | 无序列表 |
| 13 | 有序列表 |
| 1003 | 表格 |

## 常见错误

- `1770001 invalid param`: 参数格式错误，常见于 index 位置错误
- `99992402`: 表格创建失败（复杂表格建议拆分成多个文本块）
