# Online Book Reader

Online Book Reader is a website that allows users to save books, read them and record their progress through 
them without downloading any files. It uses only web-hosted plain text files so no epub files need to be downloaded.

![Responsive Mockup](/readme_assets/responsive.webp)

# Agile Methodology

## Summary of Methodology

An agile methodology was used to develop this project, using elements of SCRUM agile. GitHub Projects was used as the
digital platform for this agile methodology:<br>
<a href="https://github.com/users/harrypmdev/projects/6" target="_blank">Online Book Reader GitHub Agile Project</a>.

## Specifics of Methodology

During the development of this project:

- Overarching themes were identified, then broken down into epics, then user stories.
- User stories were added to a prioritised backlog, and MoSCoW prioritisation labels were added to each user story.
Story points were assigned to each user story based on their expected effort relative to other user stories.
- Completion criteria were written for each user story with the user's perspective kept central.
- A series of short iterations/sprints were utilised. A kanban board recorded the progress of each iteration, moving
user stories from 'To Do', to 'In Progress' and then to 'Done'.
- During the 'In Progress' stage for a user story, it was broken down into technical level tasks that needed to be
completed. These are viewable by clicking on the completed user stories.
- After each iteration, MoSCoW prioritisations and the backlog were re-evaluated.

<details>
<summary> Final Spreedsheet Breakdown of Themes, Epics and User Stories </summary>

![Nav Bar Mobile](/readme_assets/agile_excel.webp)

</details> 
<br>

# Flowchart

# Rationale for Chosen Libraries

- The **Django framework** and its **relevant libraries** were chosen for their familiarity to myself as a developer and its
functionality for rapidly developing dynamic websites with user authorisation and intuitive data modelling through the
Django ORM.
- **Gunicorn** was chosen for booting the site in production for its stability and efficiency.
- Python **Ruff linter** was chosen for its easy installation via pip, its speed, automatic formatting and
comprehensive functionality.
- **Whitenoise** was chosen for simple serving of static files in production.
- **Bootstrap** (CSS and JS) was chosen for its general-purpose CSS classes and modals which allows ultra-fast styling
of HTML in a manner that is intuitive and familiar for users.
- **Boostrap Crispy** was chosen for its ability to present simple forms without unnecessary custom HTML and CSS.

# Features

### Navbar

- The navbar allows for easy navigation of the site's features in line with standard web design practices
that users expect and can use intuitively.
- The navbar shows different options depending on whether the user is authenticated or not, reflecting
the different features avaiable to authenticated and unauthenticated users.
- The navbar always informs the user if they are logged in, so they do not lose track of what is happening
on the site or accidentally use another person's account.

<br>

<details>
<summary> Navbar (Not logged in) (Desktop) Screenshot </summary>

![Navbar (Not Logged In) Desktop](/readme_assets/navbar_desktop_unlogged.png)

</details> 

<details>
<summary> Navbar (Not logged in) (Mobile) Screenshot </summary>

![Navbar (Not Logged In) Mobile](/readme_assets/navbar_mobile_unlogged.png)

</details> 

<details>
<summary> Navbar (Logged in) (Desktop) Screenshot </summary>

![Navbar (Logged In) Desktop](/readme_assets/navbar_desktop_logged.png)

</details> 

<details>
<summary> Navbar (Logged in) (Mobile) Screenshot </summary>

![Navbar (Logged In) Mobile ](/readme_assets/navbar_mobile_logged.png)

</details> 
<br>

### Footer

- The footer aids UX by providing thematic consistency across the site's pages, with all pages utilising
the header and footer and the header and footing using the same bootstrap styles.
- The site's developer is credited on the footer. This avoids the footer looking empty or confusing to a user,
and allows them to recognise it as a footer. It also allows the developer to be credited without a separate
page to do so.
- Freepik is credited on the footer. This is as per their 
<a href="https://support.freepik.com/s/article/Attribution-How-when-and-where?language=en_US&_gl=1*ufl9o0*_gcl_au*MTg1NDE3NTA1NS4xNzM1NDkxODI3*_ga*NTMxMzQ4NTgyLjE3MzU0OTE4Mjc.*_ga_QWX66025LC*MTczNTQ5MTgyNy4xLjEuMTczNTQ5MTg1MC4zNy4wLjA.">attribution requirements.</a>

