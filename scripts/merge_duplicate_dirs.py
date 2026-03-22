#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重复目录合并脚本
安全地合并重复目录，确保数据不丢失
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple

class DirectoryMerger:
    """目录合并器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.merged_items = []
        self.errors = []
    
    def merge_directories(self, source: Path, target: Path, dry_run: bool = True) -> bool:
        """
        合并目录
        
        Args:
            source: 源目录（将被删除）
            target: 目标目录（保留）
            dry_run: 是否为模拟模式
            
        Returns:
            bool: 是否成功
        """
        if not source.exists():
            print(f"   ⚠️  源目录不存在: {source}")
            return False
        
        if not target.exists():
            print(f"   📁 创建目标目录: {target}")
            if not dry_run:
                target.mkdir(parents=True, exist_ok=True)
        
        # 检查源目录中的文件
        source_files = list(source.rglob('*'))
        source_files = [f for f in source_files if f.is_file()]
        
        if not source_files:
            print(f"   ✅ 源目录为空，可直接删除")
            if not dry_run:
                shutil.rmtree(source)
            self.merged_items.append({
                'source': str(source),
                'target': str(target),
                'action': '删除空目录'
            })
            return True
        
        print(f"   📊 源目录包含 {len(source_files)} 个文件")
        
        # 检查是否有冲突文件
        conflicts = []
        for source_file in source_files:
            relative_path = source_file.relative_to(source)
            target_file = target / relative_path
            
            if target_file.exists():
                # 比较文件大小和修改时间
                if source_file.stat().st_size != target_file.stat().st_size:
                    conflicts.append(str(relative_path))
        
        if conflicts:
            print(f"   ⚠️  发现 {len(conflicts)} 个冲突文件:")
            for conflict in conflicts[:5]:
                print(f"      - {conflict}")
            if len(conflicts) > 5:
                print(f"      ... 还有 {len(conflicts) - 5} 个")
            print(f"   ⚠️  需要手动处理冲突")
            return False
        
        # 复制文件
        copied_count = 0
        for source_file in source_files:
            relative_path = source_file.relative_to(source)
            target_file = target / relative_path
            
            if not target_file.exists():
                target_file.parent.mkdir(parents=True, exist_ok=True)
                if not dry_run:
                    shutil.copy2(source_file, target_file)
                copied_count += 1
        
        print(f"   ✅ 复制了 {copied_count} 个新文件到目标目录")
        
        # 删除源目录
        if not dry_run:
            shutil.rmtree(source)
        
        self.merged_items.append({
            'source': str(source),
            'target': str(target),
            'action': f'合并了 {copied_count} 个文件'
        })
        
        return True
    
    def merge_emollm_dirs(self, dry_run: bool = True):
        """合并 EmoLLM 目录"""
        print("\n📁 合并 EmoLLM 目录...")
        
        source = self.project_root / 'backend' / 'data' / 'EmoLLM'
        target = self.project_root / 'data' / 'EmoLLM'
        
        if not source.exists():
            print("   ✅ 源目录不存在，无需合并")
            return True
        
        return self.merge_directories(source, target, dry_run)
    
    def merge_user_data_dirs(self, dry_run: bool = True):
        """合并用户数据目录"""
        print("\n📁 合并用户数据目录...")
        
        merges = [
            (self.project_root / 'backend' / 'avatars', 
             self.project_root / 'backend' / 'data' / 'avatars'),
            (self.project_root / 'backend' / 'uploads', 
             self.project_root / 'backend' / 'data' / 'uploads'),
            (self.project_root / 'backend' / 'models', 
             self.project_root / 'backend' / 'data' / 'models'),
            (self.project_root / 'backend' / 'tmp', 
             self.project_root / 'backend' / 'data' / 'tmp'),
        ]
        
        success_count = 0
        for source, target in merges:
            if source.exists():
                print(f"\n   合并: {source.name}")
                if self.merge_directories(source, target, dry_run):
                    success_count += 1
            else:
                print(f"\n   ✅ {source.name} 不存在，跳过")
        
        return success_count == len([s for s, _ in merges if s.exists()])
    
    def execute(self, dry_run: bool = True):
        """执行合并"""
        mode = "【模拟模式】" if dry_run else "【执行模式】"
        print(f"\n{'='*80}")
        print(f"重复目录合并 {mode}")
        print(f"{'='*80}\n")
        
        emollm_success = self.merge_emollm_dirs(dry_run)
        user_data_success = self.merge_user_data_dirs(dry_run)
        
        print(f"\n{'='*80}")
        print("合并摘要:")
        print(f"  - EmoLLM 目录: {'✅ 成功' if emollm_success else '⚠️  需要手动处理'}")
        print(f"  - 用户数据目录: {'✅ 成功' if user_data_success else '⚠️  部分失败'}")
        print(f"  - 总计: {len(self.merged_items)} 个目录")
        
        if self.errors:
            print(f"\n⚠️  错误: {len(self.errors)} 个")
            for error in self.errors:
                print(f"   - {error}")
        
        if dry_run:
            print(f"\n💡 这是模拟运行，实际文件未被移动")
            print(f"   要执行实际合并，请运行: python scripts/merge_duplicate_dirs.py --execute")
        else:
            print(f"\n✅ 合并完成！")
        
        print(f"{'='*80}")

if __name__ == "__main__":
    import sys
    
    dry_run = "--execute" not in sys.argv
    
    merger = DirectoryMerger()
    merger.execute(dry_run=dry_run)




