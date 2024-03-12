REM 批处理文件名: run_daily_script.bat

@echo off
REM 设置 Python 解释器路径
set PYTHON="C:\Users\administr\anaconda3\envs\pv\python.exe"

REM 设置 Python 脚本路径
set SCRIPT="C:\Users\administr\pv\auto_run_10p.py"

REM 运行 Python 脚本
%PYTHON% %SCRIPT%