<br>
<details>
<summary> Footer Screenshot </summary>

![Footer](/readme_assets/footer.png)

</details> 
<br>

### Home Page

- The home page provides a simple and welcoming landing page for new users. Returning authenticated users are
redirected to the dashboard, where they can immediately access their books.
- Two 'call to action' buttons are presented - 'Get Started' and 'About Us'. These invites users who already know
about the site and want to register to do so right away, and users who need more information to easily access it.
- Only a title, single image and two buttons are shown as to not overwhelm the user with information and keep a
modern, minimalist design that reflects good UX practices.

<br>

<details>
<summary> Home Page (Desktop) Screenshot </summary>

![Home Page Desktop](/readme_assets/home_desktop.png)

</details> 

<details>
<summary> Home Page (Mobile) Screenshot </summary>

![Home Page Mobile](/readme_assets/home_mobile.png)

</details> 
<br>

### Dashboard

- The dashboard allows an authenticated user to easily access all their books and add new books.
- The dashboard presents all the user's books so they can see what they are currently reading.
- Most recently read books are listed first, so the user can easily return to their most recent book.
- Books' borders and progress bars are randomly coloured from a handful of pre-determined colours
to add visual variance and character. These colours do not change once a book has been added, 
so viewers do not get confused and the 'character' of the book remains consistent.
- All books on the dashboard have both a progress bar and percentage, so the user can easily view how
far through the book they are. The progress bar animates upon hovering over the book, aiding UX by
indicated the book is clickable and providing fun interactivity and feedback.

<br>

<details>
<summary> Dashboard Page (Desktop) Screenshot </summary>

![Dashboard Page Desktop](/readme_assets/dashboard_desktop.png)

</details> 

<details>
<summary> Dashboard Page (Mobile) Screenshot </summary>

![Dashboard Page Mobile](/readme_assets/dashboard_mobile.png)

</details> 
<br>

### About Us

- The about us page provides the user with basic information about the site, and gives legal and ethical
disclaimers relating to issues like book copyrights and adult content in books.
- The site is always accessible on the navbar, allowing new or returning users to immediately understand
the site's purpose and basic functionality.
- A quote from author C.S Lewis is included to aid the page aesthetically for better UX and to encourage the
reader to use the site for reading.

<br>

<details>
<summary> About Us Page (Desktop) Screenshot </summary>

![About Us Page Desktop](/readme_assets/about_us_desktop.png)

</details> 

<details>
<summary> About Us Page (Mobile) Screenshot </summary>

![About Us Page Mobile](/readme_assets/about_us_mobile.png)

</details> 
<br>

### User Authentication

- The site's user authentication features facilitate the site's key unique features. Users need to be able
to register and log in to save books and their progress through them.
- The navbar when unauthenticated presents the options to 'Log In' and 'Register'. The home page also has a call to
action button that links to the registration page. This is good UX as it encourages new users to register, whilst
returning users are likely logged in already, or at least are less likely to leave the site than a new user as they
have come to the site with deliberate purpose.
- The navbar when authenticated provides 'Profile' and 'Logout' options, so redundant choices are not available to
the user dependant on their state of authentication.
- The register page provides guidance on what passwords are likely to be valid, so users are not confused as to why
their passwords are appearing as invalid.

<br>

<details>
<summary> Log In Page (Desktop) Screenshot </summary>

![Log In Page Desktop](/readme_assets/log_in_desktop.png)

</details> 

<details>
<summary> Log In Page (Mobile) Screenshot </summary>

![Log In Page Mobile](/readme_assets/log_in_mobile.png)

</details> 
<br>
<details>
<summary> Register Page (Desktop) Screenshot </summary>

