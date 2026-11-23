"""Corrupt one certified input; record the exact checker response."""
import subprocess

terms = [2, 3, 7, 43, 1807, 3263443, 10650056950807, 113423713055421844361000443,
         12864938683278671740537145998360961546653259485195806]
cases = (
    ("control", terms, 0, "covered=1 missing=0 bad=0"),
    ("shift_denominator", [*terms[:-1], terms[-1] + 1], 1, "reason=sum"),
    ("duplicate_term", [*terms[:-1], terms[-2]], 1, "reason=duplicate_term"),
    ("remove_m", [4, *terms[1:]], 1, "reason=label_not_a_denominator"),
    ("delete_line", [], 1, "missing m=2"),
)
for name, denominators, expected_exit, marker in cases:
    data = "2: " + " ".join(map(str, denominators)) + "\n" if denominators else ""
    proc = subprocess.run(["build/check_certificates", "2", "2", "0"],
                          input=data, capture_output=True, text=True, timeout=10)
    assert proc.returncode == expected_exit and marker in proc.stdout, (name, proc)
    assert not proc.stderr
    print(f"{name} exit={proc.returncode}")
    print(proc.stdout, end="")
