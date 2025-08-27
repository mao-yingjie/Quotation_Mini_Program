#!/usr/bin/env bash
set -e
command -v tectonic >/dev/null 2>&1 || { echo 'WARNING: tectonic not found. Install via zypper'; }
command -v pandoc >/dev/null 2>&1 || { echo 'WARNING: pandoc not found. Install via zypper'; }
echo 'Checks done.'
