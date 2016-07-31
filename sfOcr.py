import os, re

#ffmpeg -i /home/christin/Documents/work/Video_name.mov -r 25 -s WxH -f /home/christin/Documents/work/image-%03d.jpeg

rule ocr:
    input:  'data/sheeter_video_tiff/{file}.tiff'
    output: 'data/tesseract/{file}.txt'
    run:  
        shell('tesseract {input} {output}.tmp')
        with open(list(output)[0] + '.tmp.txt') as f:
            num = f.readline().strip()
        with open(list(output)[0], 'w') as fout:
            print(wildcards.file + '\t' + num, file=fout)

ls = ['data/tesseract/' + x.split('.')[0] + '.txt'
      for x in os.listdir('data/sheeter_video_tiff/')]

rule cat:
    input:  ls
    output: 'ocr2.txt'
    run:  
        shell('touch {output}')
        for afile in list(input):
            shell('cat {afile} >> {output}')

rule all:
    input:  'ocr2.txt'
    output: 'ocr2.clean.txt'
    run:
        with open(list(output)[0], 'w') as fout, open(list(input)[0]) as f:
            for line in f:
                name, val = line.split('\t')
                if val.strip():
                    val = val.strip()
                    #print( val, len(val), len(re.findall('\d',val)))
                    if len(val) == 3 and 3 == len(re.findall('\d',val)):
                        n, nn = name.split('-')
                        print(n + '\t' + nn + '\t' + line.strip(), file=fout)
