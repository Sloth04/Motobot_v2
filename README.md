# Motobot v2

Motobot is a project which you can use to write your 
periods of time as minutes in your local database.
It uses [python-telegram-bot](https://docs.python-telegram-bot.org/en/v20.0a1/index.html) as main bot lib.

Using a [Sqlite](https://www.sqlite.org/index.html) database to store all data about members or time.

## Authors
All members took an active part in modernization.
- Sasha Chepurnyi [backend and database composition]
- Maria Demchenko [backend/frontend and consept maker]
- Kate Dolzhko [backend/frontend and consept maker]
- Valeria Polishyk [backend]

## Installation

- **First you need to install [poetry](https://python-poetry.org/) and git.**
- **Do git clone.**

```bash
git clone "repo_url"
```
- **Install all dependencies with**  ```poetry install```

```bash
poetry install
```

- **Create ```.env```. The repo has ```.env.example``` as an example**

**Create token and fill ```.env```**
Create your token with [@BotFather](https://telegram.me/BotFather).
Follow proposed instructions

```bash
TOKEN='your token'
```

## Usage

- **All you need is to run main.py from poetry shell**

```bash
poetry shell
main.py
```

- **Continue talking with your bot with Telegram, it will guide you**

- **You will find your result at your database.**

***

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
