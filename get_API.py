import requests
from addict import Dict


def get_api(mem_skip, api_key, end_pt):
    headers = {
        'Accept': 'application/json',
        'clientkey': api_key
    }
    params = ({
        'skip': mem_skip
    })
    resp_val = requests.get(
        'https://api.highground.com/1.0/' + end_pt,
        headers=headers,
        params=params
    )
    return resp_val


def loop_api(api_key, file, col_list, end_pt):
    skip = 0
    api_resp = get_api(mem_skip=skip, api_key=api_key, end_pt=end_pt)
    total = api_resp.json().get('total')
    # run the API until all records are returned
    while skip < total:
        # create a single 'header' section on the first pass
        if skip == 0:
            status = api_resp.status_code
            file.write("Status Code: " + str(status) + "\n")
            file.write("Total: " + str(total) + "\n")
            for i in range(0, len(col_list)):
                file.write(col_list[i])
                if i < len(col_list) - 1:
                    file.write(" | ")
                if i == len(col_list) - 1:
                    file.write("\n")
        # create a addict Dictionary object for easier access on getters
        resp = Dict(api_resp.json())
        # each response will return a list with up to 50 records, this loop through each node in the list
        for i in range(len(resp.data)):
            for j in range(0, len(col_list)):
                file.write(resp.data[i][col_list[j]])
                if j < len(col_list) - 1:
                    file.write(" | ")
                if j == len(col_list) - 1:
                    file.write("\n")
            skip += 1
        api_resp = get_api(mem_skip=skip, api_key=api_key, end_pt=end_pt)
    file.close()
    quit()