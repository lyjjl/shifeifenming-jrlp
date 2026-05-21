#!/usr/bin/env bash
# ============================================================
# build.sh - jrlp-sealdice-plugin 打包脚本
# 编译 TypeScript 插件并打包后端文件
#
# 用法:
#   ./build.sh                              # → dist/jrlp-build.zip (不含图片)
#   ./build.sh dist foo.zip                 # → 自定义路径/文件名
#   ./build.sh dist foo.zip withimg         # → 包含 backend/img/
#   ./build.sh --dir output                 # → 直接输出到 output/ 目录 (不打包)
#   ./build.sh --dir output withimg         # → 输出到目录 (含图片)
# ============================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

# ---- 解析参数 ----
MODE="zip" # zip 或 dir
OUTPUT_DIR=""
ZIP_NAME=""
INCLUDE_IMG=""

if [ "${1:-}" = "--dir" ]; then
	MODE="dir"
	OUTPUT_DIR="${2:-dist}"
	INCLUDE_IMG="${3:-}"
else
	OUTPUT_DIR="${1:-dist}"
	ZIP_NAME="${2:-jrlp-build.zip}"
	INCLUDE_IMG="${3:-}"
fi

# ---- 1. 安装依赖并编译 JS 插件 ----
echo "==> Installing dependencies..."
pnpm install --frozen-lockfile

echo "==> Building JS plugin (dist/jrlp.js)..."
pnpm run build

# ---- 2. 暂存需要打包的文件 ----
STAGING_DIR="$(mktemp -d)"
trap 'rm -rf "$STAGING_DIR"' EXIT

echo "==> Staging files..."

# 编译产物
cp dist/jrlp.js "$STAGING_DIR/"

# 后端代码（排除虚拟环境和缓存）
mkdir -p "$STAGING_DIR/backend"
cp backend/main.py "$STAGING_DIR/backend/"
cp backend/pyproject.toml "$STAGING_DIR/backend/"
cp backend/uv.lock "$STAGING_DIR/backend/"

# 可选文件（不存在时静默跳过）
cp backend/favicon.ico "$STAGING_DIR/backend/" 2>/dev/null || true
cp backend/imageDownloader.py "$STAGING_DIR/backend/" 2>/dev/null || true
cp backend/rename.py "$STAGING_DIR/backend/" 2>/dev/null || true

# 角色图片目录（仅在明确要求时包含）
if [ "$INCLUDE_IMG" = "withimg" ]; then
	echo "==> Including backend/img/..."
	cp -r backend/img "$STAGING_DIR/backend/"
else
	echo "==> Skipping backend/img/ (use 'withimg' to include)"
fi

# ---- 3. 输出 ----
if [ "$MODE" = "dir" ]; then
	mkdir -p "$OUTPUT_DIR"
	rm -rf "${OUTPUT_DIR:?}/"*
	cp -r "$STAGING_DIR"/* "$OUTPUT_DIR/"
	echo "==> Done: files staged in $OUTPUT_DIR/"
else
	mkdir -p "$OUTPUT_DIR"
	rm -f "$OUTPUT_DIR/$ZIP_NAME"
	echo "==> Creating archive: $OUTPUT_DIR/$ZIP_NAME"
	(cd "$STAGING_DIR" && zip -r "$ROOT_DIR/$OUTPUT_DIR/$ZIP_NAME" .)
	echo "==> Done: $(du -sh "$OUTPUT_DIR/$ZIP_NAME" | cut -f1)  $OUTPUT_DIR/$ZIP_NAME"
fi
