"""
批量 OCR：将目录下的图片识别并输出为 Markdown
"""
import argparse
import sys
from pathlib import Path


_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


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


def resolve_images(input_path: Path) -> list[Path]:
    if input_path.exists() and input_path.is_file():
        if input_path.suffix.lower() in _IMAGE_SUFFIXES:
            return [input_path]
        return []
    return list_images(input_path)


def parse_predict_result(result: object) -> str:
    if not isinstance(result, list) or not result:
        return ""
    cleaned: list[str] = []
    for item in result:
        if isinstance(item, dict):
            texts = item.get("rec_texts")
            if isinstance(texts, list):
                for t in texts:
                    s = str(t).strip()
                    if s:
                        cleaned.append(s)
            continue

        if isinstance(item, list) and len(item) == 2:
            rec = item[1]
            if isinstance(rec, (list, tuple)) and rec:
                s = str(rec[0]).strip()
                if s:
                    cleaned.append(s)
    return "\n".join(cleaned)


def build_markdown(pages: list[tuple[str, str]], *, include_header: bool = True) -> str:
    parts: list[str] = []
    if include_header:
        parts.append("# OCR 结果\n\n")
    for image_name, text in pages:
        parts.append(f"## {image_name}\n\n")
        parts.append("```text\n")
        parts.append(text)
        if text and not text.endswith("\n"):
            parts.append("\n")
        parts.append("```\n\n")
    return "".join(parts)


def run_ocr_for_images(*, ocr: object, images: list[Path]) -> list[tuple[str, str]]:
    pages: list[tuple[str, str]] = []
    predict = getattr(ocr, "predict", None)
    if not callable(predict):
        raise TypeError("ocr 必须包含可调用的 predict 方法")

    total = len(images)
    for idx, p in enumerate(images, start=1):
        print(f"[{idx}/{total}] {p.name}")
        result = predict(str(p))
        pages.append((p.name, parse_predict_result(result)))
    return pages


def slice_images(images: list[Path], *, start_index: int, end_index: int | None) -> list[Path]:
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
    parser = argparse.ArgumentParser(description="用飞桨 PaddleOCR 批量识别图片并输出 Markdown")
    parser.add_argument("--run-tests", action="store_true", help="运行自测并退出")
    parser.add_argument("--input", default=r"d:\Users\tanle\Desktop\sp\第1章", help="图片目录或单张图片路径")
    parser.add_argument("--output", default=None, help="输出 Markdown 路径（默认：目录为 <input>/ocr.md；单图不传则输出到终端）")
    parser.add_argument("--lang", default="en", help="识别语言（默认 en）")
    parser.add_argument("--start-index", type=int, default=1, help="从第几张开始（1-based，默认 1）")
    parser.add_argument("--end-index", type=int, default=None, help="到第几张结束（1-based，默认到最后）")
    parser.add_argument("--append", action="store_true", help="追加写入到输出文件（用于分批运行）")
    args = parser.parse_args(argv)

    if args.run_tests:
        return _run_self_tests()

    input_path = Path(args.input)
    images = resolve_images(input_path)
    if not images:
        print(f"未找到图片文件: {input_path}", file=sys.stderr)
        return 1

    from paddleocr import PaddleOCR

    ocr = PaddleOCR(lang=args.lang)
    selected_images = images if input_path.is_file() else slice_images(images, start_index=args.start_index, end_index=args.end_index)
    pages = run_ocr_for_images(ocr=ocr, images=selected_images)

    if input_path.is_file() and not args.output:
        print(pages[0][1])
        return 0

    output_path = Path(args.output) if args.output else (input_path / "ocr.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    include_header = not args.append or not output_path.exists()
    md = build_markdown(pages, include_header=include_header)
    mode = "a" if args.append else "w"
    with output_path.open(mode, encoding="utf-8", newline="\n") as f:
        f.write(md)
    print(str(output_path))
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

        def test_resolve_images_accepts_file(self) -> None:
            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "one.jpg"
                p.write_bytes(b"x")
                got = resolve_images(p)
                self.assertEqual(got, [p])

        def test_parse_predict_result_joins_texts(self) -> None:
            fake = [{"rec_texts": ["Hello", "World"], "rec_scores": [0.9, 0.8]}]
            self.assertEqual(parse_predict_result(fake), "Hello\nWorld")

        def test_parse_predict_result_merges_multiple_items(self) -> None:
            fake = [{"rec_texts": ["A"]}, {"rec_texts": ["B", "C"]}]
            self.assertEqual(parse_predict_result(fake), "A\nB\nC")

        def test_build_markdown_contains_headings_and_fences(self) -> None:
            md = build_markdown([("img1.jpg", "Hello")])
            self.assertIn("# OCR 结果", md)
            self.assertIn("## img1.jpg", md)
            self.assertIn("```text", md)
            self.assertIn("Hello", md)
            self.assertIn("```", md)

        def test_slice_images_works(self) -> None:
            images = [Path(f"{i}.jpg") for i in range(1, 6)]
            self.assertEqual(slice_images(images, start_index=2, end_index=None), images[1:])
            self.assertEqual(slice_images(images, start_index=1, end_index=1), images[0:1])
            with self.assertRaises(ValueError):
                slice_images(images, start_index=6, end_index=None)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(_Tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
