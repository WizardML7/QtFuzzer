# This Python file uses the following encoding: utf-8
import sys
from PySide6 import QtWidgets
from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import (
QWidget,
QLabel,
QCheckBox,
QApplication,
QDialog,
QTabWidget,
QLineEdit,
QDialogButtonBox,
QFrame,
QListWidget,
QGroupBox,
QMainWindow,
QVBoxLayout,
QMenu,
QHBoxLayout,
QMenuBar,
QPushButton,
QGridLayout,
QSpinBox,
QTextEdit,
QComboBox,
QFormLayout
)
import mechanicalsoup
import time

browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features':'html5lib'},
    user_agent='MechanicalSoup')


class Main_Window(QWidget):

    def __init__(self, parent = None):
        super(Main_Window, self).__init__(parent)

        #Initializing fuzz params
        #TODO add sensitive,sanitized,and extensions file GUI
        self.action = ""
        self.customAuth = ""
        self.Fvector = "C:/Users/dloiacono/Projects/fuzz/vectors.txt"
        self.Fwords = "C:/Users/dloiacono/Projects/fuzz/words.txt"
        self.sensitive = "C:/Users/dloiacono/Projects/fuzz/sensitive.txt"
        self.sanitized = "C:/Users/dloiacono/Projects/fuzz/sanitized.txt"
        self.extensions = "C:/Users/dloiacono/Projects/fuzz/extensions.txt"
        self.Surl = ""
        self.Ourls = dict([])


        #Creating GUI to be added to layout
        self.create_menu()
        actionHBox = self.create_action_options()
        self.create_grid_group_box()
        self.create_form_group_box()

        #Adding layouts and menu bar to main_layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addStretch()
        self.main_layout.setMenuBar(self._menu_bar)
        self.main_layout.addLayout(actionHBox)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self._grid_group_box)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self._form_group_box)

        #setting layout
        self.setLayout(self.main_layout)

        self.setGeometry(500,500,500,500)
        self.setWindowTitle("Fuzz")


    def setActionDiscover(self):
        print("set to discover")
        self.action = "discover"

    def setActionTest(self):
        print("set to test")
        self.action = "test"


    def setFvector(self):
        self.Fvector = self.v_line_edit.text()
        print(self.Fvector)


    def setFwords(self):
        self.Fwords = self.w_line_edit.text()
        print(self.Fwords)


    def setSurl(self):
        self.Surl = self.s_url.text()
        print(self.Surl)

    def addOurl(self):
        the_input = self.O_urls.text()
        self.Ourls.update({the_input:True})
        self.O_urls_list.addItem(the_input)
        print(self.Ourls)

    def setCustomAuth(self):
        self.customAuth = self.auth_line_edit.text()
        print(self.customAuth)

    def setSensitive(self):
        self.sensitive = self.sensitive_line_edit.text()
        print(self.sensitive)

    def setSanitized(self):
        self.sanitized = self.sanitized_line_edit.text()
        print(self.sanitized)

    def setExtensions(self):
        self.extensions = self.extensions_line_edit.text()
        print(self.extensions)

    def create_menu(self):
        self._menu_bar = QMenuBar(self)

        self._file_menu = QMenu("&File", self)
        self._menu_bar.addMenu(self._file_menu)

        self._report_menu = QMenu("Report",self)
        self._menu_bar.addMenu(self._report_menu)

        self._options_menu = QMenu("Options",self)
        self._menu_bar.addMenu(self._options_menu)

        self._help_menu = QMenu("Help",self)
        self._readMe_action = self._help_menu.addAction("Display Readme")
        self._menu_bar.addMenu(self._help_menu)
        #TODO Add window w/ action that displays Readme


    def create_action_options(self):
        actionHBox = QHBoxLayout()

        discover_button = QPushButton("Discover")
        test_button = QPushButton("Test")
        actionHBox.addWidget(discover_button)
        actionHBox.addWidget(test_button)
        discover_button.clicked.connect(self.setActionDiscover)
        test_button.clicked.connect(self.setActionTest)
        return actionHBox

    def create_grid_group_box(self):
        self._grid_group_box = QGridLayout()
        layout = QGridLayout()

        auth_label = QLabel("Custom Auth")
        self.auth_line_edit = QLineEdit()
        layout.addWidget(auth_label,0,0)
        layout.addWidget(self.auth_line_edit,0,1)
        auth_button = QPushButton("Enter")
        layout.addWidget(auth_button,0,2)
        auth_button.clicked.connect(self.setCustomAuth)

        v_label = QLabel("Path to Vector file")
        self.v_line_edit = QLineEdit()
        layout.addWidget(v_label,1,0)
        layout.addWidget(self.v_line_edit,1,1)
        v_button = QPushButton("Enter")
        layout.addWidget(v_button,1,2)
        v_button.clicked.connect(self.setFvector)

        w_label = QLabel("Path to Words file")
        self.w_line_edit = QLineEdit()
        layout.addWidget(w_label,2,0)
        layout.addWidget(self.w_line_edit,2,1)
        w_button = QPushButton("Enter")
        layout.addWidget(w_button,2,2)
        w_button.clicked.connect(self.setFwords)

        sensitive_label = QLabel("Path to Sensitive info file")
        self.sensitive_line_edit = QLineEdit()
        layout.addWidget(sensitive_label,3,0)
        layout.addWidget(self.sensitive_line_edit,3,1)
        sensitive_button = QPushButton("Enter")
        layout.addWidget(sensitive_button,3,2)
        sensitive_button.clicked.connect(self.setSensitive)

        sanitized_label = QLabel("Path to sanitized info file")
        self.sanitized_line_edit = QLineEdit()
        layout.addWidget(sanitized_label,4,0)
        layout.addWidget(self.sanitized_line_edit,4,1)
        sanitized_button = QPushButton("Enter")
        layout.addWidget(sanitized_button,4,2)
        sanitized_button.clicked.connect(self.setSanitized)

        extensions_label = QLabel("Path to extensions info file")
        self.extensions_line_edit = QLineEdit()
        layout.addWidget(extensions_label,5,0)
        layout.addWidget(self.extensions_line_edit,5,1)
        extensions_button = QPushButton("Enter")
        layout.addWidget(extensions_button,5,2)
        extensions_button.clicked.connect(self.setExtensions)

        layout.setColumnStretch(1, 10)
        layout.setColumnStretch(2, 20)
        self._grid_group_box.addLayout(layout,0,0)

    def create_form_group_box(self):
        self._form_group_box = QGridLayout()
        layout = QGridLayout()

        self.s_url = QLineEdit()
        s_url_button = QPushButton("Enter")
        s_url_button.clicked.connect(self.setSurl)

        self.O_urls = QLineEdit()
        O_urls_button = QPushButton("Enter")

        self.O_urls_list = QListWidget()
        O_urls_list_button = QPushButton("Confirm")

        #Line meant to add an inputted Ommited Url to the Ommit list
        O_urls_button.clicked.connect(self.addOurl)

        layout.addWidget(QLabel("Starting URL"),0,0)
        layout.addWidget(self.s_url,0,1)
        layout.addWidget(s_url_button,0,2)

        layout.addWidget(QLabel("Input URL to Ommit"),1,0)
        layout.addWidget(self.O_urls,1,1)
        layout.addWidget(O_urls_button,1,2)

        layout.addWidget(QLabel("Ommited URL's"),2,0)
        layout.addWidget(self.O_urls_list,2,1)
        layout.addWidget(O_urls_list_button,2,2)

        start_button = QPushButton("Start")
        layout.addWidget(start_button,3,2)

        #Line to send all fuzz params to fuzz. Still need to fix many params
        start_button.pressed.connect(self.fuzz)

        self._form_group_box.addLayout(layout,0,0)

    def guessingPages (self,siteList, f,e,url):
        # #Iterating through list and attempting to visit pages by guessing
        for line in f:
            for ex in e:
                try:
                    browser.open(url + "/" + line + ex)
                    siteList.update({line:False})
                except:
                    continue

    def linkCrawling(self,siteList,key,new,inputList,cookieList,v,s,sens,url,action,count):
        if(siteList[key] == False):
            # urlInput = False
            if new is None:
                browser.open(url + "/" + key)
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
                        if(action == 'test'):
                            self.testVectors(inputList[key],v,s,sens)
                    else:
                        #I will try to put the new function here
                        if(action == 'test'):
                            self.testVectors(inputList[key],v,s,sens)

                        newStr = newStr[newStr.find('>') + 1:]
                        newStr = newStr[:newStr.find('<')]

                        if(newStr not in siteList or siteList[newStr] == False):
                            siteList.update({newStr:False})
                            count += 1
                            if count < 5:
                                self.linkCrawling(siteList,newStr,new,inputList,cookieList,v,s,sens,url,action,count)
                            else:
                                print("Recursion limit reached")


    def testVectors(self,inputs,v,s,sens):
        for i in inputs:
            #print(i)
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

