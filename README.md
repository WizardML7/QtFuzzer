# QtFuzzer
This python fuzzer is intended for use in assisting the testing of web applications. The crawling capabilities have been capped significantly and as such do not pose a danger of an unintended DOS attack. Use of this program is not generally considered invasive but abuse after modification could be. 

Currently, the reporting feature is unfinished and only outputs results into the command line. Additionally, the GUI is at its infant stages with improvements to be made. 

Notes on the capability of the test function. Currently does not have the ability to input arguments that are not accessible from the html as a form. In other words, it is only able to fuzz the client side form inputs. Testing the found API arguments that are regularly hidden in complex applications is another thing that may be added in the future through the help of the Python Requests library. 
