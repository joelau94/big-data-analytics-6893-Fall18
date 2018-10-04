#!/bin/bash

# Recommendation
python rec.py \
    --data-file ../data/movielens-20m-dataset/rating.csv \
    --sample-rate 0.1 \
    --rank 10 \
    --num-iters 10 \
    --reg-lambda 0.1 \
    --seed 23 \
    --task MovieLens

python rec.py \
    --data-file ../data/restaurant-data/rating_final.csv \
    --sample-rate 1.0 \
    --rank 5 \
    --num-iters 10 \
    --reg-lambda 0.1 \
    --seed 23 \
    --task Restaurant

python rec.py \
    --data-file ../data/songs-dataset/songsDataset.csv \
    --sample-rate 0.1 \
    --rank 20 \
    --num-iters 10 \
    --reg-lambda 0.1 \
    --seed 23 \
    --task Songs

# Regression
# Decision Tree
python reg_cls.py \
    --data-file ../data/cadata-regression/cadata.libsvm \
    --data-format libsvm \
    --model DecisionTreeRegressor \
    --max-categories 4

# Random Forest
python reg_cls.py \
    --data-file ../data/cadata-regression/cadata.libsvm \
    --data-format libsvm \
    --model RandomForestRegressor \
    --max-categories 4

# Gradient-boost Trees
python reg_cls.py \
    --data-file ../data/cadata-regression/cadata.libsvm \
    --data-format libsvm \
    --model GBTRegressor \
    --max-categories 4 \
    --max-iter 10

# Classification
# Decision Tree
python reg_cls.py \
    --data-file ../data/cod-rna-classification/cod-rna.libsvm \
    --data-format libsvm \
    --model DecisionTreeClassifier \
    --max-categories 4

# Random Forest
python reg_cls.py \
    --data-file ../data/cod-rna-classification/cod-rna.libsvm \
    --data-format libsvm \
    --model RandomForestClassifier \
    --max-categories 4 \
    --num-trees 10

# Gradient-boost Trees
python reg_cls.py \
    --data-file ../data/cod-rna-classification/cod-rna.libsvm \
    --data-format libsvm \
    --model GBTClassifier \
    --max-categories 4 \
    --max-iter 10