# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from rb_api.items import RbApiItem
from scrapy.exceptions import CloseSpider

class RiobrancoSpider(scrapy.Spider):
    name = 'RioBranco'
    allowed_domains = ['extranet.frsp.org']
    start_urls = ['https://extranet.frsp.org/Arearestrita2/FRB/Login.aspx']
    urls = ['https://extranet.frsp.org/AreaRestrita2/FRB/Boletim.aspx',
    'https://extranet.frsp.org/areaRestrita2/FichaFinanceiraFRSP/FichaFinanceira.aspx']
   
    #usage: scrapy crawl RioBranco -a user= -a password=

    def __init__(self, user='', password='', **kwargs):
        super().__init__(**kwargs)
        self.rb_user = user
        self.rb_password = password

    def parse(self, response):
        self.log('visitando a página de login: {}'.format(response.url))
        yield scrapy.FormRequest.from_response(
            response,
            url=response.url,
            formdata={'UserName' : self.rb_user, 'Password': self.rb_password},
            callback=self.logged_in)
    
    def logged_in(self, response): 
        login = response.css('a[id="ctl00_LoginStatus2"]').extract_first()
        if login is None:
           raise CloseSpider('Não foi possível fazer login COD: 1')
        yield scrapy.Request(
            url=self.urls[0],
            callback=self.boletim,
        )

    def boletim(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            url=response.url,
            formdata={
                '__VIEWSTATE': response.xpath("//input[@name='__VIEWSTATE']/@value").extract(),
                '__EVENTVALIDATION': response.xpath("//input[@name='__EVENTVALIDATION']/@value").extract(),
                '__EVENTTARGET': 'ctl00$contentCentro$rptBoletim$ctl09$Reserved_AsyncLoadTarget'
            },
            callback=self.parse_boletim)
       
    def parse_boletim(self, response):
        mainTable = response.css('table[style="border-collapse:collapse;"]').css('tr[valign="top"]')
        td = mainTable[1].css('td').xpath('@class').extract()
        if td is None:
            raise CloseSpider('Não foi possível obter os dados do usuário COD: 2')
        for row in mainTable[1:len(td)]:
            disc = row.css('td[class="{}"] div::text'.format(td[1])).extract_first()
            av1 = row.css('td[class="{}"] div::text'.format(td[2])).extract_first()
            av2 = row.css('td[class="{}"] div::text'.format(td[3].split()[0])).extract_first()
            exame = row.css('td[class="{}"] div::text'.format(td[4].split()[0])).extract_first() 
            media = row.css('td[class="{}"] div::text'.format(td[5].split()[0])).extract_first()
            resultado = row.css('td[class="{}"] div::text'.format(td[6])).extract_first()
            print(disc)
            boletim = RbApiItem(disciplina=disc, av1=av1,av2=av2,exame=exame,media=media,resultado=resultado)
            yield boletim
          # yield {'disciplina': disc, 'av1': av1, 'av2': av2, 'exame': exame, 'media' : media, 'resultado' : resultado}
        
        #RESOURCES = {'crawl.json': 'resources.py'}
        #DEBUG = False
