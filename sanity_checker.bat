python -m build
pytest tests
pyreverse -o png -p sentimeter src\sentimeter
flake8 src --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
flake8 apps --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
black .
pip uninstall sentimeter
git log --format="%C(auto) %h %d %s" > changelog.md
git status
