#!/bin/bash
cmdname=$(basename $0)
INSTALL=false

function usage {
    cat << USAGE >&2
Usage:
  $cmdname [-i] [task task2 task3 ...]
  -i | --install                                     Install dependencies for the task
  task                                               Task name to run [js (alias: frontend), python (alias: backend), eslintreport (alias: lint-report) or eslint (alias: lint)]
USAGE
  exit 1
}

function install_js {
  cd eventol/front
  npm install -g yarn
  yarn install
  cd -
}

function install_python {
   pip3 install -r requirements.txt
   pip3 install -r requirements-dev.txt
}

function run_install {
  TASK=$1
  if [ "$TASK" == "js" ] || [ "$TASK" == "frontend" ]; then
    install_js
  elif [ "$TASK" == "python" ] || [ "$TASK" == "backend" ]; then
    install_python
  elif [ "$TASK" == "pylint" ] || [ "$TASK" == "pythonlint" ]; then
    install_python
  elif [ "$TASK" == "eslint-report" ] || [ "$TASK" == "lint-report" ]; then
    install_js
  elif [ "$TASK" == "eslint" ] || [ "$TASK" == "lint" ]; then
    install_js
  else
    echo "Invalid task to install. Plataforms: js (alias: frontend, eslintreport, lint-report, eslint, lint) and python (alias: backend)"
    exit 1
  fi
}

function jstest {
  cd eventol/front
  npm test
  cd -
}

function eslint {
  cd eventol/front
  npm run eslint
  cd -
}

function eslintreport {
  cd eventol/front
  npm run eslint-report
  cd -
}

function pythonlint {
  pylint --output-format=colorized eventol/eventol eventol/manager
}

function pythontest {
  cd eventol/front
  yarn install
  timeout 20 npm start || true
  cd -
  cd eventol/
  ./manage.py test -v 3
  # py.test --cov-report term-missing --cov-report html --cov
  cd -
}

function run_task {
  TASK=$1
  if [ "$TASK" == "js" ] || [ "$TASK" == "frontend" ]; then
    jstest
  elif [ "$TASK" == "python" ] || [ "$TASK" == "backend" ]; then
    pythontest
  elif [ "$TASK" == "pylint" ] || [ "$TASK" == "pythonlint" ]; then
    pythonlint
  elif [ "$TASK" == "eslint-report" ] || [ "$TASK" == "lint-report" ]; then
    eslintreport
  elif [ "$TASK" == "eslint" ] || [ "$TASK" == "lint" ]; then
    eslint
  else
    echo "Invalid task. Plataforms: js (alias: frontend), python (alias: backend), eslintreport (alias: lint-report) or eslint (alias: lint)"
    exit 1
  fi
}

# process arguments
while [[ $# -gt 0 ]]
do
  case "$1" in
    -i)
      INSTALL=true
      shift 1
    ;;
    --install)
      INSTALL=true
      shift 1
    ;;
    --help)
      usage
    ;;
    -*)
      echoerr "Unknown argument: $1"
      usage
    ;;
    --*)
      echoerr "Unknown argument: $1"
      usage
    ;;
    *)
      INSTALL=${INSTALL:false}
      for TASK in "$@"; do
        if $INSTALL; then
          run_install $INSTALL
        fi
        run_task $TASK
        shift 1
      done
    ;;
  esac
done

if [[ "$TASK" == "" ]]; then
  echoerr "Error: you need to provide a task to run."
  usage
fi
