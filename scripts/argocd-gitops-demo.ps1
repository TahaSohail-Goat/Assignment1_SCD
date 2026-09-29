<#
Installs pinned local-demo Argo CD and applies CivicPulse's declarative Application.

Run after `scripts/k8s-up.sh` has created the `kind-civicpulse` cluster and its out-of-band
Secret. The public repository is the source of application manifests; this script never reads or
writes a secret value. It leaves the cluster running for inspection. Remove it with:
  kind delete cluster --name civicpulse
#>
[CmdletBinding()]
param(
    [string]$Context = 'kind-civicpulse',
    [string]$ArgoCdVersion = 'v3.5.3'
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

function Invoke-Kubectl {
    param([Parameter(Mandatory)][string[]]$CmdArgs)
    & kubectl --context $Context @CmdArgs
    if ($LASTEXITCODE -ne 0) { throw "kubectl failed: $($CmdArgs -join ' ')" }
}

Invoke-Kubectl -CmdArgs @('cluster-info')
Invoke-Kubectl -CmdArgs @('-n', 'civicpulse', 'get', 'secret', 'civicpulse-secrets')

Invoke-Kubectl -CmdArgs @('create', 'namespace', 'argocd', '--dry-run=client', '-o', 'yaml') | kubectl --context $Context apply -f -
if ($LASTEXITCODE -ne 0) { throw 'Could not create the argocd namespace' }

$manifest = "https://raw.githubusercontent.com/argoproj/argo-cd/$ArgoCdVersion/manifests/install.yaml"
Invoke-Kubectl -CmdArgs @('-n', 'argocd', 'apply', '--server-side', '--force-conflicts', '-f', $manifest)
Invoke-Kubectl -CmdArgs @('-n', 'argocd', 'rollout', 'status', 'deployment/argocd-repo-server', '--timeout=300s')
Invoke-Kubectl -CmdArgs @('-n', 'argocd', 'rollout', 'status', 'deployment/argocd-server', '--timeout=300s')

Invoke-Kubectl -CmdArgs @('apply', '-f', 'gitops/argocd/civicpulse-application.yaml')
$deadline = (Get-Date).AddMinutes(5)
do {
    $application = Invoke-Kubectl -CmdArgs @('-n', 'argocd', 'get', 'application', 'civicpulse', '-o', 'json') | ConvertFrom-Json
    $sync = $application.status.sync.status
    $health = $application.status.health.status
    Write-Host "CivicPulse Application: sync=$sync health=$health"
    if ($sync -eq 'Synced' -and $health -eq 'Healthy') { break }
    Start-Sleep -Seconds 5
} while ((Get-Date) -lt $deadline)

if ($sync -ne 'Synced' -or $health -ne 'Healthy') {
    throw "Argo CD did not reach Synced/Healthy within five minutes (sync=$sync health=$health)"
}

Invoke-Kubectl -CmdArgs @('-n', 'argocd', 'get', 'application', 'civicpulse')
Invoke-Kubectl -CmdArgs @('-n', 'civicpulse', 'get', 'deployments,pods')
Write-Host 'Ready. Evidence: kubectl --context kind-civicpulse -n argocd get application civicpulse -o yaml'
