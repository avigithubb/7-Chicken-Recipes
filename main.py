from time import sleep
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas


# EDGE_DRIVER_PATH = "D:\Edge_webdriver\msedgedriver.exe"
CHROME_DRIVER_PATH = "D:\Chrome_Driver\chromedriver.exe"
# edge_options = Options()
chrome_options = Options()
# edge_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=chrome_options)


driver.get("https://www.allrecipes.com/chicken-breast-dinners-for-every-night-of-the-week-8667964")

heading = driver.find_element(By.TAG_NAME, "h1").text
weekDay = driver.find_elements(By.CLASS_NAME, 'mntl-sc-block-heading__text')

increment = 0

ingredient_head = ""
my_labels = []
my_values = []
my_ingredients = []

for i in range(len(weekDay)-1):
    scroll_height = 1500 + increment
    scroll_bar = driver.find_element(By.CLASS_NAME, 'comp')
    current_labels = []
    current_values = []
    current_ingredients = []

    driver.execute_script(f"arguments[0].scrollTop = {scroll_height};", scroll_bar)
    sleep(2)

    button = driver.find_elements(By.CLASS_NAME, 'mntl-sc-block-universal-featured-link__link')

    # driver.execute_script("arguments[0].scrollIntoView();", button)
    sleep(2)
    button[i].click()
    # driver.execute_script(f"arguments[0].scrollTop = {100};", scroll_bar)

    labels = driver.find_elements(By.CLASS_NAME, 'mm-recipes-details__label')

    values = driver.find_elements(By.CLASS_NAME, 'mm-recipes-details__value')
    ingredient_head = driver.find_element(By.CSS_SELECTOR, '#mm-recipes-structured-ingredients__heading_1-0').text
    ingredients = driver.find_elements(By.CLASS_NAME, 'mm-recipes-structured-ingredients__list-item ')
    for i in range(len(labels)-1):
        sleep(1)
        current_labels.append(labels[i].text)
        current_values.append(values[i].text)
        current_ingredients.append(ingredients[i].text)

    my_labels.append(current_labels)
    my_values.append(current_values)
    my_ingredients.append(current_ingredients)

    driver.back()
    driver.back()
    increment += 300
    sleep(2)

weekDay = driver.find_elements(By.CLASS_NAME, 'mntl-sc-block-heading__text')

weekday_recipe = []

for i in range(len(weekDay)-1):
    # print(heading)
    weekday_recipe.append(weekDay[i].text)
    # print(my_labels[i])
    # print(my_values[i])
    # print(ingredient_head)
    # print(my_ingredients[i])


# Creating a dictionary with hashable keys (string representation of labels)
Chicken_recipes = {
    heading: weekday_recipe,
}

print(my_labels[0])
print(my_values)
# for i in range(len())
# all_labels = my_labels[0]
# for i in range(len(my_labels)):
#     key = " | ".join(my_labels[i])
#     Chicken_recipes[key] = {
#         "values": my_values[i],
#         "ingredients": my_ingredients[i]
#     }

all_preparations = []
for i in range(len(my_values[0])):
    prepare = []
    for j in range(len(my_values)):
        try:
            prepare.append(my_values[j][i])
        except IndexError:
            prepare.append("")

    all_preparations.append(prepare)

for i in range(len(my_labels[0])):
    Chicken_recipes[my_labels[0][i]] = all_preparations[i]

# Adding the ingredient_head key separately
Chicken_recipes[ingredient_head] = my_ingredients

for key, value in Chicken_recipes.items():
    print(key, value)

df = pandas.DataFrame(Chicken_recipes)
my_recipe_csv = df.to_csv("My 7 recipes")
