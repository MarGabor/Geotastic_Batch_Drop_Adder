import argparse
import pandas
import datetime
import os
import math
import selenium

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

def upload_chunks_to_geotastic(chunked_csv_path_list):

    #build web driver
    driver = selenium.webdriver.Firefox()

def main():
    
    set_script_path()

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--csvpath", action="store", help="Path to CSV file with coordinates.", required=True)
    argParser.add_argument("-o", "--outpath", action="store", help="Path to save the chunked CSV files to.", required=True)
    argParser.add_argument("-cs", "--chunksize", default='500', action="store", help="Chunk size of each output CSV file.", required=False)

    args = argParser.parse_args()

    chunked_csv_path_list = split_csv(args.csvpath, args.outpath, chunk_size=int(args.chunksize))

    upload_chunks_to_geotastic(chunked_csv_path_list)

    exit(0)

if __name__ == "__main__":
    main()