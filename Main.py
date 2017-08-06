from appJar import gui
import datetime, os
from get_API import loop_api

# these are all the lists available to initialize elsewhere in the routine
apiList = [
    "Member Activity",
    "CheckIn Cycles",
    "CheckIn Sessions",
    "Goal Cycles",
    "Goals" 
]
# each of these lists reflect the columns available to recall in the API
# TODO - review nested lists below. get_API.py needs update to read and print nesting in this format
# Example is listed below for 'Member Activity' - manager data is nested
Member_Activity_List = [
    "Id",
    "FullName",
    "UserName",
    "EmployeeId",
    "LocationId",
    "LocationName",
    "DepartmentID",
    "DepartmentName",
    "Role",
    "Status",
    "LastActiveDate",
    [
        "Managers",
        [
            "FullName",
            "EmployeeId"
        ]
    ]
]
CheckIn_Cycles_List = [
    "Id",
    "Name",
    "Description",
    "Status",
    "CreatedDate",
    "ModifiedDate",
    "DueDate",
    "ClosedDate",
    "ArchivedDate"
]
CheckIn_Sessions_List = [
    "Id",
    "Cycle",
    "Status",
    "CreatedDate",
    "ModifiedDate",
    "CompletedDate",
    [
        "Reviewee",
        [
         "Name",
         "EmployeeId",
         "SubmittedDate",
         "Status",
         "NeedsSignOff",
         "CheckInCompleted"
        ]
     ],
    [
        "Manager",
        [
            "Name",
            "EmployeeId",
            "ViewiedDate",
            "Status",
            "CheckInCompleted"
        ]
    ],
]
Goal_Cycles_List = [
    "Id",
    "Name",
    "Description",
    "Status",
    "GoalWeighted",
    "RecurrenceFrequency",
    "ClosePromptDate",
    "ClosePeriod",
    "CycleStats: TotalParticipants",
    "CycleStats: TotalParticipantWithGoals",
    "CycleStats: TotalParticipantWitNotStartedGoals",
    "CycleStats: TotalGoalNumber",
    "TotalEditingGoalNumber",
    "TotalGoalsSubmittedForApprovalToSet",
    "TotalGoalsInProgress",
    "TotalGoalsPendingClosure",
    "TotalGoalsSubmittedForApprovalToClose",
    "TotalGoalsClosed",
    "TotalGoalsOntime",
    "AvgGoalCompletePercentage"
]
Goals_List = [
    "ID",
    "Name",
    "Description",
    "CycleId",
    "Status",
    "Visibility",
    "CreatedDate",
    "ModifiedDate",
    "LastCheckInDate",
    "CheckInFrequency",
    "UpToDate"
    "GoalOwnerEmpId",
    "ApproverEmpId",
    "PercentCompleted",
    "Weight"
]
# used for the Submit/Cancel UI buttons
goBtn = [
    "Submit",
    "Cancel"
]


def launch_api(button):
    if button == "Cancel":
        app.stop()
    else:
        # create and return file object
        file = create_file(api_name=app.getRadioButton("apiList"))
        # get the list of columns user selected in UI
        col_list = app.getListItems(title="field_box")
        # based on the selected radio button, call a specific API
        if app.getRadioButton(title="apiList") == "Member Activity":
            loop_api(api_key=apiKey, file=file, col_list=col_list, end_pt="MembersActivity")
        elif app.getRadioButton(title="apiList") == "CheckIn Cycles":
            loop_api(api_key=apiKey, file=file, col_list=col_list, end_pt="CheckInCycles/")
        elif app.getRadioButton(title="apiList") == "CheckIn Sessions":
            loop_api(api_key=apiKey, file=file, col_list=col_list, end_pt="CheckInSessions/")
        elif app.getRadioButton(title="apiList") == "Goal Cycles":
            loop_api(api_key=apiKey, file=file, col_list=col_list, end_pt="GoalCycles/")
        elif app.getRadioButton(title="apiList") == "Goals":
            loop_api(api_key=apiKey, file=file, col_list=col_list, end_pt="Goals/")
        app.stop()


def create_file(api_name=None,):
    mydir = app.directoryBox(title="myDirectory")
    file_name = api_name + datetime.date.today().strftime("%d%m%Y")
    file_path = os.path.join(mydir, file_name)
    file = open(file_path, mode='w')
    return file


def api_list(title):
    """Returns the list associated with an API name"""
    if title == "Member Activity":
        return Member_Activity_List
    elif title == "CheckIn Cycles":
        return CheckIn_Cycles_List
    elif title == "CheckIn Sessions":
        return CheckIn_Sessions_List
    elif title == "Goal Cycles":
        return Goal_Cycles_List
    elif title == "Goals":
        return Goals_List


# TODO - need to update the logic here to loop through each nested array in the master list as they're now multi-level
def changer(rb):
    """Changes the list box values when a radio button is selected"""
    val = api_list(title=app.getRadioButton(rb))
    app.updateListItems(title="field_box", items=val)


# create GUI object from appJar
app = gui()
# API uses a header value as password. Need to collect it from users
# TODO - require user to enter the key. If blank, popup error box.
apiKey = app.addLabelEntry(title="API Key")
app.addHorizontalSeparator(colour=None)
app.addLabel(title="guiLabel", text="Which API do you want to extract?")
# Creates 1 radio button per list item
for i in apiList:
    app.addRadioButton(title="apiList", name=i, )
# creates multi-select list
app.addListBox(name="field_box", values="")
# allows list box to act as multi-select
app.setListBoxMulti(title="field_box", multi=True)
# when radio button changes, call function 'changer' to change the columns
app.setRadioButtonChangeFunction("apiList", changer)
app.addLabel(title="dirLabel", text="You'll select the directory to save the file after clicking submit")
app.addButtons(names=goBtn, funcs=launch_api)
app.go()

