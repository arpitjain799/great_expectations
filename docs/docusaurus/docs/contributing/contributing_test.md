---
title: Contribution and Testing
---

## Running tests
You can run all unit tests by running `pytest` in the `great_expectations` directory root. By default the tests will be run against `pandas` and `sqlite`, with the ability to test additional backends like `postgresql`, `spark`, and `mssql` using `pytest` flags. To run a test against a specific backend like PostgreSQL, you can run `pytest --postgresql`.

Currently the list of supported `pytest` flags for general testing are as follows:   

  * `--spark`: Execute tests against Spark backend.
  * `--postgresql`: Execute tests against PostgreSQL.
  * `--mysql`: Execute tests against MySql.
  * `--mssql`: Execute tests against Microsoft SQL Server.
  * `--bigquery`: Execute tests against Google BigQuery (requires additional set up).
  * `--aws`: Execute tests against AWS resources like S3, Redshift and Athena (requires additional setup).

In addition, if you would like to skip all local backend tests (with the exception of the pandas backend), you can run `pytest --no-sqlalchemy`. 

Note: as of early 2020, the tests generate many warnings. Most of these are generated by dependencies (pandas, sqlalchemy, etc.) You can suppress them with pytest’s `--disable-pytest-warnings` flag: `pytest --no-sqlalchemy --disable-pytest-warnings`.

### BigQuery tests

In order to run BigQuery tests, you first need to go through the following steps:

