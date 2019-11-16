from spider import Spider
from user import User

checked_links = []
user_input = User("Kawalerka", "900", "1100", "Krzyki")

release_spider = Spider(user_input.make_taget_url(), checked_links)
release_spider.add_pages()
pages = len(release_spider.next_pages)
i = 0
while i < pages:
    scanning = Spider(release_spider.next_pages[i], checked_links)
    scanning.crowl()
    scanning.crawling_on_photos()
    i += 1

print(scanning.target_links)
print(scanning.photos)