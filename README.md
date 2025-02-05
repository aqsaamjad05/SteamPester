# steam comment bot

a Python script that automatically comments on a friend's Steam profile daily; this script uses Selenium for web automation and maintains a day count for tracking repeated comments.

## features

- logs into your Steam account automatically.
- navigates to a friend's Steam profile.
- posts a daily comment with an incrementing day count.

## prerequisites

make sure you have the following installed on your system:

- [Python 3.7+](https://www.python.org/downloads/)
- [Google Chrome](https://www.google.com/chrome/)
- [ChromeDriver](https://sites.google.com/chromium.org/driver/)

## installation

1. clone the repository:

   ```sh
   git clone https://github.com/yourusername/steam-comment-bot.git
   cd steam-comment-bot
   ```

2. create a virtual environment (optional but recommended):

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. create a `.env` file in the project directory and add your Steam credentials and target profile:

   ```ini
   STEAM_USERNAME="your_steam_username"
   STEAM_PASSWORD="your_steam_password"
   FRIEND_STEAM_PROFILE="https://steamcommunity.com/id/yourfriendsprofile"
   ```

5. run the script:

   ```sh
   python steam_comment_bot.py
   ```

## how it works

- the script logs into your Steam account using Selenium.
- it tracks the number of days a comment has been posted in `day_count.txt`.
- each time the script runs, it increments the day count and posts a comment like:

  ```
  day X of asking sirnyges to hop on val :steambored: - commentBot <3
  ```

- the comment section and post button are located using XPath and CSS selectors.

## notes

- the script **does not use cookies or session storage** to persist login between runs.
- Steam may require **Steam Guard authentication** (2FA) if enabled (it needs to be enabled in order to post comments)
- if Steam changes its login system or page structure, the script may need to be updated.

## troubleshooting

- **ChromeDriver version mismatch:** ensure your ChromeDriver matches your Chrome version.

  ```sh
  chrome://settings/help  # Check your Chrome version
  ```

  download the correct version from [here](https://sites.google.com/chromium.org/driver/).

- **element not found errors:** increase Selenium wait times or update XPaths if Steam UI changes.

## disclaimer

this script is for **educational purposes only**. Automating interactions on Steam may violate their terms of service. Use it responsibly at your own risk.
