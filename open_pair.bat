@echo off
chcp 65001 > nul
rem --------------------------------
rem open_seq_simult_utf8.bat  （UTF-8 BOMなしで保存すること）
rem 
rem color フォルダ内の *_c.png を順に処理し、
rem 各ペアを同時に開き、キー入力で次へ進むサンプル
rem --------------------------------

setlocal enabledelayedexpansion

set "COLOR_DIR=color"
set "DEPTH_DIR=depth_vi"

rem color フォルダ内の *_c.png を展開して配列に格納
set INDEX=0
for %%F in ("%COLOR_DIR%\*_c.png") do (
    set /a INDEX+=1
    set "IMG!INDEX!=%%~F"
)

if %INDEX% EQU 0 (
    echo [WARN] color フォルダに対象画像が見つかりませんでした。
    goto END
)

set /a CURRENT=1

:PROCESS_LOOP
if %CURRENT% GTR %INDEX% (
    echo 全ファイルを処理しました。
    goto END
)

set "COLOR_PATH=!IMG%CURRENT%!"
for %%A in ("!COLOR_PATH!") do (
    set "FNAME=%%~nA"
)
rem ベース名（末尾の "_c" を取り除く）
set "BASE=!FNAME:~0,-2!"
set "DEPTH_PATH=%DEPTH_DIR%\!BASE!_depth_vi.png"

echo ================================================
echo [%CURRENT%/%INDEX%] Opening both:
echo    Color: !COLOR_PATH!
echo    Depth: !DEPTH_PATH!
echo ================================================

rem ① Labelme と深度画像を同時に起動
start "" labelme "!COLOR_PATH!"
if exist "!DEPTH_PATH!" (
    start "" "!DEPTH_PATH!"
) else (
    echo [WARN] 対応する深度画像が見つかりません: !DEPTH_PATH!
)

echo.
echo 次のペアを開くには何かキーを押してください…
pause >nul
echo.

set /a CURRENT+=1
goto PROCESS_LOOP

:END
echo バッチを終了します。
endlocal
