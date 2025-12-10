const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 配置输入输出目录
const SRC_DIR = path.join(__dirname, '../subconverter');
const DIST_DIR = path.join(__dirname, '../dist');

// 辅助函数：生成 Provider 名称
function getProviderName(url) {
    return "RP_" + crypto.createHash('md5').update(url).digest('hex').substring(0, 8).toUpperCase();
}

// 核心转换函数
function convertIniToJson(filename) {
    const iniPath = path.join(SRC_DIR, filename);
    const iniContent = fs.readFileSync(iniPath, 'utf-8');

    const config = {
        proxyGroups: [],
        ruleProviders: {},
        rules: []
    };

    const lines = iniContent.split('\n');

    lines.forEach(line => {
        line = line.trim();
        if (!line || line.startsWith(';')) return;

        // 解析策略组
        if (line.startsWith('custom_proxy_group=')) {
            const content = line.replace('custom_proxy_group=', '');
            const parts = content.split('`');
            if (parts.length >= 2) {
                const name = parts[0];
                const type = parts[1];

                const group = { name, type };

                // 根据不同类型解析不同参数
                if (type === 'select') {
                    // select 类型: name`select`filter1`filter2`...
                    group.filter = parts.slice(2).join('`');
                } else if (type === 'url-test' || type === 'fallback') {
                    // url-test/fallback 类型: name`type`filter`url`interval`tolerance
                    group.filter = parts[2] || "";
                    group.url = parts[3] || "http://www.gstatic.com/generate_204";
                    group.interval = parseInt(parts[4]) || 300;
                    group.tolerance = parseInt(parts[5]) || 50;
                    group.lazy = true;
                } else if (type === 'load-balance') {
                    // load-balance 类型: name`type`filter`url`interval`strategy
                    group.filter = parts[2] || "";
                    group.url = parts[3] || "http://www.gstatic.com/generate_204";
                    group.interval = parseInt(parts[4]) || 300;
                    group.strategy = parts[5] || "consistent-hashing";
                } else {
                    // 其他类型，保持原逻辑
                    group.filter = parts[2] || "";
                }

                config.proxyGroups.push(group);
            }
        }

        // 解析 ruleset
        if (line.startsWith('ruleset=')) {
            const firstCommaIndex = line.indexOf(',');
            if (firstCommaIndex === -1) return;
            const targetGroup = line.substring(8, firstCommaIndex).trim();
            let ruleSource = line.substring(firstCommaIndex + 1).trim();

            if (ruleSource.startsWith('[]')) {
                const raw = ruleSource.replace('[]', '');
                if (raw === 'FINAL') config.rules.push(`MATCH,${targetGroup}`);
                else config.rules.push(`${raw},${targetGroup}`);
            } else {
                // 处理 clash-domain/classic 前缀
                let behavior = 'classical';
                if (ruleSource.startsWith('clash-domain:')) {
                    behavior = 'domain';
                    ruleSource = ruleSource.replace('clash-domain:', '');
                } else if (ruleSource.startsWith('clash-classic:')) {
                    behavior = 'classical';
                    ruleSource = ruleSource.replace('clash-classic:', '');
                }

                const providerName = getProviderName(ruleSource);
                config.ruleProviders[providerName] = {
                    type: "http",
                    behavior: behavior,
                    url: ruleSource,
                    path: `./ruleset/${providerName}.yaml`,
                    interval: 86400
                };
                config.rules.push(`RULE-SET,${providerName},${targetGroup}`);
            }
        }

        // 解析规则指向 (custom_rule_group)
        if (line.startsWith('custom_rule_group=')) {
            const [ruleName, groupName] = line.replace('custom_rule_group=', '').split('`');
            if (ruleName && groupName) {
                config.rules.push(`RULE-SET,${ruleName},${groupName}`);
            }
        }
    });

    return config;
}

// 主程序：遍历并处理
if (!fs.existsSync(DIST_DIR)) fs.mkdirSync(DIST_DIR, { recursive: true });

fs.readdirSync(SRC_DIR).forEach(file => {
    if (path.extname(file) === '.ini') {
        try {
            console.log(`正在转换: ${file}...`);
            const jsonConfig = convertIniToJson(file);
            const outName = file.replace('.ini', '.json');
            fs.writeFileSync(path.join(DIST_DIR, outName), JSON.stringify(jsonConfig, null, 2));
            console.log(`✅ 生成成功: dist/${outName}`);
        } catch (e) {
            console.error(`❌ 转换失败 ${file}:`, e.message);
        }
    }
});