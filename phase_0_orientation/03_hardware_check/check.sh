#!/usr/bin/env bash
# Phase 0 hardware readiness check — read-only, no installs, no side effects.
# Usage: bash check.sh
set -u

pass() { printf "  \033[32mOK\033[0m   %s\n" "$1"; }
warn() { printf "  \033[33mWARN\033[0m %s\n" "$1"; }
fail() { printf "  \033[31mFAIL\033[0m %s\n" "$1"; }

echo "=== Phase 0 hardware check ==="
echo

# --- 1. Physical RAM ---
echo "1. Physical RAM"
RAM_GB=0
case "$(uname -s)" in
  Darwin)
    RAM_BYTES=$(sysctl -n hw.memsize 2>/dev/null || echo 0)
    RAM_GB=$(( RAM_BYTES / 1024 / 1024 / 1024 ))
    ;;
  Linux)
    RAM_KB=$(awk '/MemTotal/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)
    RAM_GB=$(( RAM_KB / 1024 / 1024 ))
    ;;
  *)
    warn "Unknown OS $(uname -s) — cannot detect RAM automatically"
    ;;
esac
if [ "$RAM_GB" -ge 16 ]; then pass "${RAM_GB} GB — comfortable for full profile"
elif [ "$RAM_GB" -ge 12 ]; then pass "${RAM_GB} GB — full profile OK if nothing else is running"
elif [ "$RAM_GB" -ge 8 ]; then warn "${RAM_GB} GB — light profile only"
else fail "${RAM_GB} GB — cloud fallback required"
fi
echo

# --- 2. Free disk on CWD ---
echo "2. Free disk (current partition)"
if command -v df >/dev/null 2>&1; then
  FREE_GB=$(df -Pk . 2>/dev/null | awk 'NR==2 {printf "%d", $4/1024/1024}')
  if [ "${FREE_GB:-0}" -ge 30 ]; then pass "${FREE_GB} GB free"
  elif [ "${FREE_GB:-0}" -ge 15 ]; then warn "${FREE_GB} GB free — enough for one profile, tight"
  else fail "${FREE_GB:-0} GB free — need 15+ GB for Phase 3 images"
  fi
else
  warn "df not available"
fi
echo

# --- 3. Docker CLI ---
echo "3. Docker CLI"
if command -v docker >/dev/null 2>&1; then
  pass "$(docker --version)"
else
  fail "docker not found — install Docker Desktop or Docker Engine"
  echo
  echo "VERDICT: CLOUD_FALLBACK (no Docker)"
  exit 1
fi
echo

# --- 4. Docker daemon ---
echo "4. Docker daemon"
if docker info >/dev/null 2>&1; then
  pass "daemon responsive"
else
  fail "daemon not reachable — start Docker Desktop or 'sudo systemctl start docker'"
  echo
  echo "VERDICT: install-blocked (Docker installed but not running)"
  exit 1
fi
echo

# --- 5. Docker memory allocation ---
echo "5. Docker memory pool"
DOCKER_MEM_BYTES=$(docker info --format '{{.MemTotal}}' 2>/dev/null || echo 0)
DOCKER_MEM_GB=$(( DOCKER_MEM_BYTES / 1024 / 1024 / 1024 ))
if [ "$DOCKER_MEM_GB" -ge 12 ]; then pass "${DOCKER_MEM_GB} GB — full profile OK"
elif [ "$DOCKER_MEM_GB" -ge 6 ]; then warn "${DOCKER_MEM_GB} GB — light profile OK; raise to 12+ for full"
else fail "${DOCKER_MEM_GB} GB — too low; raise in Docker Desktop → Settings → Resources"
fi
echo

# --- 6. Compose v2 ---
echo "6. Docker Compose v2"
if docker compose version >/dev/null 2>&1; then
  pass "$(docker compose version --short 2>/dev/null || docker compose version)"
else
  fail "Compose v2 not found — install the plugin or use Docker Desktop"
fi
echo

# --- Verdict ---
echo "=== Verdict ==="
if [ "$RAM_GB" -ge 12 ] && [ "$DOCKER_MEM_GB" -ge 12 ] && [ "${FREE_GB:-0}" -ge 30 ]; then
  echo "FULL — run Phase 3 full profile"
elif [ "$RAM_GB" -ge 8 ] && [ "$DOCKER_MEM_GB" -ge 6 ] && [ "${FREE_GB:-0}" -ge 15 ]; then
  echo "LIGHT — run Phase 3 light profile"
else
  echo "CLOUD_FALLBACK — see ../04_cloud_fallback/"
fi
