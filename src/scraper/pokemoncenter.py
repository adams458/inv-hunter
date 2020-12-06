from scraper.common import ScrapeResult, Scraper, ScraperFactory


class PokemonCenterScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        # get name of product
        tag = self.soup.p('h1', class_='jsx-1022525614 product-title')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.title.string('p', class_='jsx-1022525614 product-price-value')
        price_str = self.set_price(tag)
        if price_str:
            alert_subject = f'In Stock for {price_str}'
        else:
            self.logger.warning(f'missing price: {self.url}')

        # check for add to cart button
        tag = self.soup.p(class_='jsx-1839038600 product-add btn btn-secondary')
        if tag and 'add to cart' in tag.text.lower():
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class PokemonCenterScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'p'

    @staticmethod
    def get_driver_type():
        return 'requests'

    @staticmethod
    def get_result_type():
        return PokemonCenterScrapeResult