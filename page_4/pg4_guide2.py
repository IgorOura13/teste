# Internal library
from utils import show_code
from machine_learning_algorithm import train_model

# Code

def run_guide2():
    extra = '''
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
from imblearn.over_sampling import RandomOverSampler

def train_model(input):
    '''
    show_code(train_model, extra)