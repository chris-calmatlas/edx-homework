# Requirements
- In this project, you are asked to build a web application of your own. The nature of the application is up to you, subject to a few requirements:

- Your web application must be sufficiently distinct from the other projects in this course (and, in addition, may not be based on the old CS50W Pizza project), and more complex than those.
    - A project that appears to be a social network is a priori deemed by the staff to be indistinct from Project 4, and should not be submitted; it will be rejected.
    - A project that appears to be an e-commerce site is strongly suspected to be indistinct from Project 2, and your README.md file should be very clear as to why it’s not. Failing that, it should not be submitted; it will be rejected.
- Your web application must utilize Django (including at least one model) on the back-end and JavaScript on the front-end.
- Your web application must be mobile-responsive.

> The most common cause for failure of the final project is not spending enough effort on this next instruction. Read it completely. Your README.md file should be minimally multiple paragraphs in length, and should provide a comprehensive documentation of what you did and, if applicable, why you did it. Ensure you allocate sufficient time and energy to writing a README.md that you are proud of and that documents your project thoroughly, and that distinguishes this project from others in the course and defends its complexity. Simply saying, effectively, “It’s different from the other projects and it was complex to build.” is not at all sufficient justification of distinctiveness and complexity. This section alone should consist of several paragraphs, before you even begin to talk about the documentation of your project.

- In a README.md in your project’s main directory, include a writeup describing your project, and specifically your file MUST include all of the following:
    - Under its own header within the README called Distinctiveness and Complexity: Why you believe your project satisfies the distinctiveness and complexity requirements, mentioned above.
    - What’s contained in each file you created.
    - How to run your application.
    - Any other additional information the staff should know about your project.
- If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to a requirements.txt file!
Though there is not a hard requirement here, a README.md in the neighborhood of 500 words is likely a solid target, assuming the other requirements are also satisfied.

Failure to adhere to these requirements WILL result in a failing grade for the project, and you will need to wait and resubmit.

Beyond these requirements, the design, look, and feel of the website are up to you!

# Distinctiveness and Complexity
The purpose of this program is to generate a recurring schedule for a list of workers. This could be used in a number of settings including shift coverage, on-call rotations, or volunteer hour tracking. 

This program is distinct from the other assignments because of the focus on dates and scheduling rather than texts and commerce. 

This program is sufficiently complex because it will include user and team management with rudimentary rbac as well as a "free version" that uses local storage to save sessions without the need to login.

## Initial Program spec
These set of requirements include javascript editing of single page applications, as well as other django views and models.

### Schedule
A schedule is a table of days with a defined start and end date with individuals occupying hours within those days.
- [ ] Max 20 people per schedule
- [ ] Max 1 year long
- [ ] Add a list of people/workers 
- [ ] Click on a day to add a workers scheduled time
- [ ] Allow repeat every x number of days until, or for y occurrences
- [ ] Allow repeat weekly on day of the week until, or for y weeks

### Users
- [ ] No login required: Unauthenticated users should be able to create a schedule. Unauthenticated users should have a save and edit ability as long as their session is cached.

- [ ] Public access read only: Those without a cached session will have read access. Schedules by unauthenticated users are publicly accessible. A warning should be shown explaining this. 

- [ ] Multiple schedules: Authenticated users should have the ability to create mulitple schedules and have write access from any session on schedules they own. 

### RBAC
- [ ] Private schedules: Authenticated users should have the ability to mark a schedule private.

- [ ] Owners (The creaters of the schedule) should be able to invite viewers (read-only) and contributors (edit-rights) to private schedules.

### Pages
- [ ] index - Homepage
- [ ] schedules - Authenticated users see all schedules to which they have access
- [ ] schedule - individual schedule page to allow editing. Authenticated users should be able to Subscribe or unsubscribe. Unsubscribing should revoke any given role a user had. Owners should be able to invite users, revoke access, and delete the schedule

## Extended program spec
The following are additional todo items that exceed the minimum requirement for complexity as outlined for project 5 capstone. But they would be cool features. Consider this a wish list

- [ ] Generate schedules based on criteria
- [ ] Send email notifications
- [ ] Expire public schedules
- [ ] Integrate with other calendar platforms