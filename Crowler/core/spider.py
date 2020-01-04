import requests
import re
import urllib.parse

from Crowler.core.filtrs import User_Filtr

class Spider():

    def __init__(self, target_url, target_links, photos):
        self.target_url = target_url
        self.target_links = target_links
        self.next_pages = [target_url]

    def decode_html(self, url):
        response = requests.get(url)
        return(response.content.decode('utf-8'))

    def extract_links(self):
        html = self.decode_html(self.target_url)
        return re.findall('(?:href=")(.*?)"', html)

    def crowl(self):
        href_links = self.extract_links()

        for link in href_links:
            link = urllib.parse.urljoin(self.target_url, link)

            if "#" in link:
                # These links are from olx.pl so have #
                link = link.split("#")[0]

                if "https://www.olx.pl/oferta" in link and link not in self.target_links:
                    #print(link)
                    self.target_links.append(link)
            """  Maybe someday...  
            elif "https://www.otodom.pl/oferta" in link and link not in self.target_links:
                self.target_links.append(link)
            """

    def take_all_info(self):
        infos = []
        for link in self.target_links:
            if link != None:
                html = self.decode_html(link)
                photos = re.findall('(?:<img src=")(.*?)"', html)
                price = re.findall('(?:<strong class="xxxx-large not-arranged"">)(.*?) zł</strong>', html)
                if price == []:
                    price = re.findall('(?:<strong class="xxxx-large arranged"">)(.*?) zł</strong>', html)
                title = re.findall('(.*)</h1', html)
                try:
                    infos.append([link, photos[0], price[0], title[0]])
                except Exception:
                    infos = "Wybierz inny przedział!"
        return infos


    def number_of_pages(self):
        html = self.decode_html(self.target_url)
        existance_page = re.findall('(?:&page=)(.*?)" data-cy="page-link-last">', html)
        return(existance_page)

    def add_pages(self):
        number = self.number_of_pages()
        if len(number)==0:
            pass
        else:
            amount = number[0]
            i = 2
            while i <= int(amount):
                link = self.target_url + "&page=" + str(i)
                self.next_pages.append(link)
                i += 1
