
import json, re, time, sys
from concurrent.futures import ThreadPoolExecutor
import requests

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
TV_CONFIGS = [{"name": "饭太硬", "url": "http://www.饭太硬.net/tv"}, {"name": "肥猫", "url": "http://肥猫.net/"}, {"name": "老刘备", "url": "https://raw.liucn.cc/box/m.json"}, {"name": "小马", "url": "https://szyyds.cn/tv/x.json"}, {"name": "摸鱼儿", "url": "http://www.y456y.com"}, {"name": "王二小", "url": "http://new.王二小放牛娃.top"}, {"name": "小盒子4K", "url": "http://xhztv.top/4k.json"}, {"name": "创享影视", "url": "https://ys.cxkjg.cn/api/provide/tvbox"}, {"name": "影仓", "url": "http://124.71.19.220/c/1"}, {"name": "伦理接口", "url": "http://47.96.82.41:5188/rose/18/xgg.json"}, {"name": "小盒子单仓", "url": "http://xhztv.top/xhz"}, {"name": "嗷呜", "url": "http://itv666.cc/aowu/config.webp"}, {"name": "无名", "url": "https://6800.kstore.vip/fish.json"}, {"name": "小盒子多仓", "url": "http://xhztv.top/dc"}, {"name": "拾光多仓", "url": "http://xmbjm.fh4u.org/dc.txt"}, {"name": "挺好分享多仓", "url": "http://ztha.top/TVBox/GYCK.json"}, {"name": "小盒子", "url": "https://www.xhztv.pro/"}]
ONLINE = [{"name": "No影视", "url": "https://novipnoad.org/"}, {"name": "注视影视", "url": "https://gaze.red/"}, {"name": "搜TV啦", "url": "https://www.sotvla.cc/"}, {"name": "雪落影视", "url": "https://xlys.me/"}, {"name": "多瑙影视", "url": "https://www.duonaovod.com"}, {"name": "白嫖者联盟", "url": "https://www.tdgo.shop"}, {"name": "蛋蛋魔法", "url": "https://ddmf.net"}, {"name": "青空次元", "url": "https://www.sorani.net"}, {"name": "APP影院", "url": "https://www.appmovie.art"}, {"name": "爱电影", "url": "https://kuhh4jo.com"}, {"name": "金牌影视", "url": "https://www.vv3nwjk.com"}, {"name": "937影视", "url": "https://www.937tv.vip"}, {"name": "爱壹帆", "url": "https://iyf.tv"}, {"name": "厂长资源", "url": "https://www.czzymovie.com"}, {"name": "LIBVIO", "url": "https://libviobd.com"}, {"name": "Auete影视", "url": "https://www.aeete.com"}, {"name": "电影人生", "url": "https://dyrs.tv"}, {"name": "奈飞工厂", "url": "https://www.netflixgc.com"}, {"name": "奈菲影视", "url": "https://www.nfyingshi.com"}, {"name": "泥视频", "url": "https://www.nivod.vip"}, {"name": "PPnix", "url": "https://www.ppnix.com/cn/"}, {"name": "独播库", "url": "https://www.dbku.tv"}, {"name": "布布追剧", "url": "https://bubuzhuiju.com"}, {"name": "影猫仓库", "url": "https://www.ymck.pro"}, {"name": "爱看机器人", "url": "https://www1.aikanbot.com"}, {"name": "91毒舌", "url": "https://www.duse0.com/"}, {"name": "光速影视", "url": "https://www.yingshiso.link/"}, {"name": "好好看", "url": "https://www.hhkan2.com/"}, {"name": "IFN", "url": "https://ifn.watch/register?code=8B1EF6"}, {"name": "4k影视", "url": "https://www.4kvm.cc/"}, {"name": "饭搭子影视", "url": "https://fdzys.com"}, {"name": "SA视频", "url": "https://www.lsjys11.com/"}, {"name": "奈飞工厂", "url": "https://naifei.fyi/"}, {"name": "剧OK", "url": "https://juok3.top/"}, {"name": "蛋蛋奇", "url": "https://www.dandanqi.cc/"}, {"name": "宅男影视", "url": "https://zndy.top/"}, {"name": "影视大全", "url": "https://yingshidaquan.top/"}, {"name": "剧踪影院", "url": "https://www.juzong01.me/"}, {"name": "简云影视", "url": "https://jianyunys.com/"}, {"name": "片库", "url": "https://4k01.pianku.online/"}, {"name": "66 大片网", "url": "https://www.77dpw.vip/"}, {"name": "嘀嗒影视", "url": "https://www.didahd.xyz/"}, {"name": "追影", "url": "https://zhuiying3.cc/"}, {"name": "歪比巴卜", "url": "https://wbbb1.com/"}, {"name": "开心影院", "url": "https://www.kxyy1.cc/"}, {"name": "豆花电影网", "url": "https://dhvideo.cc/"}, {"name": "ZIP0", "url": "https://zip0.com/?r=KBDIG8"}, {"name": "爱盼", "url": "https://www.aipan.me/"}, {"name": "可可影视", "url": "https://www.kkys14.com/"}, {"name": "樱之空", "url": "https://skr.skr1.cc:666/"}, {"name": "洛雪TV", "url": "https://tv.lxyy.club/"}, {"name": "西瓜影视", "url": "https://www.kanmovie.com/"}, {"name": "创享影视", "url": "https://ys.cxkjg.cn/"}]

