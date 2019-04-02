import scrapy
from scrapy.exporters import JsonItemExporter

#importa as perguntas do techtudo e salva na pasta adequada

class TechTudoItem(scrapy.Item):
	pergunta = scrapy.Field()
	titulo_pergunta = scrapy.Field()
##
class TechTudoSpider(scrapy.Spider):
	name = 'techtudo-spider'
	start_urls = ['https://forum.techtudo.com.br/perguntas/?ordenacao=ativo&pagina=1'] # primeira pagina de perguntas
	max_pags = 100
	pag_atual = 1
	def parse(self,response):
		item = TechTudoItem()
		self.log('Estou aqui: {}'.format(response.url))
		perguntas = response.css('h2 a::attr(title)').extract() # descricao da pergunta
		titulos = response.css('h2 a::text').extract()
		#titulos_perguntas = response.xpath()
		'''item['pergunta'] = perguntas
		item['titulo_pergunta'] = titulos
		yield item'''
		for pergunta,titulo in zip(perguntas,titulos):
			item['pergunta'] = pergunta
			item['titulo_pergunta'] = titulo
			yield item
		# indo para a prox pagina
		prox_pag = response.css('.botao::attr(href)').extract()[-1] # extraindo ref para a prox pagina
		if prox_pag and self.pag_atual < self.max_pags: # caso nao seja nulo
			self.pag_atual +=1
			url = response.urljoin(prox_pag)
			print('indo para a pagina {} :'.format(prox_pag[prox_pag.rfind('=')+1:]))
			yield scrapy.Request(url,self.parse)