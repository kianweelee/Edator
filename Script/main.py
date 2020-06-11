#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 11:07:29 2020

@author: kianweelee
"""

# Importing the required packages
import os.path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import PySimpleGUI as sg
from sklearn.impute import SimpleImputer
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import linregress
from scipy.stats import chi2_contingency
import itertools
from sklearn.preprocessing import LabelEncoder
from Report import model
from Graph import plot

def main():
    # Create a path to access csv file and also define a path to deposit EDA plots and report
        ## Required to create a GUI using pySimpleGUI

    layout = [
    [sg.Frame(layout=[
    [sg.Radio('CSV', "file_format", default=True, size=(10,1)), sg.Radio('XLS', "file_format")]], title='File Format',title_color='red', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Please input the folder path')],
    [sg.Text('File path:', size=(18, 1)), sg.Input(), sg.FileBrowse()],
    [sg.Text('Export plots to:', size=(18, 1)), sg.Input(), sg.FolderBrowse()],
    [sg.Text('Export report to:', size=(18, 1)), sg.Input(), sg.FolderBrowse()],
    [sg.Text('Export cleaned csv to:', size=(18, 1)), sg.Input(), sg.FolderBrowse()],
    [sg.Submit(), sg.Cancel()]]

    window = sg.Window('Edator', layout)

    event, values = window.read()
    csv_option, xls_option, file_path, plot_path, report_path, clean_csv_path = values[0], values[1], values[2], values[3], values[4], values[5]
    print(values[0])
    print(values[1])
    window.close()

    # Creating a txt file in the report_path
    filename = os.path.join(report_path, "report" + ".txt")

    # Assigning csv file to a variable call 'data'
    if csv_option:
    	data = pd.read_csv(file_path)
    else:
    	data = pd.read_excel(file_path, index_col=0)

    # Create a function to separate out numerical and categorical data
        ## Using this function to ensure that all non-numerical in a numerical column
        ## and non-categorical in a categorical column is annotated
    def cat_variable(df):
        return list(df.select_dtypes(include = ['category', 'object']))

    def num_variable(df):
        return list(df.select_dtypes(exclude = ['category', 'object']))

    categorical_variable = cat_variable(data)
    numerical_variable = num_variable(data)

    # Assigning variable filename to report and enable writing mode
    report = open(filename, "w")

    # Execute overview function in model module
    data = model.overview(data, numerical_variable, report)


    # Create a function to decide whether to drop all NA values or replace them
    ## Drop it if NAN count < 5 %
    nan_prop = (data.isna().mean().round(2)*100) # Show % of NaN values per column

    def drop_na():
        return [i for i, v in nan_prop.items() if v < 5 and v > 0]

    cols_to_drop = drop_na()

    data = data.dropna(subset = cols_to_drop)


    ## Using Imputer to fill NaN values
    ## Counting the proportion of NaN

    def fill_na():
        return [i for i, v in nan_prop.items() if v > 5]

    cols_to_fill = fill_na()

    cat_var_tofill = []
    num_var_tofill = []

    for var in cols_to_fill:
        if var in categorical_variable:
            cat_var_tofill.append(var)
        else:
            num_var_tofill.append(var)

    imp_cat = SimpleImputer(missing_values = np.nan, strategy='most_frequent')
    try:
        data[cat_var_tofill] = imp_cat.fit_transform(data[cat_var_tofill])
    except ValueError:
        pass

    imp_num = SimpleImputer(missing_values = np.nan, strategy='median')
    try:
        data[num_var_tofill] = imp_num.fit_transform(data[num_var_tofill])
    except ValueError:
        pass

    # Create a function to process outlier data
    def outlier():
        z = np.abs(stats.zscore(data[numerical_variable]))
        z_data = data[(z < 3).all(axis=1)] # Remove any outliers with Z-score > 3 or < -3
        return z_data

    data = outlier()

    # Create a function to compute correlation
    ## Pearson and Spearsman correlation for numerical-numerical data
    ## One-Way ANOVA for numerical-categorical data
    ## Chi-Square test for categorical-categorical data

    ## Creating possible combinations among a list of numerical variables
    num_var_combination = list(itertools.combinations(numerical_variable, 2))

    ## Creating possible combinations among a list of categorical variables
    cat_var_combination = list(itertools.combinations(categorical_variable, 2))

    ## Creating possible combinations among a list of numerical and categorical variuable
    catnum_combination = list(itertools.product(numerical_variable, categorical_variable))

    ## Running the report now
    model.run(num_var_combination,catnum_combination,cat_var_combination,report,data)

    # Create an output file that shows cleaned data
    data2 = data.copy()
    data2.to_csv(r'{}/cleaned_csv.csv'.format(clean_csv_path), index = False)

    # Running plot.py from Graph package
    plot.run(data, categorical_variable,numerical_variable,plot_path)



# Running program
if __name__ == "__main__":
    main()