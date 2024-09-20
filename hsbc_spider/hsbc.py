# -*- coding:utf-8
# __author__ : funny
# __create_time__ : 16/11/6 10:41
import requests
import json
import pymysql
# https://www.services.cn-banking.hsbc.com.cn/PublicContent/common/rate/zh/exchange-rates.html
import config


class ExchangeRateSpider(object):
    def craw(self):
        html_cont = self.download(
            'https://www.services.cn-banking.hsbc.com.cn/mobile/channel/digital-proxy/cnyTransfer/ratesInfo/remittanceRate')
        rate_date, rate_data = self.parse(html_cont)
        self.add_rate(rate_date, rate_data)

    def add_rate(self, rate_date, rate_data):
        if rate_data is None or len(rate_data) == 0:
            return
        print(rate_date, rate_data)
        connection = pymysql.connect(**config.dbconfig)
        with connection.cursor() as cursor:
            for rate in rate_data:
                if rate['exchangeRateCurrency'] == 'CNY':
                    continue
                rate1 = 1 / float(rate['transferBuyingRate'])
                sql = 'INSERT INTO hsbc_rate (date,type,' \
                      'trans_buy_rate,trans_sell_rate,notes_buy_rate,notes_sell_rate,' \
                      'trans_buy_rate1)' \
                      ' values("' + rate_date + '","' + rate['exchangeRateCurrency'] + \
                      '",' + rate['transferBuyingRate'] + ',' + rate['transferSellingRate'] + ',' + rate[
                          'notesBuyingRate'] + ',' + rate['notesSellingRate'] + \
                      ',' + str(rate1) + ')'
                print(sql)
                cursor.execute(sql)
        connection.commit()
        connection.close()

    def download(self, url):
        requests.adapters.DEFAULT_RETRIES = 3
        response = requests.get(url, timeout=3, headers={'Content-type': 'application/json'})
        response.encoding = 'utf-8'
        if response.status_code != 200:
            return None
        return response.content.decode("utf-8")

    def parse(self, html_cont):
        print(html_cont)
        if html_cont is None:
            return
        cont_json = json.loads(html_cont)
        rate_date = cont_json['data']['lastUpdateDate']
        rate_data = cont_json['data']['counterForRepeatingBlock']
        return rate_date, rate_data


def rate_job():
    obj_spider = ExchangeRateSpider()
    obj_spider.craw()


rate_job()
