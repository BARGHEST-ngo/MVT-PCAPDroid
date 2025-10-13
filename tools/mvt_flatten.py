from pathlib import Path
from urllib.parse import urlparse
import subprocess
import time

rd = Path(__file__).resolve().parents[1]
p = rd / "mvt-indicators"

def collect_domains(root: Path):
    out = []
    for f in root.rglob("*.txt"):
        if f.name == "domains.txt":
            with f.open(encoding="utf-8") as fh:
                for line in fh:
                    s = line.strip()
                    if not s:
                        continue
                    u = urlparse(s)
                    host = (u.netloc or u.path).lstrip(".")
                    if host:
                        out.append(host)
    return out

def collect_ips(root: Path):
    out = []
    for f in root.rglob("*.txt"):
        if f.name == "ip-addresses.txt":
            with f.open(encoding="utf-8") as fh:
                for line in fh:
                    s = line.strip()
                    if s:
                        out.append(s)
    return out

p.parent.mkdir(parents=True, exist_ok=True)

if not p.exists():
    subprocess.run(
        ["git", "clone", "https://github.com/mvt-project/mvt-indicators.git", str(p)],
        check=True
    ) 

domains_list = collect_domains(p)
ips_list = collect_ips(p)

Path("domains.txt").write_text("\n".join(sorted(set(domains_list))) + "\n", encoding="utf-8")
Path("ips.txt").write_text("\n".join(sorted(set(ips_list))) + "\n", encoding="utf-8")
