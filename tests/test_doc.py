"""Test documentation code blocks in markdown files."""

import ast
import io
import re
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest


class CodeBlock:
    """Represents a Python code block found in markdown."""

    def __init__(
        self,
        content: str,
        file_path: Path,
        line_number: int,
        language: str = "python",
        should_skip: bool = False,
        skip_reason: str = "",
    ):
        self.content = content
        self.file_path = file_path
        self.line_number = line_number
        self.language = language
        self.should_skip = should_skip
        self.skip_reason = skip_reason

    def __str__(self):
        return f"{self.file_path}:{self.line_number} ({'skipped' if self.should_skip else 'executable'})"


class ExecutionResult:
    """Represents the result of executing a code block."""

    def __init__(
        self,
        code_block: CodeBlock,
        success: bool = True,
        error: Optional[str] = None,
        output: str = "",
    ):
        self.code_block = code_block
        self.success = success
        self.error = error
        self.output = output


class DocTestExtractor:
    """Extract and test code blocks from markdown files."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.global_namespace: Dict[str, Any] = {}

    def find_markdown_files(self, paths: List[Path]) -> List[Path]:
        """Find all markdown files in the given paths."""
        markdown_files = []

        for path in paths:
            if path.is_file() and path.suffix in [".md", ".markdown"]:
                markdown_files.append(path)
            elif path.is_dir():
                markdown_files.extend(path.rglob("*.md"))
                markdown_files.extend(path.rglob("*.markdown"))

        return sorted(markdown_files)

    def extract_code_blocks(self, file_path: Path) -> List[CodeBlock]:
        """Extract Python code blocks from a markdown file."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError) as e:
            if self.verbose:
                print(f"Warning: Could not read {file_path}: {e}")
            return []

        code_blocks = []
        lines = content.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Check for HTML comment skip marker on previous line
            skip_reason = ""
            should_skip = False

            if i > 0:
                prev_line = lines[i - 1].strip()
                if re.search(r"<!--\s*skip\s*-->", prev_line, re.IGNORECASE):
                    should_skip = True
                    skip_reason = "HTML comment skip marker"
                elif re.search(
                    r"<!--\s*mktestdocs:\s*skip\s*-->", prev_line, re.IGNORECASE
                ):
                    should_skip = True
                    skip_reason = "mktestdocs skip marker"

            # Look for code fences
            if line.startswith("```"):
                # Extract language and check for skip marker
                fence_info = line[3:].strip()
                language = fence_info.split()[0] if fence_info else ""

                # Check if skip marker is in fence info
                if "skip" in fence_info.lower():
                    should_skip = True
                    skip_reason = "fence skip marker"

                # Collect code content first
                i += 1
                code_lines = []
                start_line = i + 1  # Line number where code starts (1-indexed)

                # Collect code until closing fence
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    code_lines.append(lines[i])
                    i += 1

                # Only process Python code blocks or blocks without language that seem to be Python
                if language in ["python", "py"] or (not language and code_lines):
                    # For blocks without language, assume Python only if content looks like Python
                    if not language and code_lines:
                        code_content = "\n".join(code_lines).strip()
                        # Simple heuristic: if it doesn't look like Python, skip it
                        if (
                            code_content.startswith("echo ")
                            or code_content.startswith("console.log")
                            or code_content.startswith("curl ")
                            or "console." in code_content
                            or "$" in code_content.split("\n")[0]
                        ):  # Shell command indicators
                            continue

                    if code_lines:  # Only add non-empty code blocks
                        code_content = "\n".join(code_lines)

                        # Check for inline skip markers in the code
                        if not should_skip:
                            if re.search(r"#\s*skip", code_content, re.IGNORECASE):
                                should_skip = True
                                skip_reason = "inline skip comment"
                            elif re.search(
                                r"#\s*mktestdocs:\s*skip", code_content, re.IGNORECASE
                            ):
                                should_skip = True
                                skip_reason = "inline mktestdocs skip comment"

                        code_blocks.append(
                            CodeBlock(
                                content=code_content,
                                file_path=file_path,
                                line_number=start_line,
                                language=language or "python",
                                should_skip=should_skip,
                                skip_reason=skip_reason,
                            )
                        )

            i += 1

        return code_blocks

    def validate_syntax(self, code_block: CodeBlock) -> Optional[str]:
        """Check if the code block has valid Python syntax."""
        try:
            ast.parse(code_block.content)
            return None
        except SyntaxError as e:
            return f"Syntax error: {e}"

    def execute_code_block(self, code_block: CodeBlock) -> ExecutionResult:
        """Execute a code block and return the result."""
        if code_block.should_skip:
            return ExecutionResult(
                code_block, success=True, output=f"Skipped: {code_block.skip_reason}"
            )

        # Check syntax first
        syntax_error = self.validate_syntax(code_block)
        if syntax_error:
            return ExecutionResult(code_block, success=False, error=syntax_error)

        # Capture stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        captured_output = io.StringIO()
        captured_error = io.StringIO()

        try:
            sys.stdout = captured_output
            sys.stderr = captured_error

            # Execute the code in the global namespace to maintain state
            exec(code_block.content, self.global_namespace)

            output = captured_output.getvalue()
            error_output = captured_error.getvalue()

            if error_output and not output:
                # If there's only error output, treat it as a failure
                return ExecutionResult(code_block, success=False, error=error_output.strip())

            return ExecutionResult(code_block, success=True, output=output + error_output)

        except Exception as e:
            error_msg = f"{type(e).__name__}: {e}\n"
            if self.verbose:
                error_msg += traceback.format_exc()
            return ExecutionResult(code_block, success=False, error=error_msg.strip())

        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