![Register Page Desktop](/readme_assets/register_desktop.png)

</details> 

<details>
<summary> Register Page (Mobile) Screenshot </summary>

![Register Page Mobile](/readme_assets/register_mobile.png)

</details> 
<br>

### Profile Information

- The view profile information feature allows the viewer to see their basic profile information at any
time by going to the 'profile' page, accessible from the navbar whenever authenticated.
- This allows the user to see their total books to keep track of their reading, and their email so they
know what data the site is storing about them.

<br>

<details>
<summary> Profile Information Screenshot </summary>

![Profile Information Desktop/Mobile](/readme_assets/profile.png)

</details> 
<br>

### Delete Profile

- The delete profile feature allows the user to delete their profile at any time.
- Users have a right to erase information the site is storing about them. They may decide, for example,
they no longer wish the site to have access to their email after observing what email the site has for them
with the profile information feature.
- A modal popup checks with the user that they definitely want to delete their account, to protect against
accidental clicks/taps and warn users about the repercussions of deleting an account.

<br>

<details>
<summary> Delete Profile Screenshot </summary>

![Delete Profile](/readme_assets/delete_profile.png)

</details> 
<br>

### Add Book

- The add book feature allows users to easily add books to their dashboard.
- If a book is already on a user's dashboard, the same book will be retrieved as not
duplicate information, and to allow users to accurately view ratings for books.
- The 'add book' button is always the first option on the dashboard, so that a user
is always invited to easily add another book.
- The 'add book' button links to an add book page. This page has information about how
exactly to add a book, explained step-by-step so nobody is confused.
- The add book page then has a URL submit form which validates the given URL to ensure
it is both a valid URL and a text file.

<br>

<details>
<summary> Add Book Button (Desktop) Screenshot </summary>

![Add Book Button Desktop](/readme_assets/add_book_button_desktop.png)

</details> 

<details>
<summary> Add Book Button (Mobile) Screenshot </summary>

![Add Book Button Mobile](/readme_assets/add_book_button_mobile.png)

</details> 
<br>
<details>
<summary> Add Book Page (Desktop) Screenshot </summary>

![Add Book Page Desktop](/readme_assets/add_book_page_desktop.png)

</details> 

<details>
<summary> Add Book Page (Mobile) Screenshot </summary>

![Add Book Page Mobile](/readme_assets/add_book_page_mobile.png)

</details> 
<br>

### Manage Book Title and Author

- The manage book feature allows users to update the title and author of their book at any time.
- The title and auto fields auto fill with an automatically generated title and author when possible,
but the user may wish to edit this and the site may not be able to generate a title and author for
all books.

<br>

<details>
<summary> Manage Book Screenshot </summary>

![Manage Book](/readme_assets/manage_book.png)

</details> 
<br>

### Ratings

- The ratings feature allows users to rate books out of 5 stars and view an average of other users'
ratings.
- The choice of a 5 star rating system allows users to untuitively understand ratings on the site and 
make ratings themselves without having the rating system explained to them.
- Ratings are viewable and editable on the manage book page. Since this page is redirected to immediately
after a book is added, this allows users to immediately see the average rating a book has if it has already
been added.
- The total number of ratings is shown so the user can see how reliable the rating is likely to be.
- The rating does not save until the user clicks the 'submit' button, allowing them a chance to review their
rating.
- The user can change their rating at any time, but the cursor hover state stops appearing and the stars appear
coloured once the user has given a rating once, so is obvious to the user they have previously rated the book without
needing to explicitly tell them this.

<br>

<details>
<summary> Ratings (No Rating Given, Showing Average) Screenshot </summary>

![Ratings (No Rating Given)](/readme_assets/ratings_not_rated.png)

</details> 
<br>
<details>
<summary> Rating Just Given (Showing User Rating) Screenshot </summary>

![Ratings (Rating Just Given)](/readme_assets/ratings_rated.png)

</details> 

### Delete Book

- The delete book feature allows a user to delete a book at any time.
- This allows them to prevent their dashboard from becoming clogged once they
finish a book.
- A modal popup confirms the user's intent to prevent accidents or unintended repercussions.

