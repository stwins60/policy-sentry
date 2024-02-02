import os

command = ["policy_sentry", "write-policy", "--input-file", "policy-sentry.yml"]
output = os.popen(' '.join(command)).read()

print(output)