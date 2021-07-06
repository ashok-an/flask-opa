package example

default allow = false

# allow root
allow {
  input.method == "GET"
  input.path == [""]
}

# allow swagger
allow {
  input.method == "GET"
  input.path[0] == ["swaggerui", "swagger.json"][_]
}

# any-one can list
allow {
  input.method == "GET"
  input.path == ["office"]
}

# one can get/set his/her info
allow {
  input.method == ["GET", "PUT"][_]
  input.path == ["office", input.user]
}

# only manager can add or delete
allow {
  input.method == "POST"
  input.path == ["office"]
  input.user == "mike"
}

# only manager can delete
allow {
  input.method == "DELETE"
  emp := input.path[1]
  input.path == ["office", emp]
  input.user == "mike"
  emp != "mike"
}
