# angel-mortal-bot

## Installing dependencies
This bot was made in `python 3.8`
We used pipenv to manage the virtualenv and packages of our project.

`pip install pipenv`

You can then install the required packages through the command

`pipenv install`

<br>

## Configuring .env file
Here are the variables you need to have in your .env file

```
BOT_TOKEN = telegram bot token generated through BotFather
GOOGLE_SCRIPT = link to your [google sheets](###data-storage-format)
HOST = local
```

<br>

## Hosting on Heroku
1. Ensure that in the Procfile, the run script naming is consistent with the main Python script
2. Ensure that Heroku has config vars appropriately set to reflect the environment variables
3. Push the code to heroku

<br>

## Viewing logs:
- Logs can be viewed using `heroku logs -t`

<br>

## Running the bot locally:
- `pipenv run python bot.py`

<br>

## Angels and mortal data storage:
Data for angels and mortals in the bot is stored on Google Sheets, using Google Apps Script to update
and get the player profiles. 

<br>

### Data storage format:
![Google Sheets](/assets/angel-mortal-sheets-storage.png)

<br>

Below is the Google Apps Script code used to make `GET` and `POST` requests
to update the player profiles in Google Sheets

```
const SHEET_ID = "SHEET_ID"
const SHEET_NAME = "SHEET_NAME"

// Update angel mortal pairings sheet
function doPost(e) {
  const VERSION = 5 
  const params = e.parameters
  const username = params.username
  const chatId = params.chat_id

  const result = updateUserChatId(username, chatId)

  return ContentService
    .createTextOutput(JSON.stringify({
      result: result, version: VERSION
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

// Get angel mortal pairings sheet
function doGet(e) {
  const SpreadSheet = SpreadsheetApp.openById(SHEET_ID);
  const Sheet = SpreadSheet.getSheetByName(SHEET_NAME)
  const range = Sheet.getDataRange()
  if(!range) throw new Error('Invalid sheetname')

  const data = range.getValues()
  const transformedData = transformData({ data })

  return ContentService
    .createTextOutput(JSON.stringify(transformedData))
    .setMimeType(ContentService.MimeType.JSON);
}

const transformData = ({ data }) => {
  const sheetData = data
  const columns = sheetData[0] 
  const rows = sheetData.slice(1)
  let fromPair = []

  rows.reduce((accumulator, currentRow) => {
    let rowObject = {}
    for (let count = 0; count < currentRow.length; count++) {
      rowObject = {
        ...rowObject,
        [columns[count]]: currentRow[count]
      }
    }
    accumulator.push(rowObject)
    return accumulator
  }, fromPair)

  return fromPair
}

function updateUserChatId(username, chatId) {
  const SpreadSheet = SpreadsheetApp.openById(SHEET_ID);
  const Sheet = SpreadSheet.getSheetByName(SHEET_NAME)

  const sheetStartRow = 2;
  const sheetStartCol = 1;
  const sheetChatIdCol = 4;
  const lastRowWithContent = Sheet.getLastRow();
  const totalRows = lastRowWithContent - sheetStartRow;

  const sourceRange = Sheet.getRange(sheetStartRow, sheetStartCol, totalRows + 1);
  const sourceData = sourceRange.getValues();

  for (i in sourceData) {
    const currUsername = sourceData[i][0]
    const sheetRowIdx = Number(i) + Number(sheetStartRow)

    // Case sensitive checking of username
    if (currUsername == username) {
      Sheet.getRange(sheetRowIdx, sheetChatIdCol).setValue(chatId)
      return `User ${username} has its chat ID successfully updated with ${chatId}`
    }
  }

   return `Unable to find user ${username} in the Google Sheet for ${SHEET_NAME}`
}
```
