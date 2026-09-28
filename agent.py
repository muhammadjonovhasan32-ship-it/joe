import os
import shutil
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from config import ALLOWED_FOLDERS, BLOCKED_EXTENSIONS, MAX_FILE_SIZE


class WindowsAgent:
    """Windows kompyuter bilan xavfsiz ishlash uchun agent."""

    def __init__(self):
        self.log_file = Path("agent_log.json")
        self.load_log()

    def load_log(self) -> None:
        """Audit log'ni yuklash."""
        if self.log_file.exists():
            with open(self.log_file, "r", encoding="utf-8") as f:
                self.log = json.load(f)
        else:
            self.log = []

    def save_log(self) -> None:
        """Audit log'ni saqlash."""
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(self.log, f, ensure_ascii=False, indent=2)

    def log_action(self, action: str, details: dict) -> None:
        """Harakatni qayd qilish."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
        }
        self.log.append(entry)
        self.save_log()

    def is_path_allowed(self, path: str) -> bool:
        """Papkani tekshirish — ruxsat berilganmi?"""
        path_obj = Path(path).resolve()
        for allowed in ALLOWED_FOLDERS:
            try:
                path_obj.relative_to(Path(allowed).resolve())
                return True
            except ValueError:
                continue
        return False

    def list_files(self, folder: str) -> dict:
        """Papkadagi fayllarni ko'rsatish."""
        if not self.is_path_allowed(folder):
            return {"error": f"Ruxsat yo'q: {folder}"}

        try:
            folder_path = Path(folder)
            files = []
            for item in folder_path.iterdir():
                files.append({
                    "name": item.name,
                    "type": "folder" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None,
                })
            self.log_action("list_files", {"folder": folder, "count": len(files)})
            return {"files": files}
        except Exception as e:
            return {"error": str(e)}

    def read_file(self, file_path: str) -> dict:
        """Faylni o'qish (faqat text)."""
        if not self.is_path_allowed(file_path):
            return {"error": f"Ruxsat yo'q: {file_path}"}

        try:
            path = Path(file_path)
            
            # Fayl kattamasini tekshirish
            if path.stat().st_size > MAX_FILE_SIZE:
                return {"error": f"Fayl juda katta (max {MAX_FILE_SIZE} bytes)"}
            
            # Kengaytmani tekshirish
            if path.suffix in BLOCKED_EXTENSIONS:
                return {"error": f"Bu fayl turi blokirovka qilingan: {path.suffix}"}

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            self.log_action("read_file", {"file": file_path, "size": len(content)})
            return {"content": content}
        except Exception as e:
            return {"error": str(e)}

    def create_folder(self, folder_path: str) -> dict:
        """Papka yaratish."""
        if not self.is_path_allowed(folder_path):
            return {"error": f"Ruxsat yo'q: {folder_path}"}

        try:
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            self.log_action("create_folder", {"folder": folder_path})
            return {"success": True, "message": f"Papka yaratildi: {folder_path}"}
        except Exception as e:
            return {"error": str(e)}

    def delete_file(self, file_path: str) -> dict:
        """Faylni o'chirish (tasdiq kerak)."""
        if not self.is_path_allowed(file_path):
            return {"error": f"Ruxsat yo'q: {file_path}"}

        try:
            Path(file_path).unlink()
            self.log_action("delete_file", {"file": file_path})
            return {"success": True, "message": f"Fayl o'chirildi: {file_path}"}
        except Exception as e:
            return {"error": str(e)}

    def copy_file(self, src: str, dst: str) -> dict:
        """Faylni ko'chirish."""
        if not self.is_path_allowed(src) or not self.is_path_allowed(dst):
            return {"error": "Ruxsat yo'q"}

        try:
            shutil.copy2(src, dst)
            self.log_action("copy_file", {"src": src, "dst": dst})
            return {"success": True, "message": f"Fayl ko'chirildi: {src} -> {dst}"}
        except Exception as e:
            return {"error": str(e)}

    def run_command(self, command: str, timeout: int = 10) -> dict:
        """CMD buyrug'ini bajarish."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            self.log_action("run_command", {"command": command})
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"error": "Buyruq vaqti tugadi"}
        except Exception as e:
            return {"error": str(e)}

    def search_files(self, folder: str, pattern: str) -> dict:
        """Fayllarni izlash."""
        if not self.is_path_allowed(folder):
            return {"error": f"Ruxsat yo'q: {folder}"}

        try:
            folder_path = Path(folder)
            results = []
            for file in folder_path.rglob(pattern):
                results.append(str(file))
            
            self.log_action("search_files", {"folder": folder, "pattern": pattern, "count": len(results)})
            return {"results": results}
        except Exception as e:
            return {"error": str(e)}

    def get_system_info(self) -> dict:
        """Kompyuter haqida ma'lumot."""
        try:
            result = subprocess.run(
                "systeminfo",
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.log_action("get_system_info", {})
            return {"info": result.stdout}
        except Exception as e:
            return {"error": str(e)}
