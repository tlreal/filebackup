"""
批量 OCR：调用百度千帆 Layout Parsing API，将图片识别并输出为 Markdown
"""
import argparse
import base64
import os
import sys
import time
from pathlib import Path

import requests


_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
_DOCUMENT_SUFFIXES = {".pdf"}

API_URL = "https://z87e8cr0f654u1g0.aistudio-app.com/layout-parsing"


def file_type_from_path(path: Path) -> int:
    suffix = path.suffix.lower()
    if suffix in _IMAGE_SUFFIXES:
        return 1
    if suffix in _DOCUMENT_SUFFIXES:
        return 0
    raise ValueError(f"不支持的文件类型: {suffix}")


def build_payload(file_data: str, *, file_type: int) -> dict:
    return {
        "file": file_data,
        "fileType": file_type,
        "useDocOrientationClassify": False,
        "useDocUnwarping": False,
        "useChartRecognition": False,
    }


def list_images(directory: Path) -> list[Path]:
    if not directory.exists() or not directory.is_dir():
        return []
    images: list[Path] = []
    for p in directory.iterdir():
        if not p.is_file():
            continue
        if p.suffix.lower() not in _IMAGE_SUFFIXES:
            continue
        images.append(p)
    images.sort(key=lambda p: p.name.lower())
    return images


def list_supported_files(directory: Path) -> list[Path]:
    if not directory.exists() or not directory.is_dir():
        return []
    files: list[Path] = []
    supported_suffixes = _IMAGE_SUFFIXES | _DOCUMENT_SUFFIXES
    for p in directory.iterdir():
        if not p.is_file():
            continue
        if p.suffix.lower() not in supported_suffixes:
            continue
        files.append(p)
    files.sort(key=lambda p: p.name.lower())
    return files


def resolve_images(input_path: Path) -> list[Path]:
    if input_path.exists() and input_path.is_file():
        if input_path.suffix.lower() in (_IMAGE_SUFFIXES | _DOCUMENT_SUFFIXES):
            return [input_path]
        return []
    return list_supported_files(input_path)


def call_cr_api(file_path: Path, *, token: str) -> dict | None:
    """调用千帆 Layout Parsing API"""
    try:
        with open(file_path, "rb") as file:
            file_bytes = file.read()
            file_data = base64.b64encode(file_bytes).decode("ascii")

        headers = {
            "Authorization": f"token {token}",
            "Content-Type": "application/json"
        }

        payload = build_payload(file_data, file_type=file_type_from_path(file_path))

        response = requests.post(API_URL, json=payload, headers=headers, timeout=180)

        if response.status_code != 200:
            print(f"  API 错误: {response.status_code} - {response.text}")
            return None

        return response.json().get("result")

    except Exception as e:
        print(f"  请求失败: {e}")
        return None


def run_ocr_for_images(images: list[Path], output_dir: Path, *, token: str, start_index: int = 1, delay: float = 0.5) -> list[Path]:
    """批量处理文件（图片或 PDF），每个输入文件保存为单独的 md 文件"""
    output_dir.mkdir(parents=True, exist_ok=True)
    md_files: list[Path] = []
    total = len(images)

    for idx, p in enumerate(images, start=start_index):
        print(f"[{idx}/{start_index + total - 1}] {p.name}")

        result = call_cr_api(p, token=token)
        if result and "layoutParsingResults" in result:
            layout_results = result["layoutParsingResults"]
            if layout_results:
                # 合并所有页面的 markdown 文本
                md_parts = []
                for res in layout_results:
                    md_text = res.get("markdown", {}).get("text", "")
                    if md_text:
                        md_parts.append(md_text)

                combined_md = "\n\n".join(md_parts)

                # 保存为单独的 md 文件，用全局索引命名
                md_filename = f"{idx:02d}.md"
                md_path = output_dir / md_filename
                md_path.write_text(combined_md, encoding="utf-8", newline="\n")
                md_files.append(md_path)
                print(f"  识别成功，{len(combined_md)} 字符 -> {md_filename}")
            else:
                print(f"  未识别到内容")
        else:
            print(f"  API 返回结果为空")

        # 避免请求过快
        if idx < start_index + total - 1:
            time.sleep(delay)

    return md_files


def build_markdown(pages: list[tuple[str, str]], *, include_header: bool = True, merge: bool = False) -> str:
    """构建 Markdown 输出"""
    parts: list[str] = []
    if include_header:
        parts.append("# OCR 结果\n\n")

    if merge:
        # 合并模式：所有内容连续输出，不分图片
        all_text = []
        for image_name, text in pages:
            if text:
                all_text.append(text)
        combined = "\n\n".join(all_text)
        parts.append(combined)
        if combined and not combined.endswith("\n"):
            parts.append("\n")
    else:
        # 分页模式：每张图片单独一个标题
        for image_name, text in pages:
            parts.append(f"## {image_name}\n\n")
            if text:
                parts.append(text)
                if not text.endswith("\n"):
                    parts.append("\n")
            parts.append("\n")

    return "".join(parts)


