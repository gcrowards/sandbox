from selenium import webdriver
from time import sleep

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

page = r"https://kcpetproject.org/adopt/cats/?PrimaryBreed=0&Age_3=12-60&Age_4=%3E%3D60&search=+Search+&ClientID=11&Species=Cat"
driver.get(page)

# Wait for it to load all the cats
retries = 20
searchString = 'results_animal_link'
while not driver.find_elements_by_class_name(searchString):
    sleep(0.1)
    retries = retries - 1

catElements = driver.find_elements_by_class_name(searchString)
catLinks = {x.text: x.get_attribute("href") for x in catElements}
print("Found {} cats links.".format(len(catLinks)))

declawedCats = []

for catName in catLinks:
    driver.get(catLinks[catName])
    retries = 20
    while not driver.find_elements_by_class_name('details_animal_left_details') and retries > 0:
        sleep(0.1)
        retries = retries - 1
    details = driver.find_element_by_class_name('details_animal_left_details')
    # print(details.text)
    if 'Declawed:' not in details.text or 'Age:' not in details.text:
        continue
    declawedVal = details.text.split('Declawed:', 1)[1].split('\n')[0]
    ageVal = details.text.split('Age:', 1)[1].split('\n')[0]
    if 'No' not in declawedVal:
        print('\033[92m'+'{} is declawed! {}. Age: {}. Link: {}'.format(catName, declawedVal, ageVal, catLinks[catName]))
        declawedCats.append(catName)
    else:
        print('\033[93m'+'{} has claws! Age: {}'.format(catName, ageVal))

print('\033[92m'+'Declawed cats: {}'.format(declawedCats))

driver.quit()