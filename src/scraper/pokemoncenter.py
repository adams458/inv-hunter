import logging

from scraper.common import ScrapeResult, Scraper, ScraperFactory


class PokemonCenterScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        # get name of product
        tag = self.soup.body.find('h1', class_='jsx-1022525614 product-title')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            logging.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.select_one('p', class_='jsx-1022525614 product-price-value')
        price_str = self.set_price(tag)
        if price_str:
            alert_subject = f'In Stock for {price_str}'
        else:
            logging.warning(f'missing price: {self.url}')

        # check for add to cart button
        tag = self.soup.body.find('div', class_='jsx-1839038600 product-add btn btn-secondary')
        if tag and 'Add to Cart' in tag.text.lower():
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class PokemonCenterScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'pokemoncenter'

    @staticmethod
    def get_result_type():
        return PokemonCenterScrapeResult

    @staticmethod
    def generate_short_name(url):
        parts = [i for i in url.path.split('/') if i]
        if parts:
            return parts[1]
            
time.sleep(2)