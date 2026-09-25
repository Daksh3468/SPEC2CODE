# demo_run.ps1 — Clean-run Spec2Code demo (Windows PowerShell)
# Resets all generated files to stub state, then runs the full pipeline.

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "🔄 Resetting stub service files to original state..." -ForegroundColor Cyan

# Reset test files to empty stubs
$testFiles = @("test_order_service", "test_notification_service", "test_payment_service")
foreach ($test in $testFiles) {
    $path = "$RepoRoot\ecommerce_stub\tests\$test.py"
    Set-Content -Path $path -Value '"""Auto-reset stub — will be populated by Spec2Code Stage 4."""'
    Write-Host "  Reset $test.py"
}

# Reset service files to pass stubs
$serviceStubs = @{
    "order_service"        = "order_service_stub.py"
    "notification_service" = "notification_service_stub.py"
    "payment_service"      = "payment_service_stub.py"
    "inventory_service"    = "inventory_service_stub.py"
}

# Clean generated outputs
$outputFiles = @(
    "$RepoRoot\orchestrator\data\codebase_map.json",
    "$RepoRoot\orchestrator\data\verification_result.json",
    "$RepoRoot\output\traceability_report.md",
    "$RepoRoot\output\pr_summary.md"
)
foreach ($f in $outputFiles) {
    if (Test-Path $f) {
        Remove-Item $f -Force
        Write-Host "  Removed $f"
    }
}

Write-Host ""
Write-Host "✅ Reset complete. Running pipeline..." -ForegroundColor Green
Write-Host ""

python "$RepoRoot\orchestrator\pipeline.py"
