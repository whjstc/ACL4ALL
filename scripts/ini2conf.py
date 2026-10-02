#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ACL4ALL INI to Shadowrocket CONF 自动转换器
单一真理源 (Single Source of Truth): subconverter/advanced.ini
输出产物: Shadowrocket/config/ACL4ALL_Advanced.conf
"""

import sys
import os
import re
from pathlib import Path

# 基础目录
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_INI = BASE_DIR / "subconverter" / "advanced.ini"
OUT_CONF = BASE_DIR / "Shadowrocket" / "config" / "ACL4ALL_Advanced.conf"

STATIC_HEADER = """# Shadowrocket 进阶分流配置 (ACL4ALL_Advanced)
# 统一架构: 自动由 subconverter/advanced.ini 转换生成，保持全生态 100% 对齐
# 严禁手动直接修改本文件，请维护 subconverter/advanced.ini
# 更新时间: 自动生成

[General]
bypass-system = true
skip-proxy = 192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,localhost,*.local,captive.apple.com,*.ccb.com,*.abchina.com.cn,*.psbc.com,www.baidu.com
tun-excluded-routes = 10.0.0.0/8, 100.64.0.0/10, 127.0.0.0/8, 169.254.0.0/16, 172.16.0.0/12, 192.0.0.0/24, 192.0.2.0/24, 192.88.99.0/24, 192.168.0.0/16, 198.51.100.0/24, 203.0.113.0/24, 224.0.0.0/4, 255.255.255.255/32, 239.255.255.250/32

dns-server = https://doh.pub/dns-query,https://dns.alidns.com/dns-query,223.5.5.5,119.29.29.29
fallback-dns-server = system
ipv6 = true
prefer-ipv6 = false
dns-direct-system = false
icmp-auto-reply = true
always-reject-url-rewrite = false
private-ip-answer = true
dns-direct-fallback-proxy = true
hijack-dns = 8.8.8.8:53,8.8.4.4:53
udp-policy-not-supported-behaviour = REJECT
block-quic = all-proxy
update-url = https://raw.githubusercontent.com/whjstc/ACL4ALL/main/Shadowrocket/config/ACL4ALL_Advanced.conf

[Proxy]
"""

STATIC_FOOTER = """
[Host]
*.apple.com = server:system
*.icloud.com = server:system
localhost = 127.0.0.1

[URL Rewrite]
^https?://(www.)?g.cn https://www.google.com 302
^https?://(www.)?google.cn https://www.google.com 302

