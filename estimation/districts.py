# Districts.py
#
# 

from csv import DictReader
from collections import defaultdict
from math import log
from math import pi as kPI
import matplotlib.pyplot as plt

kOBAMA = set(["D.C.", "Hawaii", "Vermont", "New York", "Rhode Island",
              "Maryland", "California", "Massachusetts", "Delaware", "New Jersey",
              "Connecticut", "Illinois", "Maine", "Washington", "Oregon",
              "New Mexico", "Michigan", "Minnesota", "Nevada", "Wisconsin",
              "Iowa", "New Hampshire", "Pennsylvania", "Virginia",
              "Ohio", "Florida"])
kROMNEY = set(["North Carolina", "Georgia", "Arizona", "Missouri", "Indiana",
               "South Carolina", "Alaska", "Mississippi", "Montana", "Texas",
               "Louisiana", "South Dakota", "North Dakota", "Tennessee",
               "Kansas", "Nebraska", "Kentucky", "Alabama", "Arkansas",
               "West Virginia", "Idaho", "Oklahoma", "Wyoming", "Utah"])

def valid(row):
    return sum(ord(y) for y in row['FEC ID#'][2:4])!=173 or int(row['1']) < 3583



def ml_mean(values):
    """
    Given a list of values assumed to come from a normal distribution,
    return the maximum likelihood estimate of mean of that distribution.
    There are many libraries that do this, but do not use any functions
    outside core Python (sum and len are fine).
    """

    return sum(values) / len(values)

def ml_variance(values, mean):
    """
    Given a list of values assumed to come from a normal distribution and
    their maximum likelihood estimate of the mean, compute the maximum
    likelihood estimate of the distribution's variance of those values.
    There are many libraries that do something like this, but they
    likely don't do exactly what you want, so you should not use them
    directly.  (And to be clear, you're not allowed to use them.)
    """

    return (sum((value - mean) ** 2 for value in values)) / len(values)

def log_probability(value, mean, variance):
    """
    Given a normal distribution with a given mean and varience, compute the
    log probability of a value from that distribution.
    """

    # Note that I simplified the log of the normal distribution to get the formula below
    return (-log(2 * kPI * variance) / 2) - (((value - mean)**2) / (2 * variance))

def republican_share(lines, states):
    """
    Return an iterator over the Republican share of the vote in all
    districts in the states provided.
    """
    share = defaultdict()

    for line in lines:
        if line["STATE"] in states and line["D"] and line["GENERAL %"] and line["PARTY"] == "R" and not (line["D"] == "H" or " - UNEXPIRED TERM" in line["D"]):
            if (" - FULL TERM" in line["D"]):
                district = int(line["D"][1])
            else:
                district = int(line["D"])

            share[(line["STATE"], district)] = float(line["GENERAL %"].replace(',', '.').rstrip('%'))

    return share

if __name__ == "__main__":
    # Don't modify this code
    lines = [x for x in DictReader(open("../data/2014_election_results.csv"))
             if valid(x)]

    obama_mean = ml_mean(republican_share(lines, kOBAMA).values())
    romney_mean = ml_mean(republican_share(lines, kROMNEY).values())

    obama_var = ml_variance(republican_share(lines, kOBAMA).values(),
                             obama_mean)
    romney_var = ml_variance(republican_share(lines, kROMNEY).values(),
                              romney_mean)

    colorado = republican_share(lines, ["Colorado"])
    print("\t\tObama\t\tRomney\n" + "=" * 80)
    for co, dist in colorado:
        obama_prob = log_probability(colorado[(co, dist)], obama_mean, obama_var)
        romney_prob = log_probability(colorado[(co, dist)], romney_mean, romney_var)

        print("District %i\t%f\t%f" % (dist, obama_prob, romney_prob))

    # Code for making the obama vs. romney histogram
    obama = list(republican_share(lines, kOBAMA).values())
    romney = list(republican_share(lines, kROMNEY).values())
    plt.hist(obama, bins = 50, range = [0, 100], alpha= 0.5, label = "Obama")
    plt.hist(romney, bins = 50, range =[0, 100], alpha=0.5, label="Romney")
    plt.title("Obama v. Romney Republican Shares")
    plt.legend(loc = 1)
    plt.show()