def merge_md_files(md_files: list[Path], output_path: Path) -> None:
    """合并多个 MD 文件成一个"""
    # 按文件名的数字部分排序
    def get_file_index(path: Path) -> int:
        name = path.stem  # 去掉 .md 后缀
        try:
            return int(name)
        except ValueError:
            return 0

    sorted_files = sorted(md_files, key=get_file_index)

    all_content = []
    for md_file in sorted_files:
        if md_file.exists():
            content = md_file.read_text(encoding="utf-8")
            if content:
                all_content.append(content)

    # 直接拼接，不加额外分隔
    merged = "".join(all_content)
    output_path.write_text(merged, encoding="utf-8", newline="\n")
    print(f"已合并 {len(sorted_files)} 个文件到: {output_path}")


def slice_images(images: list[Path], *, start_index: int, end_index: int | None) -> list[Path]:
    """切片图片列表"""
    if start_index <= 0:
        raise ValueError("start_index 必须大于 0")
    if end_index is not None and end_index <= 0:
        raise ValueError("end_index 必须大于 0")

    total = len(images)
    if total == 0:
        return []
    if start_index > total:
        raise ValueError("start_index 超出图片数量")

    end = total if end_index is None else min(end_index, total)
    if end < start_index:
        raise ValueError("end_index 不能小于 start_index")

    return images[start_index - 1 : end]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="用千帆 Layout Parsing API 批量识别图片并输出 Markdown")
    parser.add_argument("--run-tests", action="store_true", help="运行自测并退出")
    parser.add_argument("--input", default=r"d:\Users\tanle\Desktop\sp\第1章", help="图片目录或单张图片路径")
    parser.add_argument("--output-dir", default=None, help="输出目录（默认：<input>/md/）")
    parser.add_argument("--token", default=None, help="API token（也可用环境变量 QIANFAN_LAYOUT_TOKEN 或 OCR_API_TOKEN）")
    parser.add_argument("--start-index", type=int, default=1, help="从第几张开始（1-based，默认 1）")
    parser.add_argument("--end-index", type=int, default=None, help="到第几张结束（1-based，默认到最后）")
    parser.add_argument("--delay", type=float, default=0.5, help="每次请求之间的延迟（秒，默认 0.5）")
    parser.add_argument("--merge-only", action="store_true", help="仅合并已存在的 md 文件，不进行 OCR")
    args = parser.parse_args(argv)

    if args.run_tests:
        return _run_self_tests()

    input_path = Path(args.input)
    images = resolve_images(input_path)
    if not images:
        print(f"未找到图片文件: {input_path}", file=sys.stderr)
        return 1

    token = args.token or os.getenv("QIANFAN_LAYOUT_TOKEN") or os.getenv("OCR_API_TOKEN")
    if not token and not args.merge_only:
        print("缺少 token：请传 --token 或设置环境变量 QIANFAN_LAYOUT_TOKEN / OCR_API_TOKEN", file=sys.stderr)
        return 2

    output_base_dir = input_path if input_path.is_dir() else input_path.parent

    # 输出目录
    output_dir = Path(args.output_dir) if args.output_dir else (output_base_dir / "md")

    # 仅合并模式
    if args.merge_only:
        md_files = sorted(output_dir.glob("*.md"))
        if not md_files:
            print(f"未找到 md 文件: {output_dir}")
            return 1
        merged_file = (input_path.with_suffix(".md") if input_path.is_file() else (input_path / "merged.md"))
        merge_md_files(md_files, merged_file)
        return 0

    selected_images = images if input_path.is_file() else slice_images(
        images, start_index=args.start_index, end_index=args.end_index
    )

    print(f"准备处理 {len(selected_images)} 张图片...\n")
    md_files = run_ocr_for_images(
        selected_images,
        output_dir,
        token=token,
        start_index=args.start_index,
        delay=args.delay,
    )

    # 自动合并
    if md_files:
        merged_file = (input_path.with_suffix(".md") if input_path.is_file() else (input_path / "merged.md"))
        merge_md_files(md_files, merged_file)

    return 0


def _run_self_tests() -> int:
    import tempfile
    import unittest

    class _Tests(unittest.TestCase):
        def test_list_images_filters_and_sorts(self) -> None:
            with tempfile.TemporaryDirectory() as td:
                d = Path(td)
                (d / "b.JPG").write_bytes(b"x")
                (d / "a.jpg").write_bytes(b"x")
                (d / "c.png").write_bytes(b"x")
                (d / "ignore.txt").write_text("x", encoding="utf-8")
                got = list_images(d)
                self.assertEqual([p.name for p in got], ["a.jpg", "b.JPG", "c.png"])

        def test_slice_images_works(self) -> None:
            images = [Path(f"{i}.jpg") for i in range(1, 6)]
            self.assertEqual(slice_images(images, start_index=2, end_index=None), images[1:])
            self.assertEqual(slice_images(images, start_index=1, end_index=1), images[0:1])

        def test_file_type_from_path(self) -> None:
            self.assertEqual(file_type_from_path(Path("a.jpg")), 1)
            self.assertEqual(file_type_from_path(Path("a.jpeg")), 1)
            self.assertEqual(file_type_from_path(Path("a.png")), 1)
            self.assertEqual(file_type_from_path(Path("a.PDF")), 0)
            with self.assertRaises(ValueError):
                file_type_from_path(Path("a.txt"))

        def test_build_payload_sets_file_type(self) -> None:
            payload = build_payload("abc", file_type=0)
            self.assertEqual(payload["fileType"], 0)
            self.assertEqual(payload["file"], "abc")

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(_Tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
