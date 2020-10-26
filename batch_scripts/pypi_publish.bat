call cd ..
call conda activate sat_image_processing
call python setup.py sdist bdist_wheel
call twine upload --skip-existing dist/*
pause