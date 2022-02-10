# Goals Monitoring Survey

## 1. General Description
During my first positions as a Junior Data Analyst I had was first expeosed to professional goal setting. This being a dounting process, and me longing to practice my python skills, I decided to create this script to help me stay on track. It's quite a simple program and i ran it every week during my first year at the job. The script intializes a survey that the user (me) can respond to, in the end the goal is to generate a file with a tabular format of data on all of those questions which I can then vizualize to generate insight into my performance ove the past year.
## 2. Why?
As a Junior Data Analyst, it is quite difficult to make your goals directly measurable. I was hired to simply add value to the overall process; to keep an eye on whether everything was happening as it should, and to implement fixes/improvements where I could. This means I didn't necessarily had a distinct output, which in turn makes it difficult to quantify my results at the end of the year (which is something that wouldn't sit well with any self respecting data professional). For this reason, I created this survey. It helps to me quantify my progressions as well as remind me of my goals every single week.
But why not just maintain a workbook in Google sheets?
This would absolutely fit the purpose; however, having tried such a solution before I know it can easily feel much more tedious than a quick weekly survey. With the script I am also able to validate my inputs, so they always arrive at the correct place, as (mostly) correct value. On top of that, the main reason was simply to test my Python skills and learn some things on the way.
## 3. Technical Implementation
The script takes care of a couple aspects:
- It asks the respondent the questions
- It will validate the answers
- If the response is not valid, the question will be asked again until it is.
- For specific question it will generate targets

There are also several modes to the script:
- Mode s: survey mode, this is the mode used to store a new record (used every friday)
- Mode d: deletion mode, this is to select a date of which you would like to delete a record
- mode t: test mode, this will generate a year worth of randomized test data.

For all of this the script refers to another script where I stored the goals and questions (survey_content.py). All the files generated are stored in the working directory from which the file is ran.
