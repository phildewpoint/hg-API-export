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
Member_Activity_List = [
    "Id",
    "FullName",
    "UserName",
    "EmployeeId",
    "LocationId",
    "LocationName",
    "DepartmentId",
    "DepartmentName",
    "Role",
    "Status",
    "LastActiveDate",
    {
        "Managers":
        [
            "FullName",
            "Email",
            "EmployeeId"
        ]
    },
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
    {
        "Reviewee":
            [
                "Name",
                "EmployeeId",
                "DueDate",
                "SubmittedDate",
                "Status",
                "NeedsSignOff",
                "RevieweeCheckInCompleted"
            ]
    },
    {
        "Manager":
            [
                "Name",
                "EmployeeId",
                "ViewedDate",
                "Status",
                "ManagerCheckInCompleted"
            ]
    }
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
    {
        "CycleStatus":
            [
                "TotalParticipants",
                "TotalParticipantsWithGoals",
                "TotalParticipantsWithNotStartedGoals",
                "TotalGoalNumber",
                "TotalEditingGoalNumber",
                "TotalGoalsSubmittedForApprovalToSet",
                "TotalGoalsInProgress",
                "TotalGoalsPendingClosure",
                "TotalGoalsSubmittedForApprovalToClose",
                "TotalGoalsClosed",
                "TotalGoalsOntime",
                "AvgGoalCompletePercentage"
            ]
    },
]
Goals_List = [
    "Id",
    "Name",
    "Description",
    "CycleName",
    "CycleId",
    "Status",
    "Visibility",
    "CreatedDate",
    "ModifiedDate",
    "CheckInFrequency",
    "UpToDate",
    {
        "Owner":
            [
                "FullName",
                "EmployeeId"
            ]
    },
    {
        "Approver":
            [
                "FullName",
                "EmployeeId"
            ]
    },
    "PercentCompleted",
    "Weight",
    "ProgressStatus"
]
# used for the Submit/Cancel UI buttons
goBtn = [
    "Submit",
    "Cancel"
]


def launch_api(button):
    if button == "Cancel":
        app.stop()
    elif not app.getEntry(name="API Key"):
        app.infoBox(title="infoBox", message="Please add an API key before submitting.")
    elif not app.getListItems(title="field_box"):
        app.infoBox(title="infobox", message="Please select at least one column before submitting.")
    else:
        # create and return file object
        file = create_file(api_name=app.getRadioButton("apiList"))
        # get the list of columns user selected in UI
        col_list = app.getListItems(title="field_box")
        # based on the selected radio button, call a specific API w/ key
        api_key = app.getEntry(name="API Key")
        if app.getRadioButton(title="apiList") == "Member Activity":
            loop_api(api_key=api_key, file=file, col_list=col_list, end_pt="MembersActivity")
        elif app.getRadioButton(title="apiList") == "CheckIn Cycles":
            loop_api(api_key=api_key, file=file, col_list=col_list, end_pt="CheckInCycles/")
        elif app.getRadioButton(title="apiList") == "CheckIn Sessions":
            loop_api(api_key=api_key, file=file, col_list=col_list, end_pt="CheckInSessions/")
        elif app.getRadioButton(title="apiList") == "Goal Cycles":
            loop_api(api_key=api_key, file=file, col_list=col_list, end_pt="GoalCycles/")
        elif app.getRadioButton(title="apiList") == "Goals":
            loop_api(api_key=api_key, file=file, col_list=col_list, end_pt="Goals/")
        close_and_clean(file=file)


def create_file(api_name=None,):
    mydir = app.directoryBox(title="myDirectory")
    if mydir is None:
        quit()
    else:
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


def changer(rb):
    """Changes the list box values when a radio button is selected"""
    # get the column listing, flatten it, display to user
    val = api_list(title=app.getRadioButton(rb))
    list_store = []
    cols = flatten(col_listing=val, list_storage=list_store)
    app.updateListBox(title="field_box", items=cols)


def flatten(col_listing, list_storage, prefix=None):
    for items in col_listing:
        if type(items) == str:
            if prefix is None:
                list_storage.append(items)
            else:
                list_storage.append(prefix + items)
        else:
            for k, v in items.items():
                combo = k + ": "
                if prefix is None:
                    flatten(col_listing=v, list_storage=list_storage, prefix=combo)
                else:
                    combo = prefix + k + ": "
                    flatten(col_listing=v, list_storage=list_storage, prefix=combo)
    return list_storage


def close_and_clean(file):
    file.close()
    app.infoBox(title="Extract Complete!", message="Your file was dropped at: \n" + file.name)
    app.stop()
    quit()


# create GUI object from appJar
app = gui()
# API uses a header value as password. Need to collect it from users
app.addLabelEntry(title="API Key")
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

