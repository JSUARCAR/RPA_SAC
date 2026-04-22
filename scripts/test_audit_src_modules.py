"""
Test de Auditoria TDD para src/web_automator.py, src/data_handler.py, src/adaptive_wait.py

Este modulo implementa tests de validacion siguiendo la metodologia TDD:
- RED: Tests que fallan antes de la implementacion
- GREEN: Implementacion minima para pasar los tests
- REFACTOR: Limpieza del codigo

Usage:
    python scripts/test_audit_src_modules.py
"""

import ast
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple

# Configuracion del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
SRC_PATH = PROJECT_ROOT / "src"


class TestResult:
    """Resultado de un test individual."""

    def __init__(
        self, name: str, passed: bool, message: str = "", details: Dict = None
    ):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details or {}

    def __str__(self):
        status = "[PASS]" if self.passed else "[FAIL]"
        result = f"{status} {self.name}"
        if self.message:
            result += f" - {self.message}"
        return result


class DocumentationAuditor:
    """Auditor de documentacion para codigo Python."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.content = self._read_file()
        self.tree = self._parse_ast()
        self.errors: List[str] = []

    def _read_file(self) -> str:
        """Lee el contenido del archivo."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _parse_ast(self) -> ast.AST:
        """Parsea el archivo como AST."""
        return ast.parse(self.content)

    def get_module_docstring(self) -> str:
        """Obtiene el docstring del modulo."""
        return ast.get_docstring(self.tree)

    def get_all_functions(self) -> List[Tuple[str, bool]]:
        """Retorna lista de (nombre, tiene_docstring) para todas las funciones."""
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                has_doc = ast.get_docstring(node) is not None
                functions.append((node.name, has_doc))
        return functions

    def get_all_classes(self) -> List[Tuple[str, bool, int]]:
        """Retorna lista de (nombre_clase, tiene_docstring, num_metodos)."""
        classes = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                has_doc = ast.get_docstring(node) is not None
                num_methods = len(
                    [n for n in node.body if isinstance(n, ast.FunctionDef)]
                )
                classes.append((node.name, has_doc, num_methods))
        return classes

    def check_numpy_style(self) -> List[str]:
        """Verifica estilo NumPy en docstrings."""
        issues = []

        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                doc = ast.get_docstring(node)
                if doc:
                    lines = doc.split("\n")

                    # D205: Blank line between summary and description
                    if len(lines) > 1 and lines[1].strip() != "":
                        # Check if line 1 is blank (correct)
                        pass
                    elif (
                        len(lines) > 1
                        and lines[0].strip()
                        and not lines[0].endswith(".")
                    ):
                        issues.append(
                            f"D400: {node.name} - First line should end with period"
                        )

                    # Check for Parameters section
                    if "Parameters" in doc or "Args" in doc:
                        if "---" not in doc and "----" not in doc:
                            # Allow if using Args: format
                            if "Args:" in doc:
                                pass  # Acceptable alternate format
                            else:
                                issues.append(
                                    f"D407: {node.name} - Missing dashed underline"
                                )

        return issues


