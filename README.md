WineQuality dataset from Kaggle is used for prediction.

We used Data Version Contol to orchetrate the pipeline. 

![image](https://user-images.githubusercontent.com/49258919/175524368-a535439c-c1d9-474b-a95d-756492e722d0.png)

•	In DVC at each stage, artifacts are produced as an output and is serving as an input to the next stage. 
•	DVC is used for data and source versioning. 
•	In DVC let’s say if there is a change in preprocessing then only preprocessing stage will run, the rest will not while in traditional ML this is not the case. 
•	In DVC the hashing and size are used for versioning. 
•	I first created a template.py where in it is mentioned what all folders need to be created. 
•	dvc.yaml is created to mention the stages of our pipeline. 
•	There is also params.yaml where all the hyperparameters and other parameters are mentioned which we are going to use in different stages. 
•	We created setup.py where we have mentioned the path of src so that we can use src as a package. 
•	Src contains all the python files. 

conda create -n wineq1 python=3.7 -y

conda activate wineq1

pip install -r requirements.txt
 
python template.py

git init

dvc init

dvc add data_given\winequalityN.csv

git add .

git commit -m 'first commit'

git remote add origin https://github.com/meghajadav/simple-dvc.git

git branch -M main

git push origin main

python src\get_data.py



python load_data.py

dvc repro

git add .

git commit -m 'stage 1 complete'

git push origin main

tox command
'''
tox
'''
tox rebuilding
'''
tox -r
'''
pytest command
'''
pytest -v
'''

setup commands
'''
pip install -e .
'''

build your own package commands
'''
python setup.py sdist bdist_wheel
'''
