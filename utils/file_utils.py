#!/usr/bin/env python3
"""
File utilities for Mail Organizer
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

def ensure_directory(path: Path) -> bool:
    """Ensure a directory exists, create if it doesn't"""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False

def backup_file(file_path: Path, backup_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Create a backup of a file
    
    Args:
        file_path: Path to the file to backup
        backup_dir: Directory to store backup (defaults to file's parent/.backup)
        
    Returns:
        Path to backup file or None if failed
    """
    if not file_path.exists():
        return None
    
    if backup_dir is None:
        backup_dir = file_path.parent / '.backup'
    
    ensure_directory(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
    backup_path = backup_dir / backup_name
    
    try:
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception:
        return None

def save_report(data: dict, filename: str, output_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Save a report to file
    
    Args:
        data: Data to save
        filename: Name of the file
        output_dir: Directory to save to (defaults to Desktop)
        
    Returns:
        Path to saved file or None if failed
    """
    if output_dir is None:
        output_dir = Path.home() / 'Desktop'
    
    ensure_directory(output_dir)
    
    file_path = output_dir / filename
    
    try:
        if filename.endswith('.json'):
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        else:
            with open(file_path, 'w') as f:
                if isinstance(data, dict):
                    for key, value in data.items():
                        f.write(f"{key}: {value}\n")
                else:
                    f.write(str(data))
        
        return file_path
    except Exception:
        return None

def get_file_size_mb(file_path: Path) -> float:
    """Get file size in MB"""
    try:
        return file_path.stat().st_size / (1024 * 1024)
    except Exception:
        return 0.0

def cleanup_old_logs(log_dir: Path, days_to_keep: int = 30) -> int:
    """
    Clean up old log files
    
    Args:
        log_dir: Directory containing log files
        days_to_keep: Number of days to keep logs
        
    Returns:
        Number of files deleted
    """
    if not log_dir.exists():
        return 0
    
    deleted_count = 0
    cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
    
    for log_file in log_dir.glob('*.log'):
        try:
            if log_file.stat().st_mtime < cutoff_time:
                log_file.unlink()
                deleted_count += 1
        except Exception:
            continue
    
    return deleted_count
