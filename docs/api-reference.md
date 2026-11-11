# API 参考

# API 参考

## POST /generate

```json
{"prompt": "一只柴犬", "steps": 12, "guidance": 4.5, "width": 1024, "height": 1024}
```

## POST /edit

```json
{"instruction": "把背景换成雪地", "image": [[[...]]], "strength": 0.75}
```

## GET /health

`{"status": "ok"}`

