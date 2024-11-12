![Tests](https://github.com/CS222-UIUC/course-project-group-negative10/actions/workflows/django.yml/badge.svg)
# *note: commit history accidentally overwritten. see below for individual contributions*

# Comp

Developers aren’t always aware of how their app is performing in comparison to their competitors and regarding changes they have made. Our tool allows app developers to track ratings and sentiment over time for their app, allowing them to pinpoint certain updates that improved user experience and those that hurt it. It also allows them to manually browse reviews themselves and view their review distribution. It supports both the play store and the apple app stoer.

##  Technical Architecture 
![image](https://user-images.githubusercontent.com/20406065/207224513-95f5e9be-b2df-434b-8ad9-07701dbf4be0.png)
The backend runs on Django (Python) and the frontend runs on React. We treat Django like an api, whenever we need information about an app we request it from Django which does all the information scraping and processing and then sends it back to the frontend, where it is displayed.
##  Installation Instructions
  - Clone the project
  - Run ```docker-compose up --build``` in the main directory
  - Visit http://localhost:3000/
  - Project is also hosted live on https://comp-222.herokuapp.com/
  
## Roles
Batuhan:
 - Created template website
 - Created the frontend UI
 - Added ability to view reviews over time (Play Store)
 - Added ability to view details about an app (Play Store)
 - Added a review browser with infinite scrolling

Charleston:
 - Setup github actions for tests and a linter
 - Added sentiment analysis
 - Added app store support (For reviews over time and sentiment analysis)

Ashley:
 - Created the design of the frontend UI
 - Completed the final presentation
 
## Functionality
- Users can see what place their app ranks on certain keywords
- Users can see how their competitors rank on certain keywords
- Users can track their performance history
- Users can create an account to register their app
- Users can export their data in csv format
- Users can run sentiment analysis on the reviews of their app
- Users can see the predicted number of downloads for their app

## Components

### Functionality
- Our first component involves the user creating their account and having the login information (username and password) stored in MongoDB for future authentication.
- The second component involves retrieving app performance data from Google Play/App Store APIs using Django. We will use the Django REST framework for creating the api which the frontend will interact with. The historical ranking information for the performance will be stored in MongoDB.
- The third component involves graphing the data and displaying it in a line graph using Matplotlib and HTML.
- The fourth component involves exporting user data to csv format using Pandas library so users are able to view and analyze data using external software.
- The fifth component allows users to run sentiment analysis to better understand whether the tone of the user-created reviews are more negative or positive using the NTLK library.
- The sixth component allows the user to view the forecasted future number of downloads based on previous trends using the Sk-learn library.

### Programming Languages
- Python
- Javascript
- SQL/noSQL(PHP)

### Major Libraries Used
- We plan on using React for frontend development and will incorporate Angular.js and Vue.js if necessary.
- NLTK (Python for sentiment analysis on reviews) will allow users to see trends in customer reviews.
- Sk-learn will be helpful for forecasting future download amounts.
- With Pandas, the user will be able to export the data to a csv file.

### Testing Methodology
- By implementing CI/CD we can deliver code in an agile environment that allows us to continuously and efficiently build, test, and deliver. The CI/CD pipeline would also allow us to efficiently implement new features and fix bugs.
- Testing library: Since Javascript and Python are the main languages in our project, we will be using Jenkins and Pytest respectively for unit testing, since it allows us to efficiently test our code. Both Jenkins and Pytest have plugins for computing testing coverage. We will follow the camelCase style guide. We plan on creating test cases for each functionality to guarantee that the individual parts of the project are working before we begin integration testing. We will proceed with integration tests by writing tests that assess how each function interacts with the other components of the project and how it varies with each component. In addition, we want to make sure to write tests for the edge cases and make sure that each individual case works. 
- Whenever someone submits a pull request, we will review it together as a team and see if it is compatible with the components that we are working on individually. We will leave comments, leave feedback, and make changes when necessary. 

### Interactions With Other Components
GET https://api.appstoreconnect.apple.com/v1/apps/{id}/perfPowerMetrics

## Schedule
Week 1:
- Create an organized github repo
- Create a Figma page to determine layout of website
- Create a very basic website with react + django.
- Learn and configure docker environment on all our ends

Week 2:
- Backend:
  - Add ability to pull data from the play/app store apis.
    - Ranking for keywords
    - Reviews
    - Download count
  - Set up user account management via mongoDB
- Frontend:
  - Create page for user login
  - Create the layout for the table

Week 3:
- Backend:
  - Add the ability to send ranking data to the frontend.
- Frontend:
  - Receive and display ranking data.

Week 4:
- Backend:
  - Ability to run sentiment analysis on an apps reviews
- Frontend:
  - Create UI to display sentiment analysis results and app reviews


Week 5:
- Backend:
  - Store app name/links along with the users login data
  - Export review(sentiment analysis) and ranking data to csv
- Frontend:
  - Create UI components for a user to add their app into the system
  - Create UI for downloading data in csv

Week 6:
- Backend:
  - Forecast future app downloads
- Frontend:
  - UI to view historical download counts in a graph and see future predictions

Week 7:
- Have random users test the website to make sure it is fully functioning and every component is working together properly
- Frontend:
  - Create a landing page for our website where viewers can view information about what our application does.

Week 8:
- Finalize presentable website, do lots of testing and debugging
- Put together a presentation/demo


## Risks
One possible risk would be poor API support from the play/app stores. To resolve this issue we will have to write our own application to scrape the app stores. This could take up to a week. We may have to adjust our schedule and remove some of the additional features as a result.

Another possible risk is insufficient technical skills or training. None of us are familiar with frontend libraries such as react or backend frameworks such as Django. To resolve this issue we may consult our mentor for situations in which we are fully stuck, but we can also learn a lot of the information we need on the web as these technologies are very widely used.

A third risk would be lack of communication for collaborating on all the different components of the project. If we aren’t on the same page on certain things then we could end up doing work that ends up wasted due either not being compatible with each other or just doing duplicate work. The in person meetings we have every week will help with this, as we will be able to plan out what everyone's roles/tasks are every week, and how they will interact. 

## Teamwork
We will use Docker to containerize our application to guarantee that implemented functionality would work across all our devices and not have issues with OS platform. To improve collaboration between our team, we will meet in-person weekly to address any issues that arise during the week and address it efficiently.

We want everyone to familiarize themselves with the frameworks and softwares being used as soon as possible. This reduces the likely friction between team members due to the varying level of familiarity and expertise in specific domains.

In addition, we have created a set meeting time for each week to make sure that everyone has the opportunity to collaborate on the code in person, and we will arrange more meeting times after that if necessary.



