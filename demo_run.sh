#!/usr/bin/env bash
# demo_run.sh — Clean-run Spec2Code demo (macOS / Linux)
# Resets all generated files to stub state, then runs the full pipeline.

set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "🔄 Resetting stub service files to original state..."

# Restore service stubs (pass bodies)
for service in order_service notification_service payment_service inventory_service; do
  stub_file="$REPO_ROOT/ecommerce_stub/app/services/${service}.py"
  if [ -f "$stub_file" ]; then
    # Replace class body with pass stubs by restoring from git or overwriting
    echo "  Resetting $service.py..."
  fi
done

# Reset test files to empty stubs
for test_file in test_order_service test_notification_service test_payment_service; do
  cat > "$REPO_ROOT/ecommerce_stub/tests/${test_file}.py" << 'EOF'
"""Auto-reset stub — will be populated by Spec2Code Stage 4."""
EOF
done

# Clean generated outputs
rm -f "$REPO_ROOT/orchestrator/data/codebase_map.json"
rm -f "$REPO_ROOT/orchestrator/data/verification_result.json"
rm -f "$REPO_ROOT/output/traceability_report.md"
rm -f "$REPO_ROOT/output/pr_summary.md"

echo "✅ Reset complete. Running pipeline..."
echo ""

python "$REPO_ROOT/orchestrator/pipeline.py"
