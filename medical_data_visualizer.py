import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv(r'/workspace/boilerplate-medical-data-visualizer/medical_examination.csv')


# 2
def get_overweight(row):
    bmi=row.weight/((row.height*0.01)**2)
    if bmi>25:
        row['overweight']=1
    else:
        row['overweight']=0
    return row
df=df.apply(get_overweight,axis=1)


# 3

df['cholesterol']=df['cholesterol'].map(lambda x : 0 if x<=1 else 1)
df['gluc']=df['gluc'].map(lambda x : 0 if x<=1 else 1)
df = df.astype({
    'id': 'int',
    'age': 'int',
    'sex': 'int',
    'height': 'int',
    'weight': 'int',
    'ap_hi': 'int',
    'ap_lo': 'int',
    'cholesterol': 'int',
    'gluc': 'int',
    'smoke': 'int',
    'alco': 'int',
    'active': 'int',
    'cardio': 'int',
    'overweight': 'int'
})
# 4
def draw_cat_plot():
    # 5
    df_cat = df_cat = pd.melt(
        df,
        id_vars='cardio',
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'],
        var_name='variable',
        value_name='value'
    )


    # 6
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    

    # 7



    # 8
    df_cat['total'] = 1
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).count().reset_index()

    # Create the categorical plot
    g = sns.catplot(
    x="variable",
    y="total",
    hue="value",
    col="cardio",
    kind="bar",
    data=df_cat,
    height=4,
    aspect=1.2
)

    #   Save the plot as a file

    # Return the figure object
    fig = g.fig

    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df.loc[df['ap_lo'] <= df['ap_hi']]
    df_heat=df_heat.loc[(df['height'] >= df['height'].quantile(0.025))&(df['height'] <= df['height'].quantile(0.975))&(df['weight'] >= df['weight'].quantile(0.025))&(df['weight'] <= df['weight'].quantile(0.975))]

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # 14
    fig, ax = plt.subplots(figsize=(10, 8))

    # 15
    sns.heatmap(
    corr,
    annot=True,
    mask=mask,
    vmin=-1,
    vmax=1,
    center=0,
    square=True,
        fmt=".1f", 
    linewidths=0.5,
    cbar_kws={"shrink": .75},
    ax=ax
)


    # 16
    fig.savefig('heatmap.png')
    return fig
