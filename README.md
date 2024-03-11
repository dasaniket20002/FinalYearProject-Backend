
# Project Title

## Final Year Project - Backend

This is the frontend part of [Final Year Project - Frontend](https://github.com/dasaniket20002/FinalYearProject-Frontend)
## Tech Stack

 - [Mongoose](https://mongoosejs.com/)
 - [MongoDB](https://www.mongodb.com/)
 - [ExpressJS](https://expressjs.com/)
 - [Axios](https://axios-http.com/)
 - [NodeJS](https://nodejs.org/en)


## Project Structure

This project contains 2 Servers, 
 - One is an ExpressJS Server (`express-app`) that handles incomming requests for login, logout and other validation in MongoDB. This Server runs on `PORT=5000` ideally.
 - Second is a Python Server (`python-app`) that handles requests regarding fetching data from Youtube API, and also generates personalised content based on client taste. This Server runs on `PORT=5001` ideally.

 ## Environment Variables

You will need 2 `.env` files for the project. 
 - For `.env` file in ExpressJS (`express-app`)
    - `PORT` - the PORT this runs on, ie, 5000.
    - `MONGODB_CS` - the connnection string provided by MongoDB.
    - `JWT_SECRET` - the JWT Secret that you want to sign with.
    - `YT_API_KEY` - the API key from Google Cloud Console that will be used to fetch YouTube Videos from YouTube Data API

 - For `.env` file in Python Server (`python-app`)
    - `YT_API_KEY` - the API key from Google Cloud Console that will be used to fetch YouTube Videos from YouTube Data API
    - `API_VERSION` - the API version from YouTube, i.e., `v3`
    - `API_NAME` - the name of the API to use, i.e., `youtube`
    - `MAX_YT_SEARCH_RESULTS` - the maximum number of serach results returned by the API
## Run Locally

Configure the project with npm and git.
Before that remember to add the `.env` files.

First clone the repository with

```bash
git clone https://github.com/dasaniket20002/FinalYearProject-Backend.git
```

Then open 2 terminals to run 2 Backend Servers, i.e, the Express Server (`express-app`) and the Python Server (`python-app`).

In first terminal
```bash
cd express-app
npm i
npm start
```

In second terminal
```bash
cd python-app
pip install --upgrade google-api-python-client numpy pandas googleapiclient scikit-learn nltk
python3 app.py
```
## API Reference

#### Validate name's existance

```http
  POST /validation/name
```

| Payload | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `value` | `string` | **Required**. the name to check for existance |

#### Validate username's existance

```http
  POST /validation/email
```

| Payload | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `value` | `string` | **Required**. the email to check for existance |

#### Validate password's credebility

```http
  POST /validation/password
```

| Payload | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `value` | `string` | **Required**. the password to check for credebility |


#### Register new User from default SignUp

```http
  POST /users/register
```

| Payload | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. name of user |
| `email` | `string` | **Required**. email ID of user |
| `password` | `string` | **Required**. password of user |


#### Register new User from Google SignUp

```http
  POST /users/registerwp
```

| Payload | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. name of user |
| `email` | `string` | **Required**. email ID of user |


#### Login User from default SignIn

```http
  POST /users/login
```

| Payload | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Optional**. name of user |
| `email` | `string` | **Optional**. email ID of user |
| `password` | `string` | **Required**. password of user |


#### Login User from Google SignIn

```http
  POST /users/loginwp
```

| Payload | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Optional**. name of user |
| `email` | `string` | **Optional**. email ID of user |


#### Get Trending Videos

```http
  GET /youtube/trending
```

| Params | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `regionCode` | `string` | **Optional**. the Region Code for the user |
| `maxResults` | `string` | **Optional**. the number of videos returned by the API |
| `accessToken` | `string` | **Optional**. the Access Token from OAuth2.0 Authorization |