def fetch(url, timeout=20):
    try:
        r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=True)
        return r.status_code, r.text
    except Exception as e:
        return None, f'ERR {type(e).__name__}: {e}'

def parse_config(text):
    if not text: return None
    t = '\n'.join(l for l in text.splitlines() if not l.strip().startswith('//'))
    try:
        return json.loads(t)
    except Exception:
        return None

def extract_sites(cfg):
    out = []
    for s in cfg.get('sites', []) or []:
        api = str(s.get('api', ''))
        out.append({'key': s.get('key'), 'name': s.get('name'), 'type': s.get('type'), 'api': api})
    return out

def nested_urls(cfg, text):
    urls = []
    if isinstance(cfg, dict):
        for k in ('urls', 'storeHouse', 'list'):
            v = cfg.get(k)
            if isinstance(v, list):
                for e in v:
                    if isinstance(e, dict) and e.get('url'): urls.append(e['url'])
                    elif isinstance(e, str) and e.startswith('http'): urls.append(e)
    if not urls and text:
        urls = re.findall(r'https?://[^\s"\'<>\]]+?\.json\b', text)[:10]
    return urls[:10]

results = {'configs': [], 'online': []}

def do_config(entry, depth=0):
    url = entry['url']
    code, text = fetch(url)
    rec = {'name': entry['name'], 'url': url, 'http': code}
    cfg = parse_config(text) if code == 200 else None
    if cfg and isinstance(cfg, dict) and cfg.get('sites'):
        sites = extract_sites(cfg)
        rec['kind'] = 'config'
        rec['site_count'] = len(sites)
        rec['apis'] = [s for s in sites if s['api'].startswith('http') and s['type'] in (0, 1)]
        rec['other_sites'] = sum(1 for s in sites if not (s['api'].startswith('http') and s['type'] in (0, 1)))
    elif depth == 0:
        nurls = nested_urls(cfg, text if code == 200 else '')
        if nurls:
            rec['kind'] = 'multirepo'
            rec['nested'] = []
            for nu in nurls[:8]:
                sub = do_config({'name': entry['name'] + ' > ' + nu[:40], 'url': nu}, depth=1)
                rec['nested'].append(sub)
        else:
            rec['kind'] = 'unparsed'
            rec['note'] = (text or '')[:120].replace('\n', ' ')
    else:
        rec['kind'] = 'unparsed'
    return rec

def do_online(entry):
    from urllib.parse import urlparse
    u = urlparse(entry['url'])
    api = f'{u.scheme}://{u.netloc}/api.php/provide/vod/?ac=list'
    code, text = fetch(api, timeout=15)
    rec = {'name': entry['name'], 'url': entry['url'], 'probe': api, 'http': code}
    data = parse_config(text) if code == 200 else None
    if isinstance(data, dict) and isinstance(data.get('class'), list):
        rec['verdict'] = 'MACCMS_HIT'
        rec['class_count'] = len(data['class'])
        rec['total'] = data.get('total')
        rec['classes'] = [c.get('type_name') for c in data['class'][:8]]
    elif isinstance(data, dict):
        rec['verdict'] = 'JSON_NO_CLASS'
        rec['keys'] = list(data.keys())[:8]
    else:
        rec['verdict'] = 'MISS'
    return rec

print('== configs ==', flush=True)
with ThreadPoolExecutor(max_workers=4) as ex:
    for rec in ex.map(do_config, TV_CONFIGS):
        results['configs'].append(rec)
        print(rec['name'], rec['kind'], rec.get('site_count', ''), 'apis:', len(rec.get('apis', [])), flush=True)
print('== online maccms probe ==', flush=True)
with ThreadPoolExecutor(max_workers=5) as ex:
    for rec in ex.map(do_online, ONLINE):
        results['online'].append(rec)
        print(rec['name'], rec['verdict'], rec.get('class_count', ''), flush=True)

import os
os.makedirs('mine-out', exist_ok=True)
json.dump(results, open('mine-out/mine-report.json', 'w'), ensure_ascii=False, indent=1)
hits = [r for r in results['online'] if r['verdict'] == 'MACCMS_HIT']
cfgs = [r for r in results['configs'] if r['kind'] == 'config']
allapis = []
for r in cfgs: allapis += r.get('apis', [])
for r in results['configs']:
    for sub in r.get('nested', []) or []:
        if sub.get('kind') == 'config': allapis += sub.get('apis', [])
with open('mine-out/mine-summary.md', 'w', encoding='utf8') as f:
    f.write(f"# zhuiju mining\n\nconfigs parsed: {len(cfgs)}, type0/1 APIs extracted: {len(allapis)}\n")
    f.write(f"online maccms hits: {len(hits)}/{len(results['online'])}\n\n## maccms hits\n")
    for h in hits: f.write(f"- {h['name']} {h['probe']} classes={h['class_count']} total={h['total']}\n")
    f.write("\n## config APIs (sample)\n")
    for a in allapis[:200]: f.write(f"- [{a['type']}] {a['name']} {a['api']}\n")
print('DONE', flush=True)