#                try:
#                    current_form = browser.select_form('form',count)
#                    print(count)
#                    count += 1
#                except:
#                    continue

                for vect in v:
#                    current_form = browser.select_form('form',count)
#                    print("Success")
                    try:
                        current_form = browser.select_form('form',count)
#                        print("Success")
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
                    #TODO fix float(500) to use slow
                    if (totalTime) > float(500):
                        print("DOS vulnerability detected")
                    # print(resp.text)
                    if str(resp) != "<Response [200]>":
                        print("Error from response")

                    for sanitized in s:
                        if sanitized in resp.text:
                            print("Found potential unsanitized outputs\n")
                            print(sanitized)

                    for sensitive in sens:
                        if sensitive in resp.text:
                            print("Found potential sensitive output\n")
                            print(sensitive)

#                    if "XSS" in resp.text:
#                        print(vect)


                    browser.refresh()
                count += 1
#                print(count)


    def fuzz(self):

        #Defineing the dict
        sites = self.Ourls

        #Defining the inputList
        inputList = dict()
        cookieList = []

#        if self.slow == "":
#            self.slow = 500
#        slow = 500

        #TODO add customAuth,sensitive,sanitized,and extensions file GUI
        with open(self.sensitive) as sens:
            with open(self.sanitized) as s:
                with open(self.Fvector) as v:
                    with open(self.extensions) as e:
                        with open(self.Fwords) as f:
                            read_data = f.read()

                            #TODO add customAuth GUI
                            if self.customAuth == 'dvwa':
                                self.Surl = "http://localhost"
                                sites.update({"Logout":True})
                                sites.update({"":False})
                                inputList.update({"Logout":[]})

                                #Going to setup

                                browser.open(self.Surl + "/setup.php")
                                browser.select_form()
                                resp = browser.submit_selected()
                                #Logging in
                                browser.open(self.Surl + "/login.php")
                                browser.select_form()
                                browser["username"] = 'admin'
                                browser["password"] = 'password'
                                resp = browser.submit_selected()
                                #Changing security level
                                browser.open(self.Surl + "/security.php")
                                browser.select_form()
                                browser['security'] = 'low'
                                resp = browser.submit_selected()

                                #browser.launch_browser()

                                browser.open(self.Surl)

                                #This function attempts to reach every page from the index page and if successful adds that page to the sites dictionary
                                self.guessingPages(sites,f,e,self.Surl)
                                #This function does the rest of the discovery
                                self.linkCrawling(sites,"",None,inputList, cookieList,v,s,sens,self.Surl,self.action,0)

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
                                self.guessingPages(sites,f,e,self.Surl)
                                self.linkCrawling(sites,"",None,inputList, cookieList,v,s,sens,self.Surl,self.action,0)

                                for key in sites:
                                    print(key)
                                    if key not in inputList:
                                        break
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
#                                browser.launch_browser()
                                print(cookieList.pop())
                                print("Program ending")


if __name__ == "__main__":
    app = QApplication(sys.argv)

#    file_name = "/words.txt"

    MainW = Main_Window()
    MainW.show()

#    tabWin = TabWindow(file_name)
#    tabWin.show()
#    browser.open("https://www.google.com/")
#    browser.launch_browser()
#    main()

    sys.exit(app.exec())

