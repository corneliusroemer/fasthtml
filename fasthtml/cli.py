# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/api/09_cli.ipynb.

# %% auto 0
__all__ = ['railway_link', 'railway_deploy']

# %% ../nbs/api/09_cli.ipynb 2
from fastcore.utils import *
from fastcore.script import call_parse, bool_arg
from subprocess import check_output, run

import json

# %% ../nbs/api/09_cli.ipynb 3
@call_parse
def railway_link():
    "Link the current directory to the current project's Railway service"
    j = json.loads(check_output("railway status --json".split()))
    prj = j['id']
    idxpath = 'edges', 0, 'node', 'id'
    env = nested_idx(j, 'environments', *idxpath)
    svc = nested_idx(j, 'services', *idxpath)

    cmd = f"railway link -e {env} -p {prj} -s {svc}"
    res = check_output(cmd.split())

# %% ../nbs/api/09_cli.ipynb 4
def _run(a, **kw):
    print('#', ' '.join(a))
    run(a)

# %% ../nbs/api/09_cli.ipynb 5
@call_parse
def railway_deploy(
    name:str, # The project name to deploy
    mount:bool_arg=True # Create a mounted volume at /app/data?
):
    """Deploy a FastHTML app to Railway"""
    nm,ver = check_output("railway --version".split()).decode().split()
    assert nm=='railwayapp', f'Unexpected railway version string: {nm}'
    if ver2tuple(ver)<(3,8): return print("Please update your railway CLI version to 3.8 or higher")
    cp = run("railway status --json".split(), capture_output=True)
    if not cp.returncode: print("Checking deployed projects...")
    project_name = json.loads(cp.stdout.decode()).get('name')
    if project_name == name: return print("This project is already deployed. Run `railway open`.")
    reqs = Path('requirements.txt')
    if not reqs.exists(): reqs.write_text('python-fasthtml')
    _run(f"railway init -n {name}".split())
    _run(f"railway up -c".split())
    _run(f"railway domain".split())
    railway_link.__wrapped__()
    if mount: _run(f"railway volume add -m /app/data".split())
    _run(f"railway up -c".split())
