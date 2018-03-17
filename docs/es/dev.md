# Create new model diagram

Add django_extensions in INSTALLED_APPS

```bash
sudo apt-get install graphviz libgraphviz-dev graphviz-dev pkg-config
pip install pygraphviz
python eventol/manage.py graph_models manager -o docs/assets/models.png
```
