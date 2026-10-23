
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
print('DONE')
