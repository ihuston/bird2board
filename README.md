# bird2board
Convert bird based bookmarks to board based ones.

![Automated tests](https://github.com/ihuston/bird2board/actions/workflows/python-app.yml/badge.svg)

This tool takes raw [Twitter Bookmarks](https://twitter.com/i/bookmarks) data 
and pushes the bookmarks to [Pinboard](https://pinboard.in).

## Installation:
1. Clone this repository
2. Install with `pip`
```
#> cd bird2board
#> pip install .
```
## Usage:

First download the raw Twitter bookmarks data:

- Open the Twitter Bookmarks page
- Using Developer tools, look for Network requests starting with `Bookmarks?variables=`.
- For each of these requests, copy the response, which starts with `{"data":{`.
You can copy the response through the right click context menu.
- Save the response JSON into a new file.
- If you have more than a single screen of bookmarks, 
  scroll down to create more requests and responses. Copy these into new files in a directory.
  
Next find your Pinboard API token:

- Sign into [Pinboard](https://pinboard.in)
- Go to Settings page and select Password tab.
- Copy the API token including the username at the start.

Then use the tool to convert the bookmark data and save in Pinboard:
```
#> bird2board --help
Usage: bird2board [OPTIONS] PATH

  Save Twitter Bookmark .json file(s) at PATH (file or directory) to account
  using PINBOARD TOKEN.

Options:
  --toread / --not-toread    set Pinboard bookmarks as "to read"
  --shared / --not-shared    set Pinboard bookmarks as shared
  --replace / --no-replace   replace existing Pinboard bookmark for an URL
  -p, --pinboard-token TEXT  user token for Pinboard API  [required]
  --help                     Show this message and exit.
```
Example usage:
```
#> bird2board -p MY_TOKEN --toread ./responses/
```
Instead of providing the Pinboard API token as an option to the script, 
you can set the `$BIRD2BOARD_PINBOARD_TOKEN` environmental variable.
```
#> export BIRD2BOARD_PINBOARD_TOKEN=MY_TOKEN
#> bird2board --toread ./responses/
```

Notes: 

- The Pinboard API requires a 3 second wait between API requests, 
so submitting a large number of bookmarks can take a long time.
- The Twitter Bookmark responses captured above are from the non-public API, 
  and there will likely be breaking changes to the response structure in the future. 