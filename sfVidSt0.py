import os

rule videoToTiff:
    input:  'data/ir_vid/{afile}.mov'
    output: 'data/ir_vid_done/{afile}.mov.done'
    run:
        newName = '_'.join( wildcards.afile.split('.')[0].replace(',','').split() )
        d = '/'.join( list(input)[0].split('/')[0:-2] ) + '/sheeter_video_tif/'
        shell('ffmpeg -i "{input}" -r 25 -s 480x640 -f image2 {d}{newName}-%03d.tif')
        shell('touch "{output}"')

# rule convert:
#     input:  'data/sheeter_video/{file}.jpeg'
#     output: 'data/sheeter_video_tiff/{file}.tiff'
#     shell:  'convert {input} -crop 60x50+260+330 -type Grayscale -depth 8 -black-threshold 50% -white-threshold 50% -negate {output}'

# rule ocr:
#     input:  'data/sheeter_video_tiff/{file}.tiff'
#     output: 'data/tesseract/{file}.txt'
#     run:  
#         shell('tesseract {input} {output}.tmp digits')
#         with open(list(output)[0] + '.tmp.txt') as f:
#             num = f.readline().strip()
#         with open(list(output)[0], 'w') as fout:
#             print(wildcards.file + '\t' + num, file=fout)

ls = ['data/ir_vid_done/' + x + '.done'
      for x in os.listdir('data/ir_vid/')
      if x != '.directory']

rule all:
    input:  ls
