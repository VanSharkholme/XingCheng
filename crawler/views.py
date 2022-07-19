from django.shortcuts import render
from django.http import FileResponse
import requests
import time
import urllib3
import datetime
import json
import xlwings as xw
import pandas as pds


# Create your views here.

def crawler(request):
    context = {}
    if request.method == 'POST':
        try:
            p_code = request.POST.get('code')
            p_code = str(p_code).split('\r\n')

            # codes = list(p_code)
            # for code in p_code:
            #     print(type(code))
            temp = p_code

            urllib3.disable_warnings()
            pds.set_option('display.max_columns', None)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
            url_zd = 'https://74.push2.eastmoney.com/api/qt/clist/get?&pn=1&pz=8000&po=0&np=1&fltt=2&invt=2&fid=f12&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f12,f21'
            url_zj = 'https://push2.eastmoney.com/api/qt/clist/get?fid=f12&po=0&pz=8000&pn=1&np=1&fltt=2&invt=2&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2&fields=f12%2Cf62'

            try:
                wb = xw.Book('输出.xlsx')
            except FileNotFoundError:
                app = xw.App(visible=False, add_book=True)
                wb = app.books.add()

            sht1 = wb.sheets(1)

            print('开始工作')
            sht1.clear()

            # with open('股票池.txt', 'r', encoding='utf-8') as f:  # 获取股票池，存入temp
            #     temp = f.read()
            # temp = temp.split('\n')
            # while '' in temp:
            #     temp.remove('\r')

            for i, v in enumerate(temp):
                if len(v) > 6:
                    temp[i] = v[-6:]

            for code in temp:
                if code[0] == str(3):
                    temp.remove(code)

            pds_old = pds.DataFrame(temp, columns=['code'])
            pds_jzc = pds.DataFrame(columns=['code', 'name', '每股净资产', '市盈率'])
            pds_sshy = pds.DataFrame(columns=['code', '所属行业'])
            pds_hlma = pds.DataFrame(
                columns=['code', '10最高点', '10最低点', '30平均成交量', '当日涨幅', '昨日涨幅', '收盘价格', '昨日换手', '今日换手', '昨日成交量', '今日成交量',
                         '开盘涨跌'])
            pds_zj = pds.DataFrame(columns=['code', '今天资金流向', '昨日资金流向'])
            for code in pds_old['code'].values:
                if code[0] == str(6):
                    url_jzc = 'http://push2.eastmoney.com/api/qt/stock/get?invt=2&fltt=2&fields=f57,f58,f162,f92&secid=1.' + code
                    url_k = 'http://3.push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.' + code + '&fields1=f1&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf57%2Cf59%2Cf61&klt=101&fqt=0&end=20500101&lmt=30'
                    url_zj = 'https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?&lmt=0&klt=101&fields1=f1&fields2=f51%2Cf52&secid=1.' + code
                else:
                    url_jzc = 'http://push2.eastmoney.com/api/qt/stock/get?invt=2&fltt=2&fields=f57,f58,f162,f92&secid=0.' + code
                    url_k = 'http://3.push2his.eastmoney.com/api/qt/stock/kline/get?secid=0.' + code + '&fields1=f1&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf57%2Cf59%2Cf61&klt=101&fqt=0&end=20500101&lmt=30'
                    url_zj = 'https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?&lmt=0&klt=101&fields1=f1&fields2=f51%2Cf52&secid=0.' + code

                try:
                    rqst = requests.get(url_jzc, headers=headers, verify=False, timeout=2)
                    time.sleep(0.5)
                    temp = json.loads(rqst.text)['data']
                    pds_jzc.loc[len(pds_jzc)] = {'code': temp['f57'], 'name': temp['f58'], '每股净资产': temp['f92'],
                                                 '市盈率': temp['f162']}
                except:
                    pass
                url_sshy = 'https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_F10_CORETHEME_CONTENT&columns=MAINPOINT_CONTENT&filter=(SECURITY_CODE%3D%22' + code + '%22)'
                try:
                    rqst = requests.get(url_sshy, headers=headers, verify=False, timeout=2)
                    time.sleep(0.5)
                    temp = json.loads(rqst.text)['result']['data'][0]['MAINPOINT_CONTENT']
                    pds_sshy.loc[len(pds_sshy)] = {'code': code, '所属行业': temp}
                except:
                    pass
                try:
                    rqst = requests.get(url_k, headers=headers, verify=False, timeout=2)
                    time.sleep(0.5)
                    temp = json.loads(rqst.text)['data']['klines']
                    h_10 = 0
                    l_10 = 100000
                    cje_ma30 = 0

                    for ii in temp:
                        ii_list = ii.split(',')
                        cje_ma30 = cje_ma30 + float(ii_list[-3])
                    cje_ma30 = int(cje_ma30 / len(temp))
                    for ii in temp[-10:]:
                        h_10 = max(h_10, float(ii.split(',')[3]))
                        l_10 = min(l_10, float(ii.split(',')[4]))
                    pds_hlma.loc[len(pds_hlma)] = {'code': code, '10最高点': h_10, '10最低点': l_10, '30平均成交量': cje_ma30,
                                                   '当日涨幅': temp[-1].split(',')[-2], '昨日涨幅': temp[-2].split(',')[-2],
                                                   '收盘价格': temp[-1].split(',')[2], '昨日换手': temp[-2].split(',')[-1],
                                                   '今日换手': temp[-1].split(',')[-1], '昨日成交量': temp[-2].split(',')[-3],
                                                   '今日成交量': temp[-1].split(',')[-3], '开盘涨跌': round(
                            (float(temp[-1].split(',')[1]) - float(temp[-2].split(',')[2])) * 100 / float(
                                temp[-2].split(',')[2]), 2)}

                    rqst = requests.get(url_zj, headers=headers, verify=False, timeout=2)
                    temp = json.loads(rqst.text)['data']['klines']
                    pds_zj.loc[len(pds_zj)] = {'code': code, '昨日资金流向': temp[-2].split(',')[1],
                                               '今天资金流向': temp[-1].split(',')[1]}
                except:
                    pass

            url_date = 'http://58.push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.000001&fields1=f1&fields2=f51&klt=101&fqt=1&end=20500101&lmt=1'
            rqst = requests.get(url_date, headers=headers, verify=False, timeout=2)
            date = json.loads(rqst.text)['data']['klines'][0]
            date = date.replace('-', '')
            url_zt = 'http://push2ex.eastmoney.com/getTopicZTPool?ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.ztzt&Pageindex=0&pagesize=300&sort=c%3Aasc&date=' + date
            rqst = requests.get(url_zt, headers=headers, verify=False, timeout=2)
            pds_zt = pds.DataFrame(json.loads(rqst.text)['data']['pool'])
            pds_zt = pds_zt[['c', 'fbt', 'lbt']]
            pds_zt.rename(columns={'c': 'code'}, inplace=True)

            rqst = requests.get(url_zd, headers=headers, verify=False, timeout=2)
            pds_zd = pds.DataFrame(json.loads(rqst.text)['data']['diff'])
            pds_zd.columns = ['code', '流通市值']

            pds_old = pds.merge(pds_old, pds_jzc, on='code', how='left')
            pds_old = pds.merge(pds_old, pds_sshy, on='code', how='left')
            pds_old = pds.merge(pds_old, pds_hlma, on='code', how='left')
            pds_old = pds.merge(pds_old, pds_zj, on='code', how='left')
            pds_last = pds.merge(pds_old, pds_zt, on='code', how='left')
            pds_last = pds.merge(pds_last, pds_zd, on='code', how='left')
            sht1.range('a1').value = pds_last

            wb.save('输出.xlsx')
            wb.close()
            try:
                app.quit()
            except NameError:
                # app = xw.apps.active
                # app.quit()
                pass
            context['status'] = '运行结束'
            # context['link'] = ''
        except:
            context['status'] = '程序出错'

        if __name__ == '__main__':
            pass
    return render(request, 'crawler/crawler.html', context)


def download(request):
    t = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    timestamp = '输出-' + str(t) + '.xlsx'
    response = FileResponse(open('输出.xlsx', 'rb'), as_attachment=True, filename=timestamp)
    return response
