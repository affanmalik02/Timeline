# Timeline: A Simple Social Media

<https://timeline.aspear.cs.umd.edu/>

## Description

Timeline is a social media site where anyone can share updates about their life
Built using Python, Flask, MongoDB, and Timeline supports secure user authentication, 
profile customization, and more.

## Setup

To setup a local instance of Timeline follow these steps:
Setup of the API key for MongoDB and update config.py

**Make sure to set the secret key in 
`config.py`!!!**

Activate your virtual environment
Then, to install the necessary packages, run `pip install -r requirements.txt`.

To run this project, stay in the directory and use the `flask run`
command. The file that is run is `run.py`

All of the view functions are in `routes.py`. The
database models are in `models.py`, and the `Client` class
is now in `client.py`.

### routes.py

There are five new template files, corresponding to five
new view functions
in `routes.py`.

- `header.html`
- `account.html`
- `login.html`
- `register.html`
- `user_detail.html`
- `404.html`
- `index.html`
- `query.html`

Now we'll go into detail about each of the new view functions:

1. `account()`
2. `login()`
3. `register()`
4. `user_detail(username)`
5. `logout()`
6. `movie_detail()`
7. `custom_404()`

### Profile pics

### forms.py

1. `RegistrationForm`:
2. `LoginForm`:

3. `SearchForm`:
4. `MovieReviewForm`:
5. `LikePostForm`:
6. `DeletePostForm`:

7. `UpdateUsernameForm`:
8. `UpdateProfileForm`:
9. `UpdateProfilePicForm`:

### models.py

1. `User` - Should have these fields:
   - `username`: required and unique with minimum length 1 and maximum length 40 characters
   - `email`: required and unique 
   - `password`: required (only store slow-hashed passwords!)
   - `joined_date`
   - `profile_pic`: optional
     - `get_id()` returns a string unique to each user and `load_user(user_id)` fetches a `User` object using that unique string
   - `name`: optional
   - `bio`: optional
   - `location`: optional
2. `Review` - Should have these fields:
   - `commenter`: required reference to a `User`
   - `content`: required with minimum length 5 and maximum length 500 characters.
   - `date`: required (can be saved as a string instead of a datetime)
   - `image`
   - `likes`

### Lexicon and Future Plans

Creating a unique lexicon for "Timeline," can help establish a distinctive brand identity and enhance user engagement

Posts: could call individual posts "Moments". This term encapsulates the idea of capturing a specific point in time, which aligns well with the theme

User Profiles: Refer to user profiles as "Chronicles". This term suggests a detailed and continuous account, much like a personal history, which fits the concept of a timeline.

Like: Instead of "likes,"  could use "Echoes". This term can symbolize the reverberation or impact a post has on the community, similar to how sound echoes resonate.

Share: Instead of "share," use "Spread". This suggests the action of spreading a moment through the timelines of others.

Followers: Call them "Timekeepers". This term fits the temporal theme and gives a sense of people who keep track of others' timelines.

Messaging/DMs: Refer to these as "Telegrams". This harkens back to older forms of communication and gives a nostalgic touch to the action of sending direct messages.

Trending Topics: Call them "Eras". This term represents significant periods in history, aligning well with the idea of trending or notable events on the platform.

Groups/Communities: Refer to them as "Guilds". Historically, a guild was an association of craftsmen or merchants, which could parallel the idea of a group with common interests.

Polls/Surveys: Call them "Censuses". In keeping with the historical theme, a census is a systematic collection of data about a population.