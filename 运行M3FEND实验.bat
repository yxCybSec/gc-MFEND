@echo off
chcp 65001 >nul
echo ========================================
echo M3FEND 论文实验运行脚本
echo ========================================
echo.

:menu
echo 请选择运行模式:
echo 1. 运行单个实验
echo 2. 只运行M3FEND的主要实验 (推荐，4个配置)
echo 3. 运行所有论文实验 (44个实验，需要很长时间)
echo 4. 退出
echo.
set /p choice=请输入选项 (1-4): 

if "%choice%"=="1" goto single
if "%choice%"=="2" goto m3fend
if "%choice%"=="3" goto all
if "%choice%"=="4" goto end
goto menu

:single
echo.
echo 运行单个实验
echo.
set /p dataset=请输入数据集 (ch/en, 默认ch): 
if "%dataset%"=="" set dataset=ch
set /p domain_num=请输入领域数量 (中文:3/6/9, 英文:3, 默认3): 
if "%domain_num%"=="" set domain_num=3
set /p model=请输入模型名称 (默认m3fend): 
if "%model%"=="" set model=m3fend
set /p gpu=请输入GPU索引 (默认0): 
if "%gpu%"=="" set gpu=0
python run_experiments.py --mode single --dataset %dataset% --domain_num %domain_num% --model %model% --gpu %gpu%
goto end

:m3fend
echo.
echo 运行M3FEND的主要实验...
echo.
python run_experiments.py --mode m3fend
goto end

:all
echo.
echo 警告: 这将运行44个实验，可能需要很长时间！
echo.
set /p confirm=确认继续? (y/n): 
if /i not "%confirm%"=="y" goto menu
python run_experiments.py --mode all
goto end

:end
echo.
echo 完成！
pause
