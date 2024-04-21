# School management system

## Overview
This Django project is a RESTful API backend for managing enrollments, courses, grades, and users in an educational institution. It provides endpoints for handling various operations related to enrollment management, course scheduling, student grades, user authentication, and more. For convinience responses are paginated and for security reasons each endpoint allows access only for specified group of users.

## Features
- **Enrollments:** Create and manage enrollments, enrollment phases, group enrollments, and student enrollments.
  - **Strategies**: Enables adding enrollment resolution.
  - **Automated Enrollment Resolution**: Utilizes Celery for scheduling and automatically resolving enrollments based on selected strategy.
- **Courses:** Manage courses, course groups, and course scheduling as well as subjects and levels.
  - **Filter for user**: Users can get all courses related to them.
- **Grades:** Record and manage student notes for different courses.
  - **Types**: Divided into regular and final grades for the course.
- **Users:** Authentication and authorization of users.
  - **Roles**: Teachers, students and staff.
- **Timetables**: Control time related aspects.
  - **Lesson Unit**: Define when each lesson starts and how long they last.
  - **Period**: Manage all courses across many semesters or other long term intervals.
  - **Class schedule**: Teachers and students can generate their class schedule in .pdf file.

## Technologies Used
- **Django:** A high-level Python web framework for rapid development and clean, pragmatic design.
- **Django REST Framework:** A powerful and flexible toolkit for building Web APIs in Django.
- **PostgreSQL:** A robust relational database management system for storing application data.
- **Celery:** Distributed task queue for handling asynchronous tasks, including scheduled enrollment resolution.

## Full ER Diagram
![diagram](https://github.com/csecluki/school_management_system/assets/49252352/0373474a-6a9f-4ece-885e-1689a033dfa8)
