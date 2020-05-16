from scipy import stats
from scipy.stats import linregress
from scipy.stats import chi2_contingency
import statsmodels.api as sm
from statsmodels.formula.api import ols
import pandas as pd


# Creating a function that provide an overview of the data
    ## To include a comment for each section
    ## To print the first 5 lines of data
    ## To print the shape of data in words
    ## To print the dtypes of each column
    ## To print the number of null values in each columns.
        ## Also to include anything like "no values", "unknown"...
        ## If data isnumeric()
    ## To print the summary of data (i.e. count,mean,min,max)
def overview(df, numerical_variable, report):
    '''


    Parameters
    ----------
    df : DataFrame
        Imported dataframe from csv_path.

    Returns
    -------
    None.

    '''
    data_head = df.head()
    data_shape = df.shape
    data_type = df.dtypes
    df = (df.drop(numerical_variable, axis=1).join(df[numerical_variable].apply(pd.to_numeric, errors='coerce'))) # Converts any non-numeric values in a numerical column into NaN
    null_values = df.isnull().sum()
    zero_prop = ((df[df == 0].count(axis=0)/len(df.index)).round(2)* 100)
    data_summary = df.describe()
    report.write("______Exploratory data analysis summary by Edator______\n\n\n\nThe first 5 rows of content comprise of:\n\n{}\n\n\nThere are a total of {} rows and {} columns.\n\n\nThe data type for each column is:\n\n{}\n\n\nNumber of NaN values for each column:\n\n{}\n\n\n% of zeros in each column:\n\n{}\n\n\nThe summary of data:\n\n{}"
                 .format(data_head, data_shape[0], data_shape[1], data_type, null_values, zero_prop, data_summary))
    return df


# Creating report for correlation
def run(num_var_combination, catnum_combination, cat_var_combination, report,data):
## For numeric variables
# Pearson correlation (Numerical)
    report.write("\n\n\n__________Correlation Summary (Pearson)__________")
    for i in num_var_combination:
        var1 = i[0]
        var2 = i[1]
        pearson_data = linregress(data[var1], data[var2])
        pearson_r2, pearson_pvalue = ((pearson_data[2]**2), pearson_data[3])
        report.write("\n\nThe Pearson R_Square and Pearson P-values between {} and {} are {} and {} respectively."
                 .format(var1, var2, pearson_r2, pearson_pvalue))

    # Spearsman correlation (Ordinal)
    report.write("\n\n\n\n__________Correlation Summary (Spearsman)__________")
    for q in num_var_combination:
        var1 = q[0]
        var2 = q[1]
        spearsman_data = stats.spearmanr(data[var1], data[var2])
        spearsman_r2, spearsman_pvalue = ((spearsman_data[0]**2), spearsman_data[1])
        report.write("\n\nThe Spearsman R_Square and Spearsman P-values between {} and {} are {} and {} respectively."
                 .format(var1, var2, spearsman_r2, spearsman_pvalue))

    ## For numeric-categorical variables
    # ONE WAY ANOVA (Cat-num variables)
    report.write("\n\n\n\n__________Correlation Summary (One Way ANOVA)__________")
    for j in catnum_combination:
        var1 = j[0]
        var2 = j[1]
        lm = ols('{} ~ {}'.format(var1,var2), data = data).fit()
        table = sm.stats.anova_lm(lm)
        one_way_anova_pvalue = table.loc[var2,'PR(>F)']
        report.write("\n\nThe One Way ANOVA P-value between {} and {} is {}."
                 .format(var1, var2, one_way_anova_pvalue))
        
    ## For categorical-categorical variables
    # Chi-Sq test
    report.write("\n\n\n\n__________Correlation Summary (Chi Square Test)__________")
    for k in cat_var_combination:
        cat1 = k[0]
        cat2 = k[1]
        chi_sq = pd.crosstab(data[cat1], data[cat2])
        chi_sq_result = chi2_contingency(chi_sq)
        report.write("\n\nThe Chi-Square P-value between {} and {} is {}."
                 .format(cat1, cat2, chi_sq_result[1]))

    report.close()
 
    