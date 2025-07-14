tim2bmp
tim2bmp.exe  <input path> <output path>

====================
AC3LayerMerger
AC3LayerMerger.exe  <tim layer1> <tim layer2> <output tim>

====================
ac3es_tools

usage: ac3es_tools.exe [-h] {bin,bpb,tim,ulz,info} ...

positional arguments:
  {bin,bpb,tim,ulz,info}
                        Commands
    bin                 Split and merge bin container files
    bpb                 Unpack and repack ACE.BPB and ACE.BPH
    tim                 Copy TIM header information and/or replace CLUT data
    ulz                 Compress, decompress and manipulate ULZ files.
    info                Try to identify files and print useful information

options:
  -h, --help            show this help message and exit

Example:

    Compress an image and put the output into the same directory
      ac3es_tools.exe ulz --compress image.tim --ulz-type=2 --level=1

    or define another destination
      ac3es_tools.exe ulz --compress jap_0002.tim --ulz-type=2 --level=1 --output-file=mycompress.ulz

    Get what parameters use from the original file
      ac3es_tools.exe info BPB/0386/0001/0000.ulz

    Work on bin containers
      ac3es_tools.exe bin --split=BPB/0114/0007.bin --out-directory=splitted/0007 --out-list=splitted/0007.txt
      ac3es_tools.exe bin --merge-list=splitted/0007.txt --out-bin=mod_0007.bin

    More parameters are available, just type help for the sub command
      ac3es_tools.exe ulz --help
      ac3es_tools.exe info --help
      ac3es_tools.exe bin --help
      ac3es_tools.exe tim --help
      ac3es_tools.exe bpb --help

    Report bugs to: infrid@infrid.com
    AC3ES Tools Version 3.0
    Homepage: <https://loadwordteam.com/>