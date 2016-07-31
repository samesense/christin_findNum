import os

#ffmpeg -i /home/christin/Documents/work/Video_name.mov -r 25 -s WxH -f /home/christin/Documents/work/image-%03d.jpegffmpeg -i /home/christin/Documents/work/findNum/data/ir_vid/Video\ Jul\ 18\,\ 10\ 16\ 51\ AM.mov -r 25 -s 480x640 -f image2 /home/christin/Documents/work/findNum/data/test/sheeter-%03d.tiff


rule convert:
    input:  'data/sheeter_video/{file}.jpeg'
    output: 'data/sheeter_video_tiff/{file}.tiff'
    shell:  'convert {input} -crop 60x50+260+330 -type Grayscale -depth 8 -black-threshold 50% -white-threshold 50% -negate {output}'

rule ocr:
    input:  'data/sheeter_video_tiff/{file}.tiff'
    output: 'data/tesseract/{file}.txt'
    run:  
        shell('tesseract {input} {output}.tmp digits')
        with open(list(output)[0] + '.tmp.txt') as f:
            num = f.readline().strip()
        with open(list(output)[0], 'w') as fout:
            print(wildcards.file + '\t' + num, file=fout)

ls = ['data/tesseract/' + x.split('.')[0] + '.txt'
      for x in os.listdir('data/sheeter_video/') if x.split('.')[0].strip()]

rule all:
    input:  ls
    output: 'ocr2.txt'
    shell:  'cat {input} > {output}'
