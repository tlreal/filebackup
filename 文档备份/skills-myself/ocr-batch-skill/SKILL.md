---
name: ocr-batch
description: 批量OCR处理 - 调用千帆API识别图片，输出Markdown并自动合并
---

# OCR Batch - 批量OCR处理

## 概述

批量处理图片OCR识别，使用百度千帆 Layout Parsing API 将图片识别为 Markdown 格式。

**功能**:
- 批量调用千帆 API 进行 OCR
- 每张图片保存为单独的 md 文件
- 自动重试失败的图片
- 按数字顺序合并所有 md 文件

**开始时宣布**: 「我正在使用 ocr-batch 技能来处理批量OCR任务。」

---

## 前置条件

1. **Python 环境**: `C:/ProgramData/miniconda3/envs/paddle26/python.exe`
2. **脚本位置**: `d:/Users/tanle/Desktop/sp/ocr_api.py`
3. **千帆 API**: 已配置 TOKEN 和 API_URL

---

## 使用方式

### 单个章节

```
/ocr --chapter "第5章"
```

### 多个章节

```
/ocr --chapters 5-16
```

### 指定图片范围

```
/ocr --chapter "第4章" --start 44 --end 44
```

---

## 处理流程

### 步骤 1: 批量OCR

```bash
cd /d/Users/tanle/Desktop/sp
C:/ProgramData/miniconda3/envs/paddle26/python.exe ocr_api.py --input "第X章"
```

**输出**:
- 每张图片 -> `第X章/md/{序号:02d}.md`
- 自动合并 -> `第X章/merged.md`

### 步骤 2: 检查失败

```python
from pathlib import Path

chapter = Path("第X章")
images = [p for p in chapter.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}]
md_files = {int(p.stem): p for p in (chapter / "md").glob("*.md") if p.stem.isdigit()}

missing = [i for i in range(1, len(images) + 1) if i not in md_files]
print(f"缺失: {missing}")
```

### 步骤 3: 重试失败的图片

```bash
# 重试单张
C:/ProgramData/miniconda3/envs/paddle26/python.exe ocr_api.py --input "第X章" --start-index N --end-index N

# 重试多张
C:/ProgramData/miniconda3/envs/paddle26/python.exe ocr_api.py --input "第X章" --start-index N --end-index M
```

### 步骤 4: 重新合并

```bash
C:/ProgramData/miniconda3/envs/paddle26/python.exe ocr_api.py --input "第X章" --merge-only
```

---

## ocr_api.py 脚本功能

| 参数 | 说明 |
|------|------|
| `--input` | 图片目录路径（如 `第5章`） |
| `--output-dir` | 输出目录（默认 `<input>/md/`） |
| `--start-index` | 从第几张开始（1-based） |
| `--end-index` | 到第几张结束 |
| `--delay` | 请求延迟（秒，默认 0.5） |
| `--merge-only` | 仅合并已有md文件 |

---

## 常见错误处理

| 错误 | 原因 | 解决方法 |
|------|------|---------|
| `500 Internal Server Error` | API服务异常 | 重试该图片 |
| `503 Service Unavailable` | API暂时不可用 | 等待后重试 |
| `Connection broken` | 网络中断 | 重试该图片 |
| `ProxyError` | 代理连接失败 | 检查代理或稍后重试 |

---

## 处理状态检查

```bash
# 检查所有章节状态
cd /d/Users/tanle/Desktop/sp
python -c "
from pathlib import Path
for i in range(1, 17):
    chapter = Path(f'第{i}章')
    if chapter.exists():
        images = len([p for p in chapter.iterdir() if p.suffix.lower() in {'.jpg', '.jpeg', '.png'}])
        md_dir = chapter / 'md'
        md_count = len(list(md_dir.glob('*.md'))) if md_dir.exists() else 0
        status = 'OK' if images == md_count else 'FAIL'
        print(f'{status} 第{i:2d}章: {images:3d} 张 -> {md_count:3d} md')
"
```

---

## 记住

- 处理完成后检查是否有缺失的图片
- 所有失败图片都要重试
- 重试完成后必须重新合并
- 合并使用数字顺序，不是字母顺序

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|---------|
| v1.0 | 2026-02-26 | 初始版本，支持千帆API批量OCR |
