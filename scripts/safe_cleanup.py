#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全清理脚本 - 处理重复目录和缓存文件
跳过.git目录，避免权限错误
"""

import os
import shutil
from pathlib import Path
from typing import List

class SafeCleaner:
    """安全清理器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.cleaned_items = []
        self.errors = []
    
    def safe_remove_directory(self, dir_path: Path, skip_patterns: List[str] = None):
        """安全删除目录，跳过特定模式"""
        if skip_patterns is None:
            skip_patterns = ['.git', '__pycache__']
        
        if not dir_path.exists():
            return True
        
        try:
            # 检查是否包含需要跳过的目录
            for root, dirs, files in os.walk(dir_path):
                for skip_pattern in skip_patterns:
                    if skip_pattern in dirs:
                        print(f"   ⚠️  跳过包含 {skip_pattern} 的目录: {root}")
                        return False
            
            # 如果目录为空或只包含可删除文件，直接删除
            if not any(dir_path.iterdir()):
                dir_path.rmdir()
                return True
            
            # 使用shutil.rmtree删除
            shutil.rmtree(dir_path, ignore_errors=True)
            return True
        except PermissionError as e:
            self.errors.append(f"权限错误: {dir_path} - {e}")
            return False
        except Exception as e:
            self.errors.append(f"删除失败: {dir_path} - {e}")
            return False
    
    def merge_user_data_dirs(self):
        """合并用户数据目录（avatars, uploads, models, tmp）"""
        print("\n📁 合并用户数据目录...")
        
        merges = [
            {
                'source': self.project_root / 'backend' / 'avatars',
                'target': self.project_root / 'backend' / 'data' / 'avatars',
                'name': 'avatars'
            },
            {
                'source': self.project_root / 'backend' / 'uploads',
                'target': self.project_root / 'backend' / 'data' / 'uploads',
                'name': 'uploads'
            },
            {
                'source': self.project_root / 'backend' / 'models',
                'target': self.project_root / 'backend' / 'data' / 'models',
                'name': 'models'
            },
            {
                'source': self.project_root / 'backend' / 'tmp',
                'target': self.project_root / 'backend' / 'data' / 'tmp',
                'name': 'tmp'
            }
        ]
        
        success_count = 0
        for merge in merges:
            source = merge['source']
            target = merge['target']
            name = merge['name']
            
            if not source.exists():
                print(f"   ✅ {name}: 源目录不存在，跳过")
                continue
            
            # 确保目标目录存在
            target.mkdir(parents=True, exist_ok=True)
            
            # 复制文件
            copied_count = 0
            try:
                for item in source.rglob('*'):
                    if item.is_file():
                        relative_path = item.relative_to(source)
                        target_file = target / relative_path
                        
                        if not target_file.exists():
                            target_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(item, target_file)
                            copied_count += 1
                
                print(f"   ✅ {name}: 复制了 {copied_count} 个新文件")
                
                # 删除源目录
                if self.safe_remove_directory(source):
                    self.cleaned_items.append(str(source))
                    success_count += 1
                    print(f"   ✅ {name}: 源目录已删除")
                else:
                    print(f"   ⚠️  {name}: 源目录删除失败（可能包含.git或权限问题）")
                    
            except Exception as e:
                print(f"   ❌ {name}: 合并失败 - {e}")
                self.errors.append(f"{name}: {e}")
        
        return success_count
    
    def handle_emollm_dir(self):
        """处理EmoLLM重复目录（跳过.git）"""
        print("\n📁 处理 EmoLLM 目录...")
        
        source = self.project_root / 'backend' / 'data' / 'EmoLLM'
        target = self.project_root / 'data' / 'EmoLLM'
        
        if not source.exists():
            print("   ✅ 源目录不存在，跳过")
            return True
        
        # 检查是否包含.git
        if (source / '.git').exists():
            print("   ⚠️  源目录包含.git，建议手动处理或使用git命令")
            print(f"   建议: 如果内容相同，可以手动删除 {source}")
            return False
        
        # 如果目标目录已包含所有文件，直接删除源目录
        if target.exists():
            print("   ✅ 目标目录已存在，检查内容...")
            # 简单检查：如果源目录文件数 <= 目标目录文件数，认为已同步
            source_files = len(list(source.rglob('*')))
            target_files = len(list(target.rglob('*')))
            
            if source_files <= target_files:
                print(f"   ✅ 目标目录文件数({target_files}) >= 源目录文件数({source_files})，删除源目录")
                if self.safe_remove_directory(source):
                    self.cleaned_items.append(str(source))
                    return True
        
        return False
    
    def cleanup_empty_dirs(self):
        """清理空目录"""
        print("\n🧹 清理空目录...")
        
        empty_dirs = []
        for root, dirs, files in os.walk(self.project_root):
            # 跳过.git和venv等目录
            if '.git' in root or 'venv' in root or 'whisper_env' in root:
                continue
            
            if not dirs and not files:
                empty_path = Path(root)
                if not empty_path.name.startswith('.'):
                    empty_dirs.append(empty_path)
        
        cleaned = 0
        for empty_dir in empty_dirs:
            try:
                empty_dir.rmdir()
                self.cleaned_items.append(str(empty_dir))
                cleaned += 1
            except Exception as e:
                self.errors.append(f"删除空目录失败: {empty_dir} - {e}")
        
        print(f"   ✅ 清理了 {cleaned} 个空目录")
        return cleaned
    
    def execute(self):
        """执行清理"""
        print("=" * 80)
        print("安全清理执行")
        print("=" * 80)
        
        # 合并用户数据目录
        user_data_success = self.merge_user_data_dirs()
        
        # 处理EmoLLM目录
        emollm_success = self.handle_emollm_dir()
        
        # 清理空目录
        empty_count = self.cleanup_empty_dirs()
        
        # 总结
        print("\n" + "=" * 80)
        print("清理摘要:")
        print(f"  - 用户数据目录合并: {user_data_success}/4 个成功")
        print(f"  - EmoLLM目录处理: {'成功' if emollm_success else '需手动处理'}")
        print(f"  - 空目录清理: {empty_count} 个")
        print(f"  - 总计清理: {len(self.cleaned_items)} 个项目")
        
        if self.errors:
            print(f"\n⚠️  错误: {len(self.errors)} 个")
            for error in self.errors[:5]:
                print(f"   - {error}")
        
        print("=" * 80)

if __name__ == "__main__":
    cleaner = SafeCleaner()
    cleaner.execute()




