Data representation and interaction
-----------------------------------

**Data as a table**

Statistical analysis - multiple observations or samples described by a set of different attributes or features

Pandas dataframe - It is different from a 2D numpy array as it has named columns, can contain a mixture of different data types by column, and has elaborate selection and pivotal mechanisms.

Creating dataframes: Reading a table from a CSV file or creating from arrays: A `pandas.DataFrame` can also be seen as a dictionary of 1D ‘series’:

    >>> t = np.linspace(-6, 6, 20)
    >>> sin_t = np.sin(t)
    >>> cos_t = np.cos(t)
    >>> pandas.DataFrame({'t': t, 'sin': sin_t, 'cos': cos_t})

    >>> data = pd.read_csv('examples/brain_size.csv')
    >>> data.head()
        Unnamed: 0  Gender  FSIQ  VIQ  PIQ  Weight  Height  MRI_Count
    0            1  Female   133  132  124     118    64.5     816932
    1            2    Male   140  150  124       0    72.5    1001121
    2            3    Male   139  123  150     143    73.3    1038437
    3            4    Male   133  129  128     172    68.8     965353
    4            5  Female   137  132  134     147    65.0     951545

    >>> print(data['Gender'])  # Columns can be addressed by name
    >>> data[data['Gender'] == 'Female']['VIQ'].mean()  # Simpler selector
    109.45

    >>> groupby_gender = data.groupby('Gender')  # returns a generator
    >>> list((type(a), type(b)) for a, b in groupby_gender)
    [(str, pandas.core.frame.DataFrame), (str, pandas.core.frame.DataFrame)]
    >>> list((type(a), type(b)) for a, b in groupby_gender['VIQ'])
    [(str, pandas.core.series.Series), (str, pandas.core.series.Series)]

groupby_gender is a powerful object that exposes many operations on the resulting group of dataframes:

    >>> groupby_gender.mean()
    Unnamed: 0   FSIQ     VIQ     PIQ  Weight  Height  MRI_Count
    Gender
    Female       19.65  111.9  109.45  110.45   137.2  65.765   862654.6
    Male         21.35  115.0  115.25  111.60   149.8  67.860   954855.4

Use tab-completion on groupby_gender to find more. Other common grouping functions are median, count (useful for checking to see the amount of missing values in different subsets) or sum. Groupby evaluation is lazy, no work is done until an aggregation function is applied.

    >>> from pandas.tools import plotting
    >>> plotting.scatter_matrix(data[['Weight', 'Height', 'MRI_Count']])

![](../images/pd_plot.png)

Hypothesis testing
------------------

**1-sample t-test: testing the value of a population mean**

`scipy.stats.ttest_1samp()` tests if the population mean of data is likely to be equal to a given value (technically if observations are drawn from a Gaussian distributions of given population mean). It returns the T statistic, and the p-value (see the function’s help):

    >>> stats.ttest_1samp(data['VIQ'], 0)
    Ttest_1sampResult(statistic=30.088099970..., pvalue=1.32891964...e-28)

With a p-value of 10^-28 we can claim that the population mean for the IQ (VIQ measure) is not 0.

**2-sample t-test: testing for difference across populations**

We have seen above that the mean VIQ in the male and female populations were different. To test if this is significant, we do a 2-sample t-test with `scipy.stats.ttest_ind()`:

    >>> female_viq = data[data['Gender'] == 'Female']['VIQ']
    >>> male_viq = data[data['Gender'] == 'Male']['VIQ']
    >>> stats.ttest_ind(female_viq, male_viq)
    Ttest_indResult(statistic=-0.77261617232..., pvalue=0.4445387766858...)

**Paired tests: repeated measurements on the same indivuals**

PIQ, VIQ, and FSIQ give 3 measures of IQ. Let us test if FISQ and PIQ are significantly different. We can use a 2 sample test:

    >>> stats.ttest_ind(data['FSIQ'], data['PIQ'])
    Ttest_indResult(statistic=0.434341903..., pvalue=0.64234434...)

The problem with this approach is that it forgets that there are links between observations: FSIQ and PIQ are measured on the same individuals. Thus the variance due to inter-subject variability is confounding, and can be removed, using a “paired test”, or “repeated measures test”:

    >>> stats.ttest_rel(data['FSIQ'], data['PIQ'])
    Ttest_relResult(statistic=1.78421903..., pvalue=0.082172632434...)

This is equivalent to a 1-sample test on the difference:

    >>> stats.ttest_1samp(data['FSIQ'] - data['PIQ'], 0)
    Ttest_1sampResult(statistic=1.78421903..., pvalue=0.082172632434...)
