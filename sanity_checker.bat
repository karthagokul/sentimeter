python -m build
pytest tests
pyreverse -o png -p sentimeter src\sentimeter
flake8 src --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
black .
git log --format="%C(auto) %h %d %s" > changelog.md
git status