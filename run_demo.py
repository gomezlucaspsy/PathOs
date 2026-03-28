from click.testing import CliRunner
from pathos.cli import main

runner = CliRunner()
result = runner.invoke(main, ['check', 'tests/sample_contradictions.py', '--interpret'])
print(result.output)
if result.exception:
    import traceback
    traceback.print_exception(type(result.exception), result.exception, result.exception.__traceback__)
