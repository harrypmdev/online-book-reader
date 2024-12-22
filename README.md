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
django ORM.
- **Gunicorn** was chosen for booting the site in production for its stability and efficiency.
- Python **Ruff linter** was chosen for its easy installation via pip, its speed, automatic formatting and
comprehensive functionality.
- **Whitenoise** was chosen for simple serving of static files in production.
- **Bootstrap** (CSS and JS) was chosen for its general-purpose CSS classes and modals which allows ultra-fast styling
of HTML in a manner that is intuitive and familiar for users.
- **Boostrap Crispy** was chosen for its ability to present simple forms without unnecessary custom HTML and CSS.

# Features

# Features Yet To Be Implemented

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
<br>

# Validators

# Testing

## Lighthouse Testing

### Home Page

### About Us Page

### Dashboard Page

### Add Book Page

### Manage Book Page

### Login Page

### Profile Page

### Register Page

### Read Page

### 404 Error Page

### 500 Error Page

### 403 CSRF Error Page

## Manual Testing

## Automated Testing

# Bugs

# Deployment

# References

 + <a href="https://balsamiq.com/wireframes/desktop/">Balsamic</a> software used for wireframing