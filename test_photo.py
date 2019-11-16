import requests
import re
import urllib.parse

response = requests.get("https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/?search%5Bfilter_float_price%3Ato%5D=1100&search%5Bfilter_float_price%3Afrom%5D=900&search%5Bfilter_enum_rooms%5D%5B0%5D=one&search%5Bdistrict_id%5D=391")
html = response.content.decode('utf-8')
print( re.findall('(?:class="fleft" src=")(.*?)"', html))