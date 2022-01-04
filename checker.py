# install selenium: pip install selenium
# Install chromedriver: https://sites.google.com/chromium.org/driver/
# Make sure the driver version is compatible with your chrome version
# for chrome version chrome=96.0.4664.110, install chromdrivers that support chrome version 96
def check_grades(COURSES, mailing_list):
    # Add chromedriver to path, see https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/ for details
    # I used option 2 (add to path).
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    #from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service

    # delays
    import time

    # send emails
    import smtplib, ssl

    UTORID = input("Enter your utorid: ")
    PASSWORD = input("Enter your password: ")
    SENDER_EMAIL = input("Enter sender's email to send grade update notifications: ") # to get notification after grade update
    EMAIL_PASSWORD = input("Enter sender's email password: ")

    # how often to refresh, in seconds
    while True:
        try:
            PERIOD = int(input("How often would you like to refresh, in seconds? "))
            break
        except:
            print("Please enter a valid number.")

    # make sure email send properly
    # message = f"Subject: {determine_greeting()}!!\n\nI hope you are well.\n\n This message is sent from Python. This is a test.\n\nKind Regards,\nQingyuan"
    # send_email(mailing_list, message, SENDER_EMAIL, EMAIL_PASSWORD)

    driver = webdriver.Chrome()

    driver.get("https://acorn.utoronto.ca/sws/#/")
    print(driver.title) # weblogin idpz | University of Toronto

    # enter utorid and password
    username = driver.find_element(By.NAME, "j_username")
    password = driver.find_element(By.NAME, "j_password")
    username.send_keys(UTORID)
    password.send_keys(PASSWORD)

    # submit
    submit_button = driver.find_element(By.NAME, "_eventId_proceed")
    submit_button.click()

    # wait a few seconds for site to load
    time.sleep(4)

    # click Academic History
    driver.find_element(By.XPATH, "//a[. = 'Academic History']").click()
    time.sleep(0.5)

    # get all the grades
    cur_grades_list = driver.find_elements(By.CLASS_NAME, "course-mark")
    # we should convert this list of objects to actual strings, because session numbers change after each refresh
    cur_grades_list = [gradeObj.text for gradeObj in cur_grades_list]
    prev_grades_list = cur_grades_list.copy()

    # sanity check: print out grades with course name substituted for unknown grades
    i = 0
    for grade in cur_grades_list:
        if not grade:
            print(COURSES[i])
            i += 1
        else:
            print(grade)
        if i == len(COURSES):
            break
    total_checks = 1
    while True: # loop to keep checking
        driver.refresh() # refresh page
        time.sleep(1)
        # get grades, convert to strings
        cur_grades_list = driver.find_elements(By.CLASS_NAME, "course-mark")
        cur_grades_list = [gradeObj.text for gradeObj in cur_grades_list]

        if cur_grades_list == prev_grades_list: # no new grades
            print(f"No new grades... Waiting {PERIOD}s")
            print(f"{total_checks} checks")
            total_checks += 1
            time.sleep(PERIOD)
            continue
        # There's a change! Find which course it is
        print("There's a change!")
        print(cur_grades_list)
        #Check to see if we're auto logged out
        if len(cur_grades_list) == 0:
            time.sleep(2)
            # auto logged out, log back in
            # enter utorid and password
            username = driver.find_element(By.NAME, "j_username")
            password = driver.find_element(By.NAME, "j_password")
            username.send_keys(UTORID)
            password.send_keys(PASSWORD)

            # submit
            submit_button = driver.find_element(By.NAME, "_eventId_proceed")
            submit_button.click()

            # wait a few seconds for site to load
            time.sleep(4)

            # click Academic History
            driver.find_element(By.XPATH, "//a[. = 'Academic History']").click()
            time.sleep(0.5)

            # get all the grades
            cur_grades_list = driver.find_elements(By.CLASS_NAME, "course-mark")
            # we should convert this list of objects to actual strings, because session numbers change after each refresh
            cur_grades_list = [gradeObj.text for gradeObj in cur_grades_list]
            prev_grades_list = cur_grades_list.copy()

            time.sleep(PERIOD//2) # mostly arbitrary, but logging back in takes time
            continue
        try:
            j = 0 # keeps track of which course it is
            for i in range(len(cur_grades_list)):
                if cur_grades_list[i] == prev_grades_list[i]:
                    if not cur_grades_list[i]: # this grade is unknown
                        j += 1
                    continue
                else: # spotted the difference
                    break
            NEW_GRADE = COURSES[j] # the course!
        except:
            print("error determining course. Sending generic email instead")
            NEW_GRADE = "a course"

        sender_email = SENDER_EMAIL
        # got the grade, can email to ourselves:
        message = f"Subject:{determine_greeting()}Grades for {NEW_GRADE} are Out!!!\n\nCheck your grades foo.\n\nThis message is sent from the Python auto grade checker."

        send_email(mailing_list, message, sender_email, EMAIL_PASSWORD)

        # can now remove NEW_GRADE from COURSES
        COURSES.remove(NEW_GRADE)
        prev_grades_list = cur_grades_list[:]

        if not COURSES:
            print("All grades have been checked. Exiting.")
            driver.quit()
            return # exit the function

# sending an email to a list of addresses
def send_email(mailing_list, message, sender_email, EMAIL_PASSWORD):
    import smtplib, ssl
    # For gmail, must go to the following link to allow less secure access:
    # https://www.google.com/settings/security/lesssecureapps

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, EMAIL_PASSWORD)
        for receiver_email in mailing_list:
            try:
                server.sendmail(sender_email, receiver_email, message)
                print(f"Sent to {receiver_email}")
            except:
                print(f"Could not mail to {receiver_email}")

def determine_greeting():
    try:
        from datetime import datetime
        now = str(datetime.now().time()) # time xx:xx:xx.xxxxx in string format

        if 3 < int(now[:2]) < 12:
            return "Good morning"
        elif 12 <= int(now[:2]) < 17:
            return "Good afternoon"
        elif 17<=int(now[:2])< 20:
            return "Good evening"
        elif 20 <= int(now[:2]) or int(now[:2])<= 3:
            return "Good night"
        else:
            return "Good morning"
    except:
        print("could not determine greeting. Using generic greeting instead.")
        return "Hello"

if __name__ == '__main__':
    # list of recipient emails
    mailing_list = []

    # WRITE DOWN COURSES WITH UNKNOWN GRADES, IN ORDER as they appear on Acorn, HERE:
    # Note this is just for notification purposes, you can write abbreviated course names
    COURSES = ["AER210", "ESC203", "PHY293"]
    # note: placing the courses out of order would merely result in the email subject displaying the wrong course, but the checker should still detect new grades.

    check_grades(COURSES, mailing_list)


# potential problem: acorn auto logging out?
# might have to make sure we're not logged out before comparing courses. - FIXED