1. [Select or create a Cloud Platform project](https://console.cloud.google.com/project).
2. [Setup Authentication](https://googleapis.dev/python/google-api-core/latest/auth.html).
3. In your project, [create a BigQuery dataset](https://cloud.google.com/bigquery/docs/datasets) (e.g. named `test_ci`) and [set the dataset default table expiration](https://cloud.google.com/bigquery/docs/updating-datasets#table-expiration) to `.1` days

After setting up authentication, you can run with your project using the environment variables `GE_TEST_BIGQUERY_PROJECT` and `GE_TEST_BIGQUERY_DATASET`, e.g.

```bash
    GE_TEST_BIGQUERY_PROJECT=<YOUR_GOOGLE_CLOUD_PROJECT> 
    GE_TEST_BIGQUERY_DATASET=test_ci
    pytest tests/test_definitions/test_expectations_cfe.py --bigquery
```

## Writing unit and integration tests

Production code in Great Expectations must be thoroughly tested. In general, we insist on unit tests for all branches of every method, including likely error states. Most new feature contributions should include several unit tests. Contributions that modify or extend existing features should include a test of the new behavior.

Experimental code in Great Expectations need only be tested lightly. We are moving to a convention where experimental features are clearly labeled in documentation and the code itself. However, this convention is not uniformly applied today.

Most of Great Expectations’ integration testing is in the [CLI](https://docs.greatexpectations.io/docs/guides/miscellaneous/how_to_use_the_great_expectations_cli), which naturally exercises most of the core code paths. Because integration tests require a lot of developer time to maintain, most contributions should not include new integration tests, unless they change the CLI itself.

Note: we do not currently test Great Expectations against all types of SQL database. CI test coverage for SQL is limited to PostgreSQL, SQLite, MSSQL, and BigQuery. We have observed some bugs because of unsupported features or differences in SQL dialects, and we are actively working to improve dialect-specific support and testing.

## Unit tests for Expectations
One of Great Expectations’ important promises is that the same Expectation will produce the same result across all supported execution environments: pandas, sqlalchemy, and Spark.

To accomplish this, Great Expectations encapsulates unit tests for Expectations as JSON files. These files are used as fixtures and executed using a specialized test runner that executes tests against all execution environments.

Test fixture files are structured as follows:

````console
{
    "expectation_type" : "expect_column_max_to_be_between",
    "datasets" : [{
        "data" : {...},
        "schemas" : {...},
        "tests" : [...]
    }]
}
````

Each item under `datasets` includes three entries: `data`, `schemas`, and `tests`.

### data

…defines a dataframe of sample data to apply Expectations against. The dataframe is defined as a dictionary of lists, with keys containing column names and values containing lists of data entries. All lists within a dataset must have the same length.

````console
"data" : {
    "w" : [1, 2, 3, 4, 5, 5, 4, 3, 2, 1],
    "x" : [2, 3, 4, 5, 6, 7, 8, 9, null, null],
    "y" : [1, 1, 1, 2, 2, 2, 3, 3, 3, 4],
    "z" : ["a", "b", "c", "d", "e", null, null, null, null, null],
    "zz" : ["1/1/2016", "1/2/2016", "2/2/2016", "2/2/2016", "3/1/2016", "2/1/2017", null, null, null, null],
    "a" : [null, 0, null, null, 1, null, null, 2, null, null],
},
````

### schemas

…define the types to be used when instantiating tests against different execution environments, including different SQL dialects. Each schema is defined as dictionary with column names and types as key-value pairs. If the schema isn’t specified for a given execution environment, Great Expectations will introspect values and attempt to guess the schema.

````console
"schemas": {
    "sqlite": {
        "w" : "INTEGER",
        "x" : "INTEGER",
        "y" : "INTEGER",
        "z" : "VARCHAR",
        "zz" : "DATETIME",
        "a" : "INTEGER",
    },
    "postgresql": {
        "w" : "INTEGER",
        "x" : "INTEGER",
        "y" : "INTEGER",
        "z" : "TEXT",
        "zz" : "TIMESTAMP",
        "a" : "INTEGER",
    }
},
````

### tests

…define the tests to be executed against the dataframe. Each item in `tests` must have `title`, `exact_match_out`, `in`, and `out`. The test runner will execute the named Expectation once for each item, with the values in `in` supplied as kwargs.

The test passes if the values in the expectation Validation Result correspond with the values in `out`. If `exact_match_out` is true, then every field in the Expectation output must have a corresponding, matching field in `out`. If it’s false, then only the fields specified in `out` need to match. For most use cases, false is a better fit, because it allows narrower targeting of the relevant output.

`suppress_test_for` is an optional parameter to disable an Expectation for a specific list of backends.

See an example below. For other examples

````console
"tests" : [{
    "title": "Basic negative test case",
    "exact_match_out" : false,
    "in": {
        "column": "w",
        "result_format": "BASIC",
        "min_value": null,
        "max_value": 4
    },
    "out": {
        "success": false,
        "observed_value": 5
    },
    "suppress_test_for": ["sqlite"]
},
...
]

````

The test fixture files are stored in subdirectories of `tests/test_definitions/` corresponding to the class of Expectation:

* column_map_expectations
* column_aggregate_expectations
* column_pair_map_expectations
* column_distributional_expectations
* multicolumn_map_expectations
* other_expectations

By convention, the name of the file is the name of the Expectation, with a .json suffix. Creating a new json file will automatically add the new Expectation tests to the test suite.

Note: If you are implementing a new Expectation, but don’t plan to immediately implement it for all execution environments, you should add the new test to the appropriate list(s) in the `candidate_test_is_on_temporary_notimplemented_list_v2_api` method within `tests/test_utils.py`. Often, we see Expectations developed first for pandas, then later extended to SqlAlchemy and Spark.

You can run just the Expectation tests with `pytest tests/test_definitions/test_expectations.py`.

## Performance testing

### Configuring Data Before Running Performance Tests

The performance tests use BigQuery.

Before running a performance test, setup data with `tests/performance/setup_bigquery_tables_for_performance_test.sh`.

For example:

```bash
GE_TEST_BIGQUERY_PEFORMANCE_DATASET=<YOUR_GCP_PROJECT> tests/performance/setup_bigquery_tables_for_performance_test.sh
```

For more information on getting started with BigQuery, please refer to the [above section on BigQuery tests](#bigquery-tests).

### Running the Performance Tests

Run the performance tests with pytest, e.g.

```
pytest tests/performance/test_bigquery_benchmarks.py \
  --bigquery --performance-tests \
  -k 'test_taxi_trips_benchmark[1-True-V3]'  \
  --benchmark-json=tests/performance/results/`date "+%H%M"`_${USER}.json \
  -rP -vv
```

Some benchmarks take a long time to complete. In this example, only the relatively fast `test_taxi_trips_benchmark[1-True-V3]` benchmark is run and the output should include runtime like the following:

```
--------------------------------------------------- benchmark: 1 tests ------------------------------------------------------
Name (time in s)                         Min     Max    Mean  StdDev  Median     IQR  Outliers     OPS  Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------
test_taxi_trips_benchmark[1-True-V3]     5.0488  5.0488  5.0488  0.0000  5.0488  0.0000       0;0  0.1981       1           1
-----------------------------------------------------------------------------------------------------------------------------
```

The result is saved for comparisons as described below.

### Comparing Performance Results

Compare test results in this directory with `py.test-benchmark compare`, e.g.

```
$ py.test-benchmark compare --group-by name tests/performance/results/initial_baseline.json tests/performance/results/*${USER}.json                                                                   

---------------------------------------------------------------------------- benchmark 'test_taxi_trips_benchmark[1-True-V3]': 2 tests ---------------------------------------------------------------------------
Name (time in s)                                        Min               Max              Mean            StdDev            Median               IQR            Outliers     OPS            Rounds  Iterations
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_taxi_trips_benchmark[1-True-V3] (initial_base)     5.0488 (1.0)      5.0488 (1.0)      5.0488 (1.0)      0.0000 (1.0)      5.0488 (1.0)      0.0000 (1.0)           0;0  0.1981 (1.0)           1           1
test_taxi_trips_benchmark[1-True-V3] (2114_work)        6.4675 (1.28)     6.4675 (1.28)     6.4675 (1.28)     0.0000 (1.0)      6.4675 (1.28)     0.0000 (1.0)           0;0  0.1546 (0.78)          1           1
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

Please refer to [pytest-benchmark documentation](https://pytest-benchmark.readthedocs.io/en/latest/comparing.html) for more info.

### Checking in new benchmark results

When creating a pull request that is intended to improve performance, please include in the pull request benchmark results showing improvements.  Please use the script `run_benchmark_multiple_times.sh` to run the benchmark multiple times.  Name the tests with the first argument provided to that script. For example, the `tests/performance/results/minimal_multithreading_*.json` files were created with the following command:

```
$ tests/performance/run_benchmark_multiple_times.sh minimal_multithreading
```

## Manual testing

We do manual testing (e.g. against various databases and backends) before major releases and in response to specific bugs and issues.