class TestDocumentation:
    """Test suite for documentation code blocks."""

    def setup_method(self):
        """Set up test environment."""
        self.extractor = DocTestExtractor(verbose=False)

    def test_extract_simple_code_block(self):
        """Test extraction of a simple Python code block."""
        markdown_content = """
# Test Document

Here's some Python code:

```python
x = 1 + 1
print(x)
```

Done.
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(markdown_content)
            f.flush()
            file_path = Path(f.name)

        try:
            code_blocks = self.extractor.extract_code_blocks(file_path)

            assert len(code_blocks) == 1
            assert code_blocks[0].content.strip() == "x = 1 + 1\nprint(x)"
            assert code_blocks[0].should_skip is False
            assert code_blocks[0].language == "python"
        finally:
            file_path.unlink()

    def test_html_comment_skip_marker(self):
        """Test HTML comment skip markers."""
        markdown_content = """
# Test Document

<!-- skip -->
```python
x = 1 / 0  # This should be skipped
```

<!-- mktestdocs: skip -->
```python
y = undefined_variable  # This should also be skipped
```
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(markdown_content)
            f.flush()
            file_path = Path(f.name)

        try:
            code_blocks = self.extractor.extract_code_blocks(file_path)

            assert len(code_blocks) == 2
            assert all(block.should_skip for block in code_blocks)
            assert code_blocks[0].skip_reason == "HTML comment skip marker"
            assert code_blocks[1].skip_reason == "mktestdocs skip marker"
        finally:
            file_path.unlink()

    def test_fence_skip_marker(self):
        """Test skip markers in code fence."""
        markdown_content = """
# Test Document

```python skip
x = 1 / 0  # This should be skipped
```

```py skip
y = undefined_variable  # This should also be skipped
```
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(markdown_content)
            f.flush()
            file_path = Path(f.name)

        try:
            code_blocks = self.extractor.extract_code_blocks(file_path)

            assert len(code_blocks) == 2
            assert all(block.should_skip for block in code_blocks)
            assert all(
                block.skip_reason == "fence skip marker" for block in code_blocks
            )
        finally:
            file_path.unlink()

    def test_inline_skip_marker(self):
        """Test inline skip markers in code."""
        markdown_content = """
# Test Document

```python
# skip
x = 1 / 0  # This should be skipped
```

```python
# mktestdocs: skip
y = undefined_variable  # This should also be skipped
```
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(markdown_content)
            f.flush()
            file_path = Path(f.name)

        try:
            code_blocks = self.extractor.extract_code_blocks(file_path)

            assert len(code_blocks) == 2
            assert all(block.should_skip for block in code_blocks)
            assert code_blocks[0].skip_reason == "inline skip comment"
            assert code_blocks[1].skip_reason == "inline mktestdocs skip comment"
        finally:
            file_path.unlink()

    def test_successful_code_execution(self):
        """Test successful execution of code blocks."""
        markdown_content = """
# Test Document

```python
x = 2 + 3
assert x == 5
```
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(markdown_content)
            f.flush()
            file_path = Path(f.name)

        try:
            code_blocks = self.extractor.extract_code_blocks(file_path)
            result = self.extractor.execute_code_block(code_blocks[0])

            assert result.success is True
            assert result.error is None
        finally:
            file_path.unlink()

    def test_failed_code_execution(self):
        """Test handling of failed code execution."""
        markdown_content = """
# Test Document

```python
x = 1 / 0  # This will raise an exception
```
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(markdown_content)
            f.flush()
            file_path = Path(f.name)

        try:
            code_blocks = self.extractor.extract_code_blocks(file_path)
            result = self.extractor.execute_code_block(code_blocks[0])

            assert result.success is False
            assert result.error is not None and "ZeroDivisionError" in result.error
        finally:
            file_path.unlink()

    def test_syntax_error_detection(self):
        """Test detection of syntax errors."""
        markdown_content = """
# Test Document

```python
if True
    print("Invalid syntax")
```
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(markdown_content)
            f.flush()
            file_path = Path(f.name)

        try:
            code_blocks = self.extractor.extract_code_blocks(file_path)
            result = self.extractor.execute_code_block(code_blocks[0])

            assert result.success is False
            assert result.error is not None and "Syntax error" in result.error
        finally:
            file_path.unlink()

    def test_skipped_code_execution(self):
        """Test that skipped code blocks are not executed."""
        code_block = CodeBlock(
            content="x = 1 / 0",  # Would fail if executed
            file_path=Path("test.md"),
            line_number=1,
            should_skip=True,
            skip_reason="test skip",
        )

        result = self.extractor.execute_code_block(code_block)

        assert result.success is True
        assert "Skipped: test skip" in result.output

    def test_mixed_code_blocks(self):
        """Test a mix of regular and skipped code blocks."""
        markdown_content = """
