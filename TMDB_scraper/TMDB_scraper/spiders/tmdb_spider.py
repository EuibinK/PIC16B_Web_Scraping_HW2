import scrapy

class TmdbSpider(scrapy.Spider):
  name = 'tmdb_spider'

  start_urls = ['https://www.themoviedb.org/movie/120-the-lord-of-the-rings-the-fellowship-of-the-ring/']

  def parse(self, response):
    '''
    Tells the spider what to do once it reaches the website
    '''

    # hardcoded url to the Cast & Crew page.
    cast_url = response.url + "/cast/"
    # navigate to the Cast & Crew page and call parse_full_credits()
    yield scrapy.Request(cast_url, callback=self.parse_full_credits)

  def parse_full_credits(self, response):
    '''
    Collects url to the movie's actors/actresses' page.
    Then navigates to each page.
    '''

    # collect a list of actors/actresses url with response.css
    # Note that we are not collecting pages for crew members.
    actor_urls = [actor.attrib["href"] for actor in response.css("ol.people.credits:not(ol.people.credits.crew) li a")]

    for actor_url in actor_urls:
      # generate a full url for each actor/actress' page
      url = "https://themoviedb.org" + actor_url

      # call parse_actor_page on each actor/actress' page
      yield scrapy.Request(url, callback = self.parse_actor_page)

  def parse_actor_page(self, response):
    '''
    Upon reaching each actor/actress' page, collect the name of the actor/actress and
    the name of each of the movies or TV shows on which that person has worked.
    Then yield a dictionary

    '''
    actor_name = response.css("div.title h2 a ::text").get()
    movies = response.css("h3:contains('Acting') + table.card.credits a.tooltip bdi::text").getall()

    # movies = response.css("a.tooltip bdi::text").getall()

    for movie in movies:
      yield {"actor" : actor_name, "movie_or_TV_name" : movie}
