# Environment Prerequisites

Phase 00 inspects the host **before** telling anyone to install anything. Only missing or incompatible tools get instructions; nothing already installed is re-installed.

- **Scan date:** 2026-09-25 · **Host:** Windows 11 Pro 10.0.26200 · shell: PowerShell 5.1 + Git Bash · **not elevated** (installs below need an administrator prompt)
- **Hardware:** Intel Core i5-8250U (4 cores / 8 threads) · 15.8 GB RAM · 145.6 GB free on `C:`
- **Virtualization:** `HypervisorPresent = True`; WSL 2.6.3 installed with **no distribution** (Docker Desktop supplies its own, so none is needed)
- **Source of versions:** assignment §3.1 (`python:3.12-slim`, `node:22-alpine`, `nginx:1.27-alpine`), §2.3 (PostgreSQL 16), §2.4 (Redis 7), §3.3 (k3d or kind, metrics-server, VPA, k6 or hey), §3.4 (ruff, mypy, eslint, tsc, Vitest, Trivy, kubeconform, Syft, kind/k3d).

## 1. Detection results

| Tool | Needed for | Required by assignment | Detected | Verdict |
|---|---|---|---|---|
| Git | all phases | — | 2.47.1 (`core.autocrlf=true`) | ✅ OK |
| GitHub CLI `gh` | issues, labels, PRs, protection | — (pack workflow) | 2.98.0, logged in as `TahaSohail-Goat`; scopes `gist`, `read:org`, `repo`, `workflow`; repo permission `ADMIN` | ✅ OK |
| curl | smoke tests | — | curl.exe 8.21.0 | ✅ OK |
| winget | installs below | — | 1.29.380 | ✅ OK |
| openssl / bash | VPA install script (Phase 09) | — | OpenSSL and Git Bash from Git for Windows | ✅ OK |
| Python | backend dev, tests | image base `python:3.12-slim` (§3.1) | 3.13.2 (+ pip 26.2.1) | ⚠️ present, **differs** (B-020) |
| Node.js / npm | frontend dev, tests | image base `node:22-alpine` (§3.1) | Node 24.13.0 / npm 11.6.2 | ⚠️ present, **differs** (B-020) |
| Docker Engine / Desktop | Compose, images, kind/k3d | required (§3.2) | not found | ❌ **missing** (B-017) |
| Docker Compose v2 | one-command stack | required (§3.2) | not found (ships with Docker Desktop) | ❌ **missing** |
| kubectl | Kubernetes phases, CD smoke | required (§3.3) | not found | ❌ **missing** |
| kind **or** k3d | local cluster | one of them (§3.3) | neither found | ❌ **missing** |
| kustomize | `kustomize build overlays/prod` (§3.4) | required in CI | not found | ⚠️ missing (optional locally; `kubectl kustomize` also works) |
| kubeconform | manifest validation (§3.4) | required in CI | not found | ⚠️ missing (optional locally) |
| k6 **or** hey | HPA load test (§3.3) | one of them | neither found (`hey` is not in winget; `k6` is) | ❌ **missing** |
| Trivy · Syft · Cosign | image scan, SBOM, signing (§3.4) | run in GitHub Actions | not found | ➖ CI-only; local copy optional (Cosign only for bonus) |
| Helm | only if Kustomize is replaced (§3.3, needs an ADR) | not required | not found | ➖ not needed |
| ruff · mypy · pytest · alembic | backend quality/tests | (§3.4) | not installed globally | ➖ installed per-project in a `.venv` in Phase 04/05, not host prerequisites |
| Ollama (host) | offline AI path | runs **as a Compose container** (§2.5) | not found | ➖ not needed on the host |
| pdftotext (Git for Windows) · PyMuPDF 1.28.2 | Phase 00 PDF extraction only | — | present | ✅ not needed to build or run the project |

Accounts/credentials needed later (not installed software): a GitHub account ✅; an LLM key from Groq or Google AI Studio **or** the Ollama path (§2.5 — no marks lost for Ollama). Keys are never committed (ASG-DED-001, ASG-AI-018). GHCR uses the workflow `GITHUB_TOKEN`; no separate token is needed (§3.4).

## 2. Nothing to do now

Git, `gh`, curl, winget and Git Bash are fine. **No install is required to finish Phases 00–07** except optionally the version-alignment options in §5. Docker and the Kubernetes tools are first needed at **Phase 08**.

## 3. Verify identity before any GitHub write (AGENTS.md §6)

