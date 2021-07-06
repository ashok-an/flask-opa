package example

# This test will pass.
test_ok {
    true
}

test_get_same_user {
  allow with input as {"method": "GET", "path": ["office", "pam"], "user": "pam"} 
}

test_del_same_user {
  not allow with input as {"method": "DELETE", "path": ["office", "pam"], "user": "pam"} 
}

test_del_manager {
  allow with input as {"method": "DELETE", "path": ["office", "dwight"], "user": "mike"} 
}

test_path_wrong_user {
  not allow with input as {"method": "GET", "path": ["office", "mike"], "user": "andy"} 
}

test_root_no_user {
  allow with input as {"method": "GET", "path": [""], "user": ""} 
}

test_root_user {
  allow with input as {"method": "GET", "path": [""], "user": "andy"} 
}

