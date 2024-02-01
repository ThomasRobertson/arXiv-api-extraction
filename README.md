## Project Overview

This project consists of two main modules: `api_worker` and `harvest_and_collect`.

### api_worker Module

The `api_worker` module provides a Flask application for interacting with a Neo4j database that stores ArXiv records. The application provides several endpoints for querying the database:

- `/authors`: Returns a list of all authors in the database.
- `/article/<id>`: Returns the details of the article with the given identifier.
- `/summary/<id>`: Returns the summary of the article with the given identifier.
- `/records`: Returns a list of record identifiers. This endpoint accepts optional query parameters for filtering the records.

The application also provides a POST endpoint at `/records` for adding a new record to the database. The record must be provided as an XML string in the request body.

### harvest_and_collect Module

The `harvest_and_collect` module provides classes to connect to and harvest records from the ArXiv database and add them to a Neo4j database.

#### Classes in harvest_and_collect Module

- `ArXivHarvester`: A class to handle the connection to the ArXiv database and fetch records.
- `ArXivRecord`: A class to represent a single record from the ArXiv database.
- `GraphDBConnexion`: Handle the database connection and provides functions to easily add records to it.

## Python Documentation

Detailed documentation for this project can be found in the `documentation` folder. You can also access it via the following URL:
- [harvest-and-collect](documentation/harvest-and-collect.md)
- [api-endpoint](documentation/api-endpoint.md)

## API Documentation

This project uses OpenAPI and Swagger for API documentation. After running the application, you can access the API documentation at `localhost:5000`. Simply navigate to `localhost:5000` in your web browser to view the Swagger UI and interact with the API documentation.

This web interface even allow you to run basic tests of the differents routes.

You can access a, maybe outdated, offline version here : [api-documentation](documentation/api-documentation.md).

## Getting Started

WIP

## Running Unit Tests

To run the unit tests for each module, navigate to the module's directory and run the following commands:

```bash
chmod +x run_unit_test.sh
sh run_unit_test.sh
```

*Note: you will find one script of each module, they cannot be run in parrallel.*

## CI/CD

This repository is hosted on GitLab and mirrored on GitHub. Please note that the CI/CD pipelines are configured for GitLab only.

The CI/CD pipeline includes automatic unit tests and linting verification. The linting verification are allowed to fail as to not block the release of new versions.

We have implemented a continuous development approach. Certain push to the `main` branch triggers an automatic release, such as `fix` and `feat`. We adhere to the Semantic Versioning standards, facilitated by the use of Conventional Commits.

*Fun fact: more than 460 jobs where runned on the GitLab runner of CentraleSupelec, 90 just to get the Semantic Versioning working.*

You can find the releases [here](https://gitlab-student.centralesupelec.fr/thomas.robertson/arxiv-api-extraction/-/releases), along with their changelogs.


## License

This project is licensed under the MIT License. See the LICENSE file for details.