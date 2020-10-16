set anaconda_dir=%1
call %anaconda_dir%/Scripts/activate.bat %anaconda_dir%
call cd ..
call conda activate sat_image_processing
call python setup.py sdist bdist_wheel
call twine upload dist/*
pause