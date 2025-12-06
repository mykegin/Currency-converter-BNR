import requests as req
x = req.get('https://www.bnr.ro/nbrfxrates.xml')
print(x.text)
