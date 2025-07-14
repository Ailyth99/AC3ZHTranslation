[![Docker Repository on Quay](https://quay.io/repository/loadwordteam/ac3es-tools/status "Docker Repository on Quay")](https://quay.io/repository/loadwordteam/ac3es-tools)
# AC3ES Tools

This is a collection of tools for manipulate games files for the game
Ace Combat 3.

You can edit `bin` containers, TIM files and ACE.BPB/BPH and has a
full working Ulz compressor/decompressor!

## Requirements

Now you need Python >= 3.9

## Usage

The tool has two sub commands, the `ulz` command for compress/decompress files
and `info` for get details about the ulz and the known iso or bpb of
the game.

### Ulz command

```
ac3es ulz [-h] [--compress FILE] [--ulz-type {0,2}]
                 [--level {1,2,4,8}] [--store-only] [--like-file LIKE_FILE]
                 [--decompress ULZ] [--output-file FILE] [--parents]
                 [--keep]

optional arguments:
  -h, --help            show this help message and exit
  --compress FILE, -c FILE
                        Compress the file in ulz
  --decompress ULZ, -d ULZ
                        decompress the file in the current directory
  --output-file FILE, -f FILE
                        override output filename
  --parents, -p         Create directories for destination files if they don't
                        exists
  --keep, -k            prompt before every removal or destructive change

compression:
  --ulz-type {0,2}      Define the ulz version to use
  --level {1,2,4,8}, -l {1,2,4,8}
                        Compression levels 1/2/4/8 uses a search buffer
                        1024/2048/4096/8192 bytes long.
  --store-only, -s      Store data on ulz file, needs anyway a compression
                        level
  --like-file LIKE_FILE
                        Get compression parameters from file
```

### Bin command

```
usage: ac3es bin [-h] [--split BIN_FILE] [--out-directory DIRECTORY] [--out-list DIRECTORY] [--merge-dir DIR]
                 [--merge-list FILE_LIST] [--merge-files FILES [FILES ...]] [--out-bin FILE_BIN] [--verbose]

options:
  -h, --help            show this help message and exit
  --split BIN_FILE, -s BIN_FILE
                        Split a bin container
  --merge-dir DIR       Create a bin file from a directory, entries will be sorted alphabetically
  --merge-list FILE_LIST
                        Use a file with filenames to create a bin, sorts the names first alphabetically
  --merge-files FILES [FILES ...]
                        Reconstruct a bin file starting from a list of given filenames, no sort is applied

bin split:
  --out-directory DIRECTORY, -d DIRECTORY
                        Output directory where to store the bin's components
  --out-list DIRECTORY, -f DIRECTORY
                        Save a components' list to a txt
  --out-bin FILE_BIN, -b FILE_BIN
                        Output bin filename
  --verbose, -v         Print more information while merges

```

### Info command

```
ac3es info [-h] FILES [FILES ...]

positional arguments:
  FILES       One or more file to get info

optional arguments:
  -h, --help  show this help message and exit
```

### TIM editing command

```
ac3es tim [-h] --source-tim TIM_FILE [--copy-header] [--copy-clut]
                    [--copy-vram] [--set-vram-x X] [--set-vram-y Y]
                    FILES [FILES ...]

positional arguments:
  FILES                 Apply the changes to one or more TIM files

optional arguments:
  -h, --help            show this help message and exit
  --source-tim TIM_FILE, -s TIM_FILE
                        Source TIM
  --copy-header         Copy the entire header data from source
  --copy-clut           Copy CLUT data from source
  --copy-vram           Copy V-RAM coordinates
  --set-vram-x X        Set V-RAM coordinate X
  --set-vram-y Y        Set V-RAM coordinate Y
```

### BPB unpack/repack command

```
ac3es bpb [-h] [--unpack DIRECTORY | --pack DIRECTORY]
                    [--bpb ACE.BPB] [--bph ACE.BPH]

optional arguments:
  -h, --help            show this help message and exit
  --unpack DIRECTORY, -u DIRECTORY
                        Unpack ACE.BPB/BPH to the given directory
  --pack DIRECTORY, -p DIRECTORY
                        Pack ACE.BPB and create ACE.BPH from a given directory
  --bpb ACE.BPB         Path for ACE.BPB
  --bph ACE.BPH         Path for ACE.BPH
```

### Examples

Compress an image and put the output into the same directory

```
ac3es ulz --compress image.tim --ulz-type=2 --level=1
```

or define another destination

```
ac3es ulz --compress jap_0002.tim --ulz-type=2 --level=1 --output-file=mycompress.ulz
```

Get what parameters use from the original file

```
ac3es info BPB/0386/0001/0000.ulz
```

Work on bin containers

```
ac3es bin --split=BPB/0114/0007.bin --out-directory=splitted/0007 --out-list=splitted/0007.txt
ac3es bin --merge-list=splitted/0007.txt --out-bin=mod_0007.bin
```

More parameters are available, just type help for the sub command

```
ac3es ulz --help
ac3es info --help
ac3es bin --help
ac3es tim --help
ac3es bpb --help
```

### Ulz compression type 0 vs type 2


They are basically the same, ulz 0 is meant to decompress faster than
ulz 2. In reality doesn't matter, the difference are few lines of
ASM inside the ACE.BIN executable.

Ulz type 0 produces files at least 4 bytes bigger than ulz 2, because
the compressed data is store a bit different regardless the
compression ratio. Read the source code for more details.

They are both based on LZ77 and I compress using the same algorithm. I
don't know why they used two nearly identical formats.

### Changelog

#### 3.0

- Tons of bugfix
- Total refactor

##### Breaking changes
The _merge_ command has been splitted up (pun intended) into

- merge-dir: to merge the content from a given directory
- merge-list: to create a bin from a txt with a list of paths
- merge-files: useful to create a bin on-the-fly

#### 2.5.0

- Shortcut -t in ulz compress
- Unpack bpb now returns the offsets
- You can recompress ulz files in place

#### 2.3.2

Fix copy-header offsets

#### 2.3.1

Add copy-header switch for TIM

#### 2.3

Unpack/repack ACE.BPB and ACE.BPH

#### 2.2

Edit TIM header and CLUT data

#### 2.1

Split and merge bin containers

#### 2.0

Ulz type 0 compression is finally working

## Contributors

- Orientalcomputer_1
- IlDucci

## Contacts

Gianluigi "Infrid" Cusimano <infrid@infrid.com>

https://loadwordteam.com/

[![a project by load word team](https://loadwordteam.com/logo-lwt-small.png "a project by load word team")](https://loadwordteam.com)

