import subprocess, time, re, os
import xml.etree.ElementTree as ET

S = 'localhost:5555'
def log(msg):
    print(msg, flush=True)
    try:
        with open('audit-out/deep-report.txt', 'a', encoding='utf-8') as f:
            f.write(str(msg) + '\n')
    except Exception:
        pass

def sh(*args, timeout=60):
    r = subprocess.run(['adb', '-s', S] + list(args), capture_output=True, text=True, timeout=timeout)
    return (r.stdout or '') + (r.stderr or '')

def shot(name):
    subprocess.run(f"adb -s {S} exec-out screencap -p > audit-out/{name}.png", shell=True)
    log(f'shot {name}')

def dump():
    sh('shell', 'uiautomator', 'dump', '/sdcard/ui.xml')
    xml = sh('shell', 'cat', '/sdcard/ui.xml')
    try: return ET.fromstring(xml)
    except Exception: return None

def nodes(root):
    out = []
    if root is None: return out
    for n in root.iter('node'):
        m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', n.get('bounds') or '')
        if m:
            x1, y1, x2, y2 = map(int, m.groups())
            out.append({'cx': (x1+x2)//2, 'cy': (y1+y2)//2, 'w': x2-x1, 'h': y2-y1,
                        'text': n.get('text') or '', 'desc': n.get('content-desc') or ''})
    return out

def tap_xy(x, y): sh('shell', 'input', 'tap', str(x), str(y))
def key(c): sh('shell', 'input', 'keyevent', str(c))

def tap_text(needle, tries=3):
    for _ in range(tries):
        for nd in nodes(dump()):
            if needle in (nd['text'] + ' ' + nd['desc']):
                log(f'tap "{nd["text"] or nd["desc"]}" at {nd["cx"]},{nd["cy"]}')
                tap_xy(nd['cx'], nd['cy']); return True
        time.sleep(2)
    log(f'tap_text MISS {needle}'); return False

def top():
    m = re.search(r'mResumedActivity:.*?(\S+/\S+)', sh('shell', 'dumpsys', 'activity', 'activities'))
    return m.group(1) if m else '?'

def sniff_count():
    logcat = sh('logcat', '-d', timeout=60)
    pats = ['shouldInterceptRequest', 'VideoParseRuler', 'Sniff', 'sniff']
    hits = {p: sum(1 for ln in logcat.splitlines() if p in ln) for p in pats}
    lines = [ln for ln in logcat.splitlines() if ('parse' in ln.lower() and ('qq' in ln or 'youku' in ln or 'iqiyi' in ln or 'mgtv' in ln or 'http' in ln))][:6]
    return hits, lines

os.makedirs('audit-out', exist_ok=True)
open('audit-out/deep-report.txt', 'w', encoding='utf-8').close()
log('=== launch ===')
sh('shell', 'am', 'start', '-n', 'com.wushisan.tvmax/com.github.tvbox.osc.ui.activity.HomeActivity')
for _ in range(24):
    if 'HomeActivity' in top(): break
    time.sleep(5)
time.sleep(25)
log('top: ' + top())

