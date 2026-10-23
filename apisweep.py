
import json, os
import requests
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
APIS = [{"key": "csp_SNzy", "name": "🐉┃索尼┃高清", "api": "https://suoniapi.com/api.php/provide/vod/?ac=list"}, {"key": "csp_非凡资源", "name": "🥗┃非凡┃资源", "api": "https://api.ffzyapi.com/api.php/provide/vod/"}, {"key": "量子资源", "name": "🥑┃量子┃资源", "api": "https://lzizy1.com/api.php/provide/vod/"}, {"key": "feisu", "name": "🛰️飞速┃采集", "api": "https://www.feisuzyapi.com/api.php/provide/vod/?ac=list"}, {"key": "虎牙", "name": "🐯虎牙采集", "api": "https://www.huyaapi.com/api.php/provide/vod/from/hym3u8"}, {"key": "火狐", "name": "🦊火狐采集", "api": "https://hhzyapi.com/api.php/provide/vod/"}, {"key": "百度", "name": "🎏百度┃采集", "api": "https://api.apibdzy.com/api.php/provide/vod/?ac=list"}, {"key": "MV_vod", "name": "🎶明星┃MV", "api": "https://mv.wogg.link/mv/vod"}, {"key": "极速资源", "name": "🚀┃极速┃资源", "api": "https://jszyapi.com/api.php/provide/vod/"}, {"key": "光速资源", "name": "💡┃光速┃资源", "api": "https://api.guangsuapi.com/api.php/provide/vod/"}, {"key": "iKun资源", "name": "🏀┃iKun┃资源", "api": "https://ikunzyapi.com/api.php/provide/vod/"}, {"key": "速播资源", "name": "⏩┃速播┃资源", "api": "https://subocaiji.com/api.php/provide/vod/"}, {"key": "金鹰资源", "name": "🦅┃金鹰┃资源", "api": "https://jinyingzy.com/api.php/provide/vod/"}, {"key": "最大资源", "name": "🏆┃最大┃资源", "api": "https://api.zuidapi.com/api.php/provide/vod/"}, {"key": "樱花资源", "name": "🌸┃樱花┃资源", "api": "https://m3u8.apiyhzy.com/api.php/provide/vod/"}, {"key": "三六零资源", "name": "🔄┃三六零┃资源", "api": "https://360zy.com/api.php/provide/vod/"}, {"key": "天涯资源", "name": "🌅┃天涯┃资源", "api": "https://tyyszy.com/api.php/provide/vod/"}, {"key": "魔都资源", "name": "🏙️┃魔都┃资源", "api": "https://www.mdzyapi.com/api.php/provide/vod/"}, {"key": "暴风采集", "name": "🌪️暴风影音", "api": "https://bfzyapi.com/api.php/provide/vod/"}]
out = []
for a in APIS:
    url = a['api']
    test = url + ('&ac=list' if '?' in url else '?ac=list')
    verdict, detail = 'FAIL', ''
    for attempt in range(2):
        try:
            r = requests.get(test, headers=UA, timeout=20)
            if r.status_code == 200:
                try:
                    d = r.json()
                    if isinstance(d, dict) and isinstance(d.get('class'), list) and len(d['class']) > 0:
                        verdict = 'ALIVE'; detail = f"classes={len(d['class'])} total={d.get('total')}"; break
                    elif isinstance(d, dict):
                        verdict = 'WEAK'; detail = 'json no class: ' + ','.join(list(d.keys())[:5]); break
                    else:
                        verdict = 'WEAK'; detail = 'json not dict'
                except Exception:
                    verdict = 'WEAK'; detail = 'http200 non-json ' + r.text[:60].replace('\n',' ')
            else:
                detail = f'http {r.status_code}'
        except Exception as e:
            detail = f'ERR {type(e).__name__}'
    out.append({'key': a['key'], 'name': a['name'], 'api': a['api'], 'verdict': verdict, 'detail': detail})
    print(a['name'], verdict, detail, flush=True)
os.makedirs('apisweep-out', exist_ok=True)
json.dump(out, open('apisweep-out/apisweep-report.json','w'), ensure_ascii=False, indent=1)
with open('apisweep-out/apisweep-summary.md','w',encoding='utf8') as f:
    for o in out: f.write(f"- {o['verdict']} | {o['name']} | {o['api']} | {o['detail']}\n")
