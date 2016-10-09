from math import sqrt

from scipy.stats import t
from numpy import mean

def degrees_of_freedom(s1, s2, n1, n2):
    """
    Compute the number of degrees of freedom using the Satterhwaite Formula
    
    @param s1 The unbiased sample variance of the first sample
    @param s2 The unbiased sample variance of the second sample
    @param n1 Thu number of observations in the first sample
    @param n2 The number of observations in the second sample
    """

    var_smean1 = (s1 ** 2) / n1
    var_smean2 = (s2 ** 2) / n2
    numerator = (var_smean1 + var_smean2) ** 2
    denomenator = ((var_smean1 ** 2) / (n1 - 1)) + ((var_smean2 ** 2) / (n2 - 1))

    return numerator / denomenator

def unbiased_sample_variance(observations, mean):
    """
    Compute the unbiased sample variance

    @param observations Iterable set of observations
    @param mean The estimated mean
    """
    
    return sum(((observation - mean) ** 2) / (len(observations) - 1) for observation in observations)

def t_statistic(mean1, mean2, n1, n2, svar1, svar2):
    """
    Compute the t-statistic for the given estimates
    """

    return (mean1 - mean2) / sqrt((svar1/n1) + (svar2 / n2))

def t_test(sample1, sample2):
    """
    Return the two-tailed p-value of a t test with unequal variance for two samples.

    @param sample1 An iterable of the first sample
    @param sample2 An iterable of the second sample
    """
    # Calculating necessary values
    mean1 = mean(sample1)
    mean2 = mean(sample2)
    svar1 = unbiased_sample_variance(sample1, mean1)
    svar2 = unbiased_sample_variance(sample2, mean2)
    n1 = len(sample1)
    n2 = len(sample2)
    tstat = t_statistic(mean1, mean2, n1, n2, svar1, svar2)
    df = degrees_of_freedom(svar1, svar2, n1, n2)
    cdf = t.cdf(tstat, df)

    return (1 - cdf) * 2

if __name__ == "__main__":
    v1 = [5, 7, 5, 3, 5, 3, 3, 9]
    v2 = [8, 1, 4, 6, 6, 4, 1, 2]

    print("p-value is %f" % t_test(v1, v2))
    
