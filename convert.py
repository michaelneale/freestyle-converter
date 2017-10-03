from bs4 import BeautifulSoup

file = open('config.xml')
soup = BeautifulSoup(file, 'lxml')

repo = soup.find_all('hudson.plugins.git.userremoteconfig')[0].url.text

print repo
