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

def precompute(input_path):
    print 'Precomputing for %s' %input_path

    name, ext = os.path.splitext(os.path.basename(input_path))
    output_file_path = os.path.join(TMP_DIR_PATH, name+'.afpt')

    

    if os.path.exists(output_file_path):
        print 'Already have precoputed file %s' % output_file_path
        return output_file_path

    p = subprocess.Popen(
        "venv/bin/python "
        + audfprint_script_path
        + " precompute"
        + " --precompdir "+TMP_DIR_PATH
        + " --density 100"
        + " --shifts 1"
        + " --samplerate 11025"
        + " --ncores 4"        
        + ' ' + input_path,
        #+ ' --opfile ' + map_file_path,
         shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = p.communicate()
    print out

    return output_file_path

def find_ads(input_path):
    print 'Finding ads in %s...' % input_path

    print 'using db %s' % ads_db_path


    matches_file_path = os.path.join(TMP_DIR_PATH, os.path.basename(input_path)+'_matches.txt')

    if not os.path.exists(matches_file_path):
        print 'Matching...'
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

        # write to file
        txt = open(matches_file_path, 'w')
        txt.write(out)
        txt.close()

        print 'Wrote matches from cache %s' % matches_file_path

    print 'Read matches from cache %s' % matches_file_path
    # read cached
    txt = open(matches_file_path, 'r')
    out = txt.read()
    txt.close()   

  
    regexp = re.compile(r'Matched[\s]*(?P<matched_duration>[0-9\.]+).*starting at[\s]*(?P<start_target>[0-9\.]*).*to time[\s]*(?P<start_piece>[0-9\.]*).*in.*\/(?P<ad_type>[a-zA-Z]*)\..*with[\s]*(?P<hashes_matched>[0-9]*).*of[\s]*(?P<hashes_total>[0-9]*)')    
    groups = [m.groupdict() for m in regexp.finditer(out)]
    
    ads = []

    for m in groups:
        ads.append({
            'start': float(m['start_target']),
            'end': float(m['start_target']) + float(m['matched_duration']),
            'type': m['ad_type']
            })        

    print ads



    

def cut_ads(input_folder, output_folder):
    pass    


if __name__ == '__main__':
    precomputed_path = precompute("/Users/gosha/Desktop/echo-test/2018-03-13-osoboe-1906.mp3")
    find_ads(precomputed_path)


    # if len(sys.argv) < 3:
    #     print('USAGE: python cut_ads_echo.py <folder_with_input_audio> <folder_for_output>')
    # else:    
    #     cut_ads(sys.argv[1], sys.argv[2])



    