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