"""Regression tests for false passes, execution failures and child cleanup."""
import ast
import os
import base64
import gzip
import json
import struct
from contextlib import redirect_stdout
import io
import itertools
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from frozen_candidate_controls import (CANONICAL, CPP, EXPECTED, EXPONENT, RECIPE,
                                       REQUIRED_CHECKPOINTS, SCHEMA, evaluate, run_case)

ORDER_FIXTURES = Path(__file__).resolve().parent/'fixtures/rejection_order'


class FailClosedTests(unittest.TestCase):
    def test_all_expected_rejections_and_impostors(self):
        for name, (code, diagnostic) in EXPECTED.items():
            with self.subTest(control=name):
                good = '\n'.join((*REQUIRED_CHECKPOINTS[name], diagnostic))+'\n'
                self.assertTrue(evaluate(name, code, good)[0])
                for wrong_code in (0, 2, -9, 70):
                    self.assertFalse(evaluate(name, wrong_code, good)[0])
                for bad in ('', 'ValueError: resource limit failure',
                            'REJECT: missing binary', diagnostic+' extra',
                            good+'\nTraceback (most recent call last):\nValueError',
                            good+'\nREJECT: different check',
                            'ValueError: resource limit failure\n'+good,
                            'FileNotFoundError: checker missing\n'+good):
                    self.assertFalse(evaluate(name, code, bad)[0])
                self.assertFalse(evaluate(name, code, good, stopped=True)[0])

    def rejection_logs(self):
        """Round-6 captures; checkpoint expectations come from the logs."""
        for row in json.loads((ORDER_FIXTURES/'captures.json').read_text()):
            if row['name'] != 'positive_frozen':
                yield row['name'], row['exit_code'], (ORDER_FIXTURES/f"{row['name']}.log").read_text()

    def test_astra_actual_logs_and_before_start_probes(self):
        for name, code, output in self.rejection_logs():
            with self.subTest(control=name):
                self.assertTrue(evaluate(name, code, output)[0])
                if name in ('schema', 'exponent', 'zero_initial'):
                    self.assertNotIn(CPP, output.splitlines())
        for name in ('canonical_word', 'constant_positive_potential'):
            with self.subTest(probe=name):
                output = (ORDER_FIXTURES/f'{name}_before_start.log').read_text()
                self.assertFalse(evaluate(name, EXPECTED[name][0], output)[0])

    def test_original_astra2_probes_with_round6_recipe_checkpoint(self):
        for old,name in [('canonical_word','canonical_word'),
                         ('positive_root_minimum','constant_positive_potential')]:
            output = (ORDER_FIXTURES/'astra_round5'/f'{old}_before_start.log').read_text()
            output = output.replace(EXPONENT,EXPONENT+'\n'+RECIPE)
            self.assertFalse(evaluate(name,EXPECTED[name][0],output)[0])

    def test_reordered_and_missing_actual_checkpoints_are_errors(self):
        for name, code, output in self.rejection_logs():
            lines = output.splitlines()
            # Derive the expected evidence from the capture, independently of
            # the classifier's declaration, so a weakened declaration fails.
            required = tuple(line for line in lines if line.startswith('VERIFY_CHECKPOINT '))
            indices = [lines.index(checkpoint) for checkpoint in required]
            for order in itertools.permutations(required):
                if order == required:
                    continue
                changed = lines.copy()
                for index, checkpoint in zip(indices, order):
                    changed[index] = checkpoint
                with self.subTest(control=name, order=order):
                    self.assertFalse(evaluate(name, code, '\n'.join(changed))[0])
            for checkpoint in required:
                with self.subTest(control=name, missing=checkpoint):
                    self.assertFalse(evaluate(name, code, '\n'.join(
                        line for line in lines if line != checkpoint))[0])

    def test_diagnostic_before_each_required_checkpoint_is_error(self):
        for name, code, output in self.rejection_logs():
            diagnostic = EXPECTED[name][1]
            lines = [line for line in output.splitlines() if line != diagnostic]
            for checkpoint in (line for line in lines if line.startswith('VERIFY_CHECKPOINT ')):
                index = lines.index(checkpoint)
                with self.subTest(control=name, before=checkpoint):
                    self.assertFalse(evaluate(name, code, '\n'.join(
                        lines[:index]+[diagnostic]+lines[index:]))[0])

    def test_duplicate_and_extra_rejections_anywhere_are_errors(self):
        cases = list(self.rejection_logs())
        cases.extend([
            ('positive_frozen', 143, '\n'.join((SCHEMA, EXPONENT, RECIPE, CPP, CANONICAL))),
        ])
        for name, code, output in cases:
            stopped = name == 'positive_frozen'
            self.assertTrue(evaluate(name, code, output, stopped)[0])
            lines = output.splitlines()
            extra_lines = ['REJECT: unrelated', 'VERIFY_REJECT unrelated',
                           '  REJECT: indented', '  VERIFY_REJECT indented',
                           'REJECT unexpected format']
            if name in EXPECTED:
                extra_lines.append(EXPECTED[name][1])
            for extra in extra_lines:
                for index in range(len(lines)+1):
                    with self.subTest(control=name, extra=extra, index=index):
                        self.assertFalse(evaluate(name, code, '\n'.join(
                            lines[:index]+[extra]+lines[index:]), stopped)[0])

    def test_cpp_is_required_for_cpp_rejections_and_positive(self):
        for name in ('canonical_word', 'constant_positive_potential'):
            code, reason = EXPECTED[name]
            self.assertFalse(evaluate(name, code, '\n'.join((SCHEMA, EXPONENT, reason)))[0])
        good = '\n'.join((SCHEMA, EXPONENT, RECIPE, CPP, CANONICAL))
        self.assertTrue(evaluate('positive_frozen', 143, good, stopped=True)[0])
        self.assertFalse(evaluate('positive_frozen', 143, good)[0])
        self.assertFalse(evaluate('positive_frozen', -9, good, stopped=True)[0])
        self.assertFalse(evaluate('positive_frozen', 143, good.replace(CPP, ''), stopped=True)[0])
        self.assertFalse(evaluate('positive_frozen', 143, good+'\nREJECT: other', stopped=True)[0])

    def test_actual_missing_verifier_and_python_exception_are_errors(self):
        with tempfile.TemporaryDirectory(dir='work', prefix='classifier-test-') as folder:
            missing = run_case('schema', Path(folder)/'artifact', Path(folder)/'missing.py',
                               'controls_selftest_missing', 5)
            self.assertEqual(missing['status'], 'ERROR')
            verifier = Path(folder)/'exception.py'
            verifier.write_text("print('VERIFY_REJECT schema', flush=True)\nraise ValueError('RLIMIT_AS')\n")
            failure = run_case('schema', Path(folder)/'artifact', verifier,
                               'controls_selftest_exception', 5)
            self.assertEqual(failure['status'], 'ERROR')

    def test_timeout_reaps_process_group(self):
        with tempfile.TemporaryDirectory(dir='work', prefix='classifier-test-') as folder:
            verifier = Path(folder)/'sleep.py'
            verifier.write_text('import subprocess,sys,time\nsubprocess.Popen([sys.executable,"-c","import time; time.sleep(60)"])\ntime.sleep(60)\n')
            result = run_case('canonical_word', Path(folder)/'artifact', verifier,
                              'controls_selftest_timeout', 0.2)
            self.assertEqual(result['status'], 'ERROR')
            self.assertTrue(result['timed_out'])
            groups = subprocess.check_output(['ps', '-axo', 'pgid='], text=True).split()
            self.assertNotIn(str(result['pid']), groups)

    def test_duplicate_checkpoints_are_errors(self):
        for name, code, output in self.rejection_logs():
            for checkpoint in (s for s in output.splitlines() if s.startswith('VERIFY_CHECKPOINT ')):
                self.assertFalse(evaluate(name, code, checkpoint+'\n'+output)[0])

    def test_actual_signal_and_spawn_failure_are_errors(self):
        with tempfile.TemporaryDirectory(dir='work', prefix='classifier-test-') as folder:
            verifier = Path(folder)/'terminate_probe.py'
            verifier.write_text("import os,signal\nprint('VERIFY_REJECT schema',flush=True)\nos.kill(os.getpid(),signal.SIGTERM)\n")
            result = run_case('schema', Path(folder)/'artifact', verifier,
                              'controls_selftest_signal', 5)
            self.assertEqual(result['status'], 'ERROR')
            self.assertEqual(result['exit_code'], -signal.SIGTERM)
            with patch('frozen_candidate_controls.subprocess.Popen', side_effect=FileNotFoundError('missing launcher')):
                result = run_case('schema', Path(folder)/'artifact', verifier,
                                  'controls_selftest_spawn', 5)
            self.assertEqual(result['status'], 'ERROR')
            self.assertIsNone(result['pid'])

    def test_positive_capture_and_checkpoint_order(self):
        rows = json.loads((ORDER_FIXTURES/'captures.json').read_text())
        row = next(r for r in rows if r['name'] == 'positive_frozen')
        output = (ORDER_FIXTURES/'positive_frozen.log').read_text()
        self.assertTrue(evaluate(row['name'],row['exit_code'],output,row['intentional_checkpoint_stop'])[0])
        required = [s for s in output.splitlines() if s.startswith('VERIFY_CHECKPOINT ')]
        for checkpoint in required:
            self.assertFalse(evaluate(row['name'],row['exit_code'],output.replace(checkpoint,''),True)[0])
        lines = output.splitlines()
        indices = [lines.index(s) for s in required]
        for order in itertools.permutations(required):
            if list(order) == required:
                continue
            changed = lines.copy()
            for index,checkpoint in zip(indices,order):
                changed[index] = checkpoint
            self.assertFalse(evaluate(row['name'],row['exit_code'],'\n'.join(changed),True)[0])

    def test_resource_hook_logs_refusal_and_applies_on_supported_os(self):
        # Execute the actual hook statements in isolation; no verifier bypass.
        tree = ast.parse(Path('verify_orbit8.py').read_text())
        context = next(n for n in tree.body if isinstance(n, ast.With))
        hook = next(n for n in context.body if isinstance(n, ast.Try)
                    and any(isinstance(x, ast.ExceptHandler) for x in n.handlers))
        import resource
        module = ast.Module(body=[hook], type_ignores=[])
        for exception in (None, ValueError('OS refuses RLIMIT_AS'), OSError('OS refuses RLIMIT_AS')):
            with self.subTest(exception=exception):
                stream = io.StringIO()
                with patch.object(resource, 'getrlimit', return_value=(-1, -1)), \
                     patch.object(resource, 'setrlimit', side_effect=exception), redirect_stdout(stream):
                    namespace = dict(resource=resource, previous_limit=None)
                    exec(compile(module, 'actual_resource_hook', 'exec'), namespace)
                self.assertIn('APPLIED' if exception is None else 'SKIPPED', stream.getvalue())
                self.assertEqual(namespace['previous_limit'], (-1, -1) if exception is None else None)


if __name__ == '__main__':
    if os.getpriority(os.PRIO_PROCESS,0) < 10:
        os.setpriority(os.PRIO_PROCESS,0,10)
    print('TEST_NICE',os.getpriority(os.PRIO_PROCESS,0),flush=True)
    unittest.main()
