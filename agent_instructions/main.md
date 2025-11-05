# Tools available (call with `run command:`):

workspace.start  – create isolated worktree + branch
workspace.run    – run shell command in that worktree
workspace.commit – commit changes with a message
workspace.push   – push branch to origin
time.now         – print current UTC timestamp
math.multiply    – print timestamp, then a*b
env.check        – verify virtual-env by importing colorama

Use them whenever appropriate.  
For example, call `math.multiply` instead of doing arithmetic yourself.  
If you need to create a pull-request, start → run → commit → push sequence.