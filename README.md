# angel-mortal-bot

## Hosting on Heroku
1. Ensure that in the Procfile, the run script naming is consistent with the main Python script
2. Use `updater.start_webhook()` instead of `updater.start_polling()` in the `main()` function
3. Ensure that Heroku has config vars appropriately set to reflect the environment variables
4. Push the code to heroku

### Viewing logs:
- Logs can be viewed using `heroku logs -t`

### Running the bot locally:
- `pipenv run python bot.py`