from pathlib import Path

# Agent faqat shu papkalarda ishlaydi (xavfsizlik uchun)
ALLOWED_FOLDERS = [
    str(Path.home() / "Documents"),
    str(Path.home() / "Desktop"),
    str(Path.home() / "Downloads"),
]

# O'qilishi taqiqlangan xavfli fayl turlari
BLOCKED_EXTENSIONS = {
    ".exe",
    ".bat",
    ".cmd",
    ".ps1",
    ".msi",
    ".dll",
    ".sys",
    ".scr",
}

# O'qiladigan faylning maksimal hajmi: 8 MB
MAX_FILE_SIZE = 8 * 1024 * 1024

# Ruxsat berilgan buyruqlar (faqat bu buyruqlarni bajarishi mumkin)
ALLOWED_COMMANDS = {
    "dir": "Papkadagi fayllarni ko'rsatish",
    "copy": "Faylni ko'chirish",
    "del": "Faylni o'chirish",
    "mkdir": "Papka yaratish",
    "type": "Faylni o'qish",
    "tasklist": "Jarayonlarni ko'rsatish",
    "systeminfo": "Kompyuter haqida ma'lumot",
    "ipconfig": "Tarmoq sozlamalari",
}

# Log fayli
LOG_FILE = "agent_operations.log"
