import argparse
import re
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path


_NUMBERED_IMAGE_RE = re.compile(r"^(?P<prefix>.*)_(?P<num>\d+)\.(?P<ext>jpg|jpeg|png)$", re.IGNORECASE)


@dataclass(frozen=True)
class RenamePlanItem:
    source: Path
    target: Path


def parse_numbered_image(filename: str) -> tuple[str, int, str] | None:
    m = _NUMBERED_IMAGE_RE.match(filename)
    if not m:
        return None
    prefix = m.group("prefix")
    num = int(m.group("num"))
    ext = m.group("ext").lower()
    if ext == "jpeg":
        ext = "jpg"
    return prefix, num, ext


def compute_pad_width(total_items: int) -> int:
    return max(4, len(str(max(1, total_items))))


def build_target_name(prefix: str, index_1_based: int, pad_width: int, ext: str) -> str:
    return f"{prefix}_{index_1_based:0{pad_width}d}.{ext}"


def list_candidate_images(directory: Path) -> list[tuple[Path, str, int, str]]:
    items: list[tuple[Path, str, int, str]] = []
    for p in directory.iterdir():
        if not p.is_file():
            continue
        parsed = parse_numbered_image(p.name)
        if not parsed:
            continue
        prefix, num, ext = parsed
        items.append((p, prefix, num, ext))
    items.sort(key=lambda x: (x[1], x[2], x[0].name.lower()))
    return items


def make_rename_plan(directory: Path, *, start_index: int = 1) -> list[RenamePlanItem]:
    candidates = list_candidate_images(directory)
    if not candidates:
        return []

    prefixes = {prefix for _, prefix, _, _ in candidates}
    if len(prefixes) != 1:
        raise ValueError(f"目录内检测到多个前缀：{sorted(prefixes)}")

    prefix = next(iter(prefixes))
    ext = candidates[0][3]
    if any(item[3] != ext for item in candidates):
        raise ValueError("目录内检测到多种图片后缀（jpg/png 混用）")

    pad_width = compute_pad_width(len(candidates) + start_index - 1)

    plan: list[RenamePlanItem] = []
    for i, (path, _, _, _) in enumerate(candidates, start=start_index):
        target_name = build_target_name(prefix, i, pad_width, ext)
        plan.append(RenamePlanItem(source=path, target=directory / target_name))

    targets = [p.target.name.lower() for p in plan]
    if len(set(targets)) != len(targets):
        raise ValueError("目标文件名存在重复，无法安全重命名")

    return plan


def apply_rename_plan(plan: list[RenamePlanItem], *, dry_run: bool) -> int:
    if not plan:
        print("未找到符合 *_NNNN.jpg/png 的图片，或无需处理。")
        return 0

    directory = plan[0].source.parent

    planned_sources = {p.source.resolve() for p in plan}
    planned_targets = {p.target.resolve() for p in plan}

    for p in plan:
        if not p.source.exists():
            raise FileNotFoundError(str(p.source))

    for target in planned_targets:
        if target.exists() and target.resolve() not in planned_sources:
            raise FileExistsError(str(target))

    for p in plan:
        print(f"{p.source.name} -> {p.target.name}")

    if dry_run:
        return 0

    token = uuid.uuid4().hex[:10]
    temp_paths: list[tuple[Path, Path]] = []
    for p in plan:
        tmp = directory / f"{p.source.name}.renametmp_{token}"
        p.source.rename(tmp)
        temp_paths.append((tmp, p.target))

    for tmp, target in temp_paths:
        tmp.rename(target)

    return 0


def _run_self_tests() -> int:
    import tempfile
    import unittest

    class _Tests(unittest.TestCase):
        def test_parse_numbered_image(self) -> None:
            self.assertEqual(parse_numbered_image("a_0020.jpg"), ("a", 20, "jpg"))
            self.assertEqual(parse_numbered_image("a_1.jpeg"), ("a", 1, "jpg"))
            self.assertEqual(parse_numbered_image("a_0003.PNG"), ("a", 3, "png"))
            self.assertIsNone(parse_numbered_image("a.jpg"))
            self.assertIsNone(parse_numbered_image("a_foo.jpg"))

        def test_make_rename_plan_single_prefix_sequential(self) -> None:
            with tempfile.TemporaryDirectory() as td:
                d = Path(td)
                (d / "book_0020.jpg").write_bytes(b"x")
                (d / "book_0021.jpg").write_bytes(b"x")
                (d / "book_0022.jpg").write_bytes(b"x")
                plan = make_rename_plan(d, start_index=1)
                self.assertEqual([p.target.name for p in plan], ["book_0001.jpg", "book_0002.jpg", "book_0003.jpg"])

        def test_make_rename_plan_rejects_multiple_prefixes(self) -> None:
            with tempfile.TemporaryDirectory() as td:
                d = Path(td)
                (d / "a_0001.jpg").write_bytes(b"x")
                (d / "b_0002.jpg").write_bytes(b"x")
                with self.assertRaises(ValueError):
                    make_rename_plan(d, start_index=1)

        def test_apply_rename_plan_works_without_collision(self) -> None:
            with tempfile.TemporaryDirectory() as td:
                d = Path(td)
                (d / "book_0020.jpg").write_bytes(b"x")
                (d / "book_0021.jpg").write_bytes(b"x")
                plan = make_rename_plan(d, start_index=1)
                apply_rename_plan(plan, dry_run=False)
                self.assertTrue((d / "book_0001.jpg").exists())
                self.assertTrue((d / "book_0002.jpg").exists())

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(_Tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="将目录内 *_NNNN.jpg/png 重命名为从 _0001 开始的连续编号")
    parser.add_argument(
        "directory",
        nargs="?",
        default=r"d:\Users\tanle\Desktop\sp\output_jpg",
        help="图片目录（默认：d:\\Users\\tanle\\Desktop\\sp\\output_jpg）",
    )
    parser.add_argument("--start", type=int, default=1, help="起始编号（默认 1）")
    parser.add_argument("--dry-run", action="store_true", help="只打印改名映射，不实际改名")
    parser.add_argument("--run-tests", action="store_true", help="运行自测并退出")
    args = parser.parse_args(argv)

    if args.run_tests:
        return _run_self_tests()

    directory = Path(args.directory)
    if not directory.exists() or not directory.is_dir():
        print(f"目录不存在：{directory}", file=sys.stderr)
        return 2

    if args.start <= 0:
        print("start 必须大于 0", file=sys.stderr)
        return 2

    try:
        plan = make_rename_plan(directory, start_index=args.start)
        return apply_rename_plan(plan, dry_run=args.dry_run)
    except Exception as e:
        print(f"失败：{e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

