# Test script
For run pylint, eslint, coverage, ... commands exists a bash script in root folder with this commands, this script is *test.sh*

## Use

### Help

```bash
$ ./test.sh --help

Usage:
  test.sh [-i] [task task2 task3 ...]
  -i | --install                                     Install dependencies for the task
  task                                               Task name to run [js (alias: frontend), python (alias: backend), pylint (alias: pythonlinst), eslintreport (alias: lint-report) or eslint (alias: lint)]
```

### Available tasks:

- **js**: React tests (alias: frontend)
- **python**: Django tests (alias: backend)
- **pylint**: Pylints (alias: pythonlinst)
- **eslint**: Eslint (alias: lint)
- **eslintreport**: Eslint with html report (alias: lint-report)

### Run one task
```bash
./test.sh TASK_NAME
```

### Run two or more tasks
```bash
./test.sh TASK_NAME1 TASK_NAME2
```

### Install task dependencies
```bash
# One task
./test.sh -i TASK_NAME

# More than one task
./test.sh -i TASK_NAME1 TASK_NAME2
```