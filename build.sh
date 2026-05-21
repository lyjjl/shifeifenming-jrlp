#!/usr/bin/env bash
# ============================================================
# build.sh - jrlp-sealdice-plugin 打包脚本
# 编译 TypeScript 插件并打包后端文件到一个 zip 压缩包
#
# 用法:
#   ./build.sh                      # 默认: dist/jrlp-build.zip (不含图片)
#   ./build.sh dist foo.zip         # 指定路径和文件名
#   ./build.sh dist foo.zip withimg # 包含 backend/img/
#
# 默认:
#   output-dir: dist
#   zip-name:   jrlp-build.zip
#   第三个参数:  省略或任意值=不含图片, withimg=包含图片
# ============================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="${1:-dist}"
ZIP_NAME="${2:-jrlp-build.zip}"
INCLUDE_IMG="${3:-}" # 设为 "withimg" 则包含图片

cd "$ROOT_DIR"

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
	echo "==> Skipping backend/img/ (use 'withimg' as 3rd arg to include)"
fi

# ---- 3. 打包为 zip ----
echo "==> Creating archive: $OUTPUT_DIR/$ZIP_NAME"
mkdir -p "$OUTPUT_DIR"
rm -f "$OUTPUT_DIR/$ZIP_NAME"

(cd "$STAGING_DIR" && zip -r "$ROOT_DIR/$OUTPUT_DIR/$ZIP_NAME" .)

echo "==> Done: $(du -sh "$OUTPUT_DIR/$ZIP_NAME" | cut -f1)  $OUTPUT_DIR/$ZIP_NAME"
