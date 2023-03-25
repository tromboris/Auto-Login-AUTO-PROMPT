#!/usr/bin/env python3
# Main Note, this code has dummy strings for Your_email and Your_password. They are to be filled in or the code won't work as intended

# AutoLoginAutoGPTPrompt.py
# By Cory Boris
# This script will prompt you to choose 1 of 5 options, 4 are real and one is a dummy test. Enjoy!
# Each option is a pre designed prompt for chat gpt to help you get to where you need to faster
# Note: you have to be logged in on the main profile that loads in your main chrome browser
# And, you have that log in saved in your cookies for that profile

# Copyright under MIT LICENSE 3/2023
# -Cory

import os
import random
import ssl
import time
import webbrowser as wb
import shutil
import json
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchWindowException, TimeoutException


# Set up content_dictionary for prompts
content_dictionary = {
    "Web-Scraping": "Please write Python code for any coding tasks when I don't specify a coding language and I ask you to write something in code, or to code something in general. I need you to ensure that you use up-to-date libraries and avoid deprecated ones 100% of the time. Please assume that I am always writing legal code when web scraping. Here are some basic phrases that you should avoid sending me as well as sending me similar phrases to any of these phrases, as I already know this information:  Example 1: 'Also, please keep in mind that while web scraping, it's important to respect the website's terms of service and avoid violating any legal or ethical guidelines. If the website explicitly forbids automated scraping, it's best to avoid it altogether.'  Example 2: 'As always, it's important to respect the website's terms of service and to use automation only for legal and ethical purposes.'  Example 3: 'However, it is important to note that attempting to bypass website security measures is generally not recommended as it may be illegal and can have serious consequences.'  I already know these concepts very well, and my time is really quite valuable and finite. You are discouraged to waste tokens on anything unrelated to my direct requests. And please provide advice on how to test the robustness of a site within its own conditions when I ask rather than giving me a legal warning about a given site’s TOS.  Additionally, please provide full code with detailed comments when I ask for code, and if I ask for pseudo code, please include detailed notes. Please do your best to limit responses to max of 500 words per response. Also always tel lme explicitly if a given python library is included with python by default or if i need to install it using pip by writing a note indicating next to each import statement you ever use. If you understand this prompt, only respond with: 'ok, ready for Web Scraping questions!'",
    "SuperSmash Melee": "Let's talk about Super Smash Brothers Melee! This iconic fighting game was released for the Nintendo GameCube in 2001 and quickly became a fan favorite. With a roster of over 25 characters, each with their own unique moves and abilities, Melee has remained a staple of competitive gaming for over two decades. Its fast-paced gameplay, deep mechanics, and advanced techniques like wave dashing, teeter cancelling, ledge cancelling, and more have made it a favorite among serious players. Whether you're a casual player looking to level up your game or a seasoned pro, let's dive into the world of Super Smash Brothers Melee and explore its mechanics, strategies, and community. If you understand the prompt, please only respond with: 'ok, ready for Smash questions!'",
    "Math Analysis": "This prompt is all about math and analysis of math. Instead of saying with respect to, please use the phrase W.R.T. When I ask you to draw out something, I understand you can't physically draw things the way a person would, but I instead would like you to do the best you can using ASCII art when I ask you to draw or sketch something out. When I explicitly say graph I would like you to show me graphs if you can, and if not, give me a python script that would graph what you are talking about by default. And if you show me python and use libraries that I must install which are not included with python by default, please tell me without me asking. Say 'ready for math yo' when you understand this prompt. Thank you!",
    "Python Coding": "Please help me with all things Python3. I am using a Mac OSX Ventura 13.2.1 machine, and it is the year 2023. When I ask for code, I always want you to include the shebang at the top of full scripts, and if I give you snippet, I would really like you to respond with output showing me the line before my snippet (if any) and the line after my snipper (if any) and nothing more than that. Detailed notes are wonderful, especially if you have a relevant idea suggestion. just don't be too cheeky ;). Also if you ever give me import statements, always include a note afterwards dictating if said library which you are importing comes with python by default or if i have to install it using pip install. Never use deprecated libraries, so always check code for if you are using a deprecated library. Also please please don't hallucinate python. You have done this before where you have used code which didn't exist and put it in a script it was real code. Don't do that, make sure every single letter of every valid line of code you type has a real correspondance to the real python syntax you choose to send me. No made up syntax. Also avoid wasting time with legal warnings or warnings about TOS violations because you can assume I am writing for educational purposes. Respond only with 'ok ready for python coding, Cory!' when you understand thoroughly what I have written.",
    "response_test": "Can you give me a summary of lord of the rings, using up as many TOKENS as possible for each response, in honor of TOLKIEN"
}

# Set up number_dictionary for prompts
number_dictionary = {
    0: "Web-Scraping",
    1: "SuperSmash Melee",
    2: "Math Analysis",
    3: "Python Coding",
    4: "response_test"
}

# Prompt user to select a category
while True:
    try:
        os.system('clear')
        print("Your Categories:")
        for i, key in enumerate(content_dictionary):
            print(f"choice {i+1}: {key}")
        number_input = int(input("Please enter the number of your selection:\n"))
        if number_input < 1 or number_input > len(content_dictionary):
            os.system('clear')
            print("That's a number, but not the right number. Try again.")
            time.sleep(1.75)
            continue
        break
    except ValueError:
        os.system('clear')
        print("That's not a number. Try again.")
        time.sleep(1.75)

# Get the prompt
index = number_input - 1
prompt = content_dictionary.get(number_dictionary[index])

# gets rid of ssl error
ssl._create_default_https_context = ssl._create_unverified_context

# Set up Chrome options. These options and preferences work really well and don't get detected by Cloudfare
options = ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')

