# COMP1730/6730 vaccination data analysis

Group coursework for ANU COMP1730/6730 (Semester 1, 2022). The program reads Our World in Data-style COVID-19 vaccination CSV files and prints answers to the assignment questions using only the Python standard library (`csv`).

This is a course project, not a general-purpose analytics tool.

## What the program does

`comp6730-2022-assignmen-1/assignment.py` defines `analyse(path_to_file)`, which:

1. Loads the CSV, maps header names to column indexes, and drops aggregate regions whose `iso_code` contains `OWID_`.
2. **Question 1** — counts unique locations and countries, then sums the latest valid figures for global vaccine doses, people with at least one dose, and people fully vaccinated.
3. **Question 2** — lists the top 10 countries (population at least about 1 million) by share of people vaccinated, and also prints the share only partly vaccinated.
4. **Question 3** — lists the 10 countries with the earliest first vaccination date, and the peak daily-vaccination day for each of those countries.
5. **Question 4** — among countries already above 50% fully vaccinated, takes the 10 with the lowest such share and estimates how many days it would take to reach 80%, using recent daily vaccinations minus first-dose vaccinations as the daily growth rate. If growth is not positive, or required columns are missing, it reports that a prediction cannot be made.

Sorting uses a hand-written heap (`top_k`) rather than Python's `sort`.

Two input files are included: `vaccinations.csv` and `vaccinations_shuffled.csv`. The `__main__` block runs `analyse` on `./vaccinations.csv`.

## Tech stack

- Python 3
- Standard library only (`csv`)

## How to run

```bash
cd comp6730-2022-assignmen-1
python3 assignment.py
```

No packages need to be installed. The script expects `vaccinations.csv` in the same directory.

A course specification is saved as `Requirement.md`. A short group note (`Readme.md`) records the original GitLab workflow for the assignment.

## Authors and role

Group project. Members named in the in-repo reports are Jingze He, Hao Xu, and Gary Chen. Gary uploaded this copy to GitHub.

Gary's individual report (`assignment_report_gary.txt`) describes his work on Question 1 and the helpers `unique_country` (filter out `OWID_` region rows) and `count_data` (sum numeric values from lists of strings). The other reports in the folder are from the other group members.
