## Why does this script exist and how does it work?
This is a small Python script to add drops to custom Geotastic (geotastic.net) maps. Often times, when adding more than a few thousand drops per CSV file at once, the connection will timeout (or some other random network error will occur). Furthermore, the normalized upload speed (processing time per drop) seems to increase with number of drops added at any single time, which is most likely an oversight in the implementation of some algorithm.
This script will take any CSV file of coordinates (with columns "lattitude, longitude") as input and chunk those files up into smaller CSV files with a chosen chunk size. Then it will proceed to open an instance of a Firefox browser and will ask you for your geotastic.net login information. It will then navigate to the provided map editor URL and start the upload process. The script should produce an error log, where any chunks that failed to upload should be documented. **(This script will not save your login credentials in any way other than for the 2 lines of code required for navigating through the geotastic.net login gate, you can check for yourself. Unlike most C-type languages, Python does not offer arbitrary memory access. Thus overwriting your memory-cached password with junk does not work. But if you're THAT paranoid about your geotastic login credentials you should probably not use this script! Feel free to modify it to your liking, though.)**

## Setting up the script
1. It wasn't necessary for me (Win 10, 64-bit), but you might need to manually install and add [Geckodriver](https://github.com/mozilla/geckodriver/releases) to your **PATH** variable.
2. Installing Python 3.9+ (very probable to also work with previous versions)
3. Installing packages
```
pip install argparse selenium
```
4. Download file *Geotastic_Batch_Drop_Adder.py*
5. Create an empty directory where the CSV chunks will be saved.

## Using the script
| Option   | Description | Required |
| --------- | ------- | ------- |
| --csvpath  |  Specify path to large CSV file. | Yes |
| --outpath  | Specify path to directory where CSV chunks are saved. | Yes |
| --editorurl | Specify URL of a Geotastic map or drop group in editor mode.  | Yes |
| --chunksize | Provide an integer to control chunk size of CSV files. (Default: 500 drops/file)  | No |
| --dropfixtimeout    | When uploading a chunk, Geotastic will most likely ask to fix the provided drops. This usually takes a little while. You can provide a timeout in seconds, if adding chunks takes longer. (Default: 90 seconds) | No |