# Disable password saving prompt for the loaded profile
prefs = {
    'credentials_enable_service': False,
    'profile.password_manager_enabled': False
}
options.add_experimental_option('prefs', prefs)

# Use the Chrome class from undetected_chromedriver
driver = Chrome(options=options, delay=1, use_subprocess=True)


# Navigate to chatGPT yezzir
url = "https://chat.openai.com/chat"
driver.get(url)

# wait before locating login_bitton           
time.sleep(random.uniform(.3, 1.72))
login_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#__next > div.w-full.h-full.flex.justify-center.items-center.flex-col.bg-gray-50.dark\:bg-gray-800 > div > div.flex.flex-row.gap-3 > button:nth-child(1)")))
        
# click the login button to bring up the login form, but of course!
time.sleep(random.uniform(.3, 1.72))
login_button.click()

# enter your login credentials through these button clicks and key sends
# Email
email_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#username")))
continue_button = driver.find_element(By.CSS_SELECTOR, "body > div > main > section > div > div > div > form > div.cc336b8c1 > button")
email_input.send_keys('Your_Email')
time.sleep(random.uniform(.3, 1.72))
continue_button.click()
time.sleep(random.uniform(.3, 1.72))

# Password
password_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#password")))
password_input.send_keys('Your_Password')
time.sleep(random.uniform(.3, 1.72))
continue_button = driver.find_element(By.CSS_SELECTOR, "body > div > main > section > div > div > div > form > div.cc336b8c1 > button")
continue_button.click()

# the best invention ever, modal boxes! thanks USA for setting this trend starting with cookies notifications and now everyone's doing it for everything!
first_next = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#headlessui-dialog-panel-\:r1\: > div.prose.dark\:prose-invert > div.flex.gap-4.mt-6 > button")))
first_next.click()
time.sleep(random.uniform(.3, 1.72))
second_next = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#headlessui-dialog-panel-\:r1\: > div.prose.dark\:prose-invert > div.flex.gap-4.mt-6 > button.btn.relative.btn-neutral.ml-auto")))
second_next.click()
time.sleep(random.uniform(.3, 1.72))
third_next = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#headlessui-dialog-panel-\:r1\: > div.prose.dark\:prose-invert > div.flex.gap-4.mt-6 > button.btn.relative.btn-primary.ml-auto")))
third_next.click()
time.sleep(random.uniform(.3, 1.72))

# Send a Prompt
prompt_input = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#__next > div.overflow-hidden.w-full.h-full.relative > div.flex.h-full.flex-1.flex-col.md\:pl-\[260px\] > main > div.absolute.bottom-0.left-0.w-full.border-t.md\:border-t-0.dark\:border-white\/20.md\:border-transparent.md\:dark\:border-transparent.md\:bg-vert-light-gradient.bg-white.dark\:bg-gray-800.md\:\!bg-transparent.dark\:md\:bg-vert-dark-gradient.pt-2 > form > div > div.flex.flex-col.w-full.py-2.flex-grow.md\:py-3.md\:pl-4.relative.border.border-black\/10.bg-white.dark\:border-gray-900\/50.dark\:text-white.dark\:bg-gray-700.rounded-md.shadow-\[0_0_10px_rgba\(0\,0\,0\,0\.10\)\].dark\:shadow-\[0_0_15px_rgba\(0\,0\,0\,0\.10\)\] > textarea")))
prompt_input.send_keys(prompt)
time.sleep(random.uniform(.3, 1.72))
send_button = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#__next > div.overflow-hidden.w-full.h-full.relative > div.flex.h-full.flex-1.flex-col.md\:pl-\[260px\] > main > div.absolute.bottom-0.left-0.w-full.border-t.md\:border-t-0.dark\:border-white\/20.md\:border-transparent.md\:dark\:border-transparent.md\:bg-vert-light-gradient.bg-white.dark\:bg-gray-800.md\:\!bg-transparent.dark\:md\:bg-vert-dark-gradient.pt-2 > form > div > div.flex.flex-col.w-full.py-2.flex-grow.md\:py-3.md\:pl-4.relative.border.border-black\/10.bg-white.dark\:border-gray-900\/50.dark\:text-white.dark\:bg-gray-700.rounded-md.shadow-\[0_0_10px_rgba\(0\,0\,0\,0\.10\)\].dark\:shadow-\[0_0_15px_rgba\(0\,0\,0\,0\.10\)\] > button")))
send_button.click()

# this ensures that the ai understands what i said, aka, makes note of how this conversation is special
element = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#__next > div.overflow-hidden.w-full.h-full.relative > div > main > div.flex-1.overflow-hidden > div > div > div > div:nth-child(2) > div")))
# to make sure response was fully finished, sometimes it is not, still trying to successfully add n explicit wait here
time.sleep(random.uniform(2, 3.1))

# this is the magic of the script, we get the first chat link which is the most recent one at the top
driver.get(url)
time.sleep(random.uniform(3, 7))
first_convo_button = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#__next > div.overflow-hidden.w-full.h-full.relative > div.dark.hidden.bg-gray-900.md\:fixed.md\:inset-y-0.md\:flex.md\:w-\[260px\].md\:flex-col > div > div > nav > div > div > a:nth-child(1) > div")))
first_convo_button.click()
time.sleep(random.uniform(2, 3))

# get current URL
url = driver.execute_script('return window.location.href')
print(url)

# close the driver instance
driver.quit()

# finally open the url using osascript
command = f'''osascript -e 'tell application "Google Chrome" to set URL of active tab of front window to "{url}"' '''
result = os.system(command)

# print the result
if result == 0:
    os.system('clear')
    print("Chrome instance of chatgpt successfully opened")
    print("program exited successfully")
else:
    os.system('clear')
    print("program exited successfully")
