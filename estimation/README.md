
Estimating Distribution Parameters
===============

Overview
---------------

This program will be autograded.  That means that it's important to
not change function names and to not add additional functionality that
may improve the program but produce different results.  Make sure that
your unit tests pass.  This what a successful set of unit tests will
look like:

    $ python3 tests.py
    .....
    ----------------------------------------------------------------------
    Ran 5 tests in 0.002s
    
    OK

Districts (10 points)
----------------------------

In the US, our legislature is made up of representatives of individual
*districts* (unlike proportional representation systems).  Your task
is to characterize districts in "Red" Republican states vs. districts
in "Blue" Democratic states.

First, you'll need to extract the Republican share of the vote in a
district.  Then, you will need to compute the parameters of a Gaussian
distribution, then compute the probability of an observation given
those parameters.

You will need to implement the following functions:
* ml_mean
* ml_variance
* log_probability
* republican_share

After you've done that, the main function will then report for each of
Colorado's district whether it looks more like a red state or a blue state.

Words Presidents Use (20 points)
-------------------------------

Each year, the president of the United States is required to make a
speech to congress describing the "State of the Union".  We are going
to create a simple *bigram language model* with *add one (Laplace)*
smoothing.  Your task is to characterize Republican vs. Democrat
presidents based on their speech.

To do this, you'll need to implement the following functions:
* train_seen
* generate
* laplace
* add_train
* log_likelihood

WARNING: Writing a unit test for generation is tricky (without
creating a testing stub for the random number generator), so make sure
you are thorough in making sure this works correctly.

The first few lines of your output file will look something like:

	Trained language model for D
	Done looking at R words, finalizing vocabulary
	Trained language model for R
	REP		DEM		Sentence
	================================================================================
	-5.555665	-5.901752	Mr. Speaker, Mr. Vice President, Members of Congress, my fellow Americans:
	-6.474396	-6.601745	And for this final one, I’m going to try to make it a little shorter.
	-5.409701	-5.095949	I've been there.
	-6.723085	-6.627878	And I understand that because it’s an election season, expectations for what we will achieve this year are low.
	-6.920930	-7.094266	But, Mr. Speaker, I appreciate the constructive approach that you and the other leaders took at the end of last year to pass a 		budget and make tax cuts permanent for working families.
	-7.753715	-7.508743	So, who knows, we might surprise the cynics again.
	-6.370917	-6.343508	But tonight, I want to go easy on the traditional list of proposals for the year ahead.
	-6.160787	-6.262366	And I will keep pushing for progress on the work that I believe still needs to be done.
	-7.437942	-7.276854	Fixing a broken immigration system.


Note: Don't worry about getting the exact same log probabilities as here (they might vary depending on the log base you're using, and also Laplace smoothing parameter).



Writeup (10 points)
-----------------------

Finally, include a brief plain-text file (not PDF, not Word, just a
plain ASCII text file) that:
* Describes your approach
* Describes whether Colorado's congression districts look more like
  the congressional districts of states that Obama won or that Romeny
  won
* Plot a
  [histogram](http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html)
  of both the Obama and Romney states.  Is it resonable to assume that
  these are a normal distribution?
* Gives an interesting example of a *word* that Obama said that no
  previous president said
* Gives an interesting example of a *bigram* that Obama said that no
  previous president said
* Generates a random sentence from a Republican and a Democrat.

Submitting Your Code
-----------------------

You'll need to submit your assignment (lm.py, districts.py,
histogram.png, and writeup.txt) on Moodle as an upload.
