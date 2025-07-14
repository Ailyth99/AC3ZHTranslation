@echo off 
echo Deleting old CD1 BPB and BPH files...

del ACE.BPB
del ACE.BPH

echo.  
echo -----------------------------
echo Repacking CD1 BPB file...
echo -----------------------------
 
copy cd1_build\ace.bph ace.bph
tools\ac3_repack ace.bpb ace.bph cd1_build\bpb

del cd\cd1.bin
copy cd\orig\cd1.bin cd\cd1.bin
echo.  
echo -----------------------------
echo Rebuilding CD1 image...
echo -----------------------------
 
tools\psx-mode2 cd\cd1.bin /ACE.BPB ACE.BPB
tools\psx-mode2 cd\cd1.bin /ACE.BPH ACE.BPH



echo.  
echo Press any key to exit...  
pause > nul