import os
import configparser
from pathlib import Path

def load_env(env_path: str = ".env") -> None:
    """Завантажує змінні середовища з файлу .env."""

    path = Path(env_path)

    if not path.exists():
        return

    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, _, value = line.partition("=")

                os.environ.setdefault(
                    key.strip(),
                    value.strip()
                )

def load_config(
    config_path: str = "config.ini"
) -> configparser.ConfigParser:
    """Завантажує налаштування з config.ini."""

    config = configparser.ConfigParser()

    config.read(config_path, encoding="utf-8")

    return config
def get_settings() -> dict:
    """Повертає всі налаштування застосунку."""

    load_env()
    config = load_config()

    return {
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "base_currency": os.getenv("BASE_CURRENCY", "UAH"),
        "exchange_api_key": os.getenv("EXCHANGE_API_KEY", ""),

        "data_file": config.get(
            "storage",
            "data_file",
            fallback="data/transactions.json"
        ),

        "budget_file": config.get(
            "storage",
            "budget_file",
            fallback="data/budgets.json"
        ),

        "export_dir": config.get(
            "storage",
            "export_dir",
            fallback="exports/"
        ),

        "app_name": config.get(
            "app",
            "name",
            fallback="Expense Tracker"
        ),

        "app_version": config.get(
            "app",
            "version",
            fallback="0.3.0"
        ),

        "warn_budget_pct": config.getfloat(
            "limits",
            "warn_budget_pct",
            fallback=80.0
        ),
    }
