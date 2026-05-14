# https://dspy.ai/api/tools/PythonInterpreter/

import os, importlib
from dspy import PythonInterpreter

# The default PythonInterpreter doesn't grant --allow-read to node_modules,
# which pyodide needs for its WASM binary. We pass a custom command here.
_runner = os.path.join(
    os.path.dirname(importlib.import_module("dspy.primitives.python_interpreter").__file__),
    "runner.js",
)
_deno_dir = os.environ.get("DENO_DIR", os.path.expanduser("~/.deno"))

_primitives_nm = os.path.join(os.path.dirname(_runner), "node_modules")

_deno_cmd = [
    "deno", "run",
    f"--allow-read={_runner},{_deno_dir},{_primitives_nm}",
    _runner,
]

# Basic execution
with PythonInterpreter(deno_command=_deno_cmd) as interp:
    result = interp("print(1 + 2)")  # Returns "3"
    print(f"1+2 = {result}")

# With host-side tools
def my_tool(question: str) -> str:
    return "answer"

with PythonInterpreter(tools={"my_tool": my_tool}, deno_command=_deno_cmd) as interp:
    result = interp("print(my_tool(question='test'))")
    print(f"tool result = {result}")