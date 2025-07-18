# Mars Exploration Web App

This interactive web application provides the latest insights and discoveries from NASA's Mars exploration missions. Built using Python, Flask, MongoDB, Beautiful Soup, and Bootstrap, this website dynamically scrapes and presents up-to-date Mars-related content, including news articles, stunning image galleries, facts about Mars, and live updates from the Curiosity Rover.

## Features

- **Latest Mars News**: Real-time updates of recent discoveries and announcements from NASA.
- **Interactive Image Gallery**: An automated slideshow of high-resolution Mars images with detailed descriptions. Images are clickable and link to full-sized versions.
- **Mars Facts Table**: A dynamically-generated HTML table providing key planetary metrics and interesting facts.
- **Curiosity Rover Updates**: Regular updates from the Mars Curiosity Rover blog, highlighting recent activities and findings.
- **Interactive Mars Hemisphere Viewer**: An embedded ArcGIS map providing detailed geographical exploration of Mars hemispheres.

## Technology Stack

- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Backend**: Python, Flask
- **Database**: MongoDB
- **Web Scraping**: Beautiful Soup, Requests, Selenium
- **Deployment**: Gunicorn

## How to Run Locally

1. Clone the repository.
2. Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

3. Run the Flask application:

```bash
python app.py
```

4. Access the web app locally at `http://localhost:5000`

## Future Improvements

- Adding user authentication for personalized experiences.
- Integrating real-time Mars weather data.
- Enhancing UI/UX with advanced frontend frameworks.

## Contributions

Feel free to fork, contribute enhancements, and submit pull requests!

