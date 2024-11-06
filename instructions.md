# MBTA Web App Project - Instructions

## Introduction

Welcome to the MBTA Web App project!

You may have used multiple Python libraries to access information on the Internet. For example, `praw` can get Reddit data by interacting with Reddit's application programming interface (API). In this project, you will access web APIs directly and begin to write your own program to connect with new data sources. Then you will build a simple website containing some webpages with a small amount of dynamic content using the `Flask` web framework. This website will help people find a nearby MBTA station and other information by providing an address or point of interest. As part of the project, you are encouraged to use AI tools to explore APIs and Python libraries that have not been covered in classes yet.

### Skills Emphasized

Throughout this project, you'll focus on developing the following skills:

- Connecting to web APIs
- Processing structured data (JSON)
- Web app development using Flask
- Experimenting with AI tools to enhance the learning process and explore new tools and techniques.

### Team Logistics:

- You may work independently or in a team of two.
- Each student (or one team member, if in a team) should **use this template repository to create a new public repository for the project, using the template's default name.**
- If in a team, add the other member as a collaborator. Both members should follow [GitHub collaboration best practices](https://github.com/firstcontributions/first-contributions/blob/main/gui-tool-tutorials/github-desktop-tutorial.md), such as using branches and pull requests for code review. This setup provides access to the code for all team members and supports effective collaboration.

---

## Part 1: Geocoding and Web APIs

The goal for Part 1 to deal with geographical data. You will write a tool that takes an address or place name and returns the closest MBTA stop and other information about that MBTA stop. For example:

```python
import mbta_helper

print(mbta_helper.find_stop_near("Boston Common"))
# Beacon St opp Walnut St
```

**Note**: It will be up to you to make this happen. If you feel confident in your ability and enjoy challenges, you can delete `mbta_helper.py` in the folder and implement it from scratch all by yourself! If you prefer more scaffolding, you can open and read code in `mbta_helper.py` as a starting point, while reading the following sections.

### 1. Accessing Web Data Programmatically

APIs allow you make requests using specifically constructed URLs and return data in a nicely structured format. There are the three main steps to using any web API:

1. **Read the API documentation:**

    You should check if the API can provide the data you need, how to request that data, and what the return format will be.

2. **Request an API developer key:**

    You will need to request a unique user key/access token to be sent with each request since web services generally limit the number of requests you can make. In order to get a key/token, you will need to agree to the API's terms, which restrict how you can use the service. If you are uncomfortable with any of the terms, please contact your professor.

    Make sure to keep your key/token secret! If someone else gets a hold of it, they can use it to make requests on your behalf, potentially using up your request limit or even getting you banned from the service. You should store your key in a separate file (e.g. `.env`) and add it to your `.gitignore` file to prevent it from being uploaded to GitHub.

3. **Test your application and launch to users:**

    The first API we will use is the [Mapbox](https://docs.mapbox.com/api/search/geocoding/), which allows you to specify a place name or address and receive its latitude and longitude. Take a few minutes to read the documentation (it's quite good). You need to sign up and get a free API Key [here](https://account.mapbox.com/).

### 2. Structured Data Responses (JSON)

Back? Ok cool, let's try it out in Python. We're going to request the response in JSON format, which we can decode using Python's [`json` module](https://docs.python.org/3/library/json.html).

```python
import json
import os
import pprint
import urllib.request

from dotenv import load_dotenv

load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"

query = "Babson College"
query = query.replace(" ", "%20") # In URL encoding, spaces are typically replaced with "%20". You can also use `urllib.parse.quote` function. 
url=f"{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&types=poi"
print(url) # Try this URL in your browser first

with urllib.request.urlopen(url) as resp:
    response_text = resp.read().decode("utf-8")
    response_data = json.loads(response_text)
    pprint.pprint(response_data)
```

We used the [`pprint` module](https://docs.python.org/3/library/pprint.html) to "pretty print" the response data structure with indentation, so it's easier to visualize. You should see something similar to the JSON response from the documentation, except built from Python data types. This response data structure is built from nested dictionaries and lists, and you can step through it to access the fields you want.

```python
print(response_data["features"][0]["properties"]["address"])
# 231 Forest St
```

**What you need to do**: Write a function (maybe two) to extract the **latitude and longitude** from the JSON response.

### 3. Building a URL (Optional)

In the above example we passed a hard-coded URL to the `urlopen` function, but in your code you will need to generate the parameters based on user input. Check out [*Understanding URLs*](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Web_mechanics/What_is_a_URL) and their structure for a helpful guide to URL components and encoding.

You can build up the URL string manually via using f-string and `str.replace` function as in the example above, but it's probably helpful to check out [`urlencode`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode) or [`parse`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote) from `urllib.parse` module.

**What you need to do**: Write a function that takes an address or place name as input and returns a properly encoded URL to make a Mapbox geocoding request.

### 4. Getting Local

Now that we can find the coordinates of a given place, let's take things one step further and find the closest public transportation station to that location.
<div style="text-align: center;">
<img src="https://www.vanshnookenraggen.com/_index/wp-content/uploads/2017/08/MTA_System.jpg" height="300" alt="old T map with illustrations of each station" />
</div>
<div style="text-align: center;">
Just a glimpse of history: MBTA stations in 50s
</div>

To accomplish this, we will use the [*MBTA-realtime API*](https://api-v3.mbta.com/docs/swagger/index.html). Check out the details for `GET /stops` in the documentation.

**Hints**: Prepare **valid** latitude and longitude coordinates of any Boston address for testing. Under `GET /stops` in the documentation,  click "Try it out" button. Enter/select the following parameters:

- `sort`: select "distance" (not "-distance") for ascending order.
- `filter[latitude]`: enter the testing latitude value.
- `filter[longitude]`: enter the testing longitude value.

Then click "Execute" button. You should be able to find a generated URL in Curl. Observe the generated URL and learn how to build that URL using variables. Don't forget to add `api_key={YOUR_MBTA_API_KEY}&` right after `?` in the URL. **Note**: You need to request an API key from [*MBTA V3 API Portal*](https://api-v3.mbta.com).

**What you need to do**: Create a function that takes a latitude and longitude and returns two values: the name of the closest MBTA stop, whether it is wheelchair accessible.

**Note**: Unfortunagely there are no MBTA stops close enough (approximately a half mile) to Babson College - you have to get out into the city!

### 5. To Wrap-up

Combine your functions from the previous sections to create a tool that takes a place name or address as input, finds its latitude/longitude, and returns the nearest MBTA stop and whether it is wheelchair accessible.

**Note**: Coordinate precision matters! Check out [xkcd 2170](https://xkcd.com/2170/) - *"What the Number of Digits in Your Coordinates Means"* and [explanation](https://www.explainxkcd.com/wiki/index.php/2170:_Coordinate_Precision).
<div style="text-align: center;">
  <img src="https://imgs.xkcd.com/comics/coordinate_precision_2x.png" height="400" alt="xkcd 2170" style="display: block; margin: 0 auto;">
</div>

### 6. Making It Cooler (Optional)

- Try out some other MBTA APIs - there are a lot of resources, and we have barely scratched the surface.
- By default, `stops` gives all types of transportation, including buses and commuter rail. Allow the user to specify how they'd like to travel (e.g. T only).
- Incorporate the MBTA realtime arrival data to suggest the optimal station to walk to.
- Connect with other local services. Example: the City of Boston has [an app](https://www.boston.gov/transportation/street-bump) that uses a phone's GPS and accelerometer to automatically report potholes to be fixed. You can also see many other apps developed for Boston residents [here](https://www.boston.gov/departments/innovation-and-technology/city-boston-apps).

---

## Part 2: Web App

The goal for Part 2 is to build a simple website that uses the `mbta_helper` module you created in Part 1.

To achieve this, we will use `Flask` - a lightweight and powerful web framework for Python that is easy to learn and simple to use, allowing you to build your web app quickly.

### 1. Get Started

You need to first install `Flask`. Run the following command:

```bash
> python -m pip install flask # on Windows
# or 
> python3 -m pip install flask # on macOS/Linux
```

### 2. Why Flask?

In the introduction, we defined `Flask` as a "web framework", but what does that actually mean? Let's dig deeper. Before this, let's develop a better understanding of how the internet works.

When you open up a web page in your browser (e.g. Chrome, Firefox, etc.), it makes an HTTP request to a server somewhere in the world. This could be something like GET me the home page. This server handles this request, sending back data (this can be in the form of HTML, JSON, etc.), which is rendered by your browser.

This is where Flask comes in - it enables you to create the logic to make a web server quickly in Python and process data in the backend. You can write logic that will execute when a request is made for one of your routes (e.g. <www.MyTicTok.com/**new**>).

### 3. Flask Quickstart

Read the following sections of [Flask Quickstart documentation](https://flask.palletsprojects.com/en/stable/quickstart/):

- A Minimal Application
- Debug Mode
- Routing
  - Variable Rules
  - Unique URLs / Redirection
  - Behavior
  - URL Building
  - HTTP Methods
- Static Files
- Rendering Templates
- Redirects and Errors

**Suggestion**: Follow every single step in this tutorial. Replicate all the code. Make the server run!

### 4. Building Your App and Getting Input from the User

What use is a web application if you can't get any data back from the user? Let's set up your own app and getting input from the user. Here are some end specifications:

1. Upon visiting the index page at `http://127.0.0.1:5000/`, the user will be greeted by a page that says hello, and includes an input **form** that requests a place name.
2. Upon clicking the 'Submit' button, the data from the form will be sent via a **POST** request to the Flask backend at the route `POST /nearest_mbta`
3. (Optional) Perform some simple validation on the user input. You can use [wtforms](https://flask.palletsprojects.com/en/3.0.x/patterns/wtforms/) to implement the validation.
4. The Flask backend will handle the request to `POST /nearest_mbta`. Then your app will render a `mbta_station.html` page for the user - presenting nearest MBTA stop and whether it is wheelchair accessible. In this step, you need to use/import the module you created for **Part 1**.
5. If something is wrong, the app will render a simple error page, which will include some indication that the search did not work, along with a button or link that redirects the user back to the home page.

It will be up to you to make this happen. If you feel confident in your ability to implement this, go for it! If you'd like more scaffolding, continue reading.

### 5. Tips and Tricks

To complete this project, the official [Flask documentation](https://flask.palletsprojects.com/en/stable/quickstart/#user-s-guide) will get you pretty far.

- **HTML Forms:**. To make forms in HTML, check out [MDN web docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form) and/or [*W3Schools*](https://www.w3schools.com/html/html_forms.asp). For even more information, check [*this*](https://letmegpt.com/?q=html%20forms) out.

- **Sending `POST` Requests:** To send the data from the form in a `POST` request, use an input with type `submit`, and set the action of the form to reflect the destination in your routes.

- **Handling POST Requests:** To learn more about handling post requests in Flask, read section [*HTTP Methods*](https://flask.palletsprojects.com/en/stable/quickstart/#http-methods) again.

- **Accessing the Form Data:** To access the form data, check out section [*'The Request Object'*](https://flask.palletsprojects.com/en/stable/quickstart/#the-request-object) on using the Flask `request` utility.

### 6. Going Further (Optional)

- **Want to keep track of some data in your web app?** Instead of using a `.txt` file or a `pickle` file, it's common practice in nearly any web app to use a **database**. A few especially well-known database choices are `MySQL`, `SQLite` (my go-to choice for a quick project/demo), or `PostgreSQL`, which all use **SQL** (Structured Query Language) to manipulate all stored data, as do many other common relational databases. Alternatively, you may use `MongoDb`, which stores data in an unstructured format similar to JSON. MongoDb is stupidly easy to set up and use, but I'd stop and think first before jumping right in. It may be the easy choice, but representing your data intelligently in a relational table can be much more effective and less of a headache later on.
  
- **But HTML is so ugly!** HTML alone may not look visually appealing, which is why we use CSS (Cascading Style Sheets) to add some extra flair and style to our HTML. You can change pretty much anything about HTML - colors, shapes, sizes, placement, etc. - with CSS rules. It's also pretty simple to write. Check out resources such as [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Learn/CSS/First_steps) and/or [W3Schools](https://www.w3schools.com/css/css_intro.asp) to learn more about CSS.
  
- **What about making my website more dynamic?** While this class may focus on Python, you can venture out a little and use [`Bootstrap`](https://getbootstrap.com/), [`Tailwind CSS`](https://tailwindcss.com/) or [`shadcn/ui`](https://ui.shadcn.com/) to add dynamic elements to your web app. They might sound scary, but you use it in a way similar to adding/linking CSS styling to your HTML. You can also write vanilla JavaScript (which isn't too difficult), which allows you to create more beautiful, responsive, and dynamic content for your web app.
  
- **Interested in an alternative to Flask?** Learn more about [Django](https://www.djangoproject.com/). They don't have many major differences other than some small quirks in conventions and style.

- **Ready to put your web app online?** Deploying your app to the internet is simpler than it sounds. You can host it  on cloud platforms like [PythonAnywhere](https://help.pythonanywhere.com/pages/Flask/) (free), [Render](https://render.com/docs/deploy-flask), [Railway](https://alphasec.io/how-to-deploy-a-python-flask-app-on-railway/), [Heroku](https://realpython.com/flask-by-example-part-1-project-setup/), etc. Check out the [Flask documentation on Deploying to Production](https://flask.palletsprojects.com/en/stable/deploying/) for more information.

---

## Part 3: *Wow!* Factors (20%)

After completing the required parts of this project, you can spice it up by adding additional features. Some suggestions:

- Refer to [6. Making it Cooler (Optional)](#6-making-it-cooler-optional) section in Part 1 and [6. Going Further (Optional)](#6-going-further-optional) section in Part 2 for more ideas.
- Display weather information - Add real-time weather data for an extra interactive touch! Note: While the weather might be similar across locations (since we're focusing on the Greater Boston area), this feature adds a layer of engagement.  Say "hello" to our old friend, [OpenWeatherMap API](https://openweathermap.org/api).
- Any interesting events in the nearby area? Try [Ticketmaster API](https://developer.ticketmaster.com/products-and-docs/apis/getting-started/) to find out concerts, sport events information.
- Yes, you guessed it! - More APIs. Some suggestions:
  - [public-apis/public-apis](https://github.com/public-apis/public-apis)
  - [n0shake/Public-APIs](https://github.com/n0shake/Public-APIs)
  - [Free Public APIs](https://www.freepublicapis.com/)
  - [RapidAPI - Discover More APIs](https://rapidapi.com/hub)
  - [ApiVault](https://apivault.dev/)
  - [APIs.guru](https://apis.guru/)
  - [PublicAPIs.io](https://publicapis.io/)
- Get Creative with AI - Stuck or looking for new ideas? Try using an AI tool for a quick brainstorming session! It can help you come up with fun feature ideas, suggest code snippets, or even troubleshoot API integrations. Think of it like having an extra teammate to bounce ideas off and make your project stand out.

---

## Project Wrap-Up

### 1. Getting Started

Use this template repository to create **a new public repository**, keeping the default name from the template. If working in a team, add the other member as a **collaborator** on GitHub and follow [GitHub collaboration best practices](https://github.com/firstcontributions/first-contributions/blob/main/gui-tool-tutorials/github-desktop-tutorial.md). Once the new repository is created, clone it (the version under your GitHub profile) to your computer.

### 2. Project Writeup and Reflection

Write a summary of your project and your reflections on it in [`README.md`](README.md), using [Markdown format](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) (1 per team, not 1 per person). The [`README.md`](README.md) file should include the following sections:

**1. Project Overview** (~1 paragraph)

Write a short abstract describing your project. Summarize the main objectives, key features, and any extensions or additional functionality implemented beyond the basic requirements.

**2. Reflection** (~3 paragraphs + screenshots)

After you finish the project, Please write a short document for reflection.

- Discuss the **development process** point of view, including what went well and what could be improved. Reflect on topics such as project scoping, testing, debugging, and any specific challenges encountered. What strategies helped the team succeed, and what adjustments might have made the project smoother?

- Discuss your **team's work division**, including how the work was planned to be divided and how it actually happened. Address any issues that arose while working together and how they were addressed. Finally, discuss what you would do differently next time.

- Discuss from a **learning** perspective, what you learned through this project and how you'll use what you learned going forward. Share your experience with AI tools - did they enhance your efficiency or understanding, and if so, how? What do you wish you had known beforehand that would have helped you succeed? Include screenshots showing key stages of development or specific challenges you overcame.

**Note**:

- Start by listing all team members' names at the top of the document.
- Make the `README.md` file clear and concise. There is no need to use fancy words or ChatGPT.

### 3. Turning in Project

1. Push your completed code and updated `README.md` to your GitHub repository (the repository where your team has been working on).
2. Submit the project's GitHub repository URL to Canvas. In the Canvas comment section, include the names of all team members. **Note: Each team member must submit on Canvas and add this comment.**

---
*updated:* *11/06/2024*
