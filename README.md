# skipSQL

## Description
skipSQL is a connector for relational database. It allows users to query and receive data from their database in nature language without using SQL

## Demo
Demo website: www.skipsql.com

## Example

```
Connected to database test_ai at localhost

Q:  What is Daniel Faviet's salary?

A:  Answer: Daniel Faviet's salary is $9000.00.

SQL executed:  SELECT salary FROM employees WHERE first_name = 'Daniel' AND last_name = 'Faviet'

---------------------

Q:  What is the average salary of Daniel Faviet's department?

A:  Answer: The average salary of Daniel Faviet's department is $9000.

SQL executed:  SELECT AVG(salary) FROM employees  WHERE last_name = 'Faviet'  AND department_id IN (SELECT department_id FROM departments)

---------------------

Q:  Who has lower than average salary in the same department as Daniel Faviet?

A:  Answer: John Chen, Ismael Sciarra, Jose Manuel Urman, and Luis Popp have lower than average salary in the same department as Daniel Faviet.

SQL executed:  SELECT e.first_name, e.last_name, e.salary  FROM employees e  INNER JOIN departments d ON e.department_id = d.department_id  INNER JOIN (SELECT AVG(salary) AS avg_salary, department_id              FROM employees              GROUP BY department_id) AS avg_sal  ON avg_sal.department_id = d.department_id  WHERE e.salary < avg_sal.avg_salary  AND EXISTS (SELECT 1              FROM employees              WHERE first_name = 'Daniel'              AND last_name = 'Faviet'              AND department_id = d.department_id)
```

## Usage

1. Set up database

Since skipsql is a database connector, user must have a database set up for it
to connect to.  If this database does not exist yet, user can set up by one of
following way as examples:
  - Create a local database by installing a open source relational database
    engine such as MySQl, postgres, MariaDB etc.
  - Use cloud service provider ie. AWS, Azure to create a database instance.
    They have free tier which are enough for just trying out this connector.

(A sample database can be tried at www.skipsql.com but connection info is not
available)

2. Fill in the connetion info in demo.py

The database instance must have a user with at least "SELECT" privilege.

3. Set up openAI API key

The connector uses openAI api for AI model, so an API key must be provided as
environment variable.

  - Follow https://platform.openai.com/docs/quickstart?context=python to set up
    the API key
  - Set the API key as environment variable. Run in terminal: ``export
    OPENAI_API_KEY="paste your key here"``

### Below steps are soon to be automated in future updates

4. Install dependencies

Run in terminal: ``pip install -r lib/requirements.txt``

5. Prepare table schema

To generate accurate SQL query, the connector needs to know what the tables
looks like. Therefore a txt file containing table schema needs to be generated.

Engine like MySQL has binaries built for this purpose.

  - If has MySQL/MariaDB installed, run ``/usr/bin/mysqldump -u <user> -h <host> -p<password> <database name> --no-data > demo_schema.txt``
  - If using postgres, connect to database and run ``\d+``, and capture output in demo_schema.txt

6. Run demo.py and start developing

## Contact

Email: tingyao.nian@outlook.com / niantingyao@gmail.com

LinkedIn: https://www.linkedin.com/in/tingyao-nian-550525107/
