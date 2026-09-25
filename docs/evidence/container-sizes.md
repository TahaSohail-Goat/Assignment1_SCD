# Container sizes and build-context sizes (ASG-DEVOPS-010, ASG-DEVOPS-012)

Measured by the `context-and-image-size` job of `ci.yml` on a GitHub-hosted runner (`ubuntu-24.04`,
Docker with BuildKit). The job's own output is the source; the run linked below is the evidence.

Run (commit `736e692`): <https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36189116384>

## Backend build context (`backend/`, ASG-DEVOPS-012)

The tree is a developer's working tree after `pip install -r requirements-dev.txt` and a bytecode
compile: a virtual environment and `__pycache__` directories sit inside `backend/`.

| | Context sent to the Docker daemon |
|---|---|
| Without `backend/.dockerignore` | **196.61 MB** |
| With `backend/.dockerignore` | **193.07 kB** |

The context is measured with a throwaway `FROM scratch` / `COPY . /ctx` Dockerfile, because BuildKit
sends only the files a `COPY` asks for, which would hide the difference for the real Dockerfile.
The `.dockerignore` removes the virtual environment, bytecode caches, tests and `.env*` files.

## Backend image (ASG-DEVOPS-010, backend part)

- Final image: **207 MB** on `python:3.12.14-slim-bookworm`.
- The dependency layer copied from the builder stage (`COPY /opt/venv /opt/venv`) is **82.9 MB**;
  the application (`COPY app`) is **180 kB**, `alembic` **5.27 kB**.
- The builder stage (pip, wheel caches, build tools) is **not** in the final image: only the virtual
  environment is copied across.

## Frontend (ASG-DEVOPS-009, -010, -012, -017)

The final CI measurement for commit `2936f8a` is from
<https://github.com/TahaSohail-Goat/Assignment1_SCD/actions/runs/36194643433>.
The job completed successfully and checked that the runtime lacks Node, `node_modules` and
source. Both image scans passed. The runtime is 60.1 MB, essentially the assignment's ~60 MB
guide; it grew from 48.4 MB on the first run because the pinned nginx base needed Alpine
security updates. No size reduction is claimed beyond the measured value.

| Measurement | Final CI run |
|---|---:|
| Build context without `frontend/.dockerignore` | 105.95 MB |
| Build context with `frontend/.dockerignore` | 160.17 kB |
| Node builder stage image | 288 MB |
| nginx runtime image | 60.1 MB |

The same CI run's `integration` job executed
`docker compose exec -T frontend ping -c 1 -W 2 database` and captured
`ping: bad address 'database'`. The step required a name-lookup failure and passed.
The video demonstration remains pending. Docker is unavailable on Artfever's local machine.
