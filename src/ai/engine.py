import json
from typing import Optional
from src.contracts.types import FileAnalysis
from src.graph.relations import CodeGraph
from src.graph.traversal import impact_analysis, reverse_lookup
from .prompts import MODE_PROMPTS


class AIEngine:
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None, model: str = "gpt-4o"):
        self.provider = provider
        self.api_key = api_key
        self.model = model

    def analyze(self, analysis: FileAnalysis, mode: str = "explain",
                graph: Optional[CodeGraph] = None) -> str:
        system = MODE_PROMPTS.get(mode, MODE_PROMPTS["explain"])
        payload = self._build_payload(analysis, graph)
        data = json.dumps(payload, indent=2)

        if not self.api_key:
            return self._dry_run(system, data, mode)

        return self._call_llm(system, data)

    def _build_payload(self, analysis: FileAnalysis, graph: Optional[CodeGraph] = None) -> dict:
        payload = {
            "file": analysis.file,
            "language": analysis.language,
            "symbols": [s.to_dict() for s in analysis.symbols],
            "dependencies": [d.to_dict() for d in analysis.dependencies],
            "imports": [i.to_dict() for i in analysis.imports],
        }

        if graph:
            payload["graph"] = {
                "summary": {
                    "total_nodes": len(graph.nodes),
                    "total_edges": len(graph.edges),
                    "node_kinds": list(set(n.kind for n in graph.nodes)),
                    "relation_types": list(set(e.relation for e in graph.edges)),
                },
                "nodes": [{"id": n.id, "kind": n.kind, "label": n.label} for n in graph.nodes],
                "edges": [{"source": e.source, "target": e.target, "relation": e.relation} for e in graph.edges],
            }

            if analysis.symbols:
                top = analysis.symbols[0].name
                payload["graph"]["impact"] = impact_analysis(graph, top)
                payload["graph"]["callers_of_top"] = reverse_lookup(graph, top)

        return payload

    def _dry_run(self, system: str, data: str, mode: str) -> str:
        payload = json.loads(data)
        sym_count = len(payload.get("symbols", []))
        dep_count = len(payload.get("dependencies", []))
        graph_info = payload.get("graph", {})
        g_summary = graph_info.get("summary", {})

        lines = [f"[{mode.upper()} MODE – dry run]"]
        lines.append(f"System: {system[:60]}...")
        lines.append(f"Analysis: {sym_count} symbols, {dep_count} dependencies")
        if g_summary:
            lines.append(f"Graph: {g_summary.get('total_nodes', 0)} nodes, "
                         f"{g_summary.get('total_edges', 0)} edges")
            if "impact" in graph_info:
                imp = graph_info["impact"]
                lines.append(f"Impact: {imp.get('impact_count', 0)} dependents, "
                             f"{imp.get('dependency_count', 0)} dependencies")
        lines.append("Set AI_API_KEY env var or pass --api-key to enable live LLM calls.")
        return "\n".join(lines)

    def _call_llm(self, system: str, data: str) -> str:
        if self.provider == "openai":
            return self._call_openai(system, data)
        return self._dry_run(system, data, "unknown")

    def _call_openai(self, system: str, data: str) -> str:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            resp = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": f"Structured code graph analysis:\n{data}"},
                ],
                temperature=0.3,
            )
            return resp.choices[0].message.content or ""
        except ImportError:
            return "openai package not installed. Run: pip install openai"
        except Exception as e:
            return f"LLM call failed: {e}"
