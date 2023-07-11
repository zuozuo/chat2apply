## TODOs
### current_user profile
* add user profile to prompt [Done]
* remember user profile [Done]
* load from db and save to db

### Others
* create custom memory class to be extended and support database storage, with doc
* create custom function class to be extended and support custom function, with doc

### Applied job agent
* support job applied history
    * current applied job list
        * remember job applied
        * load from db and save to db
    * support applied job status query
        * command line support command tips
        * command line support show history
* implement apply_job function

### Search job agent
* talk with @sihao about using real job search api parameters
* search job pagination
* compare jobs
* available job title list and location list
    * no jobs at some city, relocation to another city
    * no jobs at some job type, relocation to another job type

### Company info QA agent
* support qa about jobs
* qa about company

### Test and Monitor
* design a test framework to test the chat and apply workflow
    * use chatgpt for test case assetion
* collec useful test cases and former bugs
* setup lanchain tracing
