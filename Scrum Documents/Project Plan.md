# Project Plan for _DocInspector_

_Scrumbags_

## Team Vision

For teachers and tutors who need to track the contribution of their students in group assignments, the _DocInspector_ is a program that tracks user access and changes to a google document and outputs a visual representation of that data, that allows markers to easily see project contributions. Unlike a similar software GitInspector, the _DocInspector_ extracts metrics from a google document and outputs this into a visual format.

## The Team

| **Name** | **E-mail** | **Facebook** |
| --- | --- | --- |
| Quinn Roberts | [qrob0001@student.monash.edu](mailto:qrob0001@student.monash.edu) | https://www.facebook.com/jellysnake |
| Simon Schippl | [ssch50@student.monash.edu](mailto:ssch50@student.monash.edu) | _Simon Schippl_ |
| Ganesh Ukwatta | [gwan0006@student.monash.edu](mailto:gwan0006@student.monash.edu) | _Ganesh Ukwatta_ |
| Darcy Trenfield | [ditre3@student.monash.edu](mailto:ditre3@student.monash.edu) | _Darcy Trenfield_ |

We shall hold bi-weekly meetings @ **5pm on Sunday** _(via Messenger)_ and @ **12pm on Thursday** _(in Workshop)_

## Roles and Responsibilities

### Product Owner (Quinn Roberts)

Responsible for liaising with client in order to find requirements and subsequently communicating these requirements to the development team to be implemented in the project.

### Scrum Master (Darcy Trenfield)

In charge of guiding team meetings and resolving disputes between team members to ensure that meetings progress smoothly.

### Development Team (Ganesh Ukwatta, Simon Schippl)

The Development Team&#39;s roles include building and testing the final product and ensuring that it adheres to the prescribed requirements. The development team is responsible for planning, designing and developing the product to the point where it is delivered.

## Process Model

The process model we have decided to use is a modified variant of Scrum. It will not have daily standup meetings but rather weekly progress meetings that allow each team member to explain what tasks they have completed during the week and what they will aim to complete in the following weeks. It will also provide a good checkpoint to ensure that each member is on schedule and to allow for early detection of any issues, difficulties, or changes.

This is because daily standup meetings won&#39;t be feasible due to the individual team members having other university commitments. This is also the reason why the second meeting of the week is held via Facebook Messenger

## Definition of Done

Our definition of done constitutes a functional project as defined by a few criteria:

- It should have been at least briefly reviewed by all team members, to ensure everyone is happy with the final version of the feature.
- Any feature should be working correctly and be implemented as efficiently as is feasible. We will not require programmed test cases for any feature, but a brief guideline of how to test the feature is required.
- All features should be submitted by a pull request from a branch into master. The creator of a pull request should not be allowed to merge it, instead a separate team member must.
- This seperate team member must have also tested the feature and viewed the code to ensure it works, although a full in-depth code review is not required.

## Task allocation method

A list of necessary tasks will be compiled for each sprint where each team member will choose the tasks that they would prefer to work on and that best reflect their strengths.

The remaining tasks will be allocated amongst the team to ensure that each member has an equal workload. Before a task allocation is finalised, it will be ensured that the team member will be able to deliver their assigned tasks to a reasonably high standard. If the team does not feel confident that the individual will be able to complete the require tasks, the other three members may alter the task balance. This is only possible if all three members are in unison about the imbalance

## Progress Tracking

Progress will be assessed at the weekly team meeting where each member will discuss what they have achieved during the week, what they had trouble with and what they still have to do. This will allow us to gauge how well we are progressing as well as whether we are likely to complete all of the tasks within the sprint backlog by the end of the sprint. Completed tasks will be recorded in the backlog located in GitLab and will give a better overview of how the general completion of the project is going. Since the clients have access to Gitlab they will be able to see what tasks have been completed and are yet to complete.

