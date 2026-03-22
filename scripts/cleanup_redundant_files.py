#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
冗余文件清理脚本
扫描并列出所有需要清理的文件和目录
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict

class RedundantFileCleaner:
    """冗余文件清理器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.cleanup_list = {
            'python_cache': [],
            'duplicate_dirs': [],
            'temp_files': [],
            'empty_dirs': [],
            'virtual_envs': []
        }
    
    def scan_python_cache(self):
        """扫描 Python 缓存文件"""
        print("🔍 扫描 Python 缓存文件...")
        for root, dirs, files in os.walk(self.project_root):
            # 跳过虚拟环境
            if 'whisper_env' in root or 'venv' in root or '.venv' in root:
                continue
            
            if '__pycache__' in dirs:
                cache_dir = Path(root) / '__pycache__'
                self.cleanup_list['python_cache'].append(str(cache_dir))
            
            # 查找 .pyc 和 .pyo 文件
            for file in files:
                if file.endswith(('.pyc', '.pyo')):
                    self.cleanup_list['python_cache'].append(str(Path(root) / file))
    
    def scan_duplicate_dirs(self):
        """扫描重复目录"""
        print("🔍 扫描重复目录...")
        
        # 检查重复的 EmoLLM 目录
        emollm_paths = [
            self.project_root / 'backend' / 'data' / 'EmoLLM',
            self.project_root / 'data' / 'EmoLLM'
        ]
        
        existing_paths = [p for p in emollm_paths if p.exists()]
        if len(existing_paths) > 1:
            # 保留 data/EmoLLM，删除 backend/data/EmoLLM
            if (self.project_root / 'backend' / 'data' / 'EmoLLM').exists():
                self.cleanup_list['duplicate_dirs'].append({
                    'path': str(self.project_root / 'backend' / 'data' / 'EmoLLM'),
                    'reason': '与 data/EmoLLM 重复',
                    'action': '删除（保留 data/EmoLLM）'
                })
        
        # 检查其他重复目录
        duplicate_patterns = [
            {
                'paths': [
                    self.project_root / 'backend' / 'avatars',
                    self.project_root / 'backend' / 'data' / 'avatars'
                ],
                'keep': 'backend/data/avatars'
            },
            {
                'paths': [
                    self.project_root / 'backend' / 'uploads',
                    self.project_root / 'backend' / 'data' / 'uploads'
                ],
                'keep': 'backend/data/uploads'
            },
            {
                'paths': [
                    self.project_root / 'backend' / 'models',
                    self.project_root / 'backend' / 'data' / 'models'
                ],
                'keep': 'backend/data/models'
            },
            {
                'paths': [
                    self.project_root / 'backend' / 'tmp',
                    self.project_root / 'backend' / 'data' / 'tmp'
                ],
                'keep': 'backend/data/tmp'
            }
        ]
        
        for pattern in duplicate_patterns:
            existing = [p for p in pattern['paths'] if p.exists()]
            if len(existing) > 1:
                for path in existing:
                    if pattern['keep'] not in str(path):
                        self.cleanup_list['duplicate_dirs'].append({
                            'path': str(path),
                            'reason': f"与 {pattern['keep']} 重复",
                            'action': f"删除（保留 {pattern['keep']}）"
                        })
    
    def scan_temp_files(self):
        """扫描临时文件"""
        print("🔍 扫描临时文件...")
        
        temp_patterns = [
            '*.tmp',
            '*.temp',
            '*.log',
            '*.cache'
        ]
        
        temp_dirs = [
            self.project_root / 'backend' / 'tmp',
            self.project_root / 'data' / 'tmp'
        ]
        
        for temp_dir in temp_dirs:
            if temp_dir.exists():
                for file in temp_dir.rglob('*'):
                    if file.is_file() and not file.name.startswith('.'):
                        # 检查是否是临时文件
                        if file.suffix in ['.tmp', '.temp', '.log', '.wav', '.m4a']:
                            # 跳过重要的数据文件
                            if 'recording.wav' not in file.name:
                                self.cleanup_list['temp_files'].append({
                                    'path': str(file),
                                    'reason': '临时文件',
                                    'size': file.stat().st_size
                                })
    
    def scan_empty_dirs(self):
        """扫描空目录"""
        print("🔍 扫描空目录...")
        
        # 检查 backend/history（如果为空）
        history_dir = self.project_root / 'backend' / 'history'
        if history_dir.exists():
            try:
                if not any(history_dir.iterdir()):
                    self.cleanup_list['empty_dirs'].append({
                        'path': str(history_dir),
                        'reason': '空目录'
                    })
            except:
                pass
    
    def generate_report(self) -> str:
        """生成清理报告"""
        report = []
        report.append("=" * 80)
        report.append("冗余文件清理报告")
        report.append("=" * 80)
        report.append("")
        
        # Python 缓存
        report.append(f"📦 Python 缓存文件/目录: {len(self.cleanup_list['python_cache'])} 个")
        if self.cleanup_list['python_cache']:
            report.append("   注意：这些文件通常由 .gitignore 忽略，但可以手动清理")
            for item in self.cleanup_list['python_cache'][:10]:
                report.append(f"   - {item}")
            if len(self.cleanup_list['python_cache']) > 10:
                report.append(f"   ... 还有 {len(self.cleanup_list['python_cache']) - 10} 个")
        report.append("")
        
        # 重复目录
        report.append(f"📁 重复目录: {len(self.cleanup_list['duplicate_dirs'])} 个")
        for item in self.cleanup_list['duplicate_dirs']:
            report.append(f"   - {item['path']}")
            report.append(f"     原因: {item['reason']}")
            report.append(f"     操作: {item['action']}")
        report.append("")
        
        # 临时文件
        report.append(f"🗑️  临时文件: {len(self.cleanup_list['temp_files'])} 个")
        total_size = sum(item.get('size', 0) for item in self.cleanup_list['temp_files'])
        report.append(f"   总大小: {total_size / 1024 / 1024:.2f} MB")
        for item in self.cleanup_list['temp_files'][:10]:
            size_mb = item.get('size', 0) / 1024 / 1024
            report.append(f"   - {item['path']} ({size_mb:.2f} MB)")
        if len(self.cleanup_list['temp_files']) > 10:
            report.append(f"   ... 还有 {len(self.cleanup_list['temp_files']) - 10} 个")
        report.append("")
        
        # 空目录
        report.append(f"📂 空目录: {len(self.cleanup_list['empty_dirs'])} 个")
        for item in self.cleanup_list['empty_dirs']:
            report.append(f"   - {item['path']} ({item['reason']})")
        report.append("")
        
        report.append("=" * 80)
        report.append("注意：此报告仅列出文件，不会自动删除")
        report.append("请手动审查后执行清理操作")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def scan_all(self):
        """执行所有扫描"""
        print("开始扫描冗余文件...\n")
        self.scan_python_cache()
        self.scan_duplicate_dirs()
        self.scan_temp_files()
        self.scan_empty_dirs()
        print("\n扫描完成！\n")

if __name__ == "__main__":
    cleaner = RedundantFileCleaner()
    cleaner.scan_all()
    report = cleaner.generate_report()
    print(report)
    
    # 保存报告到文件
    report_file = Path("CLEANUP_REPORT.txt")
    report_file.write_text(report, encoding='utf-8')
    print(f"\n✅ 报告已保存到: {report_file}")