<br>

<details>
<summary> Delete Book Screenshot </summary>

![Delete Book](/readme_assets/delete_book.png)

</details> 
<br>

### Reader

- The reader feature allows a user to read a book they have added to the dashboard.
- The reader has 'previous' and 'next' buttons so the user can navigate the book's pages.
- A bookmark button allows the user to save their progress at any time.
- A loading spinner shows the user when the page is loading, usually right when they first
load their book or immediately after resizing their page. This shows the user through visual language
they will be familar with that the page is functioning correctly and the page will be available shortly.
- The 'next', 'previous' and 'bookmark' buttons are disabled and dimmed when the page is loading
to prevent erroneous input and convey to the user that the buttons cannot be used at these times.

<br>

<details>
<summary> Read Page (Desktop) (Page Bookmarked) Screenshot </summary>

![Read Page Desktop](/readme_assets/read_desktop.png)

</details> 

<details>
<summary> Read Page (Mobile) (Page Not Bookmarked) Screenshot </summary>

![Read Page Mobile](/readme_assets/read_mobile.png)

</details> 
<br>

### Messages

- The messages feature allows information to be conveyed to the user in an easy and intuitive manner.
- Messages appear at the top of the page to confirm successful input/action, while error messages appear
to provide the user with guidance if something goes wrong so invalid input or any potential server errors
are handled gracefully.

<br>

<details>
<summary> Success Message Screenshot </summary>

![Success Message](/readme_assets/message_logged_in.png)

</details>

<details>
<summary> Error Message Screenshot </summary>

![Error Message](/readme_assets/message_not_reading_book.png)

</details> 

<details>
<summary> Neutral Advisory Information Screenshot </summary>

![Neutral Advisory Information](/readme_assets/message_neutral.png)

</details> 
<br>

# Features Yet To Be Implemented

Though Online Book Reader is a completed site, several features could be implemented in the future to improve
the site's functionality.

- **User Comments** -- allowing users to comment would allow them to share their opinions on books in more detail
than the rating system, and foster a sense of community on the website.
- **Page of Contents** -- an automatically generate page of contents would make books easier to navigate and if new
chapters were also put on a new page, books would be displayed on screen even more similarly to real life books.
- **Jump to Page** -- a feature allowing users to jump to any page in a book could be helpful if the user is reading
the book on paper alongside the website, or wishes to jump to a specific section of the book.
<br><br>

# Data Modelling & Schema

A relational database (PostgreSQL) was used to store the relevant data for this project.
The most obvious entity that needed to be created was a 'Book' entity for each book. However,
the user's progress through a book and their custom title and author needed to be stored. Also,
the 'Book' entity and the Django 'User' entity have a many-to-many relationship, as a user can have many books
and a book can be read by many users.
<br><br>
Though Django has built in many-to-many functionality and can handle junction tables behind the scenes,
this was not ideal for this project due to the need to store progress, titles and authors for every user
and directly manipulate the junction table at many points throughout the project. As such, a custom junction
table was designed and implemented.
<br><br>
'Rating' and 'Comment' entities were also planned for the rating and comment features. The comment feature
was relegated to "won't have" prioritisation for this project time frame, meaning it was not implemented and
an entity for comments was never created. An entity for ratings was created when the ratings feature
was implemnted however. A UML table describing the resulting schema is below. <br>

<details>
<summary> UML Table Database Schema </summary>

![Nav Bar Mobile](/readme_assets/schema.webp)

</details>
<br>
These entities are implemented through django ORM in `books/models.py`.
<br><br>

# Validators