The current task will also be visible in the GitLab Boards, as described below. This combined with the ability to set a deadline for each feature means that we will be able to easily notice when a task is taking longer than estimated, and handle the situation appropriately

## Backlog Management

We will also be utilising the _Boards_ feature of GitLab to organise the tasks. There will be four columns, one for the project backlog, one for the sprint backlog, one for the task that each member is currently working on and one for the completed tasks from that sprint.

This has the advantage to being able to assign tasks to different members of the team as well as due dates which gives greater management ability over the project. This allows access to the backlogs to all members of the team so that the necessary tasks are always visible and clear.

## Time Tracking

When a team member begins working on a feature, they must set a specific deadline on when these tasks will be completed. Team members will come together for the weekly meeting to discuss where each member is up to in their allocated tasks, and allows them the option to extend or reduce the deadline for a specific task.

A member may also re-allocate a task to another member that is not only capable of completing the task to a reasonably high standard, but also able to complete the task at a reduced deadline, subject to the approval of the other members.

To record the time spent on the development of each feature, we intend to edit the label of the feature completed on Gitlab, with the amount of time spent on it.

## Risk Management

## Technical

- **Team member lacks knowledge in required areas**

Low Impact | Moderate likelihood.

_This risk would be identified by the scrum master confirming with each team member that they feel capable of doing the assigned tasks._

_This is a risk that would be identified at the start of the sprint, during the task allocation phase. It can be mitigated fairly easily by simply allocating time into the tasks for learning the technology or knowledge required._

_Also of note is that this will be mitigated as each team member selects the bulk of the tasks themselves. Hence a team member will most likely not select a task they don&#39;t feel they can complete._

- **Unfamiliarity with language causing delays in development**

Moderate Impact | Low Likelihood

_This will be identified by the scrum master who will communicate with each team member about how they feel about their skills and familiarity of the language before development commences._

_Likewise to the above this will mostly be mitigated by both choosing the language to implement and by allocating extended time for learning the language. Additionally as features must be reviewed by a separate team member before they can be merged this will ensure that team members with more knowledge can ensure that the code is logical and reasonable._

- **Google drive changing API**
  - **Adding/removing/changing URL interactions**

High Impact | Low Likelihood

_The team will keep track of changes that Google makes to the API if any by checking the API site multiple times weekly._

_If Google was to suddenly remove or change the API then the project would simply have to be re-written to handle this. Thankfully it is very low risk, however if Google were to remove all 3rd party interactions with Google Docs then this project becomes technically impossible. If the API is changed then the relevant sections of code will need to be re-written to handle this. If the API is removed then alternatives such as directly scraping the HTML would need to be considered._

- **Hardware issues for a team member**

Moderate Impact | Moderate Likelihood

_Team members affected by hardware issues will communicate with team members about their problems to alert the team._

_As we will be utilising a Git server and practicing good git practices such as pushing to remote often any work lost should be minimal. Additionally Monash provides computers through their labs and their libraries. This means that the student should be able to continue working through these facilities. The workload for that student can also be distributed throughout the other team members_

- **Git issues**
  - **Loss of code from server**

High Impact | Low Likelihood

_Git will be accessed regularly throughout the week to ensure that any Git problems are identified early._

_Regularly pulling from the git repo will ensure that there are recent files available on team members devices. This means that in the situation where the code is lost from the server, the files are still available and can be upload to another repository to continue production._

  - **Gitlab stops functioning correctly**

High Impact | Low Likelihood

_As GitLab will be accessed regularly throughout the week, any problems with GitLab will be quickly identified._

_Monash E-Solutions (providers of the GitLab Hosting) does regular backups of the code, which will mean that any loss will only be recent code. Additionally each of the students will have a local copy of the code. These can be used to reconstruct the code if the GitLab instance comes back online shortly. Alternatively other Git providers such as BitBucket or Github could be used to host the code using the local copies on the teams devices._

  - **Loss of work from bad git practices**

Moderate Impact | Moderate Likelihood

