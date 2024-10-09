@echo off
setlocal

REM Проверка на наличие ключа для 7-Zip
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\7-Zip" >nul 2>&1

REM Если ключ найден, записываем 1 в файл result.txt
if %errorlevel%==0 (
    echo 1 > result.txt
) else (
    REM Если ключ не найден, записываем 0 в файл result.txt
    echo 0 > result.txt
)

endlocal