# ---------- SITE AUDIT: stage 1 FastSearch, stage 2 dialog walk ----------
import json as _json
SITES = _json.loads(r'''[{"key": "csp_douban", "name": "🌕┃豆瓣┃热播", "type": 3, "api": "csp_DouDou", "searchable": 0, "quickSearch": 0}, {"key": "csp_KungFu404", "name": "🔥┃设置Token", "type": 3, "api": "csp_KungFu404", "searchable": 0, "quickSearch": null}, {"key": "APP商店", "name": "🎰┃蜂蜜┃商店", "type": 3, "api": "csp_Market", "searchable": 0, "quickSearch": null}, {"key": "直播转点播", "name": "📺︎┃电视┃点播", "type": 3, "api": "https://raw.liucn.cc/box/libs/tv/zb.min.js", "searchable": 1, "quickSearch": 0}, {"key": "虎牙直播js", "name": "🐯┃虎牙┃直播", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 0, "quickSearch": 0}, {"key": "csp_XYQBiu_斗鱼", "name": "🐟┃斗鱼┃直播", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 0, "quickSearch": 0}, {"key": "玩偶", "name": "👽玩偶哥哥┃4K弹幕", "type": 3, "api": "csp_WoGG", "searchable": 1, "quickSearch": 1}, {"key": "YGP", "name": "🚀┃叨观┃新片", "type": 3, "api": "csp_YGP", "searchable": 0, "quickSearch": 0}, {"key": "alllive", "name": "📽️┃一直播┃LIVE", "type": 3, "api": "csp_Alllive", "searchable": 0, "quickSearch": 0}, {"key": "米搜", "name": "🦋┃米盘┃搜搜", "type": 3, "api": "csp_MIPanSo", "searchable": 1, "quickSearch": 1}, {"key": "抠搜", "name": "🍄┃抠抠┃搜搜", "type": 3, "api": "csp_KkSs", "searchable": 1, "quickSearch": 1}, {"key": "Lib", "name": "🌟┃Lib┃秒播", "type": 3, "api": "csp_Libvio", "searchable": 1, "quickSearch": 1}, {"key": "文采", "name": "💮┃文采┃秒播", "type": 3, "api": "csp_Jpys", "searchable": 1, "quickSearch": 1}, {"key": "糯米", "name": "🍓┃糯米┃秒播", "type": 3, "api": "csp_Nmyswv", "searchable": 1, "quickSearch": 1}, {"key": "苹果", "name": "🍎┃苹果┃IJK", "type": 3, "api": "csp_LiteApple", "searchable": 1, "quickSearch": 1}, {"key": "萌米", "name": "👀┃萌米┃多线", "type": 3, "api": "csp_AppTT", "searchable": null, "quickSearch": null}, {"key": "欢视", "name": "👓┃欢视┃多线", "type": 3, "api": "csp_AppTT", "searchable": 1, "quickSearch": 1}, {"key": "南瓜", "name": "🎃┃南瓜┃多线", "type": 3, "api": "csp_NanGua", "searchable": 1, "quickSearch": 1}, {"key": "热播", "name": "📺┃热播┃多线", "type": 3, "api": "csp_AppTT", "searchable": 1, "quickSearch": 1}, {"key": "可可", "name": "👻┃可可┃多线", "type": 3, "api": "csp_Kekys", "searchable": 1, "quickSearch": 1}, {"key": "zxzj", "name": "🍊┃在线┃外剧", "type": 3, "api": "csp_Zxzj", "searchable": 1, "quickSearch": 1}, {"key": "低端", "name": "⏮️┃低端┃外剧", "type": 3, "api": "csp_Ddrk", "searchable": 1, "quickSearch": 1}, {"key": "贱贱", "name": "🐭┃贱贱┃P2P", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "厂长", "name": "📔┃厂长┃不卡", "type": 3, "api": "csp_NewCz", "searchable": 1, "quickSearch": 1}, {"key": "原创", "name": "☀┃原创┃不卡", "type": 3, "api": "csp_YCyz", "searchable": 1, "quickSearch": 1}, {"key": "比特", "name": "🍄┃Btt┃秒播", "type": 3, "api": "csp_Bttwoo", "searchable": 1, "quickSearch": 1}, {"key": "Auete", "name": "🏝┃Aue┃无广", "type": 3, "api": "csp_Auete", "searchable": 1, "quickSearch": 1}, {"key": "新6V", "name": "🧲┃新6V┃磁力", "type": 3, "api": "csp_SixV", "searchable": 1, "quickSearch": 1}, {"key": "csp_nkvlog", "name": "💢┃耐看┃电影", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_Free", "name": "💰️┃Free┃影院", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_KmeiJu", "name": "🌎┃美剧┃影视", "type": 3, "api": "csp_KmeiJu", "searchable": null, "quickSearch": null}, {"key": "csp_SuBaiBai", "name": "🏳️┃素白┃影视", "type": 3, "api": "csp_SuBaiBai", "searchable": null, "quickSearch": null}, {"key": "csp_Ikan", "name": "💕┃爱看┃影视", "type": 3, "api": "csp_Ikan", "searchable": null, "quickSearch": null}, {"key": "csp_FengGo", "name": "🐕┃疯狗┃影视", "type": 3, "api": "csp_FengGo", "searchable": null, "quickSearch": null}, {"key": "csp_Juqq", "name": "⭕┃剧圈┃影视", "type": 3, "api": "csp_Juqq", "searchable": null, "quickSearch": null}, {"key": "csp_Netfixtv", "name": "💌┃至臻┃影视", "type": 3, "api": "csp_Netfixtv", "searchable": null, "quickSearch": null}, {"key": "csp_Vidhub2", "name": "🎼┃Vid┃影视", "type": 3, "api": "csp_Vidhub2", "searchable": 1, "quickSearch": 1}, {"key": "csp_AppRZ", "name": " 🕵┃忍者┃影视", "type": 3, "api": "csp_AppRZ", "searchable": null, "quickSearch": null}, {"key": "FreeOK", "name": "️️👌┃Fre┃影视", "type": 3, "api": "csp_FreeOK", "searchable": 1, "quickSearch": 1}, {"key": "毛驴", "name": "🦙┃毛驴┃影视", "type": 3, "api": "csp_MaoLv", "searchable": 1, "quickSearch": 1}, {"key": "云播影视", "name": "☁️┃云播┃影视", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "虎虎1", "name": "🐯┃虎虎┃影视", "type": 3, "api": "csp_XBPQ", "searchable": null, "quickSearch": null}, {"key": "csp_SC1080", "name": "🏰┃圣城┃影视", "type": 3, "api": "csp_SC1080", "searchable": 1, "quickSearch": 1}, {"key": "csp_兄弟", "name": "💢┃兄弟┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_Duopan", "name": "🖍︎┃蜡笔┃云盘", "type": 3, "api": "csp_Duopan", "searchable": null, "quickSearch": null}, {"key": "荐片", "name": "🎬┃荐片┃影视", "type": 3, "api": "csp_Jianpian", "searchable": null, "quickSearch": null}, {"key": "csp_Ikanbot", "name": "💋┃爱看┃Bot", "type": 3, "api": "csp_Ikanbot", "searchable": 1, "quickSearch": 1}, {"key": "csp_hanjulao", "name": "🏵┃韩剧┃高清", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "XYQH_JOJO", "name": "🍁┃久久┃影视", "type": 3, "api": "csp_XYQHiker", "searchable": 1, "quickSearch": 1}, {"key": "csp_XYQHiker_VSYY", "name": "🎦┃VS┃影院", "type": 3, "api": "csp_XYQHiker", "searchable": 1, "quickSearch": 1}, {"key": "csp_XYQ素白白", "name": "⛈┃素白白┃影视", "type": 3, "api": "csp_XYQHiker", "searchable": 1, "quickSearch": 1}, {"key": "csp_XYQ电影牛", "name": "🍖┃电影牛┃影院", "type": 3, "api": "csp_XYQHiker", "searchable": 1, "quickSearch": 1}, {"key": "csp_Ysj", "name": "🎀┃异界┃动漫", "type": 3, "api": "csp_Ysj", "searchable": 1, "quickSearch": 1}, {"key": "csp_Dm84", "name": "🚌┃动漫┃巴士", "type": 3, "api": "csp_Dm84", "searchable": 1, "quickSearch": 1}, {"key": "csp_Anime1", "name": "🌸┃日本┃动漫", "type": 3, "api": "csp_Anime1", "searchable": 1, "quickSearch": 1}, {"key": "csp_Ying", "name": "💮┃樱花┃动漫", "type": 3, "api": "csp_Ying", "searchable": 1, "quickSearch": 1}, {"key": "聚短视频js", "name": "📽️聚短┃视频", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 0, "quickSearch": 0}, {"key": "有声小说js", "name": "🎧有声┃小说", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 0, "quickSearch": 0}, {"key": "Aid", "name": "🚑急救┃教学", "type": 3, "api": "csp_FirstAid", "searchable": 0, "quickSearch": 0}, {"key": "夸搜", "name": "🐌夸搜┃搜索", "type": 3, "api": "csp_PanSearch", "searchable": 1, "quickSearch": 1}, {"key": "YiSo", "name": "🎯易搜┃搜索", "type": 3, "api": "csp_YiSo", "searchable": 1, "quickSearch": 1}, {"key": "PanSou", "name": "📀盘搜┃搜索", "type": 3, "api": "csp_PanSou", "searchable": 1, "quickSearch": 1}, {"key": "UpYun", "name": "🌤️Up搜┃搜索", "type": 3, "api": "csp_UpYun", "searchable": 1, "quickSearch": 1}, {"key": "PanSearch", "name": "🏵️盘Se┃搜索", "type": 3, "api": "csp_PanSearch", "searchable": 1, "quickSearch": 1}, {"key": "push_agent", "name": "🛴手机┃推送", "type": 3, "api": "csp_Push", "searchable": 0, "quickSearch": 0}, {"key": "七夜", "name": "🔎┃阿里┃七夜", "type": 3, "api": "csp_Dovx", "searchable": 1, "quickSearch": 1}, {"key": "Zhaozy", "name": "🔍┃阿里┃Zhaozy", "type": 3, "api": "csp_Zhaozy", "searchable": 1, "quickSearch": 1}, {"key": "drpy_js_lf_p2p", "name": "💣┃磁力p2p┃搜索", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/lf_p2p1_min.js", "searchable": null, "quickSearch": null}, {"key": "csp_Nbys", "name": "🛫┃泥巴┃飞", "type": 3, "api": "csp_NiNi", "searchable": 1, "quickSearch": 1}, {"key": "csp_trj", "name": "🛫┃唐人街┃飞", "type": 3, "api": "csp_Tangrenjie", "searchable": 1, "quickSearch": 1}, {"key": "P4_绿豆", "name": "🐼┃绿豆┃影视", "type": 3, "api": "csp_Lvdou", "searchable": 1, "quickSearch": 0}, {"key": "P4_Kuaikan", "name": "👀┃快看┃影视", "type": 3, "api": "csp_Kuaikan", "searchable": 1, "quickSearch": 1}, {"key": "P4_哔嘀", "name": "️️💦┃哔嘀┃影视", "type": 3, "api": "csp_Bdys", "searchable": 1, "quickSearch": 1}, {"key": "P4_皮皮虾", "name": "🦐┃皮皮┃影视", "type": 3, "api": "csp_PipiXia", "searchable": 1, "quickSearch": 1}, {"key": "csp_MeiJu69", "name": "🗽┃六九┃美剧", "type": 3, "api": "csp_AppYsV2", "searchable": 1, "quickSearch": 1}, {"key": "鑫鑫影视", "name": "🥇┃鑫鑫┃App", "type": 3, "api": "csp_AppYsV2", "searchable": 1, "quickSearch": 1}, {"key": "csp_beijihu", "name": "🎪┃极狐┃App", "type": 3, "api": "csp_AppYsV2", "searchable": 1, "quickSearch": 1}, {"key": "益达影视", "name": "🌝┃益达┃App", "type": 3, "api": "csp_AppYsV2", "searchable": 1, "quickSearch": 1}, {"key": "yaya", "name": "💮┃鸭鸭┃App", "type": 3, "api": "csp_AppYsV2", "searchable": 1, "quickSearch": 1}, {"key": "xgapp", "name": "🍉┃西瓜┃v3", "type": 3, "api": "csp_AppYsV2", "searchable": 1, "quickSearch": 1}, {"key": "骑骑影院", "name": "🚵┃骑骑┃v3", "type": 3, "api": "csp_AppYsV2", "searchable": 1, "quickSearch": 1}, {"key": "圣城影视", "name": "🏰┃圣城┃影视", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "爱看影视", "name": "❤┃爱看┃蓝光", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "js_007", "name": "🕵‍┃特工┃影视", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "dr_低端", "name": "🔥┃低端┃Js", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "奇优", "name": " 🍩┃奇优┃影视", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "nangua", "name": "🎃┃南瓜┃影视", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "js_骚火电影", "name": "🔥┃骚火┃影视", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "dr_荐片", "name": "⏳┃荐片┃Js", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "js_Lib", "name": "🍲┃Lib┃影视", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "js_czsapp", "name": "🏭️┃厂长┃Js", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "js_大师兄", "name": "🐵┃师兄┃影视", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "js_电影先生", "name": "🤵┃电影┃先生", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "js_Xinsj", "name": "🐠┃视觉┃影院", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "js_农民", "name": "👨‍🌾┃农民┃影视", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "js_bzys", "name": "🌋┃B站┃影视", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "js_555", "name": "🌟┃三五┃影视", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "dr_iqiyi", "name": "🥝┃爱奇异(官)", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "dr_youku", "name": "🥔┃优酷(官)", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "dr_qq", "name": "🐧┃腾讯(官)", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "dr_mgtv", "name": "🥭┃芒果(官)", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "dr_搜狗", "name": "🚛┃搜狗(官)", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "dr_360影视", "name": "📺┃360(官) ", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "dr_奇珍异兽", "name": "🦍┃奇珍┃异兽", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "dr_腾云驾雾", "name": "☁️┃腾云┃驾雾", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "dr_百忙无果", "name": "🍋┃百忙┃无果", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": null, "quickSearch": null}, {"key": "蚂蚁", "name": "🐜1080P┃蚂蚁", "type": 3, "api": "csp_AppYsV2", "searchable": 1, "quickSearch": 1}, {"key": "即可", "name": "👋1080P┃即刻", "type": 3, "api": "csp_XBPQ", "searchable": null, "quickSearch": null}, {"key": "csp_赞赞", "name": "👌┃赞赞┃切片", "type": 3, "api": "csp_AppYsV2", "searchable": 1, "quickSearch": 1}, {"key": "csp_加速", "name": "🐰┃加速┃APP", "type": 3, "api": "csp_AppYsV2", "searchable": 1, "quickSearch": 1}, {"key": "csp_亮亮", "name": "💡┃亮亮┃APP", "type": 3, "api": "csp_AppYsV2", "searchable": 1, "quickSearch": 1}, {"key": "cc_乌鸦", "name": "🐦┃乌鸦┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "cc_茶杯狐", "name": "🍵┃茶杯┃狐", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "cc_热播之家", "name": "🔥┃热播┃之家", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "cc_shdy2", "name": "🔥┃骚火┃电影", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "cc_黑狐", "name": "🦊┃黑狐┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "cc_蛋蛋", "name": "🥚┃蛋蛋┃看剧", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "cc_相声", "name": "📻┃相声┃合集", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "cc_评书", "name": "📻┃评书┃合集", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "cc_03影院", "name": "🛀┃03┃影院", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_蘑菇", "name": "🍄┃蘑菇┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_胖虎", "name": "🐯┃胖虎┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_蛋蛋", "name": "🌊┃蛋蛋┃影院", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_达龟", "name": "🐢┃达龟┃影院", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_黑狐", "name": "🦝┃黑狐┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_奇优", "name": "🧼┃奇优┃影院", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_TVB", "name": "🅱️┃TVB┃云播", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_骚火", "name": "🅱️┃骚火┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_农民", "name": "🅱️┃农民┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_奇优2", "name": "🅱️┃奇优┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_疯狗", "name": "🅱️┃疯狗┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_万达", "name": "🅱️┃万达┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_爱看", "name": "🅱️┃爱看┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_七新", "name": "🅱️┃七新┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_超前", "name": "🅱️┃超前┃点播", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_玖摇", "name": "🅱️┃4K┃剧院", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_不卡", "name": "🅱️┃不卡┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_午舞", "name": "🅱️┃午舞┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_视觉", "name": "🅱️┃视觉┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_圣城", "name": "🅱️┃圣城┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_好戏", "name": "🅱️┃好戏┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_七月", "name": "🅱️┃七月┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_日后", "name": "🅱️┃348┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_土豪", "name": "🅱️┃土豪┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_兔年", "name": "🅱️┃┃YYDS┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_苹果", "name": "🅱️┃苹果┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_米爱", "name": "🅱️┃米爱┃影视", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_非凡", "name": "🅱️┃非凡┃资源", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_量子", "name": "🅱️┃量子┃资源", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_nkdyw", "name": "💢┃南柯┃电影", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_555电影", "name": "📯┃555┃电影", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_voflix", "name": "🌾┃VOF┃高清", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_nkvod", "name": "💢┃耐看┃电影", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_lkvod", "name": "💢┃来看┃点播", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "csp_SNzy", "name": "🐉┃索尼┃高清", "type": 1, "api": "https://suoniapi.com/api.php/provide/vod/?ac=list", "searchable": 1, "quickSearch": 1}, {"key": "csp_非凡资源", "name": "🥗┃非凡┃资源", "type": 1, "api": "https://api.ffzyapi.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 1}, {"key": "量子资源", "name": "🥑┃量子┃资源", "type": 1, "api": "https://lzizy1.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 1}, {"key": "feisu", "name": "🛰️飞速┃采集", "type": 1, "api": "https://www.feisuzyapi.com/api.php/provide/vod/?ac=list", "searchable": 1, "quickSearch": null}, {"key": "虎牙", "name": "🐯虎牙采集", "type": 1, "api": "https://www.huyaapi.com/api.php/provide/vod/from/hym3u8", "searchable": 1, "quickSearch": 1}, {"key": "火狐", "name": "🦊火狐采集", "type": 1, "api": "https://hhzyapi.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 0}, {"key": "百度", "name": "🎏百度┃采集", "type": 1, "api": "https://api.apibdzy.com/api.php/provide/vod/?ac=list", "searchable": 1, "quickSearch": null}, {"key": "js_4KHDR", "name": "🧲世界磁力┃Js", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "js_6V", "name": "✡️六维磁力┃Js", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "js_磁力熊", "name": "🐻‍贝尔磁力┃Js", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "js_酷吧", "name": "😎酷吧磁力┃Js", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "XYQH_电影港", "name": "🛳┃港口┃磁力", "type": 3, "api": "csp_XYQHiker", "searchable": null, "quickSearch": null}, {"key": "csp_MeijuMi", "name": "🧲美剧迷", "type": 3, "api": "csp_MeijuMi", "searchable": 1, "quickSearch": 1}, {"key": "csp_Xunlei8", "name": "🧲迅雷吧", "type": 3, "api": "csp_Xunlei8", "searchable": 1, "quickSearch": 1}, {"key": "mtv_xp_维奇动漫", "name": "🐼维奇丨动漫", "type": 3, "api": "csp_XBPQ", "searchable": 0, "quickSearch": 0}, {"key": "cctv", "name": "📺央视｜大全", "type": 3, "api": "csp_CCTV", "searchable": 0, "quickSearch": null}, {"key": "py_cctv_少儿", "name": "📺央视｜少儿", "type": 3, "api": "py_cctv_full", "searchable": 0, "quickSearch": 0}, {"key": "央视经典", "name": "📺央视｜经典", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 1}, {"key": "csp_XPath_企鹅体育", "name": "🐧企鹅┃直播", "type": 3, "api": "csp_XPath", "searchable": 0, "quickSearch": 0}, {"key": "py_qie", "name": "🏀┃企鹅┃体育", "type": 3, "api": "py_qie", "searchable": 0, "quickSearch": 0}, {"key": "py_cctv", "name": "❤️┃央视┃py", "type": 3, "api": "py_cctv", "searchable": 0, "quickSearch": 0}, {"key": "MV_vod", "name": "🎶明星┃MV", "type": 1, "api": "https://mv.wogg.link/mv/vod", "searchable": 1, "quickSearch": 0}, {"key": "csp_Yj1211", "name": "📽️网红┃直播", "type": 3, "api": "csp_Yj1211", "searchable": 1, "quickSearch": 1}, {"key": "csp_酷奇", "name": "🎤┃酷奇┃音乐", "type": 3, "api": "csp_XBPQ", "searchable": 0, "quickSearch": 0}, {"key": "88js", "name": "⚽ 88┃看球", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 0, "quickSearch": 0}, {"key": "csp_qiumi", "name": "⚽ Jrs┃球迷", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 0, "quickSearch": 0}, {"key": "csp_310直播", "name": "⚽310┃看球", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 0, "quickSearch": 0}, {"key": "酷奇js", "name": "🎤酷奇┃MV", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 0, "quickSearch": 0}, {"key": "js_武享吧", "name": "🥎┃格斗┃直播", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "js_a8音乐", "name": "🎸┃奥迪┃音乐", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "csp_短剧", "name": "🎧刷刷｜短剧", "type": 3, "api": "csp_XBPQ", "searchable": 0, "quickSearch": 0}, {"key": "csp_聚短视频", "name": "📽️聚短┃视频", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili短剧", "name": "🎦┃短剧┃BiL", "type": 3, "api": "csp_Bili", "searchable": 1, "quickSearch": 1}, {"key": "XBPQ_葡萄", "name": "🎦┃短剧┃葡萄", "type": 3, "api": "csp_XBPQ", "searchable": null, "quickSearch": null}, {"key": "csp_XBPQ_aoaotv", "name": "🎦┃短剧┃嗷嗷", "type": 3, "api": "csp_XBPQ", "searchable": 1, "quickSearch": 1}, {"key": "Bili", "name": "🅱哔哔┃合集", "type": 3, "api": "csp_Bili", "searchable": 1, "quickSearch": 0}, {"key": "Biliych", "name": "🅱哔哔┃歌曲", "type": 3, "api": "csp_Bili", "searchable": 1, "quickSearch": 0}, {"key": "dr_童趣", "name": "🧗‍┃童趣┃播视", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 1, "quickSearch": 1}, {"key": "dr_兔小贝", "name": "📚儿童┃启蒙", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 0, "quickSearch": 0}, {"key": "少儿教育", "name": "📚少儿┃教育", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "小学课堂", "name": "📚小学┃课堂", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "初中课堂", "name": "📚初中┃课堂", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "高中教育", "name": "📚高中┃课堂", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili", "name": "🅱️┃哔哩┃合集", "type": 3, "api": "csp_Bili", "searchable": 1, "quickSearch": 0}, {"key": "csp_Bili_dashan", "name": "💋┃搭讪┃教程", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili__dapei", "name": "💃┃搭配┃教程", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "js_B站精简", "name": "🅱️┃哔哩┃精简", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_meishi", "name": "🅱️┃美食┃合集", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_youer", "name": "🅱️┃幼儿┃教育", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_xiaoxue", "name": "🅱️┃小学┃教育", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_czxx", "name": "🅱️┃初中┃教育", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_gaozxx", "name": "🅱️┃高中┃教育", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_zyy", "name": "🅱️┃中医┃药区", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_xuqu1", "name": "🅱️┃戏曲┃合集", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_TYjs", "name": "🅱️┃体育┃健身", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_xiangsh", "name": "🅱️┃相声┃小品", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_FBqx", "name": "🅱️┃球队┃球星", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_Meinvw", "name": "🅱️┃美女┃舞蹈", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_yanchh", "name": "🅱️┃歌手┃合集", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_Nvtuan", "name": "🅱️┃女团┃热舞", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_MTV", "name": "🅱️┃歌曲┃演唱", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "csp_Bili_Yinl2", "name": "🅱️┃音悦┃合集", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0}, {"key": "js_哔哩直播", "name": "🅱️┃哔哩┃直播", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/drpy2.min.js", "searchable": 0, "quickSearch": 0}, {"key": "drpy_js_Alist", "name": "网盘 | Alist[js]", "type": 3, "api": "https://raw.liucn.cc/box/libs/js/alist.min.js", "searchable": null, "quickSearch": null}, {"key": "本地", "name": "本地存储", "type": 3, "api": "csp_Local", "searchable": 0, "quickSearch": null}, {"key": "AList", "name": "AList", "type": 3, "api": "csp_AList", "searchable": 1, "quickSearch": null}, {"key": "WebDAV", "name": "WebDAV", "type": 3, "api": "csp_WebDAV", "searchable": 1, "quickSearch": null}, {"key": "csp_AList", "name": "小雅｜云盘", "type": 3, "api": "csp_AList", "searchable": 1, "quickSearch": 1}, {"key": "短视频", "name": "📱┃网红┃美女", "type": 3, "api": "csp_XBPQ", "searchable": 0, "quickSearch": 0}, {"key": "极速资源", "name": "🚀┃极速┃资源", "type": 1, "api": "https://jszyapi.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 1}, {"key": "光速资源", "name": "💡┃光速┃资源", "type": 1, "api": "https://api.guangsuapi.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 1}, {"key": "iKun资源", "name": "🏀┃iKun┃资源", "type": 1, "api": "https://ikunzyapi.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 1}, {"key": "速播资源", "name": "⏩┃速播┃资源", "type": 1, "api": "https://subocaiji.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 1}, {"key": "金鹰资源", "name": "🦅┃金鹰┃资源", "type": 1, "api": "https://jinyingzy.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 1}, {"key": "最大资源", "name": "🏆┃最大┃资源", "type": 1, "api": "https://api.zuidapi.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 1}, {"key": "樱花资源", "name": "🌸┃樱花┃资源", "type": 1, "api": "https://m3u8.apiyhzy.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 1}, {"key": "三六零资源", "name": "🔄┃三六零┃资源", "type": 1, "api": "https://360zy.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 1}, {"key": "天涯资源", "name": "🌅┃天涯┃资源", "type": 1, "api": "https://tyyszy.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 1}, {"key": "魔都资源", "name": "🏙️┃魔都┃资源", "type": 1, "api": "https://www.mdzyapi.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 1}, {"key": "暴风采集", "name": "🌪️暴风影音", "type": 1, "api": "https://bfzyapi.com/api.php/provide/vod/", "searchable": null, "quickSearch": null}]''')
log('=== site audit: ' + str(len(SITES)) + ' sites ===')
CHROME = {'首页','历史','直播','搜索','收藏','推送','文件','豆瓣热播','请选择数据源','全部显示'}
def core(name):
    return re.sub(r'[^一-鿿A-Za-z0-9]', '', name or '')
