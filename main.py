import os

from read_utils.GPT import getGPTresponse
from read_utils.read_utils import preextract
from scraping import *
from audio import * 
from force_alignment import * 
from dict import * 
from video_generator import * 
from search import *
from read_utils import *
import os

def main(paper, output_pre = 'texts/processed_output.txt', \
          final_output = 'texts/oof.txt',speech_final = 'audio/output_converted.wav', subtitle_path = 'texts/testing.ass', \
            output_path = 'final/final.mp4',speaker_wav="assets/default.mp3", video_path = 'assets/subway.mp4'):

    print("L1: Downloading PDF")

    preextract(paper)
    os.chdir("./downloads/" + paper["title"])

    contents = []

    print("L2: Prompting GPT")
    with open('./speech.txt', 'w') as file:
        contents = getGPTresponse()
        file.write(contents[1])

    with open('./related.txt', 'w') as file:
        file.write(contents[0])

    os.chdir("../..")

    # ## AUDIO CONVERSION 
    print("L3: AUDIO CONVERSION NOW (TAKES THE LONGEST)")
    audio(f'downloads/{paper["title"]}/speech.txt', speaker_wav = speaker_wav)
    convert_audio('audio/output.wav',speech_final)
    
    # IMPORTANT PRE PROCESSING STUFF 
    process_text(f'downloads/{paper["title"]}/speech.txt', output_pre)
    process_text_section2(output_pre, final_output)

    with open(final_output, 'r') as file: 
        text = file.read().strip()
    
    # A BUNCH OF HARDCORE FORCED ALIGNMENT FORMATTING
    print("L4: FORCE ALIGNMENT")
    transcript = format_text(text)
    bundle, waveform, labels, emission1 = class_label_prob(speech_final)
    trellis,emission,tokens = trellis_algo(labels,text,emission1)
    path = backtrack(trellis, emission, tokens)
    segments = merge_repeats(path, transcript)
    word_segments = merge_words(segments)
    timing_list = []
    for (i, word) in enumerate(word_segments):
        timing_list.append((display_segment(bundle, trellis, word_segments, waveform, i)))
    
    # FINAL VIDEO
    print("L5: VIDEO GENERATION")
    convert_timing_to_ass(timing_list, subtitle_path)

    ## Finally, we need to generate the brain rot video tself
    add_subtitles_and_overlay_audio(video_path,speech_final, subtitle_path, output_path)
    print("DONE! SAVED AT " + output_path)

if __name__ == "__main__":
    main("https://www.reddit.com/r/askSingapore/")