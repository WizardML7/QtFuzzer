import mechanicalsoup
import argparse
import time

browser = mechanicalsoup.StatefulBrowser(user_agent='MechanicalSoup')
parser = argparse.ArgumentParser(description='Fuzz webpages.')
parser.add_argument('action',type=str, metavar='', help="Enter action: discover/test")
parser.add_argument('url',type=str, metavar='', help="Enter in the base url for custom authentication")
parser.add_argument('--customAuth',type=str, metavar='', required=False, help="Signal that the fuzzer should use hard-coded authentication for a specific application (e.g. dvwa).")
parser.add_argument('--commonWords',type=str, metavar='', required=False, help="Newline deliminated file used for page discovery/guessing.")
parser.add_argument('--extensions',type=str, metavar='', required=False, help="Newline deliminated file of path extensions e.g '.php' and the empty string if not specified.")
parser.add_argument('--vectors',type=str, metavar='', required=True, help="Newline-delimited file of common exploits to vulnerabilities. Required.")
parser.add_argument('--sanitizedChars',type=str, metavar='', required=False, help="Newline-delimited file of characters that should be sanitized from inputs. Defaults to just < and >")
parser.add_argument('--sensitive',type=str, metavar='', required=True, help="Newline-delimited file data that should never be leaked. It's assumed that this data is in the application's database (e.g. test data), but is not reported in any response. Required.")
parser.add_argument('--slow',type=str, metavar='', required=False, help="Number of milliseconds considered when a response is considered 'slow'. Optional. Default is 500 milliseconds")


args = parser.parse_args()


def guessingPages (siteList, f,e):
    # #Iterating through list and attempting to visit pages by guessing
    for line in f:
        for ex in e:
            try:
                browser.open(args.url + "/" + line + ex)
                siteList.update({line:False})
            except:
                continue
        
def linkCrawling(siteList,key,new,inputList,cookieList,v,s,sens,count):
    if(siteList[key] == False):
        # urlInput = False
        if new is None:
            browser.open(args.url + "/" + key)
        else:
            browser.follow_link(new)

        discovered = browser.links()
        
        #Here is where I will find all the inputs on the page.
        found = browser.get_current_page().find_all("input")
        
        cookie = browser.get_cookiejar()
        
        found = set(found)
        
        inputList[key] = found

        cookieList.append(cookie)

        siteList.update({key:True})

        if(type(discovered) != None):
            for new in discovered:
                newStr = str(new)
                # Check if http or mail 2 is inside
                if "http" in newStr or "mailto" in newStr or ".pdf" in newStr:
                    continue
                
                if "?" in newStr:
                    inputList[key].add(newStr)
                    #I will try to put the new function here
                    if(args.action == 'test'):
                        testVectors(inputList[key],v,s,sens)
                else:
                    #I will try to put the new function here
                    if(args.action == 'test'):
                        testVectors(inputList[key],v,s,sens)

                    newStr = newStr[newStr.find('>') + 1:]
                    newStr = newStr[:newStr.find('<')]

                    if(newStr not in siteList or siteList[newStr] == False):
                        siteList.update({newStr:False})
                        count += 1
                        if count < 5:
                            linkCrawling(siteList,newStr,new,inputList,cookieList,v,s,sens,count)
                        else:
                            print("Recursion limit reached")


def testVectors(inputs,v,s,sens):
    for i in inputs:
        count = 0
        if i != None:
            iStr = str(i)
            if "?" in iStr:
                iStr = iStr[iStr.find('?') + 1:]
                iStr = iStr[:iStr.find('=')]
            else:
                if "name" not in iStr:
                    continue

                iStr = iStr.split("name=\"")
                iStr = iStr[1][:iStr[1].find('\"')]
            # try:
            #     current_form = browser.select_form('form',count)
            #     count += 1
            # except:
            #     continue
            
            for vect in v:

                try:
                    current_form = browser.select_form('form',count)
#                   print("Success")
                except:
                    print("No form selected")
                    continue


                browser.__setitem__(iStr,vect)
                #Time how long response is taking and get the code
                start = time.perf_counter()
                resp = browser.submit_selected()
                end = time.perf_counter()
                totalTime = end - start
                print("Test data: ")
                print("Time taken is " + str(totalTime))
                if (totalTime) > float(args.slow):
                    print("DOS vulnerability detected")
                # print(resp.text)
                if str(resp) != "<Response [200]>":
                    print("Error from response")

                for sanitized in s:
                    if sanitized in resp.text:
                        print("Found potential unsanitized outputs\n")

                for sensitive in sens:
                    if sensitive in resp.text:
                        print("Found potential sensitive output\n")

                browser.refresh()
            count += 1


def main():
    #Defineing the dict
    sites = dict([])

    #Defining the inputList
    inputList = dict()
    cookieList = []
    
    if args.slow == "":
        slow = 500
    else:
        slow = args.slow

    with open(args.sensitive) as sens:
        with open(args.sanitizedChars) as s:
            with open(args.vectors) as v:
                with open(args.extensions) as e:
                    with open(args.commonWords) as f:
                        read_data = f.read()

                        if args.customAuth == 'dvwa':
                            sites.update({"Logout":True})
                            sites.update({"":False})
                            inputList.update({"Logout":[]})

                            #Going to setup
                            browser.open(args.url + "/setup.php")
                            browser.select_form()
                            resp = browser.submit_selected()
                            #Logging in
                            browser.open(args.url + "/login.php")
                            browser.select_form()
                            browser["username"] = 'admin'
                            browser["password"] = 'password'
                            resp = browser.submit_selected()
                            #Changing security level
                            browser.open(args.url + "/security.php")
                            browser.select_form()
                            browser['security'] = 'low'
                            resp = browser.submit_selected()
                            #browser.launch_browser()

                            browser.open(args.url)
                            
                            #This function attempts to reach every page from the index page and if successful adds that page to the sites dictionary
                            guessingPages(sites,f,e)
                            #This function does the rest of the discovery
                            linkCrawling(sites,"",None,inputList, cookieList,v,s,sens,0)

                            #This is where my for loop will be to print the final discovery findings
                            print(" ")
                            print("Discovery Findings")
                            for key in sites:
                                print(key)
                                print("\tFound inputs: ")
                                for indiv in inputList[key]:
                                    iStr = str(indiv)
                                    try:
                                        if "?" in iStr:
                                            iStr = iStr[iStr.find('?') + 1:]
                                            iStr = iStr[:iStr.find('=')]
                                        else:
                                            iStr = iStr.split("name=\"")
                                            iStr = iStr[1][:iStr[1].find('\"')]
                                        print("\t" + iStr)
                                    except:
                                        continue

                            print(cookieList.pop())
                            print("Program ending")
                        else:
                            sites.update({"":False})
                            guessingPages(sites,f,e)
                            linkCrawling(sites,"",None,inputList, cookieList,v,s,sens,0)
                            
                            for key in sites:
                                print(key)
                                for indiv in inputList[key]:
                                    iStr = str(indiv)
                                    try:
                                        if "?" in iStr:
                                            iStr = iStr[iStr.find('?') + 1:]
                                            iStr = iStr[:iStr.find('=')]
                                        else:
                                            iStr = iStr.split("name=\"")
                                            iStr = iStr[1][:iStr[1].find('\"')]
                                        print("\t" + iStr)
                                    except:
                                        continue

                            print(cookieList.pop())
                            print("Program ending")
    
        
    

if __name__ == '__main__':
    main()