# Test Document

```python
x = 1
```

<!-- skip -->
```python
y = 1 / 0  # This should be skipped
```

```python
z = x + 1
assert z == 2
```
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(markdown_content)
            f.flush()
            file_path = Path(f.name)

        try:
            code_blocks = self.extractor.extract_code_blocks(file_path)
            results = []
            stats = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}

            for code_block in code_blocks:
                result = self.extractor.execute_code_block(code_block)
                results.append(result)
                stats["total"] += 1

                if code_block.should_skip:
                    stats["skipped"] += 1
                elif result.success:
                    stats["passed"] += 1
                else:
                    stats["failed"] += 1

            assert stats["total"] == 3
            assert stats["passed"] == 2
            assert stats["failed"] == 0
            assert stats["skipped"] == 1
        finally:
            file_path.unlink()

    def test_state_persistence(self):
        """Test that state persists between code blocks."""
        markdown_content = """
# Test Document

```python
x = 42
```

```python
# This should work because x was defined in the previous block
assert x == 42
```
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(markdown_content)
            f.flush()
            file_path = Path(f.name)

        try:
            code_blocks = self.extractor.extract_code_blocks(file_path)
            results = []
            stats = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}

            for code_block in code_blocks:
                result = self.extractor.execute_code_block(code_block)
                results.append(result)
                stats["total"] += 1

                if code_block.should_skip:
                    stats["skipped"] += 1
                elif result.success:
                    stats["passed"] += 1
                else:
                    stats["failed"] += 1

            assert stats["total"] == 2
            assert stats["passed"] == 2
            assert stats["failed"] == 0
        finally:
            file_path.unlink()

    def test_non_python_code_ignored(self):
        """Test that non-Python code blocks are ignored."""
        markdown_content = """
# Test Document

```bash
echo "This is bash code"
```

```javascript
console.log("This is JavaScript");
```

```python
x = 1  # Only this should be extracted
```
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(markdown_content)
            f.flush()
            file_path = Path(f.name)

        try:
            code_blocks = self.extractor.extract_code_blocks(file_path)

            assert len(code_blocks) == 1
            assert (
                code_blocks[0].content.strip()
                == "x = 1  # Only this should be extracted"
            )
        finally:
            file_path.unlink()

    def test_documentation_code_blocks(self):
        """Test actual documentation files for code block execution."""
        project_root = Path(__file__).parent.parent
        docs_dir = project_root / "docs"
        
        if not docs_dir.exists():
            pytest.skip("docs directory not found")

        extractor = DocTestExtractor(verbose=False)
        markdown_files = extractor.find_markdown_files([docs_dir])
        
        if not markdown_files:
            pytest.skip("No markdown files found in docs")

        failed_blocks = []
        total_blocks = 0
        skipped_blocks = 0

        for md_file in markdown_files:
            # Skip known problematic files or add skip markers to them
            if "blog" in str(md_file):  # Skip blog posts that might have different requirements
                continue
                
            code_blocks = extractor.extract_code_blocks(md_file)
            
            for code_block in code_blocks:
                total_blocks += 1
                result = extractor.execute_code_block(code_block)
                
                if code_block.should_skip:
                    skipped_blocks += 1
                elif not result.success:
                    failed_blocks.append((code_block, result.error))

        # Report results and fail if there are any errors
        if failed_blocks:
            error_msg = f"\nFound {len(failed_blocks)} failing code blocks out of {total_blocks} total ({skipped_blocks} skipped):\n"
            for code_block, error in failed_blocks[:10]:  # Show first 10 errors
                error_msg += f"  {code_block}: {error}\n"
            if len(failed_blocks) > 10:
                error_msg += f"  ... and {len(failed_blocks) - 10} more errors\n"
            error_msg += "\nTo fix: Add skip markers to code blocks that should not be executed:\n"
            error_msg += "  <!-- skip --> before code block\n"
            error_msg += "  ```python skip for fence marker\n"
            error_msg += "  # skip as inline comment"
            pytest.fail(error_msg)
        else:
            print(f"\nAll {total_blocks - skipped_blocks} code blocks passed! ({skipped_blocks} skipped)")

        # Ensure we found some code blocks to test
        assert total_blocks > 0, "Should find at least some code blocks in documentation"