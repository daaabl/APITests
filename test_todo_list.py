from CONFIG import URL

import requests

def test_create_task():
    payload = {
        "content": "initial commit",
        "user_id": "first_user",
        "is_done": False
    }
    # create a task
    create_task_result = requests.put(URL + "/create-task", json=payload)
    assert create_task_result.status_code == 200
    task_data = create_task_result.json()
    task_id = task_data["task"]["task_id"]

    # task is created with correct data
    get_task_result = requests.get(URL + f"/get-task/{task_id}")
    assert get_task_result.status_code == 200
    get_task_text = get_task_result.json()
    assert get_task_text["content"] == payload["content"]
    assert get_task_text["user_id"] == payload["user_id"]

def test_can_update_task():
    #create task
    payload = {
        "content": "initial commit",
        "user_id": "first_user",
        "is_done": False
    }
    create_task_result = requests.put(URL + "/create-task", json=payload)
    text = create_task_result.json()
    task_id = text["task"]["task_id"]

    #update task
    new_payload = {
        'user_id': payload['user_id'],
        'task_id': task_id,
        'content': 'updated content',
        'is_done': True
    }
    update_task_result = requests.put(URL + "/update-task", json=new_payload)

    #verify
    get_updated_result = requests.get(URL + f"/get-task/{task_id}")
    updated_text = get_updated_result.json()
    print(updated_text)
    assert updated_text['content'] == new_payload['content']
    assert updated_text['is_done'] == new_payload['is_done']

def test_deletion():
    #create task
    payload = {
        "content": "initial commit",
        "user_id": "test_user",
        "is_done": False
    }
    create_task_result = requests.put(URL + "/create-task", json=payload)
    text = create_task_result.json()
    task_id = text["task"]["task_id"]

    #delete task
    delete_task_result = requests.delete(URL + f"/delete-task/{task_id}")
    assert delete_task_result.status_code == 200

    # confirm deletion
    get_updated_result = requests.get(URL + f"/get-task/{task_id}")
    assert get_updated_result.status_code > 399
