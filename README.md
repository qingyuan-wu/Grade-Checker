# :100: Grade Checker
Tired of refreshing your Acorn every hour to see if your courses released their grades? Grade Checker is the perfect solution! This program checks regularly (you specify the frequency) for newly released grades and sends you an e-mail in case there is any.

Keep reading for detailed documentation on how to use this program.

## :page_facing_up: Notes and Documentation for the Grade Chcker Program
* Main file: `checker.py`

The program checks for newly released grades on Acorn at user-specified frequencies.

### :arrow_down: Downloading Dependencies
On top of Python3, this program also requires **Selenium** and **ChromeDriver**.

* [Selenium](https://www.selenium.dev/) is an open-source project supporting Web automation. To download using `pip`, type `pip install selenium`.
* ChromeDriver is a WebDriver. You must download the correct version [here](https://chromedriver.chromium.org/downloads) depending on your Chrome version. Currently, I have Chrome version 96.0.4664.110.
* ChromeDriver must also be added to PATH. There are multiple ways to do this documented [here](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/).

### Using the Program
1. Scroll down to the bottom of the file to add e-mails as strings to the `mailing_list` variables. These e-mails will be notified when there is an update to the Acorn. Note for uToronto e-mails make sure the e-mail sent doesn't end up in your junk.
2. Change the `COURSES` list be adding your courses as strings **in the order that they appear on Acorn**. You should only add those for which you are expectin a grade (i.e., courses from this semester). In order helps the program identify which course's grade was released, but it is not necessary for notification purposes.
3. A sender email and the password **to this e-mail** will be asked during the execution of the program. This e-mail will send the notification, it can be your main e-mail or you can make a burner e-mail, doesn't matter. If you're using a Gmail address, you must allow "less secure app access" in Google's privcy settings [here](https://www.google.com/settings/security/lesssecureapps).
4. The program will first send out test e-mails at the start of execution. Make sure you have received these e-mails.
5. You also need to enter your UTORID and password upon request by the program.
6. `PERIOD`: this is the frequnecy at which the program refreshes the page for you. It should be between 300-600 seconds (5-10 minutes).

### :brain: Basic Operting Method
* The program uses chromedriver to log into Acorn. It then navigates to the "Academic History" tab and reads all grade data at regular frequencies.
* The grades that are read is compared to previous grades. If there's a change, the program sends an e-mail to each e-mail in `mailing_list`. 
* The program keeps running even after the release of a grade, as it removes the course from the list of courses for you.
* E-mails are sent using the `smtplib` module. See Python's documentation [here](https://docs.python.org/3/library/email.examples.html).

### :page_facing_up: Other Notes
* Acorn times out every 30-40 minutes despite the refreshes. This is accounted for in the program by first checking the grades that are read are non-empty.
* You can call the `send_email` function to test whether you are able to receive e-mails. However, a test e-mail will be sent when you run the program.
* By default, your grade is not included in the e-mail notification (only the course name). However, you can change this, as well as the content of the e-mail, by modifying the `message` parameter to the `send_email` function.
* Python scripts, including this program, continue running as long as your computer is not *sleeping*. Sleep is different from the display of the computer being on, both of which can be changed in your settings.
* Acorn does not allow you to refresh too often so make sure your frequency is relatively reasonable (around 8 minutes is good).
