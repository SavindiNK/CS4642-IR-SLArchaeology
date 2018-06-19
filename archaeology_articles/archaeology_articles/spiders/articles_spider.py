import scrapy

class ArticleSpider(scrapy.Spider):
	name = "articles"

	def start_requests(self):
		urls = [
			"https://www.archaeology.lk/articles",
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for link in response.css('div.tagcloud a.tag-cloud-link::attr(href)').extract():
			yield response.follow(link, self.parse_url)

	def parse_url(self, response):
		for link in response.css('div.blog-posts article h2 a::attr(href)').extract():
			yield response.follow(link, self.parse_article)

	def parse_article(self, response):
		title = response.css('h1.page-title::text').extract_first()
		author_url = response.css('span.meta-author a::attr(href)').extract_first()
		author = response.css('span.meta-author a::text').extract_first()
		category = response.css('span.meta-cats a::text').extract()
		tags = response.css('span.meta-tags a::text').extract()
		timestamp = response.css('span.updated::text').extract_first()
		content = response.css('div.entry-content p::text').extract()

		yield {
			'title': title,
			'author_url': author_url,
			'author':author,
			'category': category,
			'tags': tags,
			'timestamp': timestamp,
			'content': content
		}
