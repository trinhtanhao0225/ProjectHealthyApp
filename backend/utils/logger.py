# backend/utils/logger.py
"""
Module logger chung cho toàn bộ project.
- Sử dụng logging chuẩn Python
- Format đẹp, có timestamp, level, module name
- Hỗ trợ cả console và file (nếu cần sau này)
- Dễ import và dùng ở mọi nơi: from .logger import logger
"""

import logging
import sys
from pathlib import Path

# Tạo logger chính cho project
logger = logging.getLogger("nutrition-app")  # tên logger chung cho toàn app
logger.setLevel(logging.DEBUG)  # mức debug để log chi tiết trong dev

# Handler cho console (stdout/stderr)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  # chỉ log INFO trở lên ra console

# Formatter đẹp mắt
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# (Tùy chọn) Log ra file nếu muốn lưu lịch sử
# log_file = Path(__file__).parent.parent / "logs" / "app.log"
# file_handler = logging.FileHandler(log_file)
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# Hàm helper để log nhanh (nếu bạn thích dùng log() thay logger.info())
def log(message: str, level: str = "info"):
    """
    Helper để log nhanh:
    log("Hello") → logger.info("Hello")
    log("Error here", "error") → logger.error("Error here")
    """
    level = level.lower()
    if level == "debug":
        logger.debug(message)
    elif level == "info":
        logger.info(message)
    elif level == "warning" or level == "warn":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "critical":
        logger.critical(message)
    else:
        logger.info(message)

# Để tránh duplicate log khi import nhiều lần
logger.propagate = False

# Test khi chạy trực tiếp file này
if __name__ == "__main__":
    logger.debug("This is debug message")
    logger.info("This is info message")
    logger.warning("This is warning")
    logger.error("This is error message")
    log("Hello from helper", "info")