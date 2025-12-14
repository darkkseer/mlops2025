# src/logger.py

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

# ANSI 
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"

class ColoredFormatter(logging.Formatter):
    def __init__(self, use_colors: bool = True):
        super().__init__()
        self.use_colors = use_colors

    def format(self, record):
        log_msg = super().format(record)
        level = record.levelname
        if not self.use_colors:
            return log_msg
        if level == "INFO":
            return f"{Colors.GREEN}{log_msg}{Colors.RESET}"
        elif level == "WARNING":
            return f"{Colors.YELLOW}{log_msg}{Colors.RESET}"
        elif level == "ERROR" or level == "CRITICAL":
            return f"{Colors.RED}{log_msg}{Colors.RESET}"
        return log_msg

class MonitoringLogger:
    def __init__(self, log_file: str, metrics_file: str, console_colors: bool = True):
        self.log_file = Path(log_file)
        self.metrics_file = Path(metrics_file)
        self.console_colors = console_colors

        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger("monitoring")
        self.logger.setLevel(logging.INFO)

        if self.logger.handlers:
            self.logger.handlers.clear()

        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(use_colors=console_colors)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        file_formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def log(self, level: str, message: str, extra: Dict[str, Any] = None):
        getattr(self.logger, level.lower())(message)

    def log_metrics(self, metrics: Dict[str, Any]):
        with open(self.metrics_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(metrics, ensure_ascii=False) + "\n")

    def alert(self, level: str, message: str):
        color_map = {"green": "INFO", "yellow": "WARNING", "red": "ERROR"}
        self.log(color_map[level], f"🔴🔴 ALERT ({level.upper()}): {message}")