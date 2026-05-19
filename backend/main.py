import asyncio
import base64
import os
import random
import sys
import urllib.parse
from contextlib import asynccontextmanager
from pathlib import Path

import psutil
import uvicorn
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "img"
FAVICON_PATH = BASE_DIR / "favicon.ico"

VALID_EXTENSIONS = frozenset((".png", ".jpg", ".jpeg", ".gif", ".webp"))
MAX_RETRY = 3
CACHE_REFRESH_INTERVAL = 60

cached_image_paths: list[str] = []
access_counts = {"/api/v1/character/random": 0, "/api/v1/status": 0}
debug_mode = False


def debug_log(message: str) -> None:
    if debug_mode:
        print(f"[DEBUG] {message}", file=sys.stderr)


def refresh_image_cache() -> None:
    global cached_image_paths
    temp_list: list[str] = []
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    for root, _dirs, files in os.walk(IMAGE_DIR):
        for f in files:
            if f.lower().endswith(tuple(VALID_EXTENSIONS)):
                rel_path = os.path.relpath(os.path.join(root, f), IMAGE_DIR)
                temp_list.append(rel_path)
    cached_image_paths = temp_list
    debug_log(f"缓存已刷新，共加载 {len(cached_image_paths)} 张图片")


async def periodic_cache_refresh() -> None:
    while True:
        await asyncio.sleep(CACHE_REFRESH_INTERVAL)
        await asyncio.to_thread(refresh_image_cache)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await asyncio.to_thread(refresh_image_cache)
    task = asyncio.create_task(periodic_cache_refresh())
    yield
    task.cancel()
    debug_log("服务器正在关闭...")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/img", StaticFiles(directory=str(IMAGE_DIR)), name="images")


def select_accessible_image() -> tuple[str, Path]:
    """从缓存中选择一个可访问的图片，最多重试 MAX_RETRY 次"""
    for _ in range(MAX_RETRY):
        if not cached_image_paths:
            refresh_image_cache()
        if not cached_image_paths:
            break
        selected = random.choice(cached_image_paths)
        full_path = IMAGE_DIR / selected
        if full_path.is_file():
            return selected, full_path
        cached_image_paths.remove(selected)
    raise HTTPException(status_code=404, detail="没有可访问的图片")


@app.get("/api/v1/character/random")
async def get_random_character_data(image_format: str = "url"):
    access_counts["/api/v1/character/random"] += 1

    selected_rel_path, full_path = await asyncio.to_thread(select_accessible_image)

    file_name_without_extension = full_path.stem
    path_with_slashes = selected_rel_path.replace(os.sep, "/")
    encoded_sub_path = urllib.parse.quote(path_with_slashes)
    image_sub = f"/img/{encoded_sub_path}"

    debug_log(f"选中图片: {selected_rel_path} -> 编码后路径: {image_sub}")

    result: dict = {
        "filename": file_name_without_extension,
        "image_sub": image_sub,
    }

    if image_format == "base64":
        raw = await asyncio.to_thread(full_path.read_bytes)
        result["image_base64"] = base64.b64encode(raw).decode("utf-8")

    return result


@app.get("/api/v1/status")
async def get_system_status():
    access_counts["/api/v1/status"] += 1
    cpu_usage = psutil.cpu_percent(interval=0)
    mem = psutil.virtual_memory()
    return {
        "service_availability": "Available",
        "system_metrics": {
            "cpu_usage_percent": cpu_usage,
            "memory_usage": {
                "total_gb": round(mem.total / (1024**3), 2),
                "used_gb": round(mem.used / (1024**3), 2),
                "percent": mem.percent,
            },
        },
        "image_statistics": {"total_count": len(cached_image_paths)},
        "access_statistics": access_counts,
    }


@app.get("/")
async def root():
    return {"message": "欢迎！"}


@app.get("/favicon.ico")
async def favicon():
    if FAVICON_PATH.is_file():
        return FileResponse(str(FAVICON_PATH))
    return Response(status_code=204)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="JRLP 后端服务")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="绑定主机地址")
    parser.add_argument("--port", type=int, default=18428, help="绑定端口号")
    parser.add_argument("--debug", action="store_true", help="开启调试输出")

    args = parser.parse_args()
    if args.debug:
        debug_mode = True
        print("[INFO] 调试模式已开启")

    uvicorn.run("main:app", host=args.host, port=args.port, reload=args.debug)
