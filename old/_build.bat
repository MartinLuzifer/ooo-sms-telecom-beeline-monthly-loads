set ProgramName=BeelineLoad
set py_file=load.py

set Catalog=%UserProfile%\Desktop\%ProgramName%
mkdir %Catalog%

pyinstaller %py_file% --onefile --name "%ProgramName%" --distpath %Catalog% --workpath %Catalog%\bin 
rmdir %Catalog%\bin /q /s

copy account.json %Catalog%\account.json

timeout 12
