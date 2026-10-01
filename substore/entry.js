/**
 * Sub-Store 智能配置生成器
 * 兼容性修复: 使用 module.exports
 */
module.exports = async function (proxies, targetPlatform, args) {
    // 1. 安全获取参数
    const params = args || {};
    const configName = params.config || "advanced";

    // 2. 配置 CDN 路径
    // ⚠️ 确保这里的地址是你自己的仓库
    const CDN_ROOT = "https://cdn.jsdelivr.net/gh/whjstc/ACL4ALL@main";
    const JSON_URL = `${CDN_ROOT}/dist/${configName}.json`;

    const LANDING_KEYWORD = "住宅落地";
    const CHAIN_GROUP_NAME = "🔗 链式中转";

    // 3. 下载配置 JSON
    let configTemplate = {};
    try {
        // 使用 Sub-Store 内置 global utils
        const resp = await utils.http.get(JSON_URL);
        configTemplate = typeof resp.body === 'string' ? JSON.parse(resp.body) : resp.body;
    } catch (e) {
        throw new Error(`无法加载配置 [${configName}]: ${e.message}`);
    }

    // 4. 智能检测
    const hasChainGroup = configTemplate.proxyGroups && configTemplate.proxyGroups.some(g => g.name === CHAIN_GROUP_NAME);

    console.log(`[ACL4ALL] 加载配置: ${configName}.json | 链式模式: ${hasChainGroup ? "ON" : "OFF"}`);

    // 5. 节点预处理
    proxies.forEach(p => {
        if (hasChainGroup && p.name.includes(LANDING_KEYWORD)) {
            p['dialer-proxy'] = CHAIN_GROUP_NAME;
            p['udp'] = true;
            p['skip-cert-verify'] = true;
            p['interface-name'] = "";
        }
    });

    // 6. 填充策略组
    const realGroups = configTemplate.proxyGroups.map(g => {
        const filter = g.filter || "";
        g.proxies = [];

        // 逻辑 A: 引用
        if (filter.includes('[]')) {
            const refs = filter.split('`').map(s => s.replace('[]', '').trim()).filter(s => s);
            g.proxies = refs;
        }
        // 逻辑 B: 正则
        else if (filter.includes('(?=') || filter.includes('.*') || filter.includes('|') || filter.startsWith('^')) {
            try {
                const regex = new RegExp(filter, 'i');
                const matched = proxies.filter(p => regex.test(p.name)).map(p => p.name);
                g.proxies = matched.length > 0 ? matched : ["DIRECT"];
            } catch (e) { g.proxies = ["DIRECT"]; }
        }
        // 逻辑 C: 简单匹配
        else if (filter) {
            if (g.name === "🏠 住宅出口") {
                g.proxies = proxies.filter(p => p.name.includes(LANDING_KEYWORD)).map(p => p.name);
            } else {
                const matched = proxies.filter(p => p.name.includes(filter)).map(p => p.name);
                g.proxies = matched.length > 0 ? matched : [filter];
            }
        }

        if (!g.proxies || g.proxies.length === 0) g.proxies = ["DIRECT"];
        delete g.filter;
        return g;
    });

    // 7. 返回结果
    return {
        proxies: proxies,
        "proxy-groups": realGroups,
        "rule-providers": configTemplate.ruleProviders,
        rules: configTemplate.rules,
        "mixed-port": 7890,
        "allow-lan": true,
        "mode": "rule",
        "log-level": "info",
        "ipv6": false,
        "external-controller": "0.0.0.0:9090"
    };
};