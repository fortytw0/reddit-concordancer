import json

submissions_file_name = "submission_liverpool.json"

f = open(submissions_file_name)
submissions = json.load(f)
f.close()

print(submissions)