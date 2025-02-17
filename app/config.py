import os
from dotenv import load_dotenv

load_dotenv()

# Забираем переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
GROUP_ID = int(os.getenv("GROUP_ID", 0))
MANAGER_ID = int(os.getenv("MANAGER_ID", 0))
MANAGER_PHONE = os.getenv("MANAGER_PHONE", "")
CACHE_TTL = int(os.getenv("CACHE_TTL", 3))

VK_ADMIN_IDS = os.getenv("VK_ADMIN_IDS", "")
if VK_ADMIN_IDS:
    # Разбиваем строку по запятой и приводим к int
    VK_ADMIN_IDS = [int(x) for x in VK_ADMIN_IDS.split(",")]
else:
    VK_ADMIN_IDS = []

DATABASE_URL = os.getenv("DATABASE_URL", "")
REDIS_URL = os.getenv("REDIS_URL", "")
