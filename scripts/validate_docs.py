#!/usr/bin/env python
# ==============================================================================
# Script: validate_docs.py
# Proyecto: SAC Automation RPA
# Purpose: Validar calidad de documentación y calcular métricas
# ==============================================================================

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

try:
    from docstring_parser import DocstringStyle
    from docstring_parser.numpydoc import NumPyDocstring

    DOCSTRING_PARSER_AVAILABLE = True
except ImportError:
    DOCSTRING_PARSER_AVAILABLE = False
    print(
        "ADVERTENCIA: docstring_parser no instalado. Install with: pip install docstring-parser"
    )


class DocumentationValidator:
    """Validador de calidad de documentación."""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.results: Dict = {
            "timestamp": datetime.now().isoformat(),
            "files": {},
            "summary": {},
            "critical_methods": [],
            "missing_docs": [],
        }

    def analyze_file(self, filepath: Path) -> Dict:
        """Analiza un archivo Python individual."""
        result = {
            "path": str(filepath.relative_to(self.project_root)),
            "total_functions": 0,
            "documented_functions": 0,
            "complete_docstrings": 0,
            "args_documented": 0,
            "returns_documented": 0,
            "raises_documented": 0,
            "examples_count": 0,
            "coverage_percent": 0,
            "completeness_score": 0,
            "issues": [],
        }

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            exec_globals = {}
            exec(compile(content, filepath, "exec"), exec_globals)

            for name, obj in exec_globals.items():
                if callable(obj) and not name.startswith("_"):
                    result["total_functions"] += 1
                    if obj.__doc__:
                        result["documented_functions"] += 1
                        doc_info = self._analyze_docstring(obj.__doc__)
                        if doc_info["is_complete"]:
                            result["complete_docstrings"] += 1
                        result["args_documented"] += doc_info["has_args"]
                        result["returns_documented"] += doc_info["has_returns"]
                        result["raises_documented"] += doc_info["has_raises"]
                        result["examples_count"] += doc_info["has_examples"]
                    else:
                        self.results["missing_docs"].append(
                            {
                                "file": str(filepath.relative_to(self.project_root)),
                                "function": name,
                                "type": "public_api",
                            }
                        )
                        result["issues"].append(f"Falta docstring en {name}")

            if result["total_functions"] > 0:
                result["coverage_percent"] = round(
                    (result["documented_functions"] / result["total_functions"]) * 100,
                    1,
                )
                total_elements = (
                    result["args_documented"]
                    + result["returns_documented"]
                    + result["raises_documented"]
                    + result["examples_count"]
                )
                max_elements = result["documented_functions"] * 4
                result["completeness_score"] = (
                    round((total_elements / max_elements) * 100, 1)
                    if max_elements > 0
                    else 0
                )

        except Exception as e:
            result["issues"].append(f"Error analyzing: {e}")

        return result

    def _analyze_docstring(self, docstring: str) -> Dict:
        """Analiza un docstring para verificar completitud."""
        info = {
            "is_complete": False,
            "has_args": False,
            "has_returns": False,
            "has_raises": False,
            "has_examples": False,
        }

        if not docstring:
            return info

        doc_lower = docstring.lower()

        info["has_args"] = any(
            keyword in doc_lower
            for keyword in ["parameters", "parameters:", "args:", "arguments:", "arg "]
        )
        info["has_returns"] = "returns" in doc_lower or "return" in doc_lower
        info["has_raises"] = "raises" in doc_lower or "exception" in doc_lower
        info["has_examples"] = "example" in doc_lower or "usage" in doc_lower

        info["is_complete"] = all(
            [info["has_args"], info["has_returns"], info["has_raises"]]
        )

        return info

    def run(self, directories: List[str] = None) -> Dict:
        """Ejecuta el análisis completo."""
        if directories is None:
            directories = ["core", "src"]

        all_results = []

        for directory in directories:
            dir_path = self.project_root / directory
            if not dir_path.exists():
                print(f"ADVERTENCIA: Directorio {directory} no encontrado")
                continue

            for py_file in dir_path.rglob("*.py"):
                if "__pycache__" in str(py_file):
                    continue
                result = self.analyze_file(py_file)
                all_results.append(result)
                self.results["files"][str(py_file.relative_to(self.project_root))] = (
                    result
                )

        self._calculate_summary(all_results)
        return self.results

    def _calculate_summary(self, results: List[Dict]):
        """Calcula métricas de resumen."""
        if not results:
            return

        total_funcs = sum(r["total_functions"] for r in results)
        documented_funcs = sum(r["documented_functions"] for r in results)
        complete_docs = sum(r["complete_docstrings"] for r in results)

        self.results["summary"] = {
            "total_files": len(results),
            "total_functions": total_funcs,
            "documented_functions": documented_funcs,
            "complete_docstrings": complete_docs,
            "coverage_percent": round((documented_funcs / total_funcs) * 100, 1)
            if total_funcs > 0
            else 0,
            "completeness_score": round((complete_docs / total_funcs) * 100, 1)
            if total_funcs > 0
            else 0,
            "missing_docs_count": len(self.results["missing_docs"]),
        }

    def save_results(self, output_path: str = "docs/validation_results.json"):
        """Guarda los resultados en JSON."""
        output_file = self.project_root / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Resultados guardados en: {output_file}")

    def print_report(self):
        """Imprime reporte formateado."""
        print("\n" + "=" * 70)
        print("REPORTE DE VALIDACIÓN DE DOCUMENTACIÓN")
        print("SAC Automation RPA")
        print("=" * 70)

        summary = self.results["summary"]

        print(f"\n📊 RESUMEN:")
        print(f"   Archivos analizados: {summary.get('total_files', 0)}")
        print(f"   Funciones totales: {summary.get('total_functions', 0)}")
        print(f"   Funciones documentadas: {summary.get('documented_functions', 0)}")
        print(f"   Docstrings completos: {summary.get('complete_docstrings', 0)}")
        print(f"")
        print(f"   📈 DOCSTRING COVERAGE: {summary.get('coverage_percent', 0)}%")
        print(f"   📈 COMPLETENESS SCORE: {summary.get('completeness_score', 0)}%")

        if self.results["missing_docs"]:
            print(
                f"\n⚠️  FUNCIONES SIN DOCUMENTACIÓN ({len(self.results['missing_docs'])}):"
            )
            for item in self.results["missing_docs"][:10]:
                print(f"   - {item['file']}::{item['function']}")
            if len(self.results["missing_docs"]) > 10:
                print(f"   ... y {len(self.results['missing_docs']) - 10} más")

        print("\n" + "=" * 70)

        if summary.get("coverage_percent", 0) >= 90:
            print("✅ COBERTURA OBJETIVO ALCANZADA (90%)")
        else:
            gap = 90 - summary.get("coverage_percent", 0)
            print(f"⚠️  BRECHA PARA ALCANZAR 90%: {gap}%")
            print(
                f"   Funciones faltantes: ~{int(summary.get('total_functions', 0) * gap / 100)}"
            )

        print("=" * 70 + "\n")


def main():
    """Punto de entrada principal."""
    project_root = Path(__file__).parent.parent

    print("Iniciando validación de documentación...")
    print(f"Proyecto: {project_root}")

    validator = DocumentationValidator(str(project_root))
    validator.run(["core", "src"])
    validator.print_report()
    validator.save_results()

    summary = validator.results["summary"]
    coverage = summary.get("coverage_percent", 0)

    if coverage >= 90:
        print("✓ Validación PASSED")
        sys.exit(0)
    else:
        print(f"✗ Validación FAILED - Cobertura {coverage}% < 90%")
        sys.exit(1)


if __name__ == "__main__":
    main()
