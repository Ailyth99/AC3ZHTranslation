@echo off
setlocal

:input_folder
set /p "folder=A folder contain ULZ files: "
if not exist "%folder%" (
  echo not_exist
  goto input_folder
)

echo UNCOMPRESSING "%folder%" ...

for /r "%folder%" %%a in (*.ulz) do (
  echo umcprs: %%a
  ac3es_tools ulz --decompress "%%a"
  if errorlevel 1 (
    echo uncprs "%%a" fail!
  ) else (
    echo uncprs "%%a" success!
  )
)

echo COMPLETE!
endlocal
pause