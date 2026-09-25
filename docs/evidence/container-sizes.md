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

## Frontend (ASG-DEVOPS-009, -010, -012)

The CI `context-and-image-size` job now builds the Node builder and nginx runtime stages and
measures the frontend context with and without `.dockerignore`. Numerical measurements and the
runtime content check are pending a CI run on the #48 branch. Docker is not installed on Artfever's
machine, so no local image size or runtime result is claimed.

The `integration` job also captures the actual output of
`docker compose exec -T frontend ping -c 1 -W 2 database`; a failed name lookup is required.
Its output and the video demonstration are pending.
