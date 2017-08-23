import requests
from addict import Dict
from appJar import gui


def get_api(mem_skip, api_key, end_pt):
    headers = {
        'Accept': 'application/json',
        'clientkey': api_key
    }
    params = ({
        'skip': mem_skip
    })
    resp_val = requests.get(
        'https://apidemo.highground.com/1.0/' + end_pt,
        headers=headers,
        params=params
    )
    return resp_val


def buried_value(record, string, parent=None):
    """This function takes the record, string to parse, and parent. Each pass digs 1 level"""
    arry = string.split(":")
    for val in range(len(arry)):
        # get parent obj
        if parent is None:
            try:
                parent = record[arry[0]]
            except KeyError:
                return "Not Found"
        # parse out parent object
        if type(parent) is list:
            parent = parent[0]
        # call child obj
        try:
            child = parent[arry[(val + 1)]]
        except KeyError:
            return "Not Found"
        # if also parent, loop
        if type(child) != str:
            buried_value(record=record, string=string, parent=parent)
        else:
            return str(child)


def loop_api(api_key, file, col_list, end_pt):
    skip = 0
    api_resp = get_api(mem_skip=skip, api_key=api_key, end_pt=end_pt)
    if api_resp.status_code != 200:
        status_error = gui()
        texterr = "Status Code: " + str(api_resp.status_code) + "\n" + str(api_resp.content)
        status_error.errorBox(title="Error Code Returned", message=texterr)
        quit()
    total = api_resp.json().get('total')
    # run the API until all records are returned
    while skip < total:
        # create a single 'header' section on the first pass
        if skip == 0:
            status = api_resp.status_code
            file.write("Status Code: " + str(status) + "\n")
            file.write("Total: " + str(total) + "\n")
            for i in range(0, len(col_list)):
                file.write(str(col_list[i]))
                if i < len(col_list) - 1:
                    file.write(" | ")
                if i == len(col_list) - 1:
                    file.write("\n")
        # create a addict Dictionary object for easier access on getters
        resp = Dict(api_resp.json())
        # each response will return a list with up to 50 records, this loop through each node in the list
        for i in range(len(resp.data)):
            for j in range(0, len(col_list)):
                if ":" in col_list[j]:
                    buried_value(record=resp.data[i], string=col_list[j])
                else:
                    file.write(str(resp.data[i][col_list[j]]))
                if j < len(col_list) - 1:
                    file.write(" | ")
                if j == len(col_list) - 1:
                    file.write("\n")
            skip += 1
        api_resp = get_api(mem_skip=skip, api_key=api_key, end_pt=end_pt)