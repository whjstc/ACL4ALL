/**
 * VVebo 终极修复脚本 (TimeLine + Fans) for Shadowrocket
 * 整合自: bin64 & suiyuran
 * 功能：修复用户主页时间线、修复粉丝列表显示
 */

let url = $request.url;
let method = $request.method;

// 辅助函数：从 URL 提取 UID
const getUid = (url) => {
    let match = url.match(/uid=(\d+)/);
    return match ? match[1] : null;
};

// ---------------------------
// 1. 请求部分 (http-request)
// ---------------------------
if (typeof $response === "undefined") {
    // [功能 A] 拦截 UID：同时监听 users/show 和 remind/unread_count 以确保获取成功
    if (url.includes("users/show") || url.includes("remind/unread_count")) {
        let uid = getUid(url);
        if (uid) {
            $persistentStore.write(uid, "vvebo_uid");
            console.log(`[VVebo] UID已捕获: ${uid}`);
        }
        $done({});
    } 
    // [功能 B] 重定向时间线接口
    else if (url.includes("statuses/user_timeline")) {
        let uid = getUid(url) || $persistentStore.read("vvebo_uid");
        if (uid) {
            // 将 user_timeline 替换为 profile/statuses/tab
            url = url.replace("statuses/user_timeline", "profile/statuses/tab")
                     .replace("max_id", "since_id");
            // 构造新的 containerid
            url = url + `&containerid=230413${uid}_-_WEIBO_SECOND_PROFILE_WEIBO`;
            console.log(`[VVebo] 时间线重定向成功`);
            $done({ url: url });
        } else {
            console.log(`[VVebo] 未找到UID，无法重定向`);
            $done({});
        }
    } 
    else {
        $done({});
    }
} 

// ---------------------------
// 2. 响应部分 (http-response)
// ---------------------------
else {
    // [功能 C] 重构时间线数据格式
    if (url.includes("profile/statuses/tab")) {
        try {
            let data = JSON.parse($response.body);
            let statuses = [];
            
            // 提取并扁平化微博卡片
            if (data.cards) {
                statuses = data.cards
                    .map((card) => (card.card_group ? card.card_group : card))
                    .flat()
                    .filter((card) => card.card_type === 9) // 过滤出微博正文类型
                    .map((card) => card.mblog)
                    .map((status) =>
                        status.isTop
                            ? { ...status, label: "置顶" }
                            : status
                    );
            }
            
            let sinceId = (data.cardlistInfo && data.cardlistInfo.since_id) ? data.cardlistInfo.since_id : 0;
            
            // 构造旧版 API 格式
            $done({
                body: JSON.stringify({
                    statuses,
                    since_id: sinceId,
                    total_number: 100,
                }),
            });
        } catch (e) {
            console.log(`[VVebo] 时间线数据解析失败: ${e}`);
            $done({});
        }
    } 
    // [功能 D] 修复粉丝列表 (去除干扰项)
    else if (url.includes("cardlist") && url.includes("selffans")) {
        try {
            let data = JSON.parse($response.body);
            // 过滤掉 itemid 为 INTEREST_PEOPLE2 (感兴趣的人) 的卡片
            if (data.cards) {
                let originalCount = data.cards.length;
                let cards = data.cards.filter((card) => card.itemid !== "INTEREST_PEOPLE2");
                
                if (originalCount !== cards.length) {
                    console.log(`[VVebo] 已净化粉丝列表`);
                }
                $done({ body: JSON.stringify({ ...data, cards }) });
            } else {
                $done({});
            }
        } catch (e) {
            console.log(`[VVebo] 粉丝列表解析失败: ${e}`);
            $done({});
        }
    } 
    else {
        $done({});
    }
}
