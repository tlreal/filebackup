import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PPStructureV3RunConfig:
    input_path: Path
    save_path: Path
    device: str = "cpu"
    use_table_recognition: bool = True
    use_formula_recognition: bool = True
    use_chart_recognition: bool = False
    use_seal_recognition: bool = False
    chart_recognition_model_name: str = "PP-Chart2Table"
    chart_recognition_batch_size: int = 1


def build_paddleocr_pp_structurev3_args(cfg: PPStructureV3RunConfig) -> list[str]:
    return [
        sys.executable,
        "-m",
        "paddleocr",
        "pp_structurev3",
        "-i",
        str(cfg.input_path),
        "--device",
        cfg.device,
        "--save_path",
        str(cfg.save_path),
        "--use_table_recognition",
        str(cfg.use_table_recognition),
        "--use_formula_recognition",
        str(cfg.use_formula_recognition),
        "--use_chart_recognition",
        str(cfg.use_chart_recognition),
        "--use_seal_recognition",
        str(cfg.use_seal_recognition),
        "--chart_recognition_model_name",
        cfg.chart_recognition_model_name,
        "--chart_recognition_batch_size",
        str(cfg.chart_recognition_batch_size),
    ]


def run_pp_structurev3(cfg: PPStructureV3RunConfig, *, dry_run: bool) -> int:
    args = build_paddleocr_pp_structurev3_args(cfg)
    print(" ".join(args))
    if dry_run:
        return 0
    completed = subprocess.run(args, check=False)
    return int(completed.returncode)


def collect_markdown_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    files = [p for p in root.rglob("*.md") if p.is_file()]
    files.sort(key=lambda p: p.as_posix().lower())
    return files


def merge_markdown_files(md_files: list[Path], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    parts: list[str] = []
    for p in md_files:
        parts.append(f"## {p.stem}\n")
        content = p.read_text(encoding="utf-8", errors="replace")
        content = content.replace("\r\n", "\n").replace("\r", "\n")
        parts.append(content)
        parts.append("\n\n---\n\n")
    output_file.write_text("".join(parts), encoding="utf-8")


def _run_self_tests() -> int:
    import tempfile
    import unittest

    class _Tests(unittest.TestCase):
        def test_build_args_contains_expected_flags(self) -> None:
            cfg = PPStructureV3RunConfig(
                input_path=Path(r"d:\a b\in"),
                save_path=Path(r"d:\out"),
                device="cpu",
                use_table_recognition=False,
                use_formula_recognition=True,
                use_chart_recognition=False,
                use_seal_recognition=False,
                chart_recognition_model_name="PP-Chart2Table",
                chart_recognition_batch_size=1,
            )
            args = build_paddleocr_pp_structurev3_args(cfg)
            self.assertEqual(args[0:4], [sys.executable, "-m", "paddleocr", "pp_structurev3"])
            self.assertIn(str(cfg.input_path), args)
            self.assertIn(str(cfg.save_path), args)
            self.assertIn("--use_table_recognition", args)
            self.assertIn("False", args)
            self.assertIn("--chart_recognition_model_name", args)
            self.assertIn("PP-Chart2Table", args)

        def test_collect_markdown_files_sorted(self) -> None:
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                (root / "b.md").write_text("b", encoding="utf-8")
                (root / "a.md").write_text("a", encoding="utf-8")
                (root / "x").mkdir()
                (root / "x" / "c.md").write_text("c", encoding="utf-8")
                files = collect_markdown_files(root)
                self.assertEqual([p.name for p in files], ["a.md", "b.md", "c.md"])

        def test_merge_markdown_files(self) -> None:
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                p1 = root / "a.md"
                p2 = root / "b.md"
                p1.write_text("A\r\nB\rC\n", encoding="utf-8", newline="")
                p2.write_text("B", encoding="utf-8")
                out = root / "merged.md"
                merge_markdown_files([p2, p1], out)
                merged = out.read_text(encoding="utf-8")
                self.assertIn("## b\n", merged)
                self.assertIn("B", merged)
                self.assertIn("## a\n", merged)
                self.assertIn("A\nB\nC\n", merged)
                self.assertNotIn("\r", merged)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(_Tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="用 PP-StructureV3(CPU) 跑目录/图片并可选合并 Markdown")
    parser.add_argument("--run-tests", action="store_true", help="运行自测并退出")
    parser.add_argument("--dry-run", action="store_true", help="只打印将执行的命令")
    parser.add_argument("--input", required=False, help="输入目录或图片路径")
    parser.add_argument("--save-path", required=False, help="输出目录")
    parser.add_argument("--merge-md", action="store_true", help="将输出目录下的 md 合并成一个文件")
    parser.add_argument("--merged-md-path", help="合并后的 md 文件路径")
    parser.add_argument("--device", default="cpu", help="设备（默认 cpu）")
    parser.add_argument("--use-table", type=str, default="True")
    parser.add_argument("--use-formula", type=str, default="True")
    parser.add_argument("--use-chart", type=str, default="False")
    parser.add_argument("--use-seal", type=str, default="False")
    parser.add_argument("--chart-model", default="PP-Chart2Table")
    parser.add_argument("--chart-batch-size", type=int, default=1)
    args = parser.parse_args(argv)

    if args.run_tests:
        return _run_self_tests()

    if not args.input or not args.save_path:
        print("--input 和 --save-path 必填（除非 --run-tests）", file=sys.stderr)
        return 2

    cfg = PPStructureV3RunConfig(
        input_path=Path(args.input),
        save_path=Path(args.save_path),
        device=args.device,
        use_table_recognition=args.use_table.lower() == "true",
        use_formula_recognition=args.use_formula.lower() == "true",
        use_chart_recognition=args.use_chart.lower() == "true",
        use_seal_recognition=args.use_seal.lower() == "true",
        chart_recognition_model_name=args.chart_model,
        chart_recognition_batch_size=args.chart_batch_size,
    )

    code = run_pp_structurev3(cfg, dry_run=args.dry_run)
    if code != 0:
        return code

    if args.merge_md:
        md_files = collect_markdown_files(cfg.save_path)
        if not md_files:
            print(f"未找到 md 文件：{cfg.save_path}", file=sys.stderr)
            return 3
        merged_path = Path(args.merged_md_path) if args.merged_md_path else (cfg.save_path / "merged.md")
        merge_markdown_files(md_files, merged_path)
        print(str(merged_path))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
