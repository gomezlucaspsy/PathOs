from __future__ import annotations
import os
from pathlib import Path
from typing import Any, Generator

from tree_sitter import Language, Parser, Node
import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript

from pathos.core.graph import CodeNode, CodeEdge, EdgeKind, NodeKind, TopologyGraph


LANGUAGES: dict[str, tuple[Any, list[str]]] = {
    "python": (tspython.language(), [".py"]),
    "javascript": (tsjavascript.language(), [".js", ".mjs", ".cjs"]),
}


def _make_parser(lang_obj: Any) -> Parser:
    language = Language(lang_obj)
    parser = Parser(language)
    return parser


class CodeParser:
    """
    Parses source files using tree-sitter and builds a TopologyGraph.

    Uses a two-pass approach:
      Pass 1 — collect all definitions (functions, classes, modules)
      Pass 2 — resolve calls/imports to known definition node IDs

    Supported languages: Python, JavaScript.
    """

    def __init__(self) -> None:
        self._parsers: dict[str, Parser] = {
            lang: _make_parser(obj) for lang, (obj, _) in LANGUAGES.items()
        }
        self._extensions: dict[str, str] = {
            ext: lang
            for lang, (_, exts) in LANGUAGES.items()
            for ext in exts
        }
        # name -> node_id map, populated during pass 1
        self._name_index: dict[str, str] = {}

    def detect_language(self, path: Path) -> str | None:
        return self._extensions.get(path.suffix.lower())

    def parse_file(self, path: Path, graph: TopologyGraph) -> None:
        lang = self.detect_language(path)
        if lang is None:
            return

        source = path.read_bytes()
        parser = self._parsers[lang]
        tree = parser.parse(source)

        if lang == "python":
            self._extract_python(tree.root_node, source, path, graph)
        elif lang == "javascript":
            self._extract_javascript(tree.root_node, source, path, graph)

        self._resolve_call_refs(graph)

    def parse_directory(self, root: Path, graph: TopologyGraph) -> None:
        files = list(self._walk(root))
        # Pass 1: definitions
        for path in files:
            self.parse_file(path, graph)
        # Pass 2: resolve unresolved call_ref nodes to known definitions
        self._resolve_call_refs(graph)

    def _resolve_call_refs(self, graph: TopologyGraph) -> None:
        """
        Replace call_ref:X edges with direct edges to the actual node
        if X exists in the name index. Removes orphan call_ref nodes.
        """
        import networkx as nx

        g = graph._graph
        call_refs = [n for n in list(g.nodes) if n.startswith("call_ref:")]
        for ref_id in call_refs:
            name = ref_id[len("call_ref:"):]
            # strip attribute access: foo.bar -> bar, self.foo -> foo
            parts = name.split(".")
            for part in reversed(parts):
                if part in self._name_index:
                    target_id = self._name_index[part]
                    for src in list(g.predecessors(ref_id)):
                        edge_data = g.edges[src, ref_id]
                        g.add_edge(src, target_id, **edge_data)
                    break
            g.remove_node(ref_id)

    def _walk(self, root: Path) -> Generator[Path, None, None]:
        for dirpath, _, filenames in os.walk(root):
            for filename in filenames:
                p = Path(dirpath) / filename
                if self.detect_language(p) is not None:
                    yield p

    # ------------------------------------------------------------------ Python

    def _extract_python(
        self, root: Node, source: bytes, path: Path, graph: TopologyGraph
    ) -> None:
        module_id = f"module:{path}"
        graph.add_node(
            CodeNode(
                id=module_id,
                kind=NodeKind.MODULE,
                name=path.stem,
                language="python",
                source_file=str(path),
                line_start=0,
                line_end=0,
            )
        )
        self._name_index[path.stem] = module_id
        self._walk_python(root, source, path, graph, module_id)

    def _walk_python(
        self,
        node: Node,
        source: bytes,
        path: Path,
        graph: TopologyGraph,
        parent_id: str,
    ) -> None:
        if node.type == "import_statement":
            name = source[node.start_byte:node.end_byte].decode("utf-8", errors="replace").strip()
            import_id = f"import:{path}:{node.start_point[0]}"
            graph.add_node(
                CodeNode(
                    id=import_id,
                    kind=NodeKind.IMPORT,
                    name=name,
                    language="python",
                    source_file=str(path),
                    line_start=node.start_point[0],
                    line_end=node.end_point[0],
                )
            )
            graph.add_edge(CodeEdge(source=parent_id, target=import_id, kind=EdgeKind.IMPORTS))

        elif node.type == "import_from_statement":
            name = source[node.start_byte:node.end_byte].decode("utf-8", errors="replace").strip()
            import_id = f"import:{path}:{node.start_point[0]}"
            graph.add_node(
                CodeNode(
                    id=import_id,
                    kind=NodeKind.IMPORT,
                    name=name,
                    language="python",
                    source_file=str(path),
                    line_start=node.start_point[0],
                    line_end=node.end_point[0],
                )
            )
            graph.add_edge(CodeEdge(source=parent_id, target=import_id, kind=EdgeKind.IMPORTS))

        elif node.type == "function_definition":
            name_node = node.child_by_field_name("name")
            fname = name_node.text.decode() if name_node else "?"
            func_id = f"func:{path}:{fname}:{node.start_point[0]}"
            graph.add_node(
                CodeNode(
                    id=func_id,
                    kind=NodeKind.FUNCTION,
                    name=fname,
                    language="python",
                    source_file=str(path),
                    line_start=node.start_point[0],
                    line_end=node.end_point[0],
                )
            )
            graph.add_edge(CodeEdge(source=parent_id, target=func_id, kind=EdgeKind.DEFINES))
            self._name_index[fname] = func_id
            for child in node.children:
                self._walk_python(child, source, path, graph, func_id)
            return

        elif node.type == "class_definition":
            name_node = node.child_by_field_name("name")
            cname = name_node.text.decode() if name_node else "?"
            class_id = f"class:{path}:{cname}:{node.start_point[0]}"
            graph.add_node(
                CodeNode(
                    id=class_id,
                    kind=NodeKind.CLASS,
                    name=cname,
                    language="python",
                    source_file=str(path),
                    line_start=node.start_point[0],
                    line_end=node.end_point[0],
                )
            )
            graph.add_edge(CodeEdge(source=parent_id, target=class_id, kind=EdgeKind.DEFINES))
            self._name_index[cname] = class_id

            superclasses = node.child_by_field_name("superclasses")
            if superclasses:
                for sc in superclasses.children:
                    if sc.type == "identifier":
                        sc_id = f"class_ref:{sc.text.decode()}"
                        graph.add_edge(
                            CodeEdge(source=class_id, target=sc_id, kind=EdgeKind.INHERITS)
                        )

            for child in node.children:
                self._walk_python(child, source, path, graph, class_id)
            return

        elif node.type == "call":
            func_node = node.child_by_field_name("function")
            if func_node:
                call_name = source[func_node.start_byte:func_node.end_byte].decode("utf-8", errors="replace")
                call_id = f"call_ref:{call_name}"
                graph.add_edge(CodeEdge(source=parent_id, target=call_id, kind=EdgeKind.CALLS))

        for child in node.children:
            self._walk_python(child, source, path, graph, parent_id)

    # --------------------------------------------------------------- JavaScript

    def _extract_javascript(
        self, root: Node, source: bytes, path: Path, graph: TopologyGraph
    ) -> None:
        module_id = f"module:{path}"
        graph.add_node(
            CodeNode(
                id=module_id,
                kind=NodeKind.MODULE,
                name=path.stem,
                language="javascript",
                source_file=str(path),
                line_start=0,
                line_end=0,
            )
        )
        self._name_index[path.stem] = module_id
        self._walk_javascript(root, source, path, graph, module_id)

    def _walk_javascript(
        self,
        node: Node,
        source: bytes,
        path: Path,
        graph: TopologyGraph,
        parent_id: str,
    ) -> None:
        if node.type in ("import_statement", "import_declaration"):
            name = source[node.start_byte:node.end_byte].decode("utf-8", errors="replace").strip()
            import_id = f"import:{path}:{node.start_point[0]}"
            graph.add_node(
                CodeNode(
                    id=import_id,
                    kind=NodeKind.IMPORT,
                    name=name,
                    language="javascript",
                    source_file=str(path),
                    line_start=node.start_point[0],
                    line_end=node.end_point[0],
                )
            )
            graph.add_edge(CodeEdge(source=parent_id, target=import_id, kind=EdgeKind.IMPORTS))

        elif node.type in ("function_declaration", "function_definition", "arrow_function"):
            name_node = node.child_by_field_name("name")
            fname = name_node.text.decode() if name_node else f"anonymous:{node.start_point[0]}"
            func_id = f"func:{path}:{fname}:{node.start_point[0]}"
            graph.add_node(
                CodeNode(
                    id=func_id,
                    kind=NodeKind.FUNCTION,
                    name=fname,
                    language="javascript",
                    source_file=str(path),
                    line_start=node.start_point[0],
                    line_end=node.end_point[0],
                )
            )
            graph.add_edge(CodeEdge(source=parent_id, target=func_id, kind=EdgeKind.DEFINES))
            self._name_index[fname] = func_id
            for child in node.children:
                self._walk_javascript(child, source, path, graph, func_id)
            return

        elif node.type == "class_declaration":
            name_node = node.child_by_field_name("name")
            cname = name_node.text.decode() if name_node else "?"
            class_id = f"class:{path}:{cname}:{node.start_point[0]}"
            graph.add_node(
                CodeNode(
                    id=class_id,
                    kind=NodeKind.CLASS,
                    name=cname,
                    language="javascript",
                    source_file=str(path),
                    line_start=node.start_point[0],
                    line_end=node.end_point[0],
                )
            )
            graph.add_edge(CodeEdge(source=parent_id, target=class_id, kind=EdgeKind.DEFINES))
            self._name_index[cname] = class_id
            for child in node.children:
                self._walk_javascript(child, source, path, graph, class_id)
            return

        elif node.type == "call_expression":
            func_node = node.child_by_field_name("function")
            if func_node:
                call_name = source[func_node.start_byte:func_node.end_byte].decode("utf-8", errors="replace")
                call_id = f"call_ref:{call_name}"
                graph.add_edge(CodeEdge(source=parent_id, target=call_id, kind=EdgeKind.CALLS))

        for child in node.children:
            self._walk_javascript(child, source, path, graph, parent_id)
