from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Config - Replace with your credentials (only for testing)
EMAIL = "robertadelmann@yahoo.com"
PASSWORD = "Goatrope123#"

# Set up the Selenium driver
driver = webdriver.Chrome()  # or webdriver.Firefox() if using Firefox
driver.get("https://www.linkedin.com/login")

# Login
driver.find_element(By.ID, "username").send_keys(EMAIL)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
driver.find_element(By.XPATH, '//button[@type="submit"]').click()
time.sleep(3)

# Go to messaging page
driver.get("https://www.linkedin.com/messaging/")
time.sleep(5)

# Click on the first conversation (you can modify to target a specific contact)
conversations = driver.find_elements(By.CLASS_NAME, "msg-conversation-listitem")
conversations[0].click()
time.sleep(5)

# Scroll to load full history (increase range if needed)
for _ in range(5):
    driver.find_element(By.CLASS_NAME, "msg-s-message-list__event").send_keys(Keys.HOME)
    time.sleep(1)

# Extract messages
messages = driver.find_elements(By.CLASS_NAME, "msg-s-message-group")
output = ""

for group in messages:
    try:
        sender = group.find_element(By.CLASS_NAME, "msg-s-message-group__name").text
        message_blocks = group.find_elements(By.CLASS_NAME, "msg-s-event-listitem__body")
        for block in message_blocks:
            text = block.text.strip()
            output += f"{sender}: {text}\n"
    except Exception:
        continue

# Save to file
with open("linkedin_conversation.txt", "w", encoding="utf-8") as f:
    f.write(output)

driver.quit()
print("Conversation saved to linkedin_conversation.txt")
