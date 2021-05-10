# Do not use this tool now, will be update soon.

import os
import glob
import pandas as pd
import sys

bot = sys.argv[1]

os.chdir(bot + "/Scrapped Users/")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
combined_csv.to_csv( "combined.csv", index=False, encoding='utf-8-sig')
print("[*] All file merged..")