# wex-pan

Wex (newwex) TVBox 配置的纯网盘版：从源配置 https://9280.kstore.vip/newwex.json 裁剪，只保留 30 个网盘仓（配置中心、我的网盘、豆瓣首页、网盘 4K 站 17 个、115 分享、Alist、WebDav、盘搜 5 个、推送），删除采集/直播/短剧/动漫/听书/音乐/体育/Emby/哔哩等站点与顶层 lives 直播数组；其余配置（spider / parses / doh / rules / ads / headers）原样保留。站点名称已去除装饰 emoji，保持整洁。

- 每天北京时间 16:00 由 GitHub Actions 自动拉取源配置、按同一规则重新裁剪（trim.py）并提交，内容无变化时不产生新提交；更新后自动清理 jsDelivr 缓存。

## 订阅链接

- GitHub Raw: https://raw.githubusercontent.com/q1azq1a/wex-pan/main/newwex-pan.json
- jsDelivr: https://gcore.jsdelivr.net/gh/q1azq1a/wex-pan@main/newwex-pan.json