def run_module_tests(module_path: Path, module_name: str) -> List[TestResult]:
    """Ejecuta todos los tests para un modulo."""
    results = []

    # Test 1: Importacion del modulo
    try:
        # Simular importacion agregando al path
        sys.path.insert(0, str(PROJECT_ROOT))

        # Verificar que el archivo existe
        if not module_path.exists():
            results.append(
                TestResult(
                    f"{module_name} - File exists",
                    False,
                    f"File not found: {module_path}",
                )
            )
        else:
            results.append(TestResult(f"{module_name} - File exists", True, f"OK"))

        # Test 2: Modulo puede ser parseado
        try:
            with open(module_path, "r", encoding="utf-8") as f:
                ast.parse(f.read())
            results.append(TestResult(f"{module_name} - AST Parse", True, "OK"))
        except SyntaxError as e:
            results.append(
                TestResult(f"{module_name} - AST Parse", False, f"Syntax error: {e}")
            )

        # Test 3: Docstring de modulo
        auditor = DocumentationAuditor(module_path)
        module_doc = auditor.get_module_docstring()

        if module_doc and len(module_doc) >= 20:
            results.append(
                TestResult(
                    f"{module_name} - Module docstring",
                    True,
                    f"Length: {len(module_doc)} chars",
                )
            )
        else:
            results.append(
                TestResult(
                    f"{module_name} - Module docstring",
                    False,
                    f"Missing or too short (< 20 chars)",
                )
            )

        # Test 4: Cobertura de funciones
        functions = auditor.get_all_functions()
        functions_with_doc = [f for f in functions if f[1]]
        coverage = len(functions_with_doc) / len(functions) * 100 if functions else 0

        if coverage == 100:
            results.append(
                TestResult(
                    f"{module_name} - Function coverage",
                    True,
                    f"{coverage:.1f}% ({len(functions_with_doc)}/{len(functions)})",
                )
            )
        else:
            missing = [f[0] for f in functions if not f[1]]
            results.append(
                TestResult(
                    f"{module_name} - Function coverage",
                    False,
                    f"{coverage:.1f}% - Missing docstrings: {missing}",
                )
            )

        # Test 5: Clases documentadas
        classes = auditor.get_all_classes()
        if classes:
            classes_with_doc = [(c[0], c[1]) for c in classes if c[1]]
            coverage = len(classes_with_doc) / len(classes) * 100 if classes else 0

            if coverage == 100:
                results.append(
                    TestResult(
                        f"{module_name} - Class coverage",
                        True,
                        f"{coverage:.1f}% ({len(classes_with_doc)}/{len(classes)})",
                    )
                )
            else:
                missing = [c[0] for c in classes if not c[1]]
                results.append(
                    TestResult(
                        f"{module_name} - Class coverage",
                        False,
                        f"{coverage:.1f}% - Missing: {missing}",
                    )
                )

        # Test 6: Estilo NumPy basico
        numpy_issues = auditor.check_numpy_style()
        if len(numpy_issues) <= 5:  # Allow some style issues
            results.append(
                TestResult(
                    f"{module_name} - NumPy style",
                    True,
                    f"{len(numpy_issues)} minor issues (acceptable)",
                )
            )
        else:
            results.append(
                TestResult(
                    f"{module_name} - NumPy style",
                    False,
                    f"{len(numpy_issues)} issues: {numpy_issues[:3]}",
                )
            )

        # Test 7: Estructura de clases POM
        if module_name == "web_automator":
            pom_classes = [
                "BasePage",
                "LoginPage",
                "ProcessSearchPage",
                "AttachmentPage",
                "WebAutomator",
            ]
            found_classes = [c[0] for c in classes]
            missing_pom = [c for c in pom_classes if c not in found_classes]

            if not missing_pom:
                results.append(
                    TestResult(
                        f"{module_name} - POM structure",
                        True,
                        "All Page Objects present",
                    )
                )
            else:
                results.append(
                    TestResult(
                        f"{module_name} - POM structure",
                        False,
                        f"Missing POM classes: {missing_pom}",
                    )
                )

        # Test 8: Metodos criticos
        critical_methods = {
            "adaptive_wait": ["record_attempt", "predict_optimal_wait"],
            "data_handler": ["get_pending_tasks", "update_task_status", "save"],
            "web_automator": ["login", "completar_formulario", "close_session"],
        }

        short_name = module_name.replace("src/", "").replace(".py", "")
        if short_name in critical_methods:
            found_methods = [f[0] for f in functions]
            missing_critical = [
                m for m in critical_methods[short_name] if m not in found_methods
            ]

            if not missing_critical:
                results.append(
                    TestResult(
                        f"{module_name} - Critical methods",
                        True,
                        "All critical methods present",
                    )
                )
            else:
                results.append(
                    TestResult(
                        f"{module_name} - Critical methods",
                        False,
                        f"Missing: {missing_critical}",
                    )
                )

    finally:
        sys.path.pop(0)

    return results


def main():
    """Punto de entrada principal."""
    print("=" * 70)
    print("AUDITORIA TDD - Modulos src/")
    print("=" * 70)
    print()

    # Modulos a auditar
    modules = [
        (SRC_PATH / "web_automator.py", "src/web_automator"),
        (SRC_PATH / "data_handler.py", "src/data_handler"),
        (SRC_PATH / "adaptive_wait.py", "src/adaptive_wait"),
    ]

    all_results = []
    total_passed = 0
    total_failed = 0

    for module_path, module_name in modules:
        print(f"\n{'-' * 70}")
        print(f"MODULO: {module_name}")
        print(f"{'-' * 70}")

        results = run_module_tests(module_path, module_name)
        all_results.extend(results)

        for result in results:
            status_icon = "OK" if result.passed else "XX"
            print(f"  [{status_icon}] {result.name}")
            if result.message and not result.passed:
                print(f"       -> {result.message}")

        passed = len([r for r in results if r.passed])
        failed = len([r for r in results if not r.passed])
        total_passed += passed
        total_failed += failed

        print(f"\n  Resumen: {passed} passed, {failed} failed")

    # Resumen final
    print()
    print("=" * 70)
    print("RESUMEN DE AUDITORIA TDD")
    print("=" * 70)
    print(f"\nTotal Tests: {len(all_results)}")
    print(f"Passed: {total_passed} OK")
    print(f"Failed: {total_failed} XX")
    print(f"Pass Rate: {total_passed / len(all_results) * 100:.1f}%")
    print()

    if total_failed == 0:
        print("[OK] TODOS LOS TESTS PASARON - Implementacion validada")
        return 0
    else:
        print("[X] ALGUNOS TESTS FALLARON - Revision requerida")
        return 1


if __name__ == "__main__":
    sys.exit(main())
