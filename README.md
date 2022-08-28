# fastapi-event-driven

An example of application with event handlers.

You can see a list of possible handlers and contracts for them after run application on 
`http://127.0.0.1:8080/swagger` (with default settings). 


## Run

1. Create `.env` file with variables or generate it by command:
    ```shell
    make env
    ```

2. Install project requirements:
    ```shell
    make install
    ```

3. Run Redis database with docker-compose:
    ```shell
    make db
    ```

4. Run project:
    ```shell
    make run
    ```

## Developer experience

List of possible commands:
```shell
make help
```

## TODO

1. Create tests for handlers and add Github Workflow for them;
2. Add doc-strings for functions (and check them with linters);
3. Add more linters (maybe add more flake8 plugins like `flake8-cognitive-complexity` etc.)
4. Make async redis connection with `asyncio-redis`.