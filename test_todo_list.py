from CONFIG import URL

import requests

def test_create_task():
    # create a task
    payload = get_payload()
    create_task_result = create_task(payload)
    assert create_task_result.status_code == 200
    task_id = get_task_id(create_task_result)

    # task is created with correct data
    get_task_result = requests.get(URL + f"/get-task/{task_id}")
    assert get_task_result.status_code == 200
    get_task_data = get_task_result.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]

def test_can_update_task():
    #create task
    payload = get_payload()
    create_task_result = create_task(payload)
    task_id = get_task_id(create_task_result)

    #update task
    new_payload = {
        'user_id': payload['user_id'],
        'task_id': task_id,
        'content': 'updated content',
        'is_done': True
    }
    update_task(new_payload)

    #verify
    get_updated_result = requests.get(URL + f"/get-task/{task_id}")
    updated_data = get_updated_result.json()
    assert updated_data['content'] == new_payload['content']
    assert updated_data['is_done'] == new_payload['is_done']

def test_deletion():
    #create task
    payload = get_payload()
    create_task_result = create_task(payload)
    task_id = get_task_id(create_task_result)

    #delete task
    delete_task_result = requests.delete(URL + f"/delete-task/{task_id}")
    assert delete_task_result.status_code == 200

    # confirm deletion
    get_updated_result = requests.get(URL + f"/get-task/{task_id}")
    assert get_updated_result.status_code > 399

# helper functions
def get_payload():
    return {
        "content": "initial commit",
        "user_id": "test_user",
        "is_done": False
    }

def create_task(payload):
    return requests.put(URL + "/create-task", json=payload)

def update_task(payload):
    return requests.put(URL + "/update-task", json=payload)

def get_task_id(response):
    task_data = response.json()
    task_id = task_data["task"]["task_id"]
    return task_id