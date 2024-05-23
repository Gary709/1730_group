COMP1730/6730 Project Assignment
================================

As we all know the current COVID-19 pandemic has caused a massive impact around the world. It is perhaps the most deadly disease in modern human history. Fortunately, various vaccines have been developed to prevent the infection of SARS-CoV-2, the virus that caused COVID-19.

In an effort to keep track of the global vaccination rates, the “Our World in Data” website has maintained a public data source that updates the total vaccinations for every country/region on a daily basis. In this assignment, you will write a python program to analyse this data and to answer some questions about COVID-19 vaccinations.

Practical information
---------------------

The assignment is due on **Monday the 23rd of May at 9:00am, Canberra time** (the beginning of semester week 12). Like all other due dates, this deadline is hard: **late submissions will NOT be accepted**.

For this assignment, you may work in groups of up to three students. **Working in larger groups (more than three students) is not allowed**. If there is an indication of four or more students working together, or sharing parts of solutions, all students involved will have to be investigated for possible plagiarism.

A [group sign-up activity](https://wattlecourses.anu.edu.au/mod/groupselect/view.php?id=2469996) on wattle is available until the **9th of May at 9:00am (Monday of semester week 10)**. If you intend to work in a group, you and your team mates should find a free group and add yourselves to it. (The group numbers have no meaning; we only care about which students are in the same group.)

Working in a group is not mandatory. If you want to do the assignment on your own, please add yourself to the “_I want to do the assignment on my own_” group, so that we can keep track. Remember that deadline extensions can only ever be given to individuals, not to groups. If you choose to work in a group, it is your responsibility to organise your work so that it cannot be held up by the unexpected absence of one group member.

Each student must submit two files:

1.  Their code (a python file). For students working in a group, it is required that all students in the group submit _identical_ code files.
2.  An individual report, with answers to a set of questions. Details about the format of the report and the questions are in the section [Questions for the individual report](#questions-for-the-individual-report) below.

Data and files provided
-----------------------

The data for global COVID-19 vaccinations by countries are stored in a CSV file:

*   [vaccinations.csv](vaccinations.csv)

(**Please note that when marking we may test your code with this and other CSV files.**)

The file has a header line with names of the columns (see below). The following lines contain actual data. The meanings of the columns are:

*   `location`: name of the country (or region within a country).
*   `iso_code`: ISO 3166-1 alpha-3 – three-letter country codes.
*   `date`: date of the observation.
*   `total_vaccinations`: total number of doses administered. For vaccines that require multiple doses, each individual dose is counted. If a person receives one dose of the vaccine, this metric goes up by 1. If they receive a second dose, it goes up by 1 again. If they receive a third/booster dose, it goes up by 1 again.
*   `people_vaccinated`: total number of people who received at least one vaccine dose. If a person receives the first dose of a 2-dose vaccine, this metric goes up by 1. If they receive the second dose, the metric stays the same.
*   `people_fully_vaccinated`: total number of people who received all doses prescribed by the initial vaccination protocol. If a person receives the first dose of a 2-dose vaccine, this metric stays the same. If they receive the second dose, the metric goes up by 1.
*   `total_boosters`: total number of COVID-19 vaccination booster doses administered (doses administered beyond the number prescribed by the initial vaccination protocol)
*   `daily_vaccinations_raw`: daily change in the total number of doses administered. It is only calculated for consecutive days. This is a raw measure provided for data checks and transparency, but it is strongly recommended that any analysis on daily vaccination rates be conducted using `daily_vaccinations` instead.
*   `daily_vaccinations`: new doses administered per day (smoothed out over a 7-day period). For countries that don’t report data on a daily basis, it is assumed that doses changed equally on a daily basis over any periods in which no data was reported. This produces a complete series of daily figures, which is then averaged over a rolling 7-day window. An example of this calculation can be found [here](https://github.com/owid/covid-19-data/issues/333#issuecomment-763015298).
*   `total_vaccinations_per_hundred`: `total_vaccinations` per 100 people in the total population of the country.
*   `people_vaccinated_per_hundred`: `people_vaccinated` per 100 people in the total population of the country.
*   `people_fully_vaccinated_per_hundred`: `people_fully_vaccinated` per 100 people in the total population of the country.
*   `total_boosters_per_hundred`: `total_boosters` per 100 people in the total population of the country.
*   `daily_vaccinations_per_million`: `daily_vaccinations` per 1,000,000 people in the total population of the country.
*   `daily_people_vaccinated`: daily number of people receiving a _first_ COVID-19 vaccine dose (7-day smoothed).
*   `daily_people_vaccinated_per_hundred`: `daily_people_vaccinated` per 100 people in the total population of the country.

As an example, let’s look at this one line:

```
Australia,AUS,2022-04-11,56805008,22241967,21396664,13166377,53455,38931,220.28,86.25,82.97,51.06,1510,2825,0.011

```

This means that in Australia until April 11th 2022:

*   56,805,008 doses of vaccinations have been given.
*   22,241,967 people have been given at least one dose.
*   21,396,664 people have been fully vaccinated.
*   13,166,377 booster doses have been given
*   53,455 new vaccinations during that one day, i.e., equal to `total_vaccinations` of 2022-04-11 minus that value from 2022-04-10.
*   an average of 38,931 per day over the last 7 days until that date.
*   220.28 vaccine doses per 100 people.
*   86.25 people vaccinated with at least one dose per 100 people.
*   82.97 people fully vaccinated per 100 people.
*   51.06 booster doses per 100 people.
*   1,510 vaccine doses during that day per 1 million people.
*   an average of 2,825 people receiving the first vaccine dose per day during the last 7 days until that date.
*   an average of 0.011 people per 100 people receiving the first vaccine dose per day during the last 7 days until that date.

**NOTE:**

*   The data for `people_vaccinated` and `people_fully_vaccinated` are dependent on the necessary data being made available, so these metrics may not be available for some countries.
*   This dataset includes some subnational locations and international aggregates (World, continents, European Union…). They can be identified by their `iso_code` that starts with `OWID_`.

If you’re interested, you can find the original data files on the [GitHub repository by Our World in Data](https://github.com/owid/covid-19-data).

For information and examples of how to read and process CSV files, see [Lab 6](https://comp.anu.edu.au/courses/comp1730/labs/lab6/).

Questions for analysis (code)
-----------------------------

A template file for the assignment code is provided here:

*   [assignment.py](assignment.py)

In this file, there is only one function that you must implement: `analyse(path_to_file)`. The function takes one argument, which is the complete path to the data file that it should read and analyse. You can assume that the argument is a string. The function should print out the results of the analysis. It does not have to return any value. The specific questions that your analysis should answer are described below. The following are some general requirements and things to keep in mind:

*   You do not have to solve all the questions, but you can only gain marks for the ones that you have attempted (see [Marking criteria](#marking-criteria) below for details on how we will mark your submission).
*   Although we do not specify the exact format in which you should print the results of the analysis, you should make it easy for the user (and marker) to see what is being shown. _Ease of reading the output of your program is part of the marking criteria_.
*   Although there is only one function in the assignment template that you must implement, you can define other functions and use them in your solution. Indeed, _good code organisation, including appropriate use of functional decomposition, is part of the marking criteria_.

### Question 1(a): Counting unique locations

Count how many unique locations are there in the data file and print the result to the screen. For example, the printout for the provided data file may look like this:

```
Analysing data file ./vaccinations.csv

Question 1:
Number of unique locations: 235

```

> Note: The figure can of course be different, if we test your code with a different data file.

### Question 1(b): Counting unique countries

Most of these locations are countries, but some other aggregate or sub-country data has been included which is denoted by `OWID_` as the prefix for the `iso_code` string. Count the number of unique countries (that do not have `OWID_` prefix in the `iso_code`). Print the result like this:

```
Analysing data file ./vaccinations.csv

Question 1:
Number of unique locations: 235
Number of unique countries: 217

```

> Note: The figure can of course be different, if we test your code with a different data file.

_All subsequent questions refer to countries rather than locations._

### Question 1(c): Global vaccince doses

We are now interested in the total number of vaccine doses that have been globally administered in all countries. Note that for each country the vaccinations may increase daily and we of course want to know the latest figure. Print the result like this:

```
Analysing data file ./vaccinations.csv

Question 1:
Number of unique locations: 235
Number of unique countries: 217
Global vaccine doses: ...

```

> Hint: For the data file provided, this figure is about 11 billion.

### Question 1(d): Global population vaccinated

Next, we want to know the global number of people who have received at least one dose over all countries in the world and also those who are fully vaccinated. Print the result like this:

```
Analysing data file ./vaccinations.csv

Question 1:
Number of unique locations: 235
Number of unique countries: 217
Global vaccine doses: ...
Global population vaccinated: ...
Global population fully vaccinated: ...

```

### Question 2(a): Vaccinations by country

We are now interested in the data on a per country basis. Find the top 10 countries with a population of at least 1 million having the highest percentage of their population being vaccinated with at least one dose. Print the result with one line per country in descending order of the percent vaccinated (so that the country with highest percent population vaccinated is printed first), for example, like this:

```
Analysing data file ./vaccinations.csv

Question 1:
...

Question 2:

United Arab Emirates: 98.99% population vaccinated
Portugal: 95.04% population vaccinated
Cuba: 94.03% population vaccinated
...

```

### Question 2(b): Population partly vaccinated by country

For the top-10 countries found above, report the percentage of population being _partly vaccinated_. A person is called partly vaccinated if they already received one dose of vaccine but are not fully vaccinated (e.g., waiting to take the 2nd dose). Extend the output for the top-10 countries to something like:

```
Analysing data file ./vaccinations.csv

Question 1:
...

Question 2:

United Arab Emirates: 98.99% population vaccinated, 2.57% partly vaccinated
Portugal: 95.04% population vaccinated, 2.44% partly vaccinated
Cuba: 94.03% population vaccinated, 6.35% partly vaccinated
...

```

### Question 3(a): Earliest countries

Next, we want to find out, which countries are the earliest in getting their people vaccinated. Print the earliest 10 countries with one line per country, ordered by the earliest date of vaccination like this:

```
Analysing data file ./vaccinations.csv

Question 1:
...

Question 2:
...

Question 3:

Latvia: first vaccinated on 2020-12-04
Norway: first vaccinated on 2020-12-08
Denmark: first vaccinated on 2020-12-08
...

```

### Question 3(b): Peak days

For the top-10 countries found above, we now want to know, which day they administered the highest vaccinations across all days in that country by looking at the field `daily_vaccinations`. Extend the output for the top-10 countries like this:

```
Analysing data file ./vaccinations.csv

Question 1:
...

Question 2:
...

Question 3:

Latvia: first vaccinated on 2020-12-04 , 17035 people vaccinated on 2021-06-02
Norway: first vaccinated on 2020-12-08 , 69115 people vaccinated on 2021-08-30
Denmark: first vaccinated on 2020-12-08 , 133647 people vaccinated on 2021-12-20
...

```

### Question 4(a)

Find the 10 countries the lowest percentage of fully vaccinated people, where these percentages are greater 50%. Print the result like this:

```
Analysing data file ./vaccinations.csv

Question 1:
...

Question 2:
...

Question 3:
...

Question 4:

Russia: 50.06% population fully vaccinated
Falkland Islands: 50.31% population fully vaccinated
Trinidad and Tobago: 50.6% population fully vaccinated
...

```

### Question 4(b)

For the 10 countries found in question 4(a), predict how many days they would take to get to 80% population fully vaccinated? Extend the output for these 10 countries like this:

```
Analysing data file ./vaccinations.csv

Question 1:
...

Question 2:
...

Question 3:
...

Question 4:

Russia: 50.06% population fully vaccinated, ... days to 80%
Falkland Islands: 50.31% population fully vaccinated, ... days to 80% 
Trinidad and Tobago: 50.6% population fully vaccinated, ... days to 80%
...

```

NOTE: **There is not a single answer to this question.** Therefore, it is important that you explain, how you came up with the prediction, describe the limitations and assumptions. In case you need to do a bit of “research”, for example, to come up with a formula, then you may need to reference the source. Use comments and docstrings (as appropriate) in your assignment code.

Questions for the individual report
-----------------------------------

A template for your report is provided here:

*   [assignment\_report.txt](assignment_report.txt)

The template is a plain text file; write your answers where indicated in this file. **Do _not_ convert it to `doc`, `docx`, `pdf` or any other format.**

The questions for you to answer in the report are:

*   Report question 1: Write your name and ANU ID.
*   Report question 2: If you are part of a group, write the names and ANU IDs of ALL members of this group. If you are doing the assignment on your own (not part of a group), just write “not part of a group”.
*   Report question 3: Select a piece of code in your assignment solution that _you_ have written, and explain:
    
    (a) What does this piece of code do?
    
    (b) How does it work?
    
    (c) What other possible ways did you consider to implement this functionality, and why did you choose the one you did?
    
    For this question, you should choose a piece of code of reasonable size and complexity. If your code has an appropriate level of functional decomposition, then a single function is likely to be a suitable choice, but it can also be a part of a function. It should not be something trivial (like a single line, or a simple loop).
    
    For all parts of this question, it is important that your answers are at an appropriate level of detail. For part (a), describe the purpose of the code, including assumptions and restrictions. For parts (b) and (c), provide a high-level description of the algorithmic idea (and alternative ideas), not a line-by-line description of each statement.
    
    There is no hard limit on how short or how long your answer can be, but an answer that is short and clear is always better than one that is long and confusing, if both of them convey the same essential information. As a rough guideline, an appropriate answer may be about 100 - 300 words for each of parts (a) - (c).
    

Submission requirements
-----------------------

Every student must submit two files: Your assignment code (`assignment.py`) and your individual report (`assignment_report.txt`). An [assignment submission link](https://wattlecourses.anu.edu.au/mod/assign/view.php?id=2469997) will be available on wattle shortly after the assignment specification is released.

### Restrictions on code

There are certain restrictions on your code:

*   You should NOT use any global variables or code outside of functions, except for the test cases in the `if __name__ == '__main__'` section. You can add other test cases in the main section if you wish.
*   You can import modules that you find useful. However, we will test your code using the Anaconda distribution of python, so only modules available in Anaconda can be used. If in doubt about whether a module can be used, post a question to the [wattle discussion forum](https://wattlecourses.anu.edu.au/mod/forum/view.php?id=2469951) before you decide to use it.
*   The argument to the `analyse` function is the path to the CSV file to analyse. You must only read this file. You must NOT write any file, or use any of the functions of the `os` module (such as changing the working directory).
*   **You are NOT allowed to use `numpy`, `pandas` and `scipy` libraries.**

_It is very important that you follow these restrictions_. If you do not, we may not be able to test your code, in which case you can not gain any marks for code functionality.

### Assumptions

**We will test your code with CSV files other than that provided above.**

All input files will follow the same format, i.e., they will be CSV files, and have the same columns (in the same order) with the same content format, as described above (see [Data and files provided](#data-and-files-provided)). However, they will contain different data. For example, data files we provide range over a specific set of dates. You should _not_ assume this will always be the case. The number and names of countries or regions differ, or the range of dates present in the folder may be different.

### Referencing

In the course of solving the assignment problem, you will probably want to make use of all sources of knowledge available: the course materials, text books, [on-line python documentation](http://docs.python.org/), and other help that you can find on-line. This is all allowed. However, keep in mind that:

*   If you find a piece of code, or an algorithmic idea that you implement, somewhere on-line, or in a book or other material, you must reference it. Include the URL where you found it, the title of the book, or whatever is needed for us to find the source, and explain how you have used it in an appropriate place in your code (docstring or comment).
    
*   Although you can often find helpful information in on-line forums (like stackexchange, for example), _you may not use them to ask questions that are specific to the assignment_. Asking someone else to solve an assignment problem for you, whether it is in a public forum or in private, is a form of plagiarism, and if we find any indication that this may have occurred, we will be forced to investigate.
    
*   If you have any doubt about if a question is ok to ask or not, you can always post your question to the [wattle discussion forum](https://wattlecourses.anu.edu.au/mod/forum/view.php?id=2469951). We will answer it at a level of detail that is appropriate.
    

Remember that:

*   Working in groups of more than three students is **not allowed**. While you may develop your solution (python code) in a group of up to three students, you may not share your solution, or parts of your solution, with, or receive parts of a solution from, anyone outside this group.
    
*   The individual report **must be done by you yourself**. The other members of your group may not assist you with it.
    

Marking criteria
----------------

The code component accounts for 95% of the total assignment marks, and your individual report for the remaining 5%. For the questions of the code component, the breakdown is as follows:

*   Q1(a): 5%
*   Q1(b): 5%
*   Q1(c): 10%
*   Q1(d): 10%
*   Q2(a): 10%
*   Q2(b): 10%
*   Q3(a): 10%
*   Q3(b): 10%
*   Q4(a): 10%
*   Q4(b): 15%

Your code will be marked on two criteria: Functionality and code quality. The division of marks between them is 60% for functionality and 40% for code quality. We will also consider the efficiency of your code. Efficiency is part of both functionality and code quality.

Functionality encompasses code running without error on input files that follow the same format as the example files provided, and produces an output that is easy to understand and correct. Examples of increasing levels of functionality are:

*   Code runs without runtime error, and in a reasonable amount of time, on the provided example data files.
*   The output is understandable, and includes the information that is asked for in the question.
*   The output is correct for some of the provided example data files.
*   The output is correct for all of the provided example data files.
*   Code runs without runtime error, and in a reasonable amount of time, on other data files that follow the specified format.
*   The output is correct for other data files as well.

We do not specify a precise limit for what is “a reasonable amount of time”, but as a guide, your code should process the example data files in no more than a minute or two. If it takes much longer, then we will not be able to test your code fully, which is practically the same as it not running at all.

Code quality includes the aspects that we have discussed in lectures and homeworks:

*   Good code documentation. This includes appropriate use of docstrings and comments.
*   Remember that for some questions you will have to make some assumptions, and decisions how to calculate your estimate. You should describe these in the code, using docstrings and comments as appropriate.
*   Good naming. This includes variable and function names.
*   Good code organisation, including appropriate use of functional decomposition. Remember that even though the assignment template has only one function that you must implement, you can define other functions and use them in your solution.
*   Efficiency. This includes things like considering the complexity of the operations that you use, and avoiding unnecessarily slow methods of doing things. We do not require that every part is implemented in an optimally efficient way, but code that has many or large inefficiencies is considered to have lower quality.

Updated:  **29 Apr 2022**/ Responsible Officer:  [**Head of School**](mailto:head.cs@cecs.anu.edu.au)/ Page Contact:  [**Minh Bui**](mailto:comp1730@anu.edu.au)