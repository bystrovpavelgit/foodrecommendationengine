# Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
# shell script to load data
cd data
unzip yarn-synsets.csv.zip
cd ../models
unzip recipes_nlp_data.csv.zip
cd ..
python3 load_ratings.py

