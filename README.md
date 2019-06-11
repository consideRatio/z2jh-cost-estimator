# Resources to simulate the cost of an autoscaling Z2JH deployment

## Development Notes

### To make changes and test them

1. Clone the repo and make a change

2. Install `pipenv` using `pip`.

    ```sh
    pip install pipenv
    ```

3. Setup a virtual development environment

    ```sh
    pipenv install --dev
    ```

4. Run tests

    ```sh
    pipenv run pytest
    ```

### Build and upload a PyPI release

1. Test, build and upload the package

    ```sh
    # Make sure you are up to date with what you have declared to require
    pipenv install --dev

    # Update changelog, fix requirements, etc.
    pipenv lock -r > requirements.txt

    # Run tests
    pipenv run pytest

    # Commit and tag to influence the PyPI version
    # PBR will look for the latest tag and then append development
    # versions based on your git commits since the latest tag.
    git add .
    git commit


    TAG=$(pipenv run python -c 'from pbr.version import VersionInfo; print(VersionInfo("discourse_sso_oidc_bridge").version_string())')
    git tag -a $TAG -m "Release $TAG"

    # Build the package
    pipenv run python setup.py bdist_wheel

    # Upload the package to PyPI
    pipenv run twine upload --skip-existing --username consideratio dist/*
    ```

2. Push git commits and tags

    ```sh
    git push
    git push --tags
    ```
