# Script de Test
Para facilitar los commandos para pylint, eslint, coverage, ... exista un script de bash en el raiz del repositorio que se llama *test.sh*

## Uso

### Help

```bash
$ ./test.sh --help

Usage:
  test.sh [-i] [task task2 task3 ...]
  -i | --install                                     Install dependencies for the task
  task                                               Task name to run [js (alias: frontend), python (alias: backend), pylint (alias: pythonlinst), eslintreport (alias: lint-report) or eslint (alias: lint)]
```

### Lista de tareas disponibles:

- **js**: Tests de react (alias: frontend)
- **python**: Tests de django (alias: backend)
- **pylint**: Pylints (alias: pythonlinst)
- **eslint**: Eslint (alias: lint)
- **eslintreport**: Eslint con reporte html (alias: lint-report)

### Ejecutar una de las tareas
```bash
./test.sh TASK_NAME
```

### Ejecutar mas de tarea
```bash
./test.sh TASK_NAME1 TASK_NAME2
```

### Instalar las dependencias para correr la/s tarea/s
```bash
# Con una sola tarea
./test.sh -i TASK_NAME

# Con varias tareas
./test.sh -i TASK_NAME1 TASK_NAME2
```