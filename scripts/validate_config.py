#!/usr/bin/env python3
"""
配置文件验证脚本
用于验证 subconverter/advanced.ini 和 clash/meta-template.yaml 的合法性
不依赖外部库,仅使用 Python 标准库
"""

import sys
import re
from pathlib import Path

class ConfigValidator:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.errors = []
        self.warnings = []
        
    def add_error(self, msg):
        """添加错误信息"""
        self.errors.append(f"❌ {msg}")
        
    def add_warning(self, msg):
        """添加警告信息"""
        self.warnings.append(f"⚠️  {msg}")
        
    def validate_ini_file(self, ini_path):
        """验证 INI 配置文件"""
        print(f"\n🔍 验证 INI 配置: {ini_path.name}")
        print("=" * 60)
        
        if not ini_path.exists():
            self.add_error(f"文件不存在: {ini_path}")
            return False
            
        content = ini_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # 收集所有策略组名称
        proxy_groups = set()
        
        # 验证策略组定义
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # 跳过注释和空行
            if not line or line.startswith(';') or line.startswith('#'):
                continue
                
            # 检查策略组定义
            if line.startswith('custom_proxy_group='):
                group_def = line[len('custom_proxy_group='):]
                parts = group_def.split('`')
                
                if len(parts) < 2:
                    self.add_error(f"行 {i}: 策略组定义格式错误")
                    continue
                    
                group_name = parts[0]
                group_type = parts[1]
                
                # 记录策略组名称
                proxy_groups.add(group_name)
                
                # 验证策略组类型
                valid_types = ['select', 'url-test', 'fallback', 'load-balance', 'relay']
                if group_type not in valid_types:
                    self.add_error(f"行 {i}: 无效的策略组类型 '{group_type}'")
                
                # 检查是否有错误的节点过滤器在第一个参数位置
                if len(parts) > 2:
                    third_param = parts[2]
                    # 检查第三个参数是否是正则表达式(而不是选项列表)
                    if third_param and not third_param.startswith('[]') and not third_param.startswith('http'):
                        # 对于 url-test 类型,第三个参数应该是 URL
                        if group_type == 'url-test':
                            if not third_param.startswith('http'):
                                self.add_warning(f"行 {i}: url-test 类型的第三个参数应该是测试 URL")
                        # 对于 select 类型,第三个参数不应该是正则表达式
                        elif group_type == 'select':
                            if third_param.startswith('^') or third_param.startswith('(?'):
                                self.add_error(f"行 {i}: select 类型策略组 '{group_name}' 不应该在第三个参数位置使用正则表达式")
                            
        print(f"✅ 找到 {len(proxy_groups)} 个策略组定义")
        return len(self.errors) == 0
        
    def validate_yaml_file(self, yaml_path):
        """验证 YAML 配置文件(简单文本检查)"""
        print(f"\n🔍 验证 YAML 配置: {yaml_path.name}")
        print("=" * 60)
        
        if not yaml_path.exists():
            self.add_error(f"文件不存在: {yaml_path}")
            return False
            
        content = yaml_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # 简单的 YAML 语法检查
        in_proxy_groups = False
        in_rules = False
        proxy_group_count = 0
        rule_count = 0
        group_names = set()
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # 检查是否进入 proxy-groups 部分
            if stripped == 'proxy-groups:':
                in_proxy_groups = True
                in_rules = False
                continue
                
            # 检查是否进入 rules 部分
            if stripped == 'rules:':
                in_rules = True
                in_proxy_groups = False
                continue
                
            # 检查其他顶级字段
            if stripped and not stripped.startswith('#') and not stripped.startswith('-') and ':' in stripped:
                if not line.startswith(' '):
                    in_proxy_groups = False
                    in_rules = False
                    
            # 统计 proxy-groups
            if in_proxy_groups and stripped.startswith('- name:'):
                proxy_group_count += 1
                name_match = re.search(r'name:\s*["\']?([^"\']+)["\']?', stripped)
                if name_match:
                    group_names.add(name_match.group(1))
                    
            # 统计 rules
            if in_rules and stripped.startswith('- '):
                rule_count += 1
                
        print(f"✅ 找到 {proxy_group_count} 个策略组定义")
        print(f"✅ 找到 {rule_count} 条规则")
        
        # 基本的必需字段检查
        if 'proxy-groups:' not in content:
            self.add_error("缺少 proxy-groups 字段")
        if 'rules:' not in content:
            self.add_error("缺少 rules 字段")
            
        return len(self.errors) == 0
            
    def cross_validate(self, ini_path, yaml_path):
        """交叉验证两个配置文件的一致性"""
        print(f"\n🔍 交叉验证配置一致性")
        print("=" * 60)
        
        # 读取 INI 文件的策略组
        ini_groups = set()
        if ini_path.exists():
            content = ini_path.read_text(encoding='utf-8')
            for line in content.split('\n'):
                if line.strip().startswith('custom_proxy_group='):
                    group_def = line.strip()[len('custom_proxy_group='):]
                    parts = group_def.split('`')
                    if parts:
                        ini_groups.add(parts[0])
                        
        # 读取 YAML 文件的策略组
        yaml_groups = set()
        if yaml_path.exists():
            content = yaml_path.read_text(encoding='utf-8')
            for line in content.split('\n'):
                stripped = line.strip()
                if stripped.startswith('- name:'):
                    name_match = re.search(r'name:\s*["\']?([^"\']+)["\']?', stripped)
                    if name_match:
                        yaml_groups.add(name_match.group(1))
                
        # 比较策略组
        ini_only = ini_groups - yaml_groups
        yaml_only = yaml_groups - ini_groups
        common = ini_groups & yaml_groups
        
        print(f"✅ 共同策略组: {len(common)} 个")
        
        if ini_only:
            self.add_warning(f"仅在 INI 中存在的策略组 ({len(ini_only)}): {', '.join(sorted(ini_only))}")
            
        if yaml_only:
            self.add_warning(f"仅在 YAML 中存在的策略组 ({len(yaml_only)}): {', '.join(sorted(yaml_only))}")
            
    def print_results(self):
        """打印验证结果"""
        print("\n" + "=" * 60)
        print("📊 验证结果汇总")
        print("=" * 60)
        
        if self.warnings:
            print(f"\n⚠️  警告 ({len(self.warnings)} 个):")
            for warning in self.warnings:
                print(f"  {warning}")
                
        if self.errors:
            print(f"\n❌ 错误 ({len(self.errors)} 个):")
            for error in self.errors:
                print(f"  {error}")
            print("\n❌ 验证失败!")
            return False
        else:
            if self.warnings:
                print(f"\n⚠️  验证通过,但有 {len(self.warnings)} 个警告")
            else:
                print("\n✅ 验证通过,配置文件格式正确!")
            return True


def main():
    """主函数"""
    # 获取项目根目录
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent
    
    # 配置文件路径
    ini_path = base_dir / 'subconverter' / 'advanced.ini'
    yaml_path = base_dir / 'clash' / 'meta-template.yaml'
    
    print("🚀 ACL4ALL 配置验证工具")
    print("=" * 60)
    print(f"📁 项目目录: {base_dir}")
    
    # 创建验证器
    validator = ConfigValidator(base_dir)
    
    # 验证 INI 文件
    ini_valid = validator.validate_ini_file(ini_path)
    
    # 验证 YAML 文件
    yaml_valid = validator.validate_yaml_file(yaml_path)
    
    # 交叉验证
    validator.cross_validate(ini_path, yaml_path)
    
    # 打印结果
    success = validator.print_results()
    
    # 返回退出码
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
