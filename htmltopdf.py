from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pdfcrowd
from selenium.webdriver.common.keys import Keys
# import os
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def get_browser_html(url):
	browser = webdriver.Chrome()
	browser.get(url)
	time.sleep(3)
	body = browser.find_element_by_tag_name("body")
	#Get total answers for the question"
	#for example: 116 Answers would return 116
	total_answers = int(browser.find_element_by_class_name("answer_count").text.split(" ")[0])
	print "Total answers : ", total_answers
	loaded_answers_length = len(browser.find_elements_by_class_name("pagedlist_item"))
	#Load all the answers first.
	count = 0
	print "Loading all answers..."
	while True:
		body.send_keys(Keys.END)
		time.sleep(3)
		loaded_answers_length_new = len(browser.find_elements_by_class_name("pagedlist_item"))
		if loaded_answers_length == loaded_answers_length_new:
			count += 1
			if count == 3:
				break
		else:
			loaded_answers_length = loaded_answers_length_new
	time.sleep(3)
	print "All answers loaded "
	html_source = browser.page_source
	return html_source,browser
q = str(raw_input("paste question url here >>"))+"?ref=1"
urls =  [q,]
url = urls[0]
html,browser = get_browser_html(url)
client = pdfcrowd.Client("vicodin", "f9c9879101395033866005dc0c83e1b3")
file_name = url.split('/')[-1]+'.pdf'
output_file = open(file_name,'wb')
print "Converting to pdf..."
client.enableJavaScript(False)
pdf = client.convertHtml(html,output_file)
output_file.close()
print "File ", file_name, "created"
browser.close()
#justchecking