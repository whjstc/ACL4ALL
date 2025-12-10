/**
 * Sub-Store 智能配置生成器
 * 仓库地址: https://github.com/whjstc/ACL4ALL
 * 
 * 用法: 
 * 1. 默认 (advanced): script?subs=All-Nodes
 * 2. 基础版 (basic): script?subs=All-Nodes&config=basic
 */
export default async function (proxies, targetPlatform, args) {
    // 1. 获取参数 (默认为 advanced)
    const configName = args.config || "advanced";

    // 2. 【配置】CDN 路径 (使用 fastly 或 testingcf 加速)
    // 请将 whjstc/ACL4ALL 替换为你真实的 用户名/仓库名
    const CDN_ROOT = "https://testingcf.jsdelivr.net/gh/whjstc/ACL4ALL@main";
    const JSON_URL = `${CDN_ROOT}/dist/${configName}.json`;

    const LANDING_KEYWORD = "住宅落地";
    // 链式组名必须与 ini/json 中的一致
    const CHAIN_GROUP_NAME = "🔗 链式中转";

    // 3. 下载配置 JSON
    let configTemplate = {};
    try {
        // 使用 Sub-Store 内置的 http 工具下载
        const resp = await utils.http.get(JSON_URL);
        configTemplate = typeof resp.body === 'string' ? JSON.parse(resp.body) : resp.body;
    } catch (e) {
        throw new Error(`无法加载配置 [${configName}]: ${e.message}`);
    }

    // 4. 【智能检测】是否存在链式组
    const hasChainGroup = configTemplate.proxyGroups.some(g => g.name === CHAIN_GROUP_NAME);

    console.log(`[ACL4ALL] 加载配置: ${configName}.json | 链式模式: ${hasChainGroup ? "ON" : "OFF"}`);

    // 5. 节点预处理 (注入 dialer-proxy)
    proxies.forEach(p => {
        // 仅在开启链式模式且是落地节点时注入
        if (hasChainGroup && p.name.includes(LANDING_KEYWORD)) {
            p['dialer-proxy'] = CHAIN_GROUP_NAME;
            p['udp'] = true;
            p['skip-cert-verify'] = true;
            p['interface-name'] = ""; // 避免 Meta 绑定错误网卡
        }
    });

    // 6. 填充策略组 (Hydrate)
    const realGroups = configTemplate.proxyGroups.map(g => {
        const filter = g.filter || "";
        g.proxies = [];

        // 逻辑 A: 引用 ([]组名)
        if (filter.includes('[]')) {
            const refs = filter.split('`').map(s => s.replace('[]', '').trim()).filter(s => s);
            g.proxies = refs;
        }
        // 逻辑 B: 正则匹配 (使用更精确的检测)
        // 仅当 filter 以 . * + ? ^ $ { } [ ] ( ) | \ 等正则特殊字符开头，
        // 或包含 (?=) (?!) (?:) 等明确的正则语法时，才视为正则
        else if (/^[\^$.*+?]|^\([\?]|\\[dwsDWS]|\[[^\]]+\]|\{[\d,]+\}/.test(filter)) {
            try {
                const regex = new RegExp(filter, 'i');
                const matched = proxies.filter(p => regex.test(p.name)).map(p => p.name);
                g.proxies = matched.length > 0 ? matched : ["DIRECT"];
            } catch (e) {
                // 正则解析失败，回退到简单匹配
                const matched = proxies.filter(p => p.name.includes(filter)).map(p => p.name);
                g.proxies = matched.length > 0 ? matched : ["DIRECT"];
            }
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

    // 7. 返回最终配置对象
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
}