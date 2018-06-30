#!/usr/bin/env python3

import urllib.request
import os
import re
import random

feed = urllib.request.urlopen('https://www.flickr.com/services/feeds/photos_public.gne?id=130608600@N05&lang=en-us&format=atom').read()
img_re = b"img src=&quot;https:\\/\\/farm\\d+\\.staticflickr\\.com\\/\\d+\\/(\\d+)_\\w+_m\\.jpg&quot;"

img_id = random.choice(re.findall(img_re, feed))
full_url = "https://www.flickr.com/photos/spacex/%s/sizes/o/" % img_id.decode()
print(full_url)
full_re = b"<div id=\"allsizes\\-photo\">\\s+<img src=\"(https:\\/\\/.+staticflickr.com/(\\d+/)*(.+_o.jpg))\">\\s+</div>"
full_html = urllib.request.urlopen(full_url).read()

match = re.search(full_re, full_html)
orig_url = match.groups()[0].decode()
file_name = "spacex_%s" % match.groups()[2].decode()

sw_dir = os.path.expanduser('~/.spacex_wallpapers')
sw_file = os.path.join(sw_dir, file_name)

try:
    os.makedirs(sw_dir)
except OSError:
    pass

orig = urllib.request.urlopen(orig_url).read()
f = open(sw_file, 'wb')
f.write(orig)
f.close()

os.system("gsettings set org.gnome.desktop.background picture-uri file://%s" % sw_file)
