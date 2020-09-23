# Overview

Welcome to my final project for [Harvard's CS50x](https://cs50.harvard.edu/x) course. This web application helps you create a password-protected portfolio and has two views: *Admin* view and *Recruiter* view. 

You can log in as an Admin and do the following:
* Review drafts pages
* Add and delete recruiter logins
* Change admin password
* View history log of recruiter page visits

Using the logins you've set up, recruiters can log in and view your portfolio pages except the ones in draft. 

Curious to see how this app works? Take a [brief tour](https://youtu.be/naw3iA2ykko)!

# Technologies
This project depends on the following technologies:
* Flask
* Python 3
* SQLite3
* Bootstrap 4.5
* HTML, CSS, and JavaScript

# Prerequisites

To use this application, you’ll need the following:
* Knowledge of HTML
* Basic understanding of CSS
* Basic command-line skills

# Getting started

Generally, you’d build your site in a local environment and deploy it when you’re ready. But we’ll work backwards in this tutorial for the benefit of users who might not have access to a local development environment.

## Step 1: Deploy the app to PythonAnywhere
1. Download [this project](https://github.com/deeptikorwar/portfoliobuilder/archive/master.zip) to your computer.
1. Sign up for a free [PythonAnywhere account](https://www.pythonanywhere.com/), if you don’t already have one.
1. Log in to PythonAnywhere and from the **Dashboard**, open a new **Bash** console.
1. Create a virtual environment by executing the below command:

    ```
    mkvirtualenv --python=/usr/bin/python3.6 my-virtualenv
    ```
  
1. After your environment is ready, install app dependencies by executing the below commands:

    ```
    pip install Flask
    pip install Flask-Session
    pip install sqlalchemy
    ```
    
    Don’t close this tab yet, we’ll come back to it soon.

1. Open a new tab and navigate to PythonAnywhere, and then click **Files** in the top-right corner.
1. Click **Upload a file** and upload the zip file you downloaded.
1. Switch to the Bash console and execute the following commands:

    ```
    unzip portfoliobuilder-master.zip
    rm portfoliobuilder-master.zip
    ```
    
1. Go back to the other PythonAnywhere tab and click **Web** in the top-right corner.
1. Click **Add a new web app** and then click **Next** in app builder wizard. Don’t worry about the domain name for now.
1. Select **Flask**, then select **Python 3.6**, and then click **Next**. We’ll configure the app name later.
1. Switch to the Bash console in PythonAnywhere and execute the below command. Don’t forget to replace *<your_account_name>* in the below code with your PythonAnywhere account name.

    ```
    cp -a /home/<your_account_name>/portfoliobuilder-master/. mysite
    rm -r /home/<your_account_name>/portfoliobuilder-master
    ```
    
1. Switch to the other PythonAnywhere tab, scroll down and open the WSGI configuration file.
1. Replace `flask_app` with `application` as shown below and click **Save**.

    ```
    # import flask app but need to call it "application" for WSGI to work
    from application import app as application  # noqa
    ```
1. Go back to the web app setup page and change the **Working directory** to `/home/<your_account_name>/mysite`.
1. In the **Virtualenv** section, enter the path of your virtual environment. It looks something like this `/home/<your_account_name>/.virtualenvs/my-virtualenv`.
1. Scroll to the top and click **Reload <your_site>**.
1. Click your site URL to view the app.

## Step 2: Modify admin password
Upon initial login, you’ll be prompted to change the admin password.
1. Log in to your site with the following credentials:

    **Username**: admin<br/>
    **Password**: admin
    
1. Set up a new password for the admin login. From now on, use this password to login as an admin. 

## Step 3: Personalise your site
Let's go ahead and personalise the site with your details. 
1. Click **Portfolio** to view the page that lists your published portfolio items and browse the available layout options.
1. Navigate to your PythonAnywhere dashboard.
1. Select **Files** > **mysite** > **templates** > **portfolio.html**.

    Delete tags between `<p class="font-weight-bold">Option #:</p> and </ul>` to remove the options you want to delete.<br/>
    If you decide to go with Option 2, note that the image file names in the static folder must match the file names in the `portfolio` folder, so that the template can pick the appropriate image.

1. Navigate to the **templates** directory and replace *John Doe* with your name in the following files:

    ```
    about.html
    layout.html
    ```
    
1. Navigate to the **templates** directory and add content in the following pages:

    ```
    index.html
    privacy.html
    ```

## Step 4: Start drafting pages
Let's start building some portfolio pages. If required, brush up [HTML](https://www.w3schools.com/html/) and [CSS](https://www.w3schools.com/css/) skills at this stage.
1. From your PythonAnywhere dashboard, select **Files** > **mysite** > **templates** > **drafts** > **sample1.html**.
1. Add content within the main block of `sample1.html`.

To preview your changes, log in to your site, select **Review drafts** > **sample1**.

## Step 5: Move drafts to portfolio
When you are happy with your draft, move them to the `portfolio` folder. 

If you're comfortable with the command line, you can physically move the file using a Bash console from your PythonAnywhere dashboard. Just remember to change the meta tags (front matter) at the beginning of the file (refer to one of the files within the `portfolio` folder).

Or, you can copy the relevant HTML tags from the draft into one of the files within the `templates/portfolio` folder.

## Step 6: Create logins for recruiters
When you’re ready with your shiny portfolio, you can share it with recruiters by creating a separate login for each recruiter. To do this, log in to your site, select **Manage logins** > **Add new login**.

# Housekeeping
As you have limited space in your free PythonAnywhere account, free up space by deleting unused portfolio pages, images, and recruiter logins. 

# Troubleshooting
If your draft page or page within the portfolio directory is not rendered properly, check the meta tags and ensure that you’ve not missed anything.

If you forget the admin password, reupload the `data.db` file from this repo to **Files** > **mysite** and log in with the initial admin logon credentials (admin, admin). 

To reorder the items within the portfolio page, prefix file names with a number. For example, **1page.html**, **2page.html**. If you are using the card layout in your Portfolio page, remember to use **1page.png** and **2page.png** for files within the images folder.

# Tips
Browse through the [Bootstrap documentation](https://getbootstrap.com/docs/4.5/getting-started/introduction/) and make use of the various prebuilt components offered by Bootstrap.

# Acknowledgements
With thanks to the following extensions and toolkits:
* [Flask-Session](https://flask-session.readthedocs.io/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Werkzeug](https://werkzeug.palletsprojects.com/)

[CS50x Finance](https://cs50.harvard.edu/x/2020/tracks/web/finance/) was used as a starting point for this project.

# Authors
Deepti Korwar