def content_score(texts, sitename):
    keep = []
    for t in texts:
        if not t or len(t) < 2: continue
        if t in CHROME: continue
        if t == sitename: continue
        if re.match(r'^\d{1,2}月\d{1,2}日$', t): continue
        if re.match(r'^(周.|星期.)?\s*\d{1,2}:\d{2}$', t): continue
        if t.startswith('评分'): continue
        if re.match(r'^\d+(\.\d+)?$', t): continue
        keep.append(t)
    return keep

# ---- stage 1: FastSearch union over two Douban posters ----
search_alive = {}
def fastsearch_collect(tag):
    tap_text('热播剧集' if tag == 'drama' else '热播电影')
    time.sleep(8)
    ns = nodes(dump())
    grid = [n for n in ns if n['text'] and n['cy'] > 150]
    if grid:
        p = grid[0]
        tap_xy(max(p['cx'], 120), p['cy'])
    for w in range(10):
        time.sleep(4)
        if 'FastSearchActivity' in top(): break
    last_count, stable = -1, 0
    found = {}
    for i in range(20):
        time.sleep(5)
        ns = nodes(dump())
        cnt = -1
        for n in ns:
            m = re.search(r'搜索结果\s*[:：]\s*(\d+)', n['text'])
            if m: cnt = int(m.group(1))
        for n in ns:
            if n['cx'] < 330 and n['text'] and n['text'] not in ('全部显示',):
                for s in SITES:
                    if n['text'] == s['name'] or core(n['text']) == core(s['name']):
                        found[s['key']] = s['name']
        log(f'fastsearch {tag} poll {i}: count={cnt} sites_so_far={len(found)}')
        if cnt == last_count and cnt >= 0:
            stable += 1
            if stable >= 3: break
        else:
            stable = 0
        last_count = cnt
    key(4); time.sleep(3)
    if 'HomeActivity' not in top():
        key(4); time.sleep(3)
    return found

