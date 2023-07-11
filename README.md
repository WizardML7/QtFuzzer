# QtFuzzer
This python fuzzer is intended for use in assisting the testing of web applications. The crawling capabilities have been capped significantly and as such do not pose a danger of an unintended DOS attack. Use of this program is not generally considered invasive but abuse after modification could be. 

Currently, the reporting feature is unfinished and only outputs results into the command line. Additionally, the GUI is at its infant stages with improvements to be made. 

Notes on the capability of the test function. Currently does not have the ability to input arguments that are not accessible from the html as a form. In other words, it is only able to fuzz the client side form inputs. Testing the found API arguments that are regularly hidden in complex applications is another thing that may be added in the future through the help of the Python Requests library. 

# Usage
The menubar is not yet complete so disregard its usage for now. It is planned to allow for report saving and complete reset of data. Use the two buttons to toggle between the modes of Discover and Test. 

# Discover
Discover will act as a web crawling tool and will return a list of pages found and that pages associated inputs. This involves only visiting webpages with the help of mechanicalsoup and analyzing the response. The network demanded load is that of only how many pages there are on the site being crawled. 

# Test
Test is essentially the same as discover but with the addition of sending a request of a list of vectors to every input found on the page and analyzing the response to each vector. The analysis of each vector is still under development as well as inputting vectors for more complex applications and forms that require more than one input at a time. Ex: a login form that requires a username and password at the same time to craft a valid request. 

# Custom Auth
This input is to allow for a predefined setup of authentication for an application. The only custom authentication setup available currently is for the DVWA. 

# Files
The following lines shown in the GUI are for inputting the absolute paths to the various files used within the script. 

# Words File
This file is used within the guessingPages method and is what fills in the “Guess” for the first part. Ex: (Word).(Extension)

# Vector File
This file is used within the testingVectors method and is the list of vectors, also known as payloads for use to craft the requests used in the test mode. 

# Sensitive File
This file is currently used in the testingVectors method to analyze the response received after the vector was inputted but is currently not working as intended. May be scrapped. 

# Sanitized File
This file is currently used in the testingVectors method to analyze the response received after the vector was inputted but is currently not working as intended. May be scrapped. 

# Extensions File
This file is used within the guessingPages method and is what fills in the “Guess” for the second part. Ex: (Word).(Extension)

# Starting URL
This input is what allows the user to input the base URL the script will branch and “Crawl” from. Keep in mind that this what keeps the fuzzer in scope. The fuzzer will not leave the top level domain that has been specified as the base URL. For example, if https://localhost/dvwa was inputted as the Starting URL (as it is in the custom auth) it will not search through https://localhost for other endpoints. This is actually fairly important to keep in mind as many pages will include links to outside sources like social media and outside documentation. The fuzzer/crawler will NOT include these links in the report as they do not fall within the base URL. 

# URL to Ommit
This allows for the preset of Omitted URLs. Use this when it becomes apparent that certain URLs derail the crawl. The most common is a logout page which can limit the amount of pages the browser, (and a normal user) can access. Make sure to click confirm to add all that have been inputted. For now the resetting of the list of omitted URLs can only be done with the closing of the entire application. This will be fixed in the future. 
