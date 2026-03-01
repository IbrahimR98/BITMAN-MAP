\# BCIT BITMAN Program 2-Year Map



\## Overview



This project builds a visual 2-year map of BCIT’s Business Information Technology Management (BITMAN) diploma program.



It shows:



\- Year 1 Core (mandatory) courses

\- Year 2 specialization tracks:

&nbsp; - Analytics \& Data Management

&nbsp; - Artificial Intelligence Management

&nbsp; - Enterprise Systems Management

\- Courses shared across tracks

\- Specialization courses (bolded)

\- Flexible Learning courses (Highlighted in Blue) 

\- Half-semester courses (✱)



The goal of this project is to transform static program webpages into a clean, structured, and visual representation of the full diploma path.



---



\## Final Output



The final generated map:



!\[BITMAN 2-Year Map](results/bitman\_track\_map\_clean.png)



---



\## Data Sources



This project uses publicly available BCIT program and course sources/ pages:



\- BITMAN Core Diploma Page "https://www.bcit.ca/programs/business-information-technology-management-diploma-full-time-6235dipma/#courses"  

\- BITMAN Analytics Option Page 1."https://www.bcit.ca/programs/business-information-technology-management-analytics-data-management-option-diploma-fulltime-623cdipma#courses"

\- BITMAN Artificial Intelligence Management 2. "https://www.bcit.ca/programs/business-information-technology-management-artificial-intelligence-management-option-diploma-full-time-623adipma/#courses"

\- BITMAN Enterprise Systems Management Option Page 3. "https://www.bcit.ca/programs/business-information-technology-management-enterprise-systems-management-option-diploma-full-time-623bdipma/#courses"  



Course codes were extracted from these official BCIT pages.



Flexible Learning and half-semester indicators were manually verified based on BCIT course listings.



---



\## How the Project Works (Pipeline)



1\. Scrape program and specialization course lists

2\. Extract course codes

3\. Tag courses by track (core / analytics / ai / enterprise)

4\. Identify overlapping and specialization-unique courses

5\. Add additional metadata (Flexible Learning + half-semester)

6\. Generate final visual map using Matplotlib



---



\## Project Structure



