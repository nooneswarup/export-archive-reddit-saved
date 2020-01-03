# Export/Download/Archive Reddit
Many of us use Reddit and save a lot of content. But you should know that Reddit has a limit of 1000 for your saved content. After you pass this limit, you will lose your earliest saved posts.
So this project aims to download your Reddit saved posts, and also sort them by subreddits.

## Features
 * Download Reddit saved posts
 * View by categories (subreddits)
 * Running again will download newly saved posts

## How to:
For Video Guide `https://www.reddit.com/user/freeezer98/comments/ccn8dd/how_to_download_reddit_saved_posts_using_this/`

 * Download or clone repository
 * Install Python 3 and run `pip[3] install -r requirements.txt`
 * Add your Reddit credentials to `config.py`
   * To generate credentials:
     * Visit this url: https://www.reddit.com/prefs/apps/
     * Create a new app, name it, select "script"
     * Optionally add description and "about" url
     * Can use this as "redirect" url: `http://www.example.com/unused/redirect/uri`
     * Save the app, copy the public key under the app name and the secret key into `config.py`
   * User-agent can be something like "Saved posts scraper by /u/[your_username]"
   * Fill in your username and password
 * Run the file with `python[3] redditsave.py`
   * Optionally, run `redditsave.bat` if the above does not work
 * Check for folder named "Redditsaved" in Downloads
 * Browse using the landing page

### Known Issues:

 * Unsaving your most recent saved post will cause the re-sync functionality to break
 * If newly synced posts are from new subs, the new sub doesn't get added to the Filter (search/dropdown), but can be viewed by opening the HTML file
 * Comments will be added in the future due to API limitations
 * Saved comments will also be added, delayed due to styling issues


Please open an issue if you find any other issues or have enhancement suggestions.

The contributors of this project claim no responsibility for data losses in your reddit saved posts
