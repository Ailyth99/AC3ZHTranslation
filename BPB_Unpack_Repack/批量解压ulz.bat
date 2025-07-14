@echo off
setlocal

:input_folder
set /p "folder=请输入要遍历的文件夹路径: "
if not exist "%folder%" (
  echo not_exist
  goto input_folder
)

echo 正在遍历 "%folder%" 及其子文件夹中的 ulz 文件...

for /r "%folder%" %%a in (*.ulz) do (
  echo umcprs: %%a
  ac3es_tools ulz --decompress "%%a"
  if errorlevel 1 (
    echo uncprs "%%a" fail!
  ) else (
    echo uncprs "%%a" success!
  )
)

echo 完成!
endlocal
pause