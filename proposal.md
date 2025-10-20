
# Instructions
Do next step immediately after finishing a step. I.e. edit case_description.md and tasks.md continually, NOT after completing the entire workflow.

# Workflow
read @case_description_aeis.md
read @tasks.md

for {task} in tasks.md:

    if {task.completed}:
        |continue|
    for {subtask} in {task}:
        if {subtask.completed}:
            |continue|
        *create* a list of all QUESTIONS and FOLLOW-UP questions to gather ALL information necessary for completing {subtask}

        for {question} in {questions}:
            *get* an {answer} from {user} regarding {question}, repeat until answer approved by {user} (Y/N)

            for {followup} in {question.followups}:
                *get* an {answer} from {user} regarding {followup}, repeat until answer approved by {user} (Y/N)

        while {solution_not_approved}:
            *create* the OPTIMAL solution to {subtask} based on {answers} 
            *implement* the solution in case_description_aeis.md
            *get* approval/denial of the solution from {user}
        
        *mark* the subtask as done
    
    *mark* the task as done
    *append* any important questions/issues/suggestions to a summary in tasks.md (only if absolutely necessary)
