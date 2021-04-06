# instagram_without_api

Install
To install instagram-scraper:

$ pip install instagram-scraper
To update instagram-scraper:

$ pip install instagram-scraper --upgrade
Alternatively, you can clone the project and run the following command to install: Make sure you cd into the instagram-scraper-master folder before performing the command below.

$ python setup.py install
Usage
To scrape a user's media:

$ instagram-scraper <username> -u <your username> -p <your password>             
NOTE: To scrape a private user's media you must be an approved follower.

By default, downloaded media will be placed in <current working directory>/<username>.

Providing username and password is optional, if not supplied the scraper runs as a guest. Note: In this case all private user's media will be unavailable. All user's stories and high resolution profile pictures will also be unavailable.

To scrape a hashtag for media:

$ instagram-scraper <hashtag without #> --tag          
It may be useful to specify the --maximum <#> argument to limit the total number of items to scrape when scraping by hashtag.

To specify multiple users, pass a delimited list of users:

$ instagram-scraper username1,username2,username3           
You can also supply a file containing a list of usernames:

$ instagram-scraper -f ig_users.txt           
# ig_users.txt

username1
username2
username3

# and so on...
The usernames may be separated by newlines, commas, semicolons, or whitespace.

You can also supply a file containing a list of location ids:

$ instagram-scraper --tag <your_tag_here> --include-location --filter_location_file my_locations.txt           
# my_locations.txt
[some_reagion1]
location_id1
location_id2

[some_region2]
location_id3
location_id4

# and so on...
The resulting directory structure will be:

your_tag
├── some_reagion1
│   └── images_here
└── some_reagion2
    └── images_here
The locations can only be separated by newlines and spaces.

OPTIONS
--help -h               Show help message and exit.

--login-user  -u        Instagram login user.

--login-pass  -p        Instagram login password.

--followings-input      Use profiles followed by login-user as input

--followings-output     Output profiles from --followings-input to file

--filename    -f        Path to a file containing a list of users to scrape.

--destination -d        Specify the download destination. By default, media will 
                        be downloaded to <current working directory>/<username>.

--retain-username -n    Creates a username subdirectory when the destination flag is
                        set.

--media-types -t        Specify media types to scrape. Enter as space separated values. 
                        Valid values are image, video, story (story-image & story-video), broadcast
                        or none. Stories require a --login-user and --login-pass to be defined.
                      
--latest                Scrape only new media since the last scrape. Uses the last modified
                        time of the latest media item in the destination directory to compare.

--latest-stamps         Specify a file to save the timestamps of latest media scraped by user.
                        This works similarly to `--latest` except the file specified by
                        `--latest-stamps` will store the last modified time instead of using 
                        timestamps of media items in the destination directory. 
                        This allows the destination directories to be emptied whilst 
                        still maintaining history.

--cookiejar             File in which to store cookies so that they can be reused between runs.

--quiet       -q        Be quiet while scraping.

--maximum     -m        Maximum number of items to scrape.

--media-metadata        Saves the media metadata associated with the user's posts to 
                        <destination>/<username>.json. Can be combined with --media-types none
                        to only fetch the metadata without downloading the media.

--include-location      Includes location metadata when saving media metadata. 
                        Implicitly includes --media-metadata.

--profile-metadata      Saves the user profile metadata to  <destination>/<username>.json.

--proxies               Enable use of proxies, add a valid JSON with http or/and https urls.
                        Example: '{"http": "http://<ip>:<port>", "https": "https://<ip>:<port>" }'

--comments             Saves the comment metadata associated with the posts to 
                       <destination>/<username>.json. Implicitly includes --media-metadata.
                    
--interactive -i       Enables interactive login challenge solving. Has 2 modes: SMS and Email

--retry-forever        Retry download attempts endlessly when errors are received

--tag                   Scrapes the specified hashtag for media.

--filter                Scrapes the specified hashtag within a user's media.

--filter_location       Filter scrape queries by command line location(s) ids

--filter_location_file  Provide location ids by file to filter queries 

--location              Scrapes the specified instagram location-id for media.

--search-location       Search for a location by name. Useful for determining the location-id of 
                        a specific place.
                    
--template -T           Customize and format each file's name.
                        Default: {urlname}
                        Options:
                        {username}: Scraped user
                        {shortcode}: Post shortcode (profile_pic and story are empty)
                        {urlname}: Original file name from url.
                        {mediatype}: The type of media being downloaded.
                        {datetime}: Date and time of upload. (Format: 20180101 01h01m01s)
                        {date}: Date of upload. (Format: 20180101)
                        {year}: Year of upload. (Format: 2018)
                        {month}: Month of upload. (Format: 01-12)
                        {day}: Day of upload. (Format: 01-31)
                        {h}: Hour of upload. (Format: 00-23h)
                        {m}: Minute of upload. (Format: 00-59m)
                        {s}: Second of upload. (Format: 00-59s)

                        If the template is invalid, it will revert to the default.
                        Does not work with --tag and --location.
Develop
Clone the repo and create a virtualenv

$ virtualenv venv
$ source venv/bin/activate
$ python setup.py develop
Running Tests
$ python setup.py test

# or just 

$ nosetests
Contributing
Check the open issues or open a new issue to start a discussion around your feature idea or the bug you found
Fork the repository, make your changes, and add yourself to AUTHORS.md
Send a pull request