- All Python files checked with <a href="https://docs.astral.sh/ruff/" target="_blank">Ruff linter</a>,
with the only errors identified being unused imports which are simply parts of Django's framework structure.
- All JavaScript files checked with <a href="https://jshint.com/" target="_blank">JSHint</a>, no issues.
- Project's single custom CSS file (static/css/style.css) checked with 
<a href="https://jigsaw.w3.org/css-validator/validator" target="_blank">W3C CSS validator</a>, no issues.
- All of project's HTML files checked with
<a href="https://validator.w3.org/nu/#textarea" target="_blank">W3C HTML validator</a>, by taking final HTML
code produced by server and inputting to validator as Django Templating code itself cannot be validated.
No issues except minor issues produced by crispy forms on registration page.
<br><br>

# Testing

## Lighthouse Testing

### Home Page

![home.html Lighthouse Scores](/readme_assets/home_lighthouse.png)

- #### Performance - 82
    - Lighthouse rates good but not perfect for performance. This is largely because for best UX, two different
    images may be shown - one by default on smaller screens, and another if the screen hits a certain breakpoint.
    To make performance perfect, a solution could be devised so that only one image loads at all. For the project
    scope, a good if imperfect score was considered sufficient.

- #### Accessibility - 100
    - Lighthouse rates the page perfect for accessibility. This is bolstered by a custom CSS overwriting of
    bootstrap's "primary" colour to a slightly darker blue that is better for accessibility according to Lighthouse
    and <a href="https://webaim.org/resources/contrastchecker/" target="_blank">WebAim.org</a>.

- #### Best practices - 100
    - Lighthouse rates the page perfect for best practices.

- #### SEO - 100
    - Lighthouse rates the page perfect for SEO.

### About Us Page

![about_us.html Lighthouse Scores](/readme_assets/about_us_lighthouse.png)

- #### Performance - 96
    - Lighthouse rates very good but imperfect for performance. Efforts were taken to reduce the
    burden of the image on performance. The changes, such as defining set HTML dimensions and reducing
    the resolution, helped improve score. Even more specific configuration of the image could help improve
    the score further in future.

- #### Accessibility - 100
    - Lighthouse rates the page perfect for accessibility. This is bolstered by the use of always-underlined
    links, which allow users with difficulty perceiving colour to identify the links by another characteristic. 

- #### Best practices - 100
    - Lighthouse rates the page perfect for best practices.

- #### SEO - 100
    - Lighthouse rates the page perfect for SEO.

### Dashboard Page

![dashboard.html Lighthouse Scores](/readme_assets/dashboard_lighthouse.png)

- #### Performance - 94
    - Lighthouse rates very good but imperfect for performance.

- #### Accessibility - 100
    - Lighthouse rates the page perfect for accessibility. 

- #### Best practices - 100
    - Lighthouse rates the page perfect for best practices.

- #### SEO - 100
    - Lighthouse rates the page perfect for SEO.

### Add Book Page

![add_book.html Lighthouse Scores](/readme_assets/add_book_lighthouse.png)

- #### Performance - 96
    - Lighthouse rates very good but imperfect for performance. Similarly to other pages,
    even more specific image configuration could perhaps improve this even further.

- #### Accessibility - 100
    - Lighthouse rates the page perfect for accessibility. 

- #### Best practices - 100
    - Lighthouse rates the page perfect for best practices.

- #### SEO - 100
    - Lighthouse rates the page perfect for SEO.

### Manage Book Page

![manage_book.html Lighthouse Scores](/readme_assets/manage_book_lighthouse.png)

- #### Performance - 97
    - Lighthouse rates almost perfect for performance.

- #### Accessibility - 100
    - Lighthouse rates the page perfect for accessibility. 

- #### Best practices - 100
    - Lighthouse rates the page perfect for best practices.

- #### SEO - 100
    - Lighthouse rates the page perfect for SEO.

### Login Page

![login.html Lighthouse Scores](/readme_assets/login_lighthouse.png)

- #### Performance - 94
    - Lighthouse rates very good but imperfect for performance.

- #### Accessibility - 100
    - Lighthouse rates the page perfect for accessibility. 

- #### Best practices - 100
    - Lighthouse rates the page perfect for best practices.

- #### SEO - 100
    - Lighthouse rates the page perfect for SEO.

### Profile Page