print('APIS DONE')

import socket as _socket
CANDS = json.loads(r'''[{"name": "👒┃小胡┃资源┃", "api": "http://c.小胡.icu/api.php/provide/vod/", "host": "c.小胡.icu", "pre_dead": true, "source": "老刘备"}, {"name": "🐉┃索尼┃高清", "api": "https://suoniapi.com/api.php/provide/vod/?ac=list", "host": "suoniapi.com", "pre_dead": false, "source": "老刘备"}, {"name": "🕹️淘片┃采集", "api": "https://taopianapi.com/cjapi/mc/vod/json.html", "host": "taopianapi.com", "pre_dead": true, "source": "老刘备"}, {"name": "🥗┃非凡┃资源", "api": "http://ffzy1.tv/api.php/provide/vod/", "host": "ffzy1.tv", "pre_dead": true, "source": "老刘备"}, {"name": "🥑┃量子┃资源", "api": "https://lzizy1.com/api.php/provide/vod/", "host": "lzizy1.com", "pre_dead": false, "source": "老刘备"}, {"name": "🦁┃四九┃资源", "api": "https://49zy1.com/api.php/provide/vod/?ac=list", "host": "49zy1.com", "pre_dead": true, "source": "老刘备"}, {"name": "🛰️飞速┃采集", "api": "https://www.feisuzyapi.com/api.php/provide/vod/?ac=list", "host": "www.feisuzyapi.com", "pre_dead": false, "source": "老刘备"}, {"name": "🐯┃奇虎┃采集", "api": "https://caiji.qhzyapi.com/api.php/provide/vod/", "host": "caiji.qhzyapi.com", "pre_dead": true, "source": "老刘备"}, {"name": "⛱┃可可┃采集", "api": "https://kekezy1.com/api.php/provide/vod/?ac=list", "host": "kekezy1.com", "pre_dead": true, "source": "老刘备"}, {"name": "🐯虎牙采集", "api": "https://www.huyaapi.com/api.php/provide/vod/from/hym3u8", "host": "www.huyaapi.com", "pre_dead": false, "source": "老刘备"}, {"name": "🦊火狐采集", "api": "https://hhzyapi.com/api.php/provide/vod/", "host": "hhzyapi.com", "pre_dead": false, "source": "老刘备"}, {"name": "🌪️暴风影音", "api": "https://app.bfzyapi.com/api.php/provide/vod/", "host": "app.bfzyapi.com", "pre_dead": false, "source": "老刘备"}, {"name": "🎏百度┃采集", "api": "https://api.apibdzy.com/api.php/provide/vod/?ac=list", "host": "api.apibdzy.com", "pre_dead": false, "source": "老刘备"}, {"name": "🎶明星┃MV", "api": "https://mv.wogg.link/mv/vod", "host": "mv.wogg.link", "pre_dead": false, "source": "老刘备"}, {"name": "🎹┃MTV┃合集", "api": "https://mv.wogg.link/mv/vod", "host": "mv.wogg.link", "pre_dead": false, "source": "老刘备"}, {"name": "🌟 创享影视", "api": "http://ys.cxkjg.cn/api/provide/vod", "host": "ys.cxkjg.cn", "pre_dead": false, "source": "创享影视"}, {"name": "📡 金鹰", "api": "http://ys.cxkjg.cn/api/provide/vod?source=2680151544", "host": "ys.cxkjg.cn", "pre_dead": false, "source": "创享影视"}, {"name": "📡 闪电", "api": "http://ys.cxkjg.cn/api/provide/vod?source=3848762792", "host": "ys.cxkjg.cn", "pre_dead": false, "source": "创享影视"}, {"name": "📡 非凡", "api": "http://ys.cxkjg.cn/api/provide/vod?source=1840804598", "host": "ys.cxkjg.cn", "pre_dead": false, "source": "创享影视"}, {"name": "📡 量子", "api": "http://ys.cxkjg.cn/api/provide/vod?source=1470828922", "host": "ys.cxkjg.cn", "pre_dead": false, "source": "创享影视"}, {"name": "📡 WS", "api": "http://ys.cxkjg.cn/api/provide/vod?source=4118858385", "host": "ys.cxkjg.cn", "pre_dead": false, "source": "创享影视"}, {"name": "📡 速博", "api": "http://ys.cxkjg.cn/api/provide/vod?source=1016684692", "host": "ys.cxkjg.cn", "pre_dead": false, "source": "创享影视"}, {"name": "📡 HD(SN)", "api": "http://ys.cxkjg.cn/api/provide/vod?source=1208629981", "host": "ys.cxkjg.cn", "pre_dead": false, "source": "创享影视"}, {"name": "📡 红牛", "api": "http://ys.cxkjg.cn/api/provide/vod?source=2761253814", "host": "ys.cxkjg.cn", "pre_dead": false, "source": "创享影视"}, {"name": "📡 U酷", "api": "http://ys.cxkjg.cn/api/provide/vod?source=4194624554", "host": "ys.cxkjg.cn", "pre_dead": false, "source": "创享影视"}, {"name": "📡 光速", "api": "http://ys.cxkjg.cn/api/provide/vod?source=4247318859", "host": "ys.cxkjg.cn", "pre_dead": false, "source": "创享影视"}, {"name": "📡 樱花", "api": "http://ys.cxkjg.cn/api/provide/vod?source=531717376", "host": "ys.cxkjg.cn", "pre_dead": false, "source": "创享影视"}, {"name": "🧿艾旦┃蓝光", "api": "https://lovedan.net/api.php/provide/vod/", "host": "lovedan.net", "pre_dead": false, "source": "伦理接口"}, {"name": "🧿乐播┃资源", "api": "https://lbapi9.com/api.php/provide/vod/at/json/?ac=list", "host": "lbapi9.com", "pre_dead": false, "source": "伦理接口"}, {"name": "🧿量子┃资源", "api": "https://cj.lziapi.com/api.php/provide/vod/?ac=list", "host": "cj.lziapi.com", "pre_dead": false, "source": "伦理接口"}, {"name": "🧿gay┃资源", "api": "https://slapibf.com/api.php/provide/vod/?ac=list", "host": "slapibf.com", "pre_dead": false, "source": "伦理接口"}, {"name": "🧿桃花┃资源", "api": "https://thzy1.me/api.php/provide/vod/?ac=list", "host": "thzy1.me", "pre_dead": false, "source": "伦理接口"}, {"name": "🧿正品┃影视", "api": "https://lbapi9.com/api.php/provide/vod/", "host": "lbapi9.com", "pre_dead": false, "source": "伦理接口"}, {"name": "🧿大地┃采集", "api": "https://dadiapi.com/api.php", "host": "dadiapi.com", "pre_dead": false, "source": "伦理接口"}, {"name": "🧿凤凰┃影视", "api": "http://fhapi9.com/api.php/provide/vod/", "host": "fhapi9.com", "pre_dead": false, "source": "伦理接口"}, {"name": "🧿番外┃采集", "api": "http://fhapi9.com/api.php/provide/vod/", "host": "fhapi9.com", "pre_dead": false, "source": "伦理接口"}, {"name": "🧿妞妞┃影视", "api": "https://api.niuniuzy.me/api.php/provide/vod/", "host": "api.niuniuzy.me", "pre_dead": false, "source": "伦理接口"}, {"name": "49Z｜影视", "api": "https://49zyw.com/api.php/provide/vod/?ac=list", "host": "49zyw.com", "pre_dead": false, "source": "小盒子多仓 > 小盒子多仓 > https://jihulab.com/xuanzhuapp/xzys/-/ra"}, {"name": "红牛｜资源", "api": "https://www.hongniuzy2.com/api.php/provide/vod/", "host": "www.hongniuzy2.com", "pre_dead": false, "source": "小盒子多仓 > 小盒子多仓 > https://jihulab.com/xuanzhuapp/xzys/-/ra"}, {"name": "光速｜资源", "api": "http://api.guangsuapi.com/api.php/provide/vod/", "host": "api.guangsuapi.com", "pre_dead": false, "source": "小盒子多仓 > 小盒子多仓 > https://jihulab.com/xuanzhuapp/xzys/-/ra"}, {"name": "极速｜资源", "api": "https://jszyapi.com/api.php/provide/vod/", "host": "jszyapi.com", "pre_dead": false, "source": "小盒子多仓 > 小盒子多仓 > https://jihulab.com/xuanzhuapp/xzys/-/ra"}, {"name": "快车｜资源", "api": "https://caiji.kczyapi.com/api.php/provide/vod/", "host": "caiji.kczyapi.com", "pre_dead": false, "source": "小盒子多仓 > 小盒子多仓 > https://jihulab.com/xuanzhuapp/xzys/-/ra"}, {"name": "索尼｜资源", "api": "https://suoniapi.com/api.php/provide/vod/", "host": "suoniapi.com", "pre_dead": false, "source": "小盒子多仓 > 小盒子多仓 > https://jihulab.com/xuanzhuapp/xzys/-/ra"}, {"name": "量子｜资源", "api": "https://cj.lziapi.com/api.php/provide/vod/", "host": "cj.lziapi.com", "pre_dead": false, "source": "小盒子多仓 > 小盒子多仓 > https://jihulab.com/xuanzhuapp/xzys/-/ra"}, {"name": "非凡｜资源", "api": "http://cj.ffzyapi.com/api.php/provide/vod/", "host": "cj.ffzyapi.com", "pre_dead": false, "source": "小盒子多仓 > 小盒子多仓 > https://jihulab.com/xuanzhuapp/xzys/-/ra"}, {"name": "暴风", "api": "https://bfzyapi.com/api.php/provide/vod", "host": "bfzyapi.com", "pre_dead": false, "source": "小盒子多仓 > 小盒子多仓 > https://dxawi.github.io/0/0.json"}, {"name": "IK", "api": "https://ikunzyapi.com/api.php/provide/vod/from/ikm3u8/", "host": "ikunzyapi.com", "pre_dead": false, "source": "小盒子多仓 > 小盒子多仓 > https://dxawi.github.io/0/0.json"}, {"name": "海外看(墙外)", "api": "https://haiwaikan.com/api.php/provide/vod", "host": "haiwaikan.com", "pre_dead": false, "source": "小盒子多仓 > 小盒子多仓 > https://dxawi.github.io/0/0.json"}]''')
def _doh(host):
    try:
        r = requests.get(f'https://cloudflare-dns.com/dns-query?name={host}&type=A',
                         headers={'Accept':'application/dns-json','User-Agent':UA['User-Agent']}, timeout=15)
        dd = r.json()
        if dd.get('Status') == 3: return 'NXDOMAIN'
        if dd.get('Answer'): return 'RESOLVES'
        return 'NOANSWER'
    except Exception:
        try: _socket.getaddrinfo(host, 80); return 'RESOLVES_LOCAL'
        except Exception: return 'UNRESOLVED'
