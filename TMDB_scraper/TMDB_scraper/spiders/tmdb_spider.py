import scrapy

class TmdbSpider(scrapy.Spider):
  name = 'tmdb_spider'

  start_urls = ['https://www.themoviedb.org/movie/120-the-lord-of-the-rings-the-fellowship-of-the-ring/']

  def parse(self, response):

    cast_url = response.url + "/cast/"
    yield scrapy.Request(cast_url, callback=self.parse_full_credits)

  def parse_full_credits(self, response):

    actor_urls = [actor.attrib["href"] for actor in response.css("div.info a")]
    for actor_url in actor_urls:
      url = "https://themoviedb.org" + actor_url

      yield scrapy.Request(url, callback = self.parse_actor_page)

  def parse_actor_page(self, response):
    actor_name = response.css("div.title h2 a ::text").getall()
    movies = response.css("a.tooltip bdi::text").getall()

    for movie in movies:
      yield {"actor" : actor_name, "movie_or_TV_name" : movie}
