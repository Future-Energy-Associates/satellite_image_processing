call cd ..
call conda env create -f environment.yml
call conda activate sat_image_processing
call ipython kernel install --user --name=sat_image_processing
pause