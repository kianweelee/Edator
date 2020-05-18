![](https://raw.githubusercontent.com/kianweelee/Edator/master/Image/eau%20de%20parfum.png)
# Edator
 This is a python package that performs exploratory data analysis for users. It takes in a csv file and generates 3 documents that comprise of a text report containing a descriptive summary, a series of plots and a cleaned csv output.
 
## Set up
### Dependencies 
- Python 3.8x
- matplotlib==3.1.2
- numpy==1.18.1
- pandas==1.0.0
- PySimpleGUI==4.19.0
- scikit-learn==0.22.1
- scipy==1.4.1
- seaborn==0.10.0
- statsmodels==0.11.1
- more-itertools==8.3.0

### How to set up? (**Important!**)
1. You can clone or download my package.
2. Using terminal, move to the directory. 
   - Example for Mac OS users: 
   ```bash
   $ cd Downloads/Edator
   ```
3. Install the required packages using:
   ```py
   pip install -r requirements.txt
   ```
4. After that, change directory into the Script folder using:
   ```bash
   $ cd Script
   ```
5. Now, execute the main.py file by:
   ```py
   $ python main.py
   ```
6. You should see the following:
![](https://github.com/kianweelee/Edator/blob/master/Image/Screen%20Shot%202020-05-16%20at%204.45.48%20pm.png)

7. Choose the csv file, the path to export the plots, the report and the cleaned csv file to.
8. Done!

## The concept behind Edator

### Dealing with NaN values and zeros
How I deal with NaN value is that I only remove the affected rows when the percentage of NaN within that column is **less than 5%**. This applies to both numerical and categorical values. For anything above 5%, I replace the NaN values with median. For categorical values, the NaN values will be replace by mode.

Dealing with zeros is much harder as it is challenging to differentiate between a zero that is meaningful (has a purpose and should not be removed) and a zero that serves no purpose and can potentially add more noise to the dataset. Hence, I decided to inform the user about the percentage of zeros in the dataset.

### Processing outliers
I use Z-score to detect outliers. If a Z-score is 0, it indicates that the data point’s score is identical to the mean score. A Z-score of 1.0 would indicate a value that is one standard deviation from the mean. Z-scores may be positive or negative, with a positive value indicating the score is above the mean and a negative score indicating it is below the mean.

In most cases, a threshold of 3 or -3 is used to filter off outliers and I have used this approach for all of my analysis.

### Correlation
For correlation, I included:
1. Pearson and Spearman correlation for numerical-numerical variables.
2. One Way ANOVA for numerical-categorical variables
3. Chi-Square test for categorical-categorical variables

Using itertools.combinations, I identify every possible combinations among numerical-numerical variables, numerical-categorical variables and categorical-categorical variables. I then apply the correlation test based on the criteria I have set above.

### Plots
For plots, I created:
1. Scatterplot for numerical variables
2. Countplot for categorical variables
3. Boxplot for numerical-categorical variables

Similar to correlation, I used itertools.combinations to create every possible plot. I have also added the hue feature to each scatterplot. I will only do so when the categorical variable has less than 5 unique values. Example, if hue = "fruits", I should only see 4 types of fruits.

### Upcoming changes
1. Upon obtaining sufficient feedback on this script, I will register this package in PyPI to streamline installation.
2. Instead of generating txt reports, I will utilise HTML and Bootstrap to generate a much more appeasing look.
