#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
冗余文件清理执行脚本
执行实际的清理操作（谨慎使用）
"""

import os
import shutil
from pathlib import Path
from typing import List

class CleanupExecutor:
    """清理执行器"""
    
    def __init__(self, project_root: str = ".", dry_run: bool = True):
        self.project_root = Path(project_root).resolve()
        self.dry_run = dry_run
        self.deleted_items = []
        self.errors = []
    
    def cleanup_python_cache(self):
        """清理 Python 缓存文件"""
        print("🧹 清理 Python 缓存文件...")
        count = 0
        
        for root, dirs, files in os.walk(self.project_root):
            # 跳过虚拟环境
            if 'whisper_env' in root or 'venv' in root or '.venv' in root:
                continue
            
            # 删除 __pycache__ 目录
            if '__pycache__' in dirs:
                cache_dir = Path(root) / '__pycache__'
                try:
                    if not self.dry_run:
                        shutil.rmtree(cache_dir)
                    self.deleted_items.append(str(cache_dir))
                    count += 1
                except Exception as e:
                    self.errors.append(f"删除失败 {cache_dir}: {e}")
            
            # 删除 .pyc 和 .pyo 文件
            for file in files:
                if file.endswith(('.pyc', '.pyo')):
                    file_path = Path(root) / file
                    try:
                        if not self.dry_run:
                            file_path.unlink()
                        self.deleted_items.append(str(file_path))
                        count += 1
                    except Exception as e:
                        self.errors.append(f"删除失败 {file_path}: {e}")
        
        print(f"   ✅ 清理了 {count} 个缓存文件/目录")
        return count
    
    def cleanup_duplicate_dirs(self):
        """清理重复目录（需要手动确认）"""
        print("\n⚠️  重复目录清理需要手动确认，请查看 CLEANUP_REPORT.txt")
        print("   建议操作:")
        print("   1. 检查 backend/data/EmoLLM 和 data/EmoLLM 的内容")
        print("   2. 如果内容相同，删除 backend/data/EmoLLM")
        print("   3. 合并 backend/avatars 到 backend/data/avatars")
        print("   4. 合并 backend/uploads 到 backend/data/uploads")
        print("   5. 合并 backend/models 到 backend/data/models")
        print("   6. 合并 backend/tmp 到 backend/data/tmp")
        return 0
    
    def cleanup_empty_dirs(self):
        """清理空目录"""
        print("\n🧹 清理空目录...")
        count = 0
        
        empty_dirs = [
            self.project_root / 'backend' / 'history'
        ]
        
        for dir_path in empty_dirs:
            if dir_path.exists():
                try:
                    # 检查是否为空
                    if not any(dir_path.iterdir()):
                        if not self.dry_run:
                            dir_path.rmdir()
                        self.deleted_items.append(str(dir_path))
                        count += 1
                        print(f"   ✅ 删除空目录: {dir_path}")
                except Exception as e:
                    self.errors.append(f"删除失败 {dir_path}: {e}")
        
        return count
    
    def execute(self):
        """执行清理"""
        mode = "【模拟模式】" if self.dry_run else "【执行模式】"
        print(f"\n{'='*80}")
        print(f"冗余文件清理 {mode}")
        print(f"{'='*80}\n")
        
        cache_count = self.cleanup_python_cache()
        duplicate_count = self.cleanup_duplicate_dirs()
        empty_count = self.cleanup_empty_dirs()
        
        print(f"\n{'='*80}")
        print("清理摘要:")
        print(f"  - Python 缓存: {cache_count} 个")
        print(f"  - 重复目录: {duplicate_count} 个（需手动确认）")
        print(f"  - 空目录: {empty_count} 个")
        print(f"  - 总计: {len(self.deleted_items)} 个项目")
        
        if self.errors:
            print(f"\n⚠️  错误: {len(self.errors)} 个")
            for error in self.errors[:5]:
                print(f"   - {error}")
        
        if self.dry_run:
            print(f"\n💡 这是模拟运行，实际文件未被删除")
            print(f"   要执行实际清理，请运行: python scripts/cleanup_execute.py --execute")
        else:
            print(f"\n✅ 清理完成！")
        
        print(f"{'='*80}")

if __name__ == "__main__":
    import sys
    
    dry_run = "--execute" not in sys.argv
    
    executor = CleanupExecutor(dry_run=dry_run)
    executor.execute()