```powershell
gh auth status                      # Logged in as TahaSohail-Goat
gh repo view TahaSohail-Goat/Assignment1_SCD --json viewerPermission   # ADMIN
git config user.name; git config user.email
```

A second contributor uses their **own** GitHub login and their own worktree; nobody commits or reviews as the other person (AGENTS.md §7).

## 4. Install instructions — missing tools only

Run each command in an **elevated** PowerShell (Run as administrator). Package IDs were confirmed with `winget search --exact` on the scan date. Re-check versions with `winget show <id>` if a command fails.

### 4.1 Docker Desktop + Compose (B-017) — needed at Phase 08

```powershell
winget install -e --id Docker.DockerDesktop
```

1. Reboot if the installer asks.
2. Start Docker Desktop, accept the terms (review Docker's subscription terms for your use), keep **"Use the WSL 2 based engine"** enabled.
3. Verify in a new terminal:

```powershell
docker version
docker compose version
docker run --rm hello-world
```

Recommended (not required) on this 15.8 GB / 8-thread laptop, because Compose + Ollama + a kind cluster run together: create `%UserProfile%\.wslconfig` and then `wsl --shutdown`:

```ini
[wsl2]
memory=8GB
processors=6
```

### 4.2 kubectl — needed at Phase 09

Docker Desktop normally bundles a `kubectl` client. After 4.1, run `kubectl version --client`; **install standalone only if that fails**:

```powershell
winget install -e --id Kubernetes.kubectl
```

### 4.3 Local cluster — install **one** of kind or k3d

```powershell
winget install -e --id Kubernetes.kind      # kind
# or
winget install -e --id k3d.k3d              # k3d
```

Either satisfies §3.3. The CD workflow must use the same tool; the choice is recorded when Phase 09 starts.

### 4.4 Manifest tooling (CI-parity, optional locally)

```powershell
winget install -e --id Kubernetes.kustomize
winget install -e --id YannHamon.kubeconform
```

### 4.5 Load generator — k6 (`hey` is not on winget)

```powershell
winget install -e --id GrafanaLabs.k6
```

### 4.6 Optional local copies of CI security tools

```powershell
winget install -e --id AquaSecurity.Trivy
winget install -e --id Anchore.Syft
winget install -e --id Sigstore.Cosign       # bonus ASG-BONUS-003 only
```

### 4.7 In-cluster components (installed by Phase 09, not on the host)

| Component | Needed for | Note |
|---|---|---|
| metrics-server | HPA CPU metrics (ASG-K8S-023) | On kind/k3d it usually needs `--kubelet-insecure-tls`. Confirm against the upstream README at install time. |
| Vertical Pod Autoscaler | recommender in `updateMode: "Off"` (ASG-K8S-028) | Installed from the `kubernetes/autoscaler` repository's VPA scripts (bash + openssl — both present via Git Bash). Confirm against upstream at install time. |
| Ingress controller | makes the `/` and `/api` Ingress work (ASG-K8S-009) | The assignment names none; the choice is a Phase 09 decision. |

## 5. Version alignment (B-020) — optional

The images will build with Python 3.12 and Node 22 regardless of the host. The mismatch only matters for tests run **outside** Docker. Pick one; do not uninstall existing versions:

| Goal | Command |
|---|---|
| Add Python 3.12 side by side | `winget install -e --id Python.Python.3.12` then use `py -3.12 -m venv backend\.venv` |
| Add Node 22 side by side | `winget install -e --id Schniz.fnm` then `fnm install 22` and `fnm use 22` in the frontend directory |
| Don't change the host | run backend/frontend tests only inside Docker and in CI (the CI runner is the reference environment) |

Whichever is chosen, record the versions actually used in `docs/ENGINEERING-NOTES.md` question 1 (laptop vs CI differences).

## 6. Post-install verification checklist

```powershell
git --version; gh --version
docker version; docker compose version
kubectl version --client
kind version            # or: k3d version
kustomize version; kubeconform -v
k6 version
py -3.12 --version      # only if installed in §5
node --version          # 22.x only if aligned in §5
```

Paste the outputs into the PR of the phase that first needs them (Phase 08 for Docker, Phase 09 for the rest).

## 7. Windows notes

- Line endings: `.gitattributes` forces LF; do not override it with editor settings that write CRLF into Dockerfiles or shell scripts.
- Use Git Bash (or WSL) for the POSIX scripts in the assignment (`vpa-up.sh`, curl loops); PowerShell for `winget`/`gh`.
- Keep the repository on `C:` (not on a network or synced drive) so bind mounts and file watchers behave.
