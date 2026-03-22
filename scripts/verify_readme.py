#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
README.md 文档验证脚本
检查文档结构是否符合企业级标准
"""

import re
from pathlib import Path

def verify_readme():
    """验证README.md文档"""
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        print("❌ README.md 不存在")
        return False
    
    content = readme_path.read_text(encoding='utf-8')
    
    # 必需章节
    required_sections = [
        "项目概述",
        "快速开始",
        "核心功能模块",
        "测试指南",
        "部署流程",
        "贡献规范",
        "版权与许可",
        "TODO"
    ]
    
    print("=" * 80)
    print("README.md 文档验证")
    print("=" * 80)
    print()
    
    # 检查章节
    print("📋 章节检查:")
    missing_sections = []
    for section in required_sections:
        pattern = rf"##\s+.*{section}"
        if re.search(pattern, content, re.IGNORECASE):
            print(f"   ✅ {section}")
        else:
            print(f"   ❌ {section} (缺失)")
            missing_sections.append(section)
    
    print()
    
    # 统计信息
    print("📊 文档统计:")
    code_blocks = len(re.findall(r"```", content)) // 2
    tables = len(re.findall(r"^\|.*\|", content, re.MULTILINE))
    headers = len(re.findall(r"^##+\s+", content, re.MULTILINE))
    links = len(re.findall(r"\[.*\]\(.*\)", content))
    
    print(f"   - 文档长度: {len(content):,} 字符")
    print(f"   - 章节数量: {headers} 个")
    print(f"   - 代码块: {code_blocks} 个")
    print(f"   - 表格: {tables} 个")
    print(f"   - 链接: {links} 个")
    
    print()
    
    # 检查Mermaid图表
    mermaid_blocks = len(re.findall(r"```mermaid", content))
    print(f"📈 Mermaid图表: {mermaid_blocks} 个")
    
    print()
    
    # 检查TODO部分
    todo_items = len(re.findall(r"- \[ \]", content))
    todo_done = len(re.findall(r"- \[x\]", content, re.IGNORECASE))
    print(f"📝 TODO项: {todo_items} 个待完成, {todo_done} 个已完成")
    
    print()
    
    # 验证结果
    if missing_sections:
        print("❌ 验证失败: 缺少以下章节")
        for section in missing_sections:
            print(f"   - {section}")
        return False
    else:
        print("✅ 验证通过: 所有必需章节都存在")
        return True

if __name__ == "__main__":
    success = verify_readme()
    exit(0 if success else 1)




