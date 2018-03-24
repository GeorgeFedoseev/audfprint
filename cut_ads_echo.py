import subprocess
import sys
import os

import re

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
TMP_DIR_PATH = os.path.join(curr_dir_path, "processing_tmp/")
ECHO_DIR_PATH = os.path.join(curr_dir_path, "echo-msk-data/")

AUDFPRING_DIR_PATH = os.path.join(curr_dir_path, "audfprint/")

ads_db_path = os.path.join(ECHO_DIR_PATH, "ads.db")
audfprint_script_path = os.path.join(AUDFPRING_DIR_PATH, "audfprint.py")

map_file_path = os.path.join(TMP_DIR_PATH, "matches.txt")

if not os.path.exists(TMP_DIR_PATH):
    os.makedirs(TMP_DIR_PATH)





def cut_piece(input_path, start, end, output_path):
    p = subprocess.Popen(["ffmpeg", "-y",
         "-i", input_path,
         "-ss", str(start),
         "-to", str(end),        
         output_path
         ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = p.communicate()

    if p.returncode != 0:
        print("failed_ffmpeg_conversion "+str(err))
        return False
    return True

def map_audio(input_path):

    print audfprint_script_path

    print ads_db_path

    print input_path

    p = subprocess.Popen(
        "venv/bin/python "
        + audfprint_script_path
        + " match"
        + ' --find-time-range'
        + ' --max-matches 25'
        + " --dbase " + ads_db_path
        + " --ncores 4"
        + ' --sortbytime'
        + ' ' + input_path,
        #+ ' --opfile ' + map_file_path,
         shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = p.communicate()
    print out

  
    regexp = re.compile(r'Matched[\s]*(?P<matched_duration>[0-9\.]+).*starting at[\s]*(?P<start_target>[0-9\.]*).*to time[\s]*(?P<start_piece>[0-9\.]*).*with[\s]*(?P<hashes_matched>[0-9]*).*of[\s]*(?P<hashes_total>[0-9]*)')    
    groups = [m.groupdict() for m in regexp.finditer(out)]
    print groups[0]['matched_duration']




    

def cut_ads(input_folder, output_folder):
    pass    


if __name__ == '__main__':
    map_audio("/Users/gosha/Desktop/echo-test/2018-03-13-osoboe-1906.mp3")


    # if len(sys.argv) < 3:
    #     print('USAGE: python cut_ads_echo.py <folder_with_input_audio> <folder_for_output>')
    # else:    
    #     cut_ads(sys.argv[1], sys.argv[2])



    