for tag in ('drama', 'movie'):
    try:
        got = fastsearch_collect(tag)
        search_alive.update(got)
        log(f'fastsearch {tag}: +{len(got)} sites, union={len(search_alive)}')
    except Exception as e:
        log(f'fastsearch {tag} EXC: {type(e).__name__} {e}')
log('SEARCH_ALIVE_KEYS: ' + ','.join(sorted(search_alive.keys())))

# ---- stage 2: walk every site not proven alive ----
SKIP_KEYS = {'csp_douban', 'csp_KungFu404'}
targets = [s for s in SITES if s['key'] not in search_alive and s['key'] not in SKIP_KEYS]
log(f'walk targets: {len(targets)}')
def open_dialog():
    key(82); time.sleep(4)
def find_in_dialog(name, clamp_first=False):
    if clamp_first:
        for _ in range(90): key(19)
        time.sleep(2)
    for step in range(70):
        ns = nodes(dump())
        hit = [n for n in ns if n['text'] == name or core(n['text']) == core(name)]
        if hit: return hit[0]
        for _ in range(3): key(20); time.sleep(0.35)
        time.sleep(1.2)
    return None

results = {}
for idx, s in enumerate(targets):
    name, skey = s['name'], s['key']
    verdict, evidence = 'DEAD', ''
    try:
        open_dialog()
        hit = find_in_dialog(name)
        if hit is None:
            open_dialog()
            hit = find_in_dialog(name, clamp_first=True)
        if hit is None:
            verdict, evidence = 'NOT_FOUND_IN_DIALOG', ''
        else:
            tap_xy(hit['cx'], hit['cy'])
            time.sleep(12)
            for attempt in range(2):
                ns = nodes(dump())
                texts = [n['text'] for n in ns if n['text']]
                switched = any(t == name or core(t) == core(name) for t in texts)
                keep = content_score(texts, name)
                if switched and len(keep) >= 4:
                    verdict = 'ALIVE'; evidence = 'n=%d %s' % (len(keep), ' | '.join(keep[:6])); break
                if attempt == 0:
                    time.sleep(10)
                    verdict = 'DEAD' if switched else 'NO_SWITCH'
                    evidence = 'n=%d %s' % (len(keep), ' | '.join(keep[:6]))
            if verdict != 'ALIVE':
                shot(f'audit-dead-{idx}')
    except Exception as e:
        verdict, evidence = 'ERROR', f'{type(e).__name__} {e}'
    results[skey] = verdict
    log(f"AUDIT | {skey} | {name} | {verdict} | {evidence}")
    if 'HomeActivity' not in top():
        key(4); time.sleep(2)
log('WALK_RESULTS: ' + _json.dumps(results, ensure_ascii=False))
alive_total = len(search_alive) + sum(1 for v in results.values() if v == 'ALIVE')
log(f'AUDIT TOTALS: search_alive={len(search_alive)} walk_alive={sum(1 for v in results.values() if v=="ALIVE")} dead={sum(1 for v in results.values() if v=="DEAD")} no_switch={sum(1 for v in results.values() if v=="NO_SWITCH")} not_found={sum(1 for v in results.values() if v=="NOT_FOUND_IN_DIALOG")} error={sum(1 for v in results.values() if v=="ERROR")}')


log('crash buffer bytes: ' + str(len(sh('logcat', '-b', 'crash', '-d').strip())))
log('=== DONE ===')
print('DONE')