![profile.html Lighthouse Scores](/readme_assets/profile_lighthouse.png)

- #### Performance - 95
    - Lighthouse rates very good but imperfect for performance.

- #### Accessibility - 100
    - Lighthouse rates the page perfect for accessibility. 

- #### Best practices - 100
    - Lighthouse rates the page perfect for best practices.

- #### SEO - 100
    - Lighthouse rates the page perfect for SEO.

### Register Page

![register.html Lighthouse Scores](/readme_assets/register_lighthouse.png)

- #### Performance - 95
    - Lighthouse rates very good but imperfect for performance.

- #### Accessibility - 100
    - Lighthouse rates the page perfect for accessibility. 

- #### Best practices - 100
    - Lighthouse rates the page perfect for best practices.

- #### SEO - 100
    - Lighthouse rates the page perfect for SEO.

### Read Page

![register.html Lighthouse Scores](/readme_assets/read_lighthouse.png)

- #### Performance - 81
    - Lighthouse rates good but flawed for performance. This is impacted by the wait time for the
    book to load, which is often several seconds. Though this results in an immediate wait of a few
    seconds, performing the pagination on the client-side allows the user to navigate the book's pages
    with no loading time whatsoever, which Lighthouse is not measuring. Client-side pagination is also
    important to the site's methods for fitting text to the screen size. One could look into solutions to
    this initial wait time in the future however as it could be frustrating for a new user.

- #### Accessibility - 100
    - Lighthouse rates the page perfect for accessibility. 

- #### Best practices - 100
    - Lighthouse rates the page perfect for best practices.

- #### SEO - 100
    - Lighthouse rates the page perfect for SEO.

## Error Pages

Attempts to access a page that does not exist redirect to a custom 404 error page.

<details>
<summary> 404 Page (Desktop) </summary>

![404 Page Desktop](/readme_assets/404_desktop.png)

</details> 
<br>
<details>
<summary> 404 Page (Desktop) </summary>

![404 Page Mobile](/readme_assets/404_mobile.png)

</details> 
<br>
Very similar pages exist for 500 errors and 403_csrf errors also.

## Manual Testing

## Automated Testing

# Bugs

# Deployment

The production version of this site was deployed to Heroku at https://online-book-reader-80387a283ed2.herokuapp.com/ where it is live.
The development of the project was version controlled using Git and GitHub, and the project was uploaded to Heroku from GitHub directly.
<br><br>
Deployment of this site can be achieved via the following steps:
<br>
<ol>
    <li>Fork the Online Book Reader repository on GitHub.</li>
    <li>Sign up or log in to  <a target="_blank" href="https://www.heroku.com">Heroku</a>.</li>
    <li>Create a new app.</li>
    <li>Add two environment variables to 'config vars' in settings - <code>SECRET_KEY</code>, a unique string of characters
    for Django security, and <code>DATABASE_URL</code>, the url for your database.</li>
    <li>Add the Python buildpack - <code>runtime.txt</code> instructs usage of python 3.12 for this site.</li>
    <li>Connect the Heroku app to your forked GitHub repo in the deploy section.</li>
</ol>
Running the site locally can be achieved via the following steps:
<br><br>
<ol>
    <li>Clone the Online Book Reader repository to a local repository. This can be done by executing the line 
    <code>git clone https://github.com/harrypmdev/online-book-reader.git</code> in a bash terminal.</li>
    <li>Create an <code>env.py</code> file for environment variables in the project root directory.</li>
    <li>In this file, set environment variables for <code>SECRET_KEY</code>, a unique string of characters for Django security,
    and <code>DATABASE_URL</code>, the url for your database.</li>
    <li>Update <code>CSRF_TRUSTED_ORIGINS</code> and <code>ALLOWED_HOSTS</code> in <code>online_book_reader/settings.py</code> to 
    include your local host.</li>
    <li>Install project dependencies listed in <code>requirements.txt</code>. This can be done with the bash line
    <code>pip3 install -r requirements.txt</code> with your bash working directory being the project root directory.</li>
    <li>Run the server with <code>python3 manage.py runserver</code> with your bash working directory being the project root
    directory.</li>
