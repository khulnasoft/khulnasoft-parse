from abc import ABC, abstractmethod
from .context import AnalysisContext


class PipelineStep(ABC):
    @abstractmethod
    def execute(self, ctx: AnalysisContext) -> AnalysisContext:
        ...


class Pipeline:
    def __init__(self):
        self._steps: list[PipelineStep] = []

    def add_step(self, step: PipelineStep) -> "Pipeline":
        self._steps.append(step)
        return self

    def run(self, ctx: AnalysisContext) -> AnalysisContext:
        for step in self._steps:
            if ctx.has_error():
                break
            ctx = step.execute(ctx)
        return ctx


class ParseStep(PipelineStep):
    def execute(self, ctx: AnalysisContext) -> AnalysisContext:
        from pathlib import Path
        from examples.parse_example import get_language, _make_parser
        from src.core.parser import ParseResult
        from src.core.tree_sitter_utils import ts_node_to_astnode

        try:
            src = Path(ctx.filepath).read_bytes()
            ctx.source_text = src.decode("utf-8", "replace")
            lang = ctx.language or Path(ctx.filepath).suffix.lstrip(".") or "python"
            lang = {"js": "javascript", "ts": "typescript", "py": "python", "rb": "ruby"}.get(lang, lang)
            ctx.language = lang

            library = ctx.__dict__.get("_library")
            language = get_language(lang, library)
            parser_inst = _make_parser(language)
            tree = parser_inst.parse(src)

            ctx.parse_result = ParseResult(
                source_path=ctx.filepath, language=lang,
                root=ts_node_to_astnode(tree.root_node, src), source_text=ctx.source_text)
        except Exception as e:
            ctx.error = f"Parse failed: {e}"
        return ctx


class NormalizeStep(PipelineStep):
    def execute(self, ctx: AnalysisContext) -> AnalysisContext:
        from src.core.ast_normalizer import normalize
        if ctx.parse_result:
            ctx.normalized_nodes = normalize(ctx.parse_result)
        return ctx


class AnalyzeStep(PipelineStep):
    def execute(self, ctx: AnalysisContext) -> AnalysisContext:
        from src.semantic.analyzer import analyze
        if ctx.parse_result and ctx.normalized_nodes:
            ctx.analysis = analyze(ctx.parse_result, ctx.normalized_nodes)
        return ctx


class GraphStep(PipelineStep):
    def execute(self, ctx: AnalysisContext) -> AnalysisContext:
        from src.graph.builder import build
        if ctx.analysis:
            ctx.graph = build(ctx.analysis)
        return ctx