_cout = []
for _c in CANDS:
    if _c['pre_dead']:
        _cout.append({**_c, 'cloud': 'PRE_DEAD_BOCE', 'doh': 'SKIP', 'detail': '今早国内拨测已证死，不再复验'})
        continue
    _url, _verdict, _detail = _c['api'], 'FAIL', ''
    _test = _url + ('&ac=list' if '?' in _url else '?ac=list')
    for _att in range(2):
        try:
            _r = requests.get(_test, headers=UA, timeout=20)
            if _r.status_code == 200:
                try:
                    _d = _r.json()
                    if isinstance(_d, dict) and isinstance(_d.get('class'), list) and _d['class']:
                        _verdict = 'ALIVE'; _detail = f"classes={len(_d['class'])}"; break
                    _verdict = 'WEAK'; _detail = 'json无class'; break
                except Exception: _verdict = 'WEAK'; _detail = 'http200非json'; break
            _detail = f'http {_r.status_code}'
        except Exception as _e: _detail = f'ERR {type(_e).__name__}'
    _doh_s = _doh(_c['host'])
    _cout.append({**_c, 'cloud': _verdict, 'doh': _doh_s, 'detail': _detail})
    print(_c['name'], _c['host'], _verdict, _doh_s, _detail, flush=True)
json.dump(_cout, open('apisweep-out/candidates-sweep.json','w'), ensure_ascii=False, indent=1)
with open('apisweep-out/candidates-summary.md','w',encoding='utf8') as _f:
    for _o in _cout: _f.write(f"- {_o['cloud']} / {_o['doh']} | {_o['name']} | {_o['api']} | {_o['detail']}\n")
print('CANDS DONE')