</ol>
<br>

# Credits & References

### Code, Dependencies and Tools

+ Site built on the <a href="https://www.djangoproject.com/">Django framework</a> supported by the 
<a href="https://www.djangoproject.com/foundation/">Django Software Foundation</a>.
+ <a href="https://balsamiq.com/wireframes/desktop/">Balsamic</a> software used for wireframing.
+ <a href="https://www.lucidchart.com/pages/">Lucidchart</a> used for creation of entity relationship diagram.
+ Google fonts from Google are imported in <code>templates/base.html</code>.<br>
Lighthouse web page quality checker also provided by Google.<br>
Google sheets used for Agile breakdown spreadsheet showing evolution from themes to tasks.
+ Web accessibility evaluation provided by <a target="_blank" href="https://wave.webaim.org/">WAVE</a> for help in improving accessibility.
+ Colour contrast accessibility checker provided by <a href="https://webaim.org/resources/contrastchecker/">WebAIM</a>.
+ HTML and CSS validation provided by <a target="_blank" href="https://validator.w3.org/">W3</a>.
+ JavaScript validation provided by <a target="_blank" href="https://jshint.com/">JS Hint</a>.
+ <a href="https://docs.astral.sh/ruff/">Ruff linter</a> used for python linting.
+ Gunicorn WSGI HTTP server created by Benoit Chesneau and supported by 
<a href="https://github.com/benoitc/gunicorn/blob/master/MAINTAINERS">Gunicorn maintainers.</a>
+ <a href="https://whitenoise.readthedocs.io/en/stable/django.html">Whitenoise</a> used for serving of static files.
+ <a href="https://getbootstrap.com/">Bootstrap</a> front-end framework used for template styling, including use of 
<a href="https://django-crispy-forms.readthedocs.io/en/latest/">Bootstrap Crispy Forms</a> for fast form rendering and styling.
+ Restriction on creating multiple user profiles with the same email enforced by means of the <code>clean_email</code>
method of <code>RegisterForm</code> in <code>account/forms.py</code>. Method originally written by 
<a href="https://stackoverflow.com/users/98187/trey-hunner">Trey Hunner</a> on a <a href="https://stackoverflow.com/questions/52639834/how-to-make-django-form-field-unique">stackoverflow answer</a>.
+ Django template filter <code>truncatesmart</code> registered in <code>books/templatetags/truncate_smart.py</code> originally
written by <a href="https://djangosnippets.org/users/rix/">'rix'</a> on djangosnippets.org - https://djangosnippets.org/snippets/1259/.

### Media

+ Favicon (<code>static/images/favicon.ico</code>)and site icons from <a href="https://fontawesome.com/v4/license/">Font Awesome by Dave Gandy</a>.
+ All site images provided by Freepik under free license. This includes all images (except the favicon) in <code>static/images/</code>:
    + <a href="https://www.freepik.com/free-photo/book-shelf-with-bookmark_34241132.htm#fromView=keyword&page=1&position=2&uuid=f98b8262-080a-4c19-b4f5-2baf32bfdcfe&new_detail=true"><code>static/images/chosen_book.webp</code></a>.
    + <a href="https://www.freepik.com/free-photo/creative-assortment-world-book-day_12892710.htm"><code>static/images/home_books.webp</code></a>.
    + <a href="https://www.freepik.com/free-photo/front-view-education-day-concept_11380044.htm#fromView=keyword&page=1&position=1&uuid=b15fe853-0359-4f68-83e1-6c7ca4245a10&new_detail=true"><code>static/images/open_book.webp</code></a>.
    + <a href="https://www.freepik.com/free-photo/front-view-stacked-books-ladders-with-copy-space-education-day_21745444.htm"><code>static/images/stacked_book.webp</code></a>.
    + <a href="https://www.freepik.com/free-photo/creative-composition-with-different-books_12407522.htm"><code>static/images/wide_books.webp</code></a>.