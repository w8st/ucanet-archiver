from pywebcopy import save_website
from internetarchive import upload, get_item
import zipfile, requests, os, time, shutil
from datetime import datetime

url = 'https://raw.githubusercontent.com/ucanet/ucanet-registry/main/ucanet-registry.txt'

blocked_ips = [b'0.0.0.0', b'8.8.8.8']
blocked_websites = [b'web.archive.org', b'upload.wikimedia.org', b'buttercuprecipes.com']

def check_ip(ip):
	for x in blocked_ips:
		if x == ip:
			return False
	return True

def check_domain(domain):
	for x in blocked_websites:
		if x == domain:
			return False
	return True

def get_updated_domain_list():
	r = requests.get(url)
	domain_list = r.content.split(b'\n')
	return domain_list

def save_webpage_uca(addr, domain):
	save_website(
	url="http://{}".format(addr.decode("utf-8")),
	project_folder="save/",
	project_name="{}".format(domain.decode("utf-8")),
	bypass_robots=True,
	debug=True,
	open_in_browser=False,
	delay=1000
	)

domains_raw = get_updated_domain_list()

for domain_raw in domains_raw:
	d_list = domain_raw.split(b' ')
	l = [d_list[0], d_list[len(d_list)-1]]
	if check_domain(l[0]) and check_ip(l[1]):
		save_webpage_uca(l[1], l[0])

time.sleep(10)

dir_name = 'save/'
timestamp = datetime.now().strftime("%e-%b-%Y-%H:%M:%S")
zip_filename = 'save{}'.format(timestamp)
shutil.make_archive(zip_filename, 'zip', dir_name)

item_name = 'ucanet{}'.format(int(time.time()))
item = get_item(item_name)
md = {'title': 'ucanet archive {}'.format(timestamp), 'mediatype': 'data', 'description': 'ucanet archives for {}. find out more about ucanet at https://ucanet.net'.format(timestamp), 'creator': 'various ucanet domain operators'}
r = item.upload(files=['{}.zip'.format(zip_filename)], metadata=md)

os.system('rm -rf save/')
os.system('rm {}.zip'.format(zip_filename))
