import seaborn as sns
import itertools
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Create a function for plots
    ## Look into making count plots for categorical data
    ## Look into making scatterplots and barplot for numerical data
    ## Export plots into plot path
def run(data,categorical_variable,numerical_variable, num_var_combination,cat_var_combination,catnum_combination,plot_path):

    ## Set Unique categorical values that are < 5 as hue
    hue_lst = []
    for x in categorical_variable:
        if len(set(data[x])) <= 5: # if we have less than 5 unique values, we will use it for hue attributes
            hue_lst.append(x)
    ## Creating possible combinations among a list of numerical variables
    num_var_combination = list(itertools.combinations(numerical_variable, 2))
    ## Creating possible combinations among a list of categorical variables
    cat_var_combination = list(itertools.combinations(categorical_variable, 2))
    ## Creating possible combinations among a list of numerical and categorical variuable
    catnum_combination = list(itertools.product(numerical_variable, categorical_variable))

    ## Using regplot for numerical-numerical variables
    num_var_hue_combination = list(itertools.product(num_var_combination, hue_lst))
    for i in num_var_hue_combination:
        var1 = i[0][0]
        var2 = i[0][1]
        hue1 = i[1]
        plot1 = sns.scatterplot(data = data, x = var1, y = var2, hue = hue1)
        fig1 = plot1.get_figure()
        fig1.savefig(plot_path + "/{} vs {} by {} scatterplot.png".format(var1,var2, hue1))
        fig1.clf()


    ## Using countplot for categorical data
    for j in categorical_variable:
        plot2 = sns.countplot(data = data, x = j)
        fig2 = plot2.get_figure()
        fig2.savefig(plot_path + "/{}_countplot.png".format(j))
        fig2.clf()

    ## Using barplot for numerical + Categorical data
    for k in catnum_combination:
        num1 = k[0]
        cat1 = k[1]
        plot3 = sns.barplot(data = data, x = cat1, y = num1)
        fig3 = plot3.get_figure()
        fig3.savefig(plot_path + "/{}_{}_barplot.png".format(num1,cat1))
        fig3.clf()

    ## Creating heatmap to show correlation
    le = LabelEncoder()
    for cat in data[categorical_variable]:
        data[cat] = le.fit_transform(data[cat])
    plt.figure(figsize=(15,10))
    corrMatrix = data.corr()
    plot4 = sns.heatmap(corrMatrix, annot=True)
    fig4 = plot4.get_figure()
    fig4.savefig(plot_path + "/heatplot.png")
    fig4.clf()