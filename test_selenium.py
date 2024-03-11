# from selenium import webdriver

# # Path to geckodriver is not needed if it's already in your PATH
# driver = webdriver.Firefox()

# # Replace 'https://www.example.com' with the URL you wish to test
# driver.get("https://www.example.com")

# # Print the title of the webpage
# print(driver.title)

# # Close the browser
# driver.quit()


from selenium import webdriver

def get_user_agent():
    driver = webdriver.Chrome()
    driver.get("https://www.whatismybrowser.com/")
    user_agent = driver.execute_script("return navigator.userAgent;")
    driver.quit()
    return user_agent

user_agent = get_user_agent()
print("Current User-Agent string:", user_agent)