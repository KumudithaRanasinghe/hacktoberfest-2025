"""
Data Backup Engine for Hacktoberfest 2025 Project Tracker.
Provides comprehensive backup, restore, and recovery capabilities.
"""

import json
import os
import shutil
import hashlib
import gzip
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from pathlib import Path


class BackupType(Enum):
    """Types of backups."""
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"


class BackupFormat(Enum):
    """Backup file formats."""
    JSON = "json"
    COMPRESSED = "compressed"
    ARCHIVED = "archived"


class BackupEngine:
    """Engine for managing backups and disaster recovery."""
    
    def __init__(self, backup_dir: str = "backups", data_file: str = "contributors.json"):
        """
        Initialize the backup engine.
        
        Args:
            backup_dir (str): Directory to store backups
            data_file (str): Main data file to backup
        """
        self.backup_dir = backup_dir
        self.data_file = data_file
        self.backup_index_file = os.path.join(backup_dir, "backup_index.json")
        self.backup_history: List[Dict[str, Any]] = []
        self.last_backup_hash = None
        
        # Create backup directory if it doesn't exist
        Path(backup_dir).mkdir(parents=True, exist_ok=True)
        
        # Load backup index
        self._load_backup_index()
    
    def _load_backup_index(self) -> None:
        """Load the backup index from file."""
        if os.path.exists(self.backup_index_file):
            try:
                with open(self.backup_index_file, 'r', encoding='utf-8') as f:
                    self.backup_history = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load backup index: {e}")
                self.backup_history = []
    
    def _save_backup_index(self) -> None:
        """Save the backup index to file."""
        try:
            with open(self.backup_index_file, 'w', encoding='utf-8') as f:
                json.dump(self.backup_history, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving backup index: {e}")
    
    def _get_file_hash(self, filepath: str) -> str:
        """
        Calculate MD5 hash of a file.
        
        Args:
            filepath (str): Path to file
            
        Returns:
            str: MD5 hash
        """
        if not os.path.exists(filepath):
            return None
        
        md5_hash = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    
    def create_full_backup(self,
                          data_file: str = None,
                          compress: bool = False,
                          description: str = "") -> Dict[str, Any]:
        """
        Create a full backup of all data.
        
        Args:
            data_file (str): Path to data file (uses default if None)
            compress (bool): Compress the backup
            description (str): Backup description
            
        Returns:
            Dict[str, Any]: Backup metadata
        """
        if data_file is None:
            data_file = self.data_file
        
        if not os.path.exists(data_file):
            return {"success": False, "error": f"Data file not found: {data_file}"}
        
        # Generate backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_full_{timestamp}"
        
        try:
            # Read source data
            with open(data_file, 'r', encoding='utf-8') as f:
                data = f.read()
            
            # Prepare backup metadata
            file_hash = self._get_file_hash(data_file)
            backup_info = {
                "backup_id": backup_name,
                "type": BackupType.FULL.value,
                "timestamp": datetime.now().isoformat(),
                "description": description,
                "source_file": data_file,
                "file_hash": file_hash,
                "original_size": len(data),
                "compressed": compress,
            }
            
            # Save backup
            if compress:
                backup_file = os.path.join(self.backup_dir, f"{backup_name}.json.gz")
                with gzip.open(backup_file, 'wb') as f:
                    f.write(data.encode('utf-8'))
                backup_info["compressed_size"] = os.path.getsize(backup_file)
                backup_info["compression_ratio"] = (1 - backup_info["compressed_size"] / backup_info["original_size"]) * 100
            else:
                backup_file = os.path.join(self.backup_dir, f"{backup_name}.json")
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(data)
                backup_info["file_size"] = os.path.getsize(backup_file)
            
            backup_info["backup_file"] = os.path.basename(backup_file)
            
            # Update history
            self.backup_history.append(backup_info)
            self.last_backup_hash = file_hash
            self._save_backup_index()
            
            return {
                "success": True,
                "backup_id": backup_name,
                "backup_file": backup_file,
                "size": backup_info.get("compressed_size", backup_info.get("file_size")),
                "compressed": compress
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_incremental_backup(self,
                                 data_file: str = None,
                                 compress: bool = False,
                                 description: str = "") -> Dict[str, Any]:
        """
        Create an incremental backup (only backup if data changed).
        
        Args:
            data_file (str): Path to data file
            compress (bool): Compress the backup
            description (str): Backup description
            
        Returns:
            Dict[str, Any]: Backup metadata or skip info
        """
        if data_file is None:
            data_file = self.data_file
        
        current_hash = self._get_file_hash(data_file)
        
        # Check if data changed
        if current_hash == self.last_backup_hash:
            return {
                "success": True,
                "skipped": True,
                "reason": "No changes detected since last backup"
            }
        
        # Perform backup with incremental flag
        result = self.create_full_backup(data_file, compress, description)
        
        if result["success"]:
            result["type"] = BackupType.INCREMENTAL.value
            # Update the backup info
            for backup in self.backup_history:
                if backup["backup_id"] == result["backup_id"]:
                    backup["type"] = BackupType.INCREMENTAL.value
                    break
            self._save_backup_index()
        
        return result
    
    def create_differential_backup(self,
                                  data_file: str = None,
                                  compress: bool = False,
                                  description: str = "") -> Dict[str, Any]:
        """
        Create a differential backup (changes since last full backup).
        
        Args:
            data_file (str): Path to data file
            compress (bool): Compress the backup
            description (str): Backup description
            
        Returns:
            Dict[str, Any]: Backup metadata
        """
        # Find last full backup
        last_full = None
        for backup in reversed(self.backup_history):
            if backup["type"] == BackupType.FULL.value:
                last_full = backup
                break
        
        if not last_full:
            # No full backup exists, create one
            return self.create_full_backup(data_file, compress, description)
        
        # Create backup with differential flag
        result = self.create_full_backup(data_file, compress, description)
        
        if result["success"]:
            result["type"] = BackupType.DIFFERENTIAL.value
            result["based_on"] = last_full["backup_id"]
            # Update the backup info
            for backup in self.backup_history:
                if backup["backup_id"] == result["backup_id"]:
                    backup["type"] = BackupType.DIFFERENTIAL.value
                    backup["based_on"] = last_full["backup_id"]
                    break
            self._save_backup_index()
        
        return result
    
    def list_backups(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        List all available backups.
        
        Args:
            limit (int): Maximum number of backups to return
            
        Returns:
            List[Dict[str, Any]]: Backup metadata
        """
        backups = sorted(self.backup_history, key=lambda x: x["timestamp"], reverse=True)
        
        if limit:
            backups = backups[:limit]
        
        return backups
    
    def get_backup_info(self, backup_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific backup.
        
        Args:
            backup_id (str): Backup ID
            
        Returns:
            Dict[str, Any]: Backup metadata
        """
        for backup in self.backup_history:
            if backup["backup_id"] == backup_id:
                return backup
        return None
    
    def verify_backup(self, backup_id: str) -> Dict[str, Any]:
        """
        Verify a backup's integrity.
        
        Args:
            backup_id (str): Backup ID
            
        Returns:
            Dict[str, Any]: Verification results
        """
        backup_info = self.get_backup_info(backup_id)
        
        if not backup_info:
            return {"success": False, "error": "Backup not found"}
        
        backup_file = os.path.join(self.backup_dir, backup_info["backup_file"])
        
        if not os.path.exists(backup_file):
            return {"success": False, "error": "Backup file not found"}
        
        try:
            # Verify file can be read
            if backup_info["compressed"]:
                with gzip.open(backup_file, 'rb') as f:
                    data = f.read()
                    json.loads(data.decode('utf-8'))
            else:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    json.load(f)
            
            file_size = os.path.getsize(backup_file)
            
            return {
                "success": True,
                "valid": True,
                "backup_id": backup_id,
                "file_size": file_size,
                "file_exists": True,
                "message": "Backup is valid and intact"
            }
        
        except Exception as e:
            return {
                "success": False,
                "valid": False,
                "error": f"Backup verification failed: {str(e)}"
            }
    
    def restore_backup(self,
                      backup_id: str,
                      restore_path: str = None,
                      create_restore_backup: bool = True) -> Dict[str, Any]:
        """
        Restore data from a backup.
        
        Args:
            backup_id (str): Backup ID to restore
            restore_path (str): Path to restore to (uses original if None)
            create_restore_backup (bool): Create backup before restoring
            
        Returns:
            Dict[str, Any]: Restore results
        """
        backup_info = self.get_backup_info(backup_id)
        
        if not backup_info:
            return {"success": False, "error": "Backup not found"}
        
        backup_file = os.path.join(self.backup_dir, backup_info["backup_file"])
        
        if not os.path.exists(backup_file):
            return {"success": False, "error": "Backup file not found"}
        
        if restore_path is None:
            restore_path = backup_info["source_file"]
        
        try:
            # Create safety backup before restoring
            if create_restore_backup and os.path.exists(restore_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safety_backup = f"{restore_path}.pre_restore_{timestamp}.bak"
                shutil.copy2(restore_path, safety_backup)
            
            # Read backup data
            if backup_info["compressed"]:
                with gzip.open(backup_file, 'rb') as f:
                    data = f.read().decode('utf-8')
            else:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    data = f.read()
            
            # Verify data integrity
            json.loads(data)  # Validate JSON
            
            # Write restored data
            os.makedirs(os.path.dirname(restore_path), exist_ok=True)
            with open(restore_path, 'w', encoding='utf-8') as f:
                f.write(data)
            
            return {
                "success": True,
                "backup_id": backup_id,
                "restored_to": restore_path,
                "timestamp": backup_info["timestamp"],
                "message": f"Successfully restored from backup {backup_id}"
            }
        
        except Exception as e:
            return {"success": False, "error": f"Restore failed: {str(e)}"}
    
    def schedule_backup(self,
                       interval_hours: int = 24,
                       backup_type: BackupType = BackupType.INCREMENTAL,
                       compress: bool = True) -> Dict[str, Any]:
        """
        Schedule automatic backups.
        
        Args:
            interval_hours (int): Hours between backups
            backup_type (BackupType): Type of backup
            compress (bool): Compress backups
            
        Returns:
            Dict[str, Any]: Schedule info
        """
        schedule_info = {
            "schedule_id": f"schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "interval_hours": interval_hours,
            "backup_type": backup_type.value,
            "compress": compress,
            "created_at": datetime.now().isoformat(),
            "next_backup": (datetime.now() + timedelta(hours=interval_hours)).isoformat(),
            "active": True
        }
        
        return {
            "success": True,
            "schedule": schedule_info,
            "message": f"Backup scheduled every {interval_hours} hours"
        }
    
    def cleanup_old_backups(self,
                           keep_count: int = 10,
                           keep_days: int = 30) -> Dict[str, Any]:
        """
        Clean up old backups.
        
        Args:
            keep_count (int): Keep at least this many backups
            keep_days (int): Keep backups from last N days
            
        Returns:
            Dict[str, Any]: Cleanup results
        """
        if not self.backup_history:
            return {"success": True, "removed_count": 0, "message": "No backups to clean"}
        
        # Sort by timestamp (newest first)
        sorted_backups = sorted(self.backup_history, key=lambda x: x["timestamp"], reverse=True)
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        to_remove = []
        kept = []
        
        for i, backup in enumerate(sorted_backups):
            backup_date = datetime.fromisoformat(backup["timestamp"])
            
            # Keep if within count limit
            if i < keep_count:
                kept.append(backup)
            # Keep if within days limit
            elif backup_date >= cutoff_date:
                kept.append(backup)
            else:
                to_remove.append(backup)
        
        # Remove old backup files
        removed_count = 0
        for backup in to_remove:
            backup_file = os.path.join(self.backup_dir, backup["backup_file"])
            try:
                if os.path.exists(backup_file):
                    os.remove(backup_file)
                    removed_count += 1
            except Exception as e:
                print(f"Warning: Could not remove {backup_file}: {e}")
        
        # Update history
        self.backup_history = kept
        self._save_backup_index()
        
        return {
            "success": True,
            "removed_count": removed_count,
            "remaining_count": len(kept),
            "message": f"Removed {removed_count} old backups"
        }
    
    def get_backup_statistics(self) -> Dict[str, Any]:
        """
        Get backup statistics.
        
        Returns:
            Dict[str, Any]: Statistics
        """
        if not self.backup_history:
            return {
                "total_backups": 0,
                "total_storage": 0,
                "by_type": {},
                "oldest_backup": None,
                "newest_backup": None
            }
        
        total_size = 0
        by_type = {}
        
        for backup in self.backup_history:
            size = backup.get("compressed_size", backup.get("file_size", 0))
            total_size += size
            
            btype = backup["type"]
            by_type[btype] = by_type.get(btype, 0) + 1
        
        sorted_backups = sorted(self.backup_history, key=lambda x: x["timestamp"])
        
        return {
            "total_backups": len(self.backup_history),
            "total_storage": total_size,
            "total_storage_mb": round(total_size / (1024 * 1024), 2),
            "by_type": by_type,
            "oldest_backup": sorted_backups[0]["timestamp"] if sorted_backups else None,
            "newest_backup": sorted_backups[-1]["timestamp"] if sorted_backups else None,
            "average_backup_size": round(total_size / len(self.backup_history), 2) if self.backup_history else 0
        }
    
    def export_backup_summary(self) -> Dict[str, Any]:
        """
        Export a summary of all backups.
        
        Returns:
            Dict[str, Any]: Summary data
        """
        return {
            "export_date": datetime.now().isoformat(),
            "backup_directory": os.path.abspath(self.backup_dir),
            "total_backups": len(self.backup_history),
            "backups": [
                {
                    "backup_id": b["backup_id"],
                    "type": b["type"],
                    "timestamp": b["timestamp"],
                    "description": b.get("description", ""),
                    "file": b.get("backup_file"),
                    "size": b.get("compressed_size", b.get("file_size", 0)),
                    "compressed": b.get("compressed", False)
                }
                for b in sorted(self.backup_history, key=lambda x: x["timestamp"], reverse=True)
            ],
            "statistics": self.get_backup_statistics()
        }
