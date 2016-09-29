from collections import defaultdict
from csv import DictReader, DictWriter
import heapq

kHEADER = ["STATE", "DISTRICT", "MARGIN"]

def district_margins(state_lines):
    """
    Return a dictionary with districts as keys, and the difference in
    percentage between the winner and the second-place as values.

    @lines The csv rows that correspond to the districts of a single state
    """

    # Complete this function
    districts = dict()
    margins = dict()

    for x in state_lines:
        if x["D"] and not (x["D"] == "H" or " - UNEXPIRED TERM" in x["D"]) and x["GENERAL %"]:
            if (" - FULL TERM" in x["D"]):
                district = int(x["D"][1])
            else:
                district = int(x["D"])

            # Hard code West Virginia districts 3 and 5 to account for data mistakes.
            if (x["STATE"] == "West Virginia" and district == 3):
                districts[district] = [10.700000000000003]
            elif (x["STATE"] == "West Virginia" and district == 5):
                continue
            else: # For all other districts add the percentages to their district array.
                if (district not in districts.keys()):
                    districts[district] = [float(x["GENERAL %"].replace(',', '.').rstrip('%'))]
                else:
                    districts[district] = districts[district] + [float(x["GENERAL %"].replace(',', '.').rstrip('%'))]

    # Parse through the district arrays to find the top two and compute the margin.
    for (x, y) in districts.items():
        topTwo = heapq.nlargest(2, y)
        if (len(topTwo) > 1):
            margins[x] = topTwo[0] - topTwo[1]
        else:
            margins[x] = topTwo[0]

    return margins

def all_states(lines):
    """
    Return all of the states (column "STATE") in list created from a
    CsvReader object.  Don't think too hard on this; it can be written
    in one line of Python.
    """

    # Complete this function
    return set(list(x["STATE"] for x in lines if x["STATE"]))

def all_state_rows(lines, state):
    """
    Given a list of output from DictReader, filter to the rows from a single state.

    @state Only return lines from this state
    @lines Only return lines from this larger list
    """

    # Complete/correct this function
    for ii in lines:
        if (ii["STATE"] == state):
            yield ii

if __name__ == "__main__":
    # You shouldn't need to modify this part of the code
    lines = list(DictReader(open("../data/2014_election_results.csv")))
    output = DictWriter(open("district_margins.csv", 'w'), fieldnames=kHEADER)
    output.writeheader()

    summary = {}
    for state in all_states(lines):
        margins = district_margins(all_state_rows(lines, state))

        for ii in margins:
            summary[(state, ii)] = margins[ii]

    for ii, mm in sorted(summary.items(), key=lambda x: x[1]):
        output.writerow({"STATE": ii[0], "DISTRICT": ii[1], "MARGIN": mm})
