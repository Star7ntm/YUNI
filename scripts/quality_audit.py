#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目质量验收脚本
检查目录结构、冗余文件、.gitignore、README.md等
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class QualityAuditor:
    """项目质量审计器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.issues = []
        self.warnings = []
        self.recommendations = []
    
    def check_directory_structure(self) -> Dict:
        """检查目录结构是否符合高内聚低耦合原则"""
        print("🔍 检查目录结构...")
        
        issues = []
        warnings = []
        
        # 检查是否存在重复的数据目录
        duplicate_dirs = {
            'EmoLLM': [
                self.project_root / 'backend' / 'data' / 'EmoLLM',
                self.project_root / 'data' / 'EmoLLM'
            ],
            'avatars': [
                self.project_root / 'backend' / 'avatars',
                self.project_root / 'backend' / 'data' / 'avatars',
                self.project_root / 'data' / 'avatars'
            ],
            'uploads': [
                self.project_root / 'backend' / 'uploads',
                self.project_root / 'backend' / 'data' / 'uploads',
                self.project_root / 'data' / 'uploads'
            ],
            'models': [
                self.project_root / 'backend' / 'models',
                self.project_root / 'backend' / 'data' / 'models',
                self.project_root / 'data' / 'models'
            ],
            'tmp': [
                self.project_root / 'backend' / 'tmp',
                self.project_root / 'backend' / 'data' / 'tmp',
                self.project_root / 'data' / 'tmp'
            ]
        }
        
        for name, paths in duplicate_dirs.items():
            existing = [p for p in paths if p.exists()]
            if len(existing) > 1:
                issues.append({
                    'type': 'duplicate_directory',
                    'name': name,
                    'paths': [str(p) for p in existing],
                    'severity': 'high'
                })
        
        # 检查是否符合src/结构（理想状态）
        if not (self.project_root / 'src').exists():
            warnings.append({
                'type': 'missing_src_structure',
                'message': '项目未采用src/目录结构，backend和frontend在根目录',
                'severity': 'medium'
            })
        
        # 检查模块耦合度
        # backend直接依赖frontend路径
        backend_main = self.project_root / 'backend' / 'main.py'
        if backend_main.exists():
            content = backend_main.read_text(encoding='utf-8')
            if 'frontend' in content and '../frontend' in content:
                warnings.append({
                    'type': 'tight_coupling',
                    'message': 'backend/main.py直接引用frontend路径，存在耦合',
                    'severity': 'medium'
                })
        
        return {
            'issues': issues,
            'warnings': warnings,
            'score': 100 - len(issues) * 10 - len(warnings) * 5
        }
    
    def check_redundant_files(self) -> Dict:
        """检查冗余文件清理情况"""
        print("🔍 检查冗余文件...")
        
        issues = []
        warnings = []
        
        # 检查__pycache__目录（应该被.gitignore忽略，但实际存在）
        cache_dirs = []
        for root, dirs, files in os.walk(self.project_root):
            if '__pycache__' in dirs:
                cache_path = Path(root) / '__pycache__'
                # 排除虚拟环境
                if 'venv' not in str(cache_path) and 'whisper_env' not in str(cache_path):
                    cache_dirs.append(cache_path)
        
        if cache_dirs:
            warnings.append({
                'type': 'cache_directories_exist',
                'count': len(cache_dirs),
                'paths': [str(p) for p in cache_dirs[:5]],
                'severity': 'low',
                'note': '这些目录应该被.gitignore忽略，但实际存在于文件系统中'
            })
        
        # 检查空目录
        empty_dirs = []
        for root, dirs, files in os.walk(self.project_root):
            if not dirs and not files:
                empty_path = Path(root)
                # 排除.git等隐藏目录
                if not empty_path.name.startswith('.'):
                    empty_dirs.append(empty_path)
        
        if empty_dirs:
            warnings.append({
                'type': 'empty_directories',
                'count': len(empty_dirs),
                'paths': [str(p) for p in empty_dirs[:5]],
                'severity': 'low'
            })
        
        # 检查临时文件
        temp_files = []
        temp_patterns = ['.tmp', '.temp', '.cache', '.log']
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if any(file.endswith(p) for p in temp_patterns):
                    temp_path = Path(root) / file
                    # 排除.gitignore中已忽略的目录
                    if 'data/tmp' not in str(temp_path) and 'backend/data/tmp' not in str(temp_path):
                        temp_files.append(temp_path)
        
        if temp_files:
            warnings.append({
                'type': 'temporary_files',
                'count': len(temp_files),
                'paths': [str(p) for p in temp_files[:5]],
                'severity': 'low'
            })
        
        return {
            'issues': issues,
            'warnings': warnings,
            'score': 100 - len(issues) * 15 - len(warnings) * 5
        }
    
    def check_gitignore(self) -> Dict:
        """检查.gitignore是否完整"""
        print("🔍 检查.gitignore...")
        
        gitignore_path = self.project_root / '.gitignore'
        if not gitignore_path.exists():
            return {
                'issues': [{'type': 'missing_gitignore', 'severity': 'critical'}],
                'warnings': [],
                'score': 0
            }
        
        content = gitignore_path.read_text(encoding='utf-8')
        
        issues = []
        warnings = []
        
        # 检查必需的模式
        required_patterns = {
            '__pycache__/': 'Python缓存目录',
            '*.pyc': 'Python编译文件',
            '*.pyo': 'Python优化文件',
            'venv/': '虚拟环境',
            '.env': '环境变量文件',
            '*.log': '日志文件',
            '.DS_Store': 'macOS系统文件',
            'Thumbs.db': 'Windows系统文件',
            'instance/*.db': '数据库文件',
            'models/': '模型文件（大文件）'
        }
        
        for pattern, description in required_patterns.items():
            if pattern not in content:
                issues.append({
                    'type': 'missing_pattern',
                    'pattern': pattern,
                    'description': description,
                    'severity': 'medium'
                })
        
        # 检查是否有重复模式
        lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
        duplicates = [line for line in set(lines) if lines.count(line) > 1]
        if duplicates:
            warnings.append({
                'type': 'duplicate_patterns',
                'patterns': duplicates,
                'severity': 'low'
            })
        
        return {
            'issues': issues,
            'warnings': warnings,
            'score': 100 - len(issues) * 10 - len(warnings) * 3
        }
    
    def check_readme(self) -> Dict:
        """检查README.md的完整性和准确性"""
        print("🔍 检查README.md...")
        
        readme_path = self.project_root / 'README.md'
        if not readme_path.exists():
            return {
                'issues': [{'type': 'missing_readme', 'severity': 'critical'}],
                'warnings': [],
                'score': 0
            }
        
        content = readme_path.read_text(encoding='utf-8')
        
        issues = []
        warnings = []
        
        # 检查必需章节
        required_sections = [
            '项目概述',
            '快速开始',
            '核心功能模块',
            '测试指南',
            '部署流程',
            '贡献规范',
            '版权与许可',
            'TODO'
        ]
        
        missing_sections = []
        for section in required_sections:
            pattern = rf"##\s+.*{section}"
            if not re.search(pattern, content, re.IGNORECASE):
                missing_sections.append(section)
        
        if missing_sections:
            issues.append({
                'type': 'missing_sections',
                'sections': missing_sections,
                'severity': 'high'
            })
        
        # 检查技术栈版本是否准确
        # 读取requirements-locked.txt进行对比
        req_locked = self.project_root / 'requirements-locked.txt'
        if req_locked.exists():
            req_content = req_locked.read_text(encoding='utf-8')
            # 检查关键依赖版本
            key_deps = ['fastapi', 'uvicorn', 'sqlalchemy', 'PyJWT']
            for dep in key_deps:
                pattern = rf"{dep}==([\d.]+)"
                match = re.search(pattern, req_content)
                if match:
                    version = match.group(1)
                    # 检查README中是否包含此版本
                    if f"{dep}" in content and version not in content:
                        warnings.append({
                            'type': 'version_mismatch',
                            'dependency': dep,
                            'actual_version': version,
                            'severity': 'low'
                        })
        
        # 检查API路径是否准确
        # 检查是否有/api前缀
        api_patterns = [
            r'POST\s+/api/register',
            r'POST\s+/api/login',
            r'GET\s+/api/me',
            r'POST\s+/api/transcribe_json'
        ]
        
        for pattern in api_patterns:
            if not re.search(pattern, content, re.IGNORECASE):
                warnings.append({
                    'type': 'api_path_check',
                    'pattern': pattern,
                    'severity': 'low'
                })
        
        # 检查是否有代码示例
        code_blocks = len(re.findall(r'```', content)) // 2
        if code_blocks < 10:
            warnings.append({
                'type': 'insufficient_code_examples',
                'count': code_blocks,
                'severity': 'low'
            })
        
        return {
            'issues': issues,
            'warnings': warnings,
            'score': 100 - len(issues) * 15 - len(warnings) * 3
        }
    
    def generate_report(self) -> str:
        """生成验收报告"""
        print("\n" + "=" * 80)
        print("开始项目质量验收...")
        print("=" * 80 + "\n")
        
        # 执行各项检查
        dir_check = self.check_directory_structure()
        redundant_check = self.check_redundant_files()
        gitignore_check = self.check_gitignore()
        readme_check = self.check_readme()
        
        # 汇总结果
        all_issues = (
            dir_check['issues'] +
            redundant_check['issues'] +
            gitignore_check['issues'] +
            readme_check['issues']
        )
        
        all_warnings = (
            dir_check['warnings'] +
            redundant_check['warnings'] +
            gitignore_check['warnings'] +
            readme_check['warnings']
        )
        
        # 计算总分
        total_score = (
            dir_check['score'] * 0.3 +
            redundant_check['score'] * 0.2 +
            gitignore_check['score'] * 0.2 +
            readme_check['score'] * 0.3
        )
        
        # 生成报告
        report = []
        report.append("=" * 80)
        report.append("项目质量验收报告")
        report.append("=" * 80)
        report.append("")
        report.append(f"验收时间: {Path(__file__).stat().st_mtime}")
        report.append(f"项目路径: {self.project_root}")
        report.append("")
        
        report.append("=" * 80)
        report.append("1. 目录结构检查")
        report.append("=" * 80)
        report.append(f"评分: {dir_check['score']}/100")
        report.append(f"问题数: {len(dir_check['issues'])}")
        report.append(f"警告数: {len(dir_check['warnings'])}")
        report.append("")
        
        if dir_check['issues']:
            report.append("❌ 发现的问题:")
            for issue in dir_check['issues']:
                report.append(f"   - [{issue['severity'].upper()}] {issue.get('name', issue.get('type'))}")
                if 'paths' in issue:
                    for path in issue['paths'][:3]:
                        report.append(f"     • {path}")
        else:
            report.append("✅ 未发现严重问题")
        
        if dir_check['warnings']:
            report.append("")
            report.append("⚠️  警告:")
            for warning in dir_check['warnings']:
                report.append(f"   - {warning.get('message', warning.get('type'))}")
        
        report.append("")
        report.append("=" * 80)
        report.append("2. 冗余文件检查")
        report.append("=" * 80)
        report.append(f"评分: {redundant_check['score']}/100")
        report.append(f"问题数: {len(redundant_check['issues'])}")
        report.append(f"警告数: {len(redundant_check['warnings'])}")
        report.append("")
        
        if redundant_check['warnings']:
            report.append("⚠️  警告:")
            for warning in redundant_check['warnings']:
                report.append(f"   - {warning.get('type')}: {warning.get('count', 0)} 个")
        
        report.append("")
        report.append("=" * 80)
        report.append("3. .gitignore检查")
        report.append("=" * 80)
        report.append(f"评分: {gitignore_check['score']}/100")
        report.append(f"问题数: {len(gitignore_check['issues'])}")
        report.append(f"警告数: {len(gitignore_check['warnings'])}")
        report.append("")
        
        if gitignore_check['issues']:
            report.append("❌ 发现的问题:")
            for issue in gitignore_check['issues']:
                report.append(f"   - [{issue['severity'].upper()}] 缺少模式: {issue.get('pattern', 'N/A')}")
        
        report.append("")
        report.append("=" * 80)
        report.append("4. README.md检查")
        report.append("=" * 80)
        report.append(f"评分: {readme_check['score']}/100")
        report.append(f"问题数: {len(readme_check['issues'])}")
        report.append(f"警告数: {len(readme_check['warnings'])}")
        report.append("")
        
        if readme_check['issues']:
            report.append("❌ 发现的问题:")
            for issue in readme_check['issues']:
                report.append(f"   - [{issue['severity'].upper()}] {issue.get('type')}")
                if 'sections' in issue:
                    report.append(f"     缺失章节: {', '.join(issue['sections'])}")
        
        report.append("")
        report.append("=" * 80)
        report.append("总体评分")
        report.append("=" * 80)
        report.append(f"总分: {total_score:.1f}/100")
        report.append(f"总问题数: {len(all_issues)}")
        report.append(f"总警告数: {len(all_warnings)}")
        report.append("")
        
        if total_score >= 90:
            report.append("✅ 项目质量优秀，符合企业级标准")
        elif total_score >= 75:
            report.append("⚠️  项目质量良好，但存在改进空间")
        elif total_score >= 60:
            report.append("⚠️  项目质量一般，需要优化")
        else:
            report.append("❌ 项目质量不达标，需要重大改进")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def audit(self):
        """执行完整审计"""
        report = self.generate_report()
        print(report)
        return report

if __name__ == "__main__":
    auditor = QualityAuditor()
    report = auditor.audit()
    
    # 保存报告
    report_file = Path("QUALITY_AUDIT_REPORT.txt")
    report_file.write_text(report, encoding='utf-8')
    print(f"\n✅ 报告已保存到: {report_file}")




