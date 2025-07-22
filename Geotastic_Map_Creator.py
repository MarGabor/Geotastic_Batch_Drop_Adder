import argparse
import pandas
import datetime
import os
import math
import time
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By


global url_count

#defining path to script
def set_script_path():
    
    global SCRIPT_DIR
    SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
    os.chdir(SCRIPT_DIR)


#writing error messages to log
#void (str)
def err_fct(errorMsg):
    try:
        print(errorMsg)
        log_path = os.path.join(SCRIPT_DIR, "errorLog.txt")
        with open(log_path, 'a') as errFile:
            logEntry = "\n [%s] %s" % ((datetime.now()).strftime("%d/%m/%Y %H:%M:%S"), errorMsg)
            errFile.write(logEntry)
    except:
        open_file_err_msg = "Error log file could not be opened."
        if errorMsg == 'mp':
            return open_file_err_msg
        print(open_file_err_msg)
        exit(1)

#safely closing files, writing to error log if it fails
#void (file handle, str, str)
def close_file_safely(file, file_path, errMsgForward):
    try:
        file.close()
    except:
        errorMsg = "%s\nCould not close %s." % (errMsgForward, file_path)
        if errMsgForward == "mp":
            return errorMsg
        err_fct(errorMsg)
        exit(1)
        
#create dir in specified path
#void str        
def create_dir_safely(path): 
    
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    except:
        errMsg = "Failed to create \"%s\" directory. Insufficient writing priviliges in specified output path?" % os.path.split(path)[1]
        err_fct(errMsg)
        exit(1)

#splits csv file in a number of smaller csv files
#returns list of chunk paths
# (str,str,int) -> [str, str, ...]
def split_csv(csv_path, out_path, chunk_size):

    out_file_path_list = []
    with open(csv_path, 'r') as csv_file:
        line_list =[]
        i = 1
        chunk_counter = 1
        for line in csv_file:
            if i == chunk_size or line == '':
                line_list.append(line)
                chunk_csv_name = os.path.splitext(os.path.split(csv_path)[1])[0] + '_' + str(chunk_counter) + '.csv'
                out_file_path = os.path.join(out_path, chunk_csv_name)
                out_file_path_list.append(out_file_path)
                with open(out_file_path, 'w') as out_csv_chunk_file:
                    for out_line in line_list:
                        out_csv_chunk_file.write(out_line)
                i = 1
                line_list.clear()
                chunk_counter += 1
            else:
                line_list.append(line)
                i += 1
        #line iterator ends once it reaches EOF, thus this part writes the remainder of the coordinates to a file, when chunk size
        #does not perfectly divide the total number of coordinates
        chunk_csv_name = os.path.splitext(os.path.split(csv_path)[1])[0] + '_' + str(chunk_counter) + '.csv'
        out_file_path = os.path.join(out_path, chunk_csv_name)
        out_file_path_list.append(out_file_path)
        with open(out_file_path, 'w') as out_csv_chunk_file:
            for out_line in line_list:
                out_csv_chunk_file.write(out_line)

    return out_file_path_list

def write_page_source_to_file(url, source):

    global url_count
    url_count += 1
    file_path = os.path.join((os.path.join(".","page_sources")), str(url_count)) + ".txt"
    with open(file_path, 'w', encoding="utf-8") as page_source_file:
        page_source_file.write(url)
        page_source_file.write("\n")
        page_source_file.write("\n")
        page_source_file.write(source)

def navigate_to_drop_editor(driver, drop_editor_url):

    home_url = "https://geotastic.net/home"
    cookie_accept_btn = "v-btn.v-btn--block.v-btn--outlined.theme--dark.v-size--default.success--text"
    login_btn = "mr-3.v-btn.v-btn--is-elevated.v-btn--has-bg.theme--dark.v-size--default.primary"

    driver.get(home_url)
    time.sleep(5)
    write_page_source_to_file(home_url, driver.page_source)

    #accept cookies
    driver.find_element(By.CLASS_NAME, cookie_accept_btn).click()
    #open login window
    driver.find_element(By.CLASS_NAME, login_btn).click()

    time.sleep(5)
    write_page_source_to_file(driver.current_url, driver.page_source)

    #insert user name
    login_confirm_btn = "v-btn.v-btn--is-elevated.v-btn--has-bg.theme--dark.v-size--default.primary"
    user_name_element = "input-213"
    pas_element = "input-214"

    user_name = input("Enter user name:")
    driver.find_element(By.ID, user_name_element).send_keys(user_name)
    user_name = "0"
    pas = getpass.getpass(prompt='Enter password:')
    driver.find_element(By.ID, pas_element).send_keys(pas)
    pas = "0"
    time.sleep(2)
    buttons = driver.find_elements(By.CLASS_NAME, login_confirm_btn)
    
    for button in buttons:
        print(button.text)
        if button.text == "LOGIN":
            button.click()
            break

    time.sleep(5)
    #navigate to drop editor url
    driver.get(drop_editor_url)
    
    time.sleep(5)
    write_page_source_to_file(driver.current_url, driver.page_source)

def upload_chunks_to_geotastic(chunked_csv_path_list, drop_editor_url):

    global url_count
    url_count = 0

    #build web driver, utilizes geckodriver
    #geckodriver_path = os.path.join(os.path.join('.','prerequisites'),'geckodriver.exe')
    driver = webdriver.Firefox()

    try:
        navigate_to_drop_editor(driver)
    except:
        err_msg = "Failed to navigate to drop editor."
        err_fct(err_msg)
        driver.quit()
        return

    

def main():
    
    set_script_path()

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--csvpath", action="store", help="Path to CSV file with coordinates.", required=True)
    argParser.add_argument("-o", "--outpath", action="store", help="Path to save the chunked CSV files to.", required=True)
    argParser.add_argument("-el", "--editorurl", action="store", help="Map drop editor link.", required=True)
    argParser.add_argument("-cs", "--chunksize", default='500', action="store", help="Chunk size of each output CSV file.", required=False)

    args = argParser.parse_args()

    chunked_csv_path_list = split_csv(args.csvpath, args.outpath, chunk_size=int(args.chunksize))

    upload_chunks_to_geotastic(chunked_csv_path_list, args.editorurl)

    exit(0)

if __name__ == "__main__":
    main()