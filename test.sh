#!/bin/bash
set -e
set -x

cmdname=$(basename $0)
INSTALL=false

function usage {
    cat << USAGE >&2
Usage:
  $cmdname [-i] [-t task]
  -i | --install                                     Install dependencies for the task
  -t TASK | --task=TASK                              Task name to run
USAGE
  exit 1
}

function install_js {
  cd workshop/front
  npm install -g yarn
  yarn install
  cd -
}

function install_python {
   pip3 install -r requirements.txt
   pip3 install -r requirements-dev.txt
}

function run_install {
  TASK_NAME=$1
  if [ "$PLATFORM" == "js" ] || [ "$PLATFORM" == "frontend" ]; then
    install_js
  elif [ "$PLATFORM" == "python" ] || [ "$PLATFORM" == "backend" ]; then
    install_python
  elif [ "$PLATFORM" == "pylint" ] || [ "$PLATFORM" == "pythonlint" ]; then
    install_python
  elif [ "$PLATFORM" == "eslint-report" ] || [ "$PLATFORM" == "lint-report" ]; then
    install_js
  elif [ "$PLATFORM" == "eslint" ] || [ "$PLATFORM" == "lint" ]; then
    install_js
  else
    echo "Invalid platform to install. Plataforms: js (alias: frontend, eslintreport, lint-report, eslint, lint) and python (alias: backend)"
    exit 1
  fi
}

function jstest {
  cd workshop/front
  npm test
  cd -
}

function eslint {
  cd workshop/front
  npm run eslint
  cd -
}

function eslintreport {
  cd workshop/front
  npm run eslint-report
  cd -
}

function pythonlint {
  pylint --output-format=colorized --load-plugins pylint_django workshop/workshop workshop/links
}

function pythontest {
  cd workshop/front
  npm install -g yarn webpack
  yarn install
  timeout 20 npm start || true
  cd -
  cd workshop/
  py.test --cov-report term-missing --cov-report html --cov
  cd -
}

function run_task {
  TASK=$1
  if [ "$PLATFORM" == "js" ] || [ "$PLATFORM" == "frontend" ]; then
    jstest
  elif [ "$PLATFORM" == "python" ] || [ "$PLATFORM" == "backend" ]; then
    pythontest
  elif [ "$PLATFORM" == "pylint" ] || [ "$PLATFORM" == "pythonlint" ]; then
    pythonlint
  elif [ "$PLATFORM" == "eslint-report" ] || [ "$PLATFORM" == "lint-report" ]; then
    eslintreport
  elif [ "$PLATFORM" == "eslint" ] || [ "$PLATFORM" == "lint" ]; then
    eslint
  else
    echo "Invalid platform. Plataforms: js (alias: frontend), python (alias: backend), eslintreport (alias: lint-report) or eslint (alias: lint)"
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
    -t)
      TASK="$2"
      if [[ $TASK == "" ]]; then
        break;
      fi
      shift 2
    ;;
    --task=*)
      TASK="${1#*=}"
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
      for PLATFORM in "$@"; do
        if $INSTALL; then
          run_install $INSTALL
        fi
        run_task $PLATFORM
        shift 1
      done
    ;;
  esac
done

if [[ "$TASK" == "" ]]; then
  echoerr "Error: you need to provide a task to run."
  usage
fi