[MITM]
hostname = *.google.cn
"""

# GEOSITE 到 Shadowrocket 规则集的映射表 (blackmatrix7 / ACL4ALL 规则标准)
BM7_PREFIX = "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Shadowrocket"

GEOSITE_MAP = {
    "private": [
        f"RULE-SET,{BM7_PREFIX}/Lan/Lan.list,{{target}}"
    ],
    "google-cn": [
        "DOMAIN-SUFFIX,google.cn,{target}"
    ],
    "category-games@cn": [
        f"RULE-SET,{BM7_PREFIX}/SteamCN/SteamCN.list,{{target}}"
    ],
    "category-game-platforms-download": [
        "RULE-SET,https://cdn.jsdelivr.net/gh/ACL4SSR/ACL4SSR@master/Clash/Ruleset/Download.list,{target}"
    ],
    "category-public-tracker": [
        f"RULE-SET,{BM7_PREFIX}/PrivateTracker/PrivateTracker.list,{{target}}"
    ],
    "telegram": [
        f"RULE-SET,{BM7_PREFIX}/Telegram/Telegram.list,{{target}}"
    ],
    "category-communication": [
        f"RULE-SET,{BM7_PREFIX}/Whatsapp/Whatsapp.list,{{target}}",
        f"RULE-SET,{BM7_PREFIX}/Line/Line.list,{{target}}",
        f"RULE-SET,{BM7_PREFIX}/Signal/Signal.list,{{target}}"
    ],
    "category-social-media-!cn": [
        f"RULE-SET,{BM7_PREFIX}/Twitter/Twitter.list,{{target}}",
        f"RULE-SET,{BM7_PREFIX}/Facebook/Facebook.list,{{target}}",
        f"RULE-SET,{BM7_PREFIX}/Instagram/Instagram.list,{{target}}",
        f"RULE-SET,{BM7_PREFIX}/Threads/Threads.list,{{target}}",
        f"RULE-SET,{BM7_PREFIX}/LinkedIn/LinkedIn.list,{{target}}",
        "DOMAIN-SUFFIX,bsky.app,{target}",
        "DOMAIN-SUFFIX,bsky.network,{target}",
        "DOMAIN-SUFFIX,bsky.social,{target}"
    ],
    "openai": [
        f"RULE-SET,{BM7_PREFIX}/OpenAI/OpenAI.list,{{target}}"
    ],
    "bing": [
        f"RULE-SET,{BM7_PREFIX}/Copilot/Copilot.list,{{target}}",
        f"RULE-SET,{BM7_PREFIX}/Bing/Bing.list,{{target}}"
    ],
    "category-ai-!cn": [
        f"RULE-SET,{BM7_PREFIX}/Claude/Claude.list,{{target}}",
        f"RULE-SET,{BM7_PREFIX}/Gemini/Gemini.list,{{target}}",
        "DOMAIN-KEYWORD,grok,{target}",
        "DOMAIN-SUFFIX,x.ai,{target}"
    ],
    "github": [
        f"RULE-SET,{BM7_PREFIX}/GitHub/GitHub.list,{{target}}"
    ],
    "steam": [
        f"RULE-SET,{BM7_PREFIX}/Steam/Steam.list,{{target}}"
    ],
    "youtube": [
        f"RULE-SET,{BM7_PREFIX}/YouTube/YouTube.list,{{target}}"
    ],
    "apple-tvplus": [
        f"RULE-SET,{BM7_PREFIX}/AppleTV/AppleTV.list,{{target}}"
    ],
    "apple": [
        f"RULE-SET,{BM7_PREFIX}/Apple/Apple.list,{{target}}"
    ],
    "microsoft": [
        f"RULE-SET,{BM7_PREFIX}/Microsoft/Microsoft.list,{{target}}"
    ],
    "googlefcm": [
        f"RULE-SET,{BM7_PREFIX}/GoogleFCM/GoogleFCM.list,{{target}}"
    ],
    "google": [
        f"RULE-SET,{BM7_PREFIX}/Google/Google.list,{{target}}"
    ],
    "tiktok": [
        f"RULE-SET,{BM7_PREFIX}/TikTok/TikTok.list,{{target}}"
    ],
    "netflix": [
        f"RULE-SET,{BM7_PREFIX}/Netflix/Netflix.list,{{target}}"
    ],
    "disney": [
        f"RULE-SET,{BM7_PREFIX}/Disney/Disney.list,{{target}}"
    ],
    "hbo": [
        "DOMAIN-SUFFIX,litix.io,{target}",
        "DOMAIN-SUFFIX,discomax.com,{target}",
        "DOMAIN-SUFFIX,brightline.tv,{target}",
        f"RULE-SET,{BM7_PREFIX}/HBO/HBO.list,{{target}}"
    ],
    "primevideo": [
        f"RULE-SET,{BM7_PREFIX}/PrimeVideo/PrimeVideo.list,{{target}}"
    ],
    "category-emby": [
        f"RULE-SET,{BM7_PREFIX}/Emby/Emby.list,{{target}}"
    ],
    "spotify": [
        f"RULE-SET,{BM7_PREFIX}/Spotify/Spotify.list,{{target}}"
    ],
    "bahamut": [
        f"RULE-SET,{BM7_PREFIX}/Bahamut/Bahamut.list,{{target}}"
    ],
    "category-games": [
        f"RULE-SET,{BM7_PREFIX}/Game/Game.list,{{target}}",
        f"RULE-SET,{BM7_PREFIX}/Epic/Epic.list,{{target}}",
        f"RULE-SET,{BM7_PREFIX}/Sony/Sony.list,{{target}}",
        f"RULE-SET,{BM7_PREFIX}/Nintendo/Nintendo.list,{{target}}"
    ],
    "category-entertainment": [
        f"RULE-SET,{BM7_PREFIX}/GlobalMedia/GlobalMedia.list,{{target}}"
    ],
    "category-ecommerce": [
        f"RULE-SET,{BM7_PREFIX}/Amazon/Amazon.list,{{target}}",
        f"RULE-SET,{BM7_PREFIX}/PayPal/PayPal.list,{{target}}"
    ],
    "gfw": [
        f"RULE-SET,{BM7_PREFIX}/Global/Global.list,{{target}}"
    ],
    "cn": [
        f"RULE-SET,{BM7_PREFIX}/ChinaMax/ChinaMax.list,{{target}}"
    ]
}


def parse_ini(ini_path):
    """解析 advanced.ini 中的策略组与规则列表"""
    with open(ini_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    groups = []
    rulesets = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith(";") or line.startswith("#"):
            continue

        if line.startswith("custom_proxy_group="):
            content = line[len("custom_proxy_group=") :]
            parts = content.split("`")
            gname = parts[0]
            gtype = parts[1]
            groups.append((gname, gtype, parts[2:]))

        elif line.startswith("ruleset="):
            content = line[len("ruleset=") :]
            idx = content.find(",")
            if idx != -1:
                target = content[:idx].strip()
                rule_def = content[idx + 1 :].strip()
                rulesets.append((target, rule_def))

    return groups, rulesets


def generate_sr_groups(groups):
    """转换策略组定义为 Shadowrocket 格式"""
    sr_group_lines = []

    # 按使用逻辑分类排版
    core_names = {"🚀 手动选择", "🇭🇰 香港节点", "🗿 专属节点", "🏠 住宅出口", "🔗 链式中转", "♻️ 自动选择"}
    bottom_names = {"🐟 漏网之鱼", "🔀 非标端口", "🐟 遵循规则", "🎯 全球直连"}
    region_names = {
        "🇺🇸 美国节点", "🇯🇵 日本节点", "🇸🇬 新加坡节点", "🇼🇸 台湾节点", "🇰🇷 韩国节点",
        "🇨🇦 加拿大节点", "🇬🇧 英国节点", "🇫🇷 法国节点", "🇩🇪 德国节点", "🇳🇱 荷兰节点",
        "🇹🇷 土耳其节点", "🌐 其他地区"
    }

    core_defs = []
    biz_defs = []
    region_defs = []
    bottom_defs = []

    for gname, gtype, params in groups:
        if gtype == "url-test":
            # url-test: name`url-test`filter`url`interval`tolerance
            filt = params[0] if len(params) > 0 else ""
            test_url = params[1] if len(params) > 1 and params[1] else "http://www.gstatic.com/generate_204"
            interval = params[2] if len(params) > 2 and params[2] else "300"
            tolerance = params[3] if len(params) > 3 and params[3] else "50"
            line = f"{gname} = url-test,url={test_url},interval={interval},tolerance={tolerance},timeout=5,policy-regex-filter={filt}"

        elif gtype == "select":
            # select 可能是纯正则筛选 (如 住宅出口)，也可能是代理选项列表
            if len(params) == 1 and (params[0].startswith("(?") or params[0].startswith("^")):
                line = f"{gname} = select,policy-regex-filter={params[0]}"
            else:
                # 解析 [] 代理选项
                opts = []
                for p in params:
                    for sub in p.split("[]"):
                        sub = sub.strip()
                        if sub:
                            opts.append(sub)
                line = f"{gname} = select,{','.join(opts)}"
        else:
            # 兼容其他类型
            line = f"{gname} = select,{','.join(params)}"

        if gname in core_names:
            core_defs.append(line)
        elif gname in region_names:
            region_defs.append(line)
        elif gname in bottom_names:
            bottom_defs.append(line)
        else:
            biz_defs.append(line)

    sr_group_lines.append("# ========================================================")
    sr_group_lines.append("# 1. 核心与选择组")
    sr_group_lines.append("# ========================================================")
    sr_group_lines.extend(core_defs)
    sr_group_lines.append("\n# ========================================================")
    sr_group_lines.append("# 2. 核心功能与业务策略组")
    sr_group_lines.append("# ========================================================")
    sr_group_lines.extend(biz_defs)
    sr_group_lines.append("\n# ========================================================")
    sr_group_lines.append("# 3. 地区策略组")
    sr_group_lines.append("# ========================================================")
    sr_group_lines.extend(region_defs)
    sr_group_lines.append("\n# ========================================================")
    sr_group_lines.append("# 4. 兜底与直连组")
    sr_group_lines.append("# ========================================================")
    sr_group_lines.extend(bottom_defs)

    return "\n".join(sr_group_lines)


def generate_sr_rules(rulesets):
    """转换 ruleset 为 Shadowrocket 规则"""
    sr_rule_lines = []

    for target, rdef in rulesets:
        # 1. 远程完整 URL 规则集
        if rdef.startswith("http://") or rdef.startswith("https://"):
            url = rdef.split(",")[0].strip()
            # YouTubeMusic 的特殊处理：增加常用 domain 后缀提升首包速度
            if "YouTubeMusic" in url:
                sr_rule_lines.append(f"DOMAIN-SUFFIX,music.youtube.com,{target}")
                sr_rule_lines.append(f"DOMAIN-SUFFIX,youtubemusic.com,{target}")
                sr_rule_lines.append(f"RULE-SET,{BM7_PREFIX}/YouTubeMusic/YouTubeMusic.list,{target}")
            else:
                sr_rule_lines.append(f"RULE-SET,{url},{target}")

        # 2. clash-classic yaml 非标端口处理
        elif "Custom_Port_Direct" in rdef:
            sr_rule_lines.append(f"# 非标端口处理 (非 80/443 放行)")
            sr_rule_lines.append(f"DST-PORT,1-79,{target}")
            sr_rule_lines.append(f"DST-PORT,81-442,{target}")
            sr_rule_lines.append(f"DST-PORT,444-65535,{target}")

        # 3. Steam CDN
        elif "Steam_CDN" in rdef:
            pass  # 已由 SteamCN.list 覆盖

        # 4. GEOSITE 标签转换
        elif rdef.startswith("[]GEOSITE,"):
            tag = rdef[len("[]GEOSITE,") :].strip()
            mapped = GEOSITE_MAP.get(tag)
            if mapped:
                for m in mapped:
                    sr_rule_lines.append(m.format(target=target))
            else:
                print(f"⚠️  未找到 GEOSITE 标签的 Shadowrocket 映射: {tag}")

        # 5. GEOIP 规则转换
        elif rdef.startswith("[]GEOIP,"):
            parts = rdef[len("[]GEOIP,") :].split(",")
            code = parts[0].strip().upper() if parts[0].strip().lower() == "cn" else parts[0].strip().lower()
            no_resolve = ",no-resolve" if "no-resolve" in rdef else ""
            sr_rule_lines.append(f"GEOIP,{code},{target}{no_resolve}")

        # 6. FINAL 兜底
        elif rdef.startswith("[]FINAL"):
            sr_rule_lines.append(f"\n# 最终兜底\nFINAL,{target}")

    return "\n".join(sr_rule_lines)


def build_config():
    """主构建函数"""
    print(f"🔄 正在从 {SRC_INI.name} 生成 {OUT_CONF.name} ...")
    if not SRC_INI.exists():
        print(f"❌ 找不到源文件: {SRC_INI}")
        sys.exit(1)

    groups, rulesets = parse_ini(SRC_INI)
    print(f"✅ 解析出 {len(groups)} 个策略组, {len(rulesets)} 条规则集配置")

    group_block = generate_sr_groups(groups)
    rule_block = generate_sr_rules(rulesets)

    output_lines = [
        STATIC_HEADER.strip(),
        "\n[Proxy Group]",
        group_block,
        "\n[Rule]",
        rule_block,
        STATIC_FOOTER.strip(),
        ""
    ]

    out_content = "\n".join(output_lines)
    OUT_CONF.parent.mkdir(parents=True, exist_ok=True)
    OUT_CONF.write_text(out_content, encoding="utf-8")
    print(f"🎉 成功生成 Shadowrocket 进阶配置: {OUT_CONF} ({len(out_content.splitlines())} 行)")


if __name__ == "__main__":
    build_config()
