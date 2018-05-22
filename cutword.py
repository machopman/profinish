import requests

def cutw(sent):
	sent = str(sent)
	url = "http://moviejang.plearnjai.com/wcut/wcut.php?string="
	response = requests.get(url + sent)
	response = response.json()
	data = response.get("words")
	return data
