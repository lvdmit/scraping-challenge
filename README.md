# scraping-challenge
The goal of this project is creating an application that scrapes several websites for data related to the Mission to Mars and displaying this data in a single HTML page.

Visited web-sites: 
1. [NASA Mars News Site](https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest)
2. [Jet Propulsion Laboratory website](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars) 
3. [Mars Weather twitter account](https://twitter.com/marswxreport?lang=en)
4. [Mars Facts webpage](https://space-facts.com/mars/)
5. [USGS Astrogeology site](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)

The initial scraping was performed using Python, Jupyter Notebook, BeautifulSoup, Pandas, and Splinter.
The HTML-page was created using MongoDB, Flask, and Jinja2 as a template engine.

Files included within this projects:

* this README.md
* mission_to_mars.ipynb
* scrape_mars.py
* chromedriver.exe
* app.py
* index.html