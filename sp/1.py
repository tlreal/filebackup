import argparse
import re
import sys
from pathlib import Path


_ILLEGAL_FILENAME_CHARS_RE = re.compile(r'[<>:"/\\\\|?*\\x00-\\x1f]+')


def sanitize_stem(stem: str) -> str:
    cleaned = _ILLEGAL_FILENAME_CHARS_RE.sub("_", stem.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip(" _")
    return cleaned or "output"


def build_output_path(
    *,
    output_dir: Path,
    base_stem: str,
    page_number_1_based: int,
    total_pages: int,
    image_ext: str,
) -> Path:
    ext = image_ext.lstrip(".").lower()
    pad_width = max(4, len(str(max(1, total_pages))))
    filename = f"{base_stem}_{page_number_1_based:0{pad_width}d}.{ext}"
    return output_dir / filename


def normalize_page_bounds(
    *,
    total_pages: int,
    first_page: int | None,
    last_page: int | None,
) -> tuple[int, int]:
    if total_pages <= 0:
        raise ValueError("total_pages 必须大于 0")

    first = 1 if first_page is None else first_page
    last = total_pages if last_page is None else last_page

    first = max(1, first)
    last = min(total_pages, last)

    if last < first:
        raise ValueError("last_page 不能小于 first_page")

    return first, last


def convert_pdf_to_images(
    *,
    pdf_path: Path,
    output_dir: Path,
    dpi: int,
    first_page: int | None,
    last_page: int | None,
    image_ext: str,
) -> int:
    if not pdf_path.exists() or not pdf_path.is_file():
        print(f"找不到 PDF 文件：{pdf_path}", file=sys.stderr)
        return 2

    if dpi <= 0:
        print("dpi 必须大于 0", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        import fitz  # type: ignore
    except Exception:
        print("缺少依赖：PyMuPDF（pip install pymupdf）", file=sys.stderr)
        return 2

    ext = image_ext.lstrip(".").lower()
    if ext == "jpeg":
        ext = "jpg"

    doc = fitz.open(str(pdf_path))
    try:
        total_pages = doc.page_count
        base_stem = sanitize_stem(pdf_path.stem)
        first, last = normalize_page_bounds(total_pages=total_pages, first_page=first_page, last_page=last_page)

        zoom = dpi / 72.0
        matrix = fitz.Matrix(zoom, zoom)

        for page_number_1_based in range(first, last + 1):
            page = doc.load_page(page_number_1_based - 1)
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            out_path = build_output_path(
                output_dir=output_dir,
                base_stem=base_stem,
                page_number_1_based=page_number_1_based,
                total_pages=total_pages,
                image_ext=ext,
            )
            pix.save(str(out_path))
    finally:
        doc.close()

    return 0


def _run_self_tests() -> int:
    import unittest

    class _Tests(unittest.TestCase):
        def test_sanitize_stem_replaces_illegal_filename_chars(self) -> None:
            self.assertEqual(sanitize_stem('a<>:"/\\|?*b'), "a_b")

        def test_build_output_path_pads_page_numbers(self) -> None:
            p1 = build_output_path(
                output_dir=Path("out"),
                base_stem="book",
                page_number_1_based=1,
                total_pages=123,
                image_ext="jpg",
            )
            self.assertEqual(str(p1).replace("\\", "/"), "out/book_0001.jpg")

        def test_normalize_page_bounds_defaults_to_full_range(self) -> None:
            first, last = normalize_page_bounds(total_pages=10, first_page=None, last_page=None)
            self.assertEqual((first, last), (1, 10))

        def test_normalize_page_bounds_clamps_to_valid_range(self) -> None:
            first, last = normalize_page_bounds(total_pages=10, first_page=-5, last_page=999)
            self.assertEqual((first, last), (1, 10))

        def test_normalize_page_bounds_rejects_inverted_range(self) -> None:
            with self.assertRaises(ValueError):
                normalize_page_bounds(total_pages=10, first_page=5, last_page=3)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(_Tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="将 PDF 按页导出为 JPG 图片")
    parser.add_argument("pdf", nargs="?", help="PDF 文件路径")
    parser.add_argument("-o", "--output-dir", default="output_jpg", help="输出目录")
    parser.add_argument("--dpi", type=int, default=300, help="导出 DPI（越大越清晰，文件越大）")
    parser.add_argument("--first-page", type=int, default=None, help="从第几页开始（1-based）")
    parser.add_argument("--last-page", type=int, default=None, help="到第几页结束（1-based）")
    parser.add_argument("--image-ext", default="jpg", choices=["jpg", "jpeg", "png"], help="输出图片格式")
    parser.add_argument("--run-tests", action="store_true", help="运行自测并退出")
    args = parser.parse_args(argv)

    if args.run_tests:
        return _run_self_tests()

    if not args.pdf:
        parser.error("缺少 PDF 文件路径")

    pdf_path = Path(args.pdf)
    output_dir = Path(args.output_dir)
    return convert_pdf_to_images(
        pdf_path=pdf_path,
        output_dir=output_dir,
        dpi=args.dpi,
        first_page=args.first_page,
        last_page=args.last_page,
        image_ext=args.image_ext,
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
