@echo off
setlocal EnableDelayedExpansion

:input_source_folder
set /p "source_folder=Please enter the source folder path containing TIM files: "
if not exist "%source_folder%" (
  echo Source folder does not exist. Please enter again.
  goto :input_source_folder
)

:input_target_folder
set /p "target_folder=Please enter the target folder path to copy TIM files to: "
if not exist "%target_folder%" (
  mkdir "%target_folder%"
)

echo Copying TIM files...

for /r "%source_folder%" %%a in (*.tim) do (
  set "filepath=%%~dpnxa"
  set "relative_path=!filepath:%source_folder%=!"
  set "relative_path=!relative_path:\=_!"
  set "relative_path=!relative_path:/=_!"
  set "new_filename=!relative_path:.tim=!.tim"
  echo Copying "%%a" to "%target_folder%\!new_filename!"

  if exist "%target_folder%\!new_filename!" (
    echo File "%target_folder%\!new_filename!" already exists. Skipping.
  ) else (
    copy "%%a" "%target_folder%\!new_filename!"
    if errorlevel 1 (
      echo Failed to copy "%%a"!
    )
  )
)

echo Done!
endlocal
pause