_The Git repository will be assessed weekly at the team meetings to ensure that bad Git practices are identified and rectified before they have the potential to cause serious problems for the project._

_Likewise to the prior risk, one of the main methods this is mitigated is by each team member having local copies of the code and by the regular backups taken by e-solutions. In the event of a team member making a git related mistake that irrevocably destroys the repository we will ask the facilitator to either reset the git repo using the backups or to create a new one that we will populate with our local copies._

- **Communications methods go down**

Moderate Impact | Low Likelihood

_Communication between team members will occur regularly and as such, problems with communications methods will be realised within a short time frame._

_This is distinct from the risk of a team member going AWOL. This is specific to situations like an outage in Messenger or Email services. If our primary method of communication, Messenger, is down we will use Email as a backup. If that also goes down then we will organise a new communication method in our thursday meeting. In the meantime we will continue working on our features as before until we can communicate._

- **Estimation of time constraints are found to be incorrect (not enough time)**

Moderate Impact | High Likelihood

_Estimations are hard to make accurately and so weekly progress meetings will ensure that tasks are on schedule and are on track to be completed on time._

_This risk has a high likelihood of occuring as estimations are usually not very accurate. The primary method of mitigation would be to move other features out of this sprint if they cannot be completed or to re-balance the workload between the team members in order to still get the features completed in time. We will also aim to use more accurate estimation techniques as well as try to overestimate than underestimate, as it is the latter that causes issues._

## Organisational

- **A team member gets sick or is temporarily unavailable for other reasons**

Low Impact | Low Likelihood

_This risk can be identified if the affected team member does not inform the rest of the team prior to the weekly meeting. Sometimes these occurrences can be abrupt, where the affected team member can&#39;t do anything about it. This risk can be mitigated by contacting the affected team member through other means such as email or Facebook. These members should be informed on what they missed out on, and what they can do to catch up._

- **A team member drops out permanently**

Low Impact | Low Likelihood

_This risk is not easily identifiable since other team members rely on the affected team member to complete the tasks allocated to them. Signs that indicate a team member intends on dropping out include the lack of contribution to the project and the lack of communication with other team members at weekly meetings. If this risk occurs, nothing can be done to bring the team member back, and therefore cannot be mitigated. The load that was shared to the affected team member must be split amongst the remaining team members, and the project will continue from there._

- **Team member not completing their section of the work / uneven sharing of work**

Moderate Impact | Low Likelihood

_This risk can be easily identified given that the affected team member speaks up about their troubles early. Doing so will ensure they receive a sufficient amount of help, as well as receive valuable advice from other team members. The risk can be mitigated by double checking with each team member if their share of the work is fair, and they believe they are capable of completing that work within a specific deadline. If they think it isn&#39;t fair, then they should discuss these matters with the rest of the team and get it sorted out immediately to avoid risk of submitting work that is either overdue, or low in quality._

- **Introduction requirements that are infeasible or sudden increase in requirements**

Moderate Impact | Moderate Likelihood

_Infeasible requirements can be determined by making a proper attempt to meet them first, and obtaining conclusive evidence that suggests that the requirements in question cannot be done. One way of mitigating this risk is to ignore the requirement entirely, given that we inform the client beforehand. This ensures we are not misleading the client. Another way to mitigate this risk is to renegotiate the set of initial requirements with the client so that each of the requirements can be reached. Abrupt increases in requirements should be looked at by the whole team the moment they are given out. This is so that it gives more time for the team to adapt to the new set of requirements, and adjust the product accordingly._

- **Security and Privacy**
  - **User credentials are stolen**

High Impact | Low Likelihood

_One way this risk can be monitored for is by performing periodic security checks at the end of each sprint. This check will look for ways to obtain the user credentials out of the software._

_It can be mitigated by taking proactive steps to ensure sensitive data is not stored and following security best practices. Additionally any specific methods of breaching the data found in the regular checks can be fixed at the same time._