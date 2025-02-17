EventStar API
# EventStar GmbH

## Overview

EventStar GmbH is a dynamic event management solution provider aiming to streamline the organization and participation in various events. This project leverages the Django Rest Framework (DRF) to offer a robust and scalable RESTful API, facilitating seamless integration with web and mobile frontends.

## Features

- **Event Management**: Create, update, delete, and list events with detailed information.
- **Participant Registration**: Users can register for events, manage their participation, and handle special requirements.
- **Organizer Management**: Administrators can manage event organizers and their associated events.
- **Venue Management**: Manage event venues, including details like capacity and location.
- **Favoriting System**: Participants can favorite events for quick access and updates.
- **Rating System**: Participants can rate and comment on events they've attended.
- **Subscription Notifications**: Users can subscribe to events to receive notifications about updates or changes.
- **Statistics and Reports**: Administrators can access and export event-related statistics and reports.
- **Role-Based Permissions**: Secure access control based on user roles (Admin, Organizer, Participant).

## Technology Stack

- **Backend**: Django, Django Rest Framework
- **Database**: SQLite3
- **Authentication**: Django's built-in authentication system
- **Filtering**: django-filter

## Installation

### Prerequisites

- Python 3.8+
- pip
- Git

### Steps

1. **Clone the Repository**

    ```sh
    git clone https://github.com/yourusername/eventstar-api.git
    cd eventstar-api
    ```

2. **Create a Virtual Environment**

    ```sh
    python3 -m venv venv
    ```

3. **Activate the Virtual Environment**

    - On Unix or MacOS:

      ```sh
      source venv/bin/activate
      ```

    - On Windows:

      ```sh
      venv\Scripts\activate
      ```

4. **Install Dependencies**

    ```sh
    pip install -r requirements.txt
    ```

    **Note**: Ensure `django-filter` is included in your `requirements.txt`. If not, install it manually:

    ```sh
    pip install django-filter
    ```

5. **Apply Migrations**

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a Superuser**

    ```sh
    python manage.py createsuperuser
    ```

    Follow the prompts to set up an administrative account.

7. **Load Test Data**

    To populate the database with sample data, run the following commands:

    ```sh
    python manage.py shell
    ```

    In the Django shell, execute:

    ```python
    from django.contrib.auth.models import User
    from events.models import Organizer, Venue, EventCategory, Event, Participant, Rating, Subscription

    # Create Users
    admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
    organizer_user1 = User.objects.create_user(username='organizer1', email='organizer1@example.com', password='organizerpass1')
    organizer_user2 = User.objects.create_user(username='organizer2', email='organizer2@example.com', password='organizerpass2')
    participant_user1 = User.objects.create_user(username='participant1', email='participant1@example.com', password='participantpass1')
    participant_user2 = User.objects.create_user(username='participant2', email='participant2@example.com', password='participantpass2')

    # Create Organizers
    organizer1 = Organizer.objects.create(user=organizer_user1, company_name='Organizer One GmbH')
    organizer2 = Organizer.objects.create(user=organizer_user2, company_name='Organizer Two GmbH')

    # Create Venues
    venue1 = Venue.objects.create(name='Grand Hall', address='123 Main St, City', capacity=500)
    venue2 = Venue.objects.create(name='Conference Center', address='456 Side St, City', capacity=300)

    # Create Event Categories
    category1 = EventCategory.objects.create(name='Conference')
    category2 = EventCategory.objects.create(name='Workshop')
    category3 = EventCategory.objects.create(name='Concert')

    # Create Events
    event1 = Event.objects.create(
         title='Tech Conference 2024',
         description='A conference about the latest in technology.',
         date='2024-06-15T09:00:00Z',
         venue=venue1,
         organizer=organizer1,
         max_participants=100,
         price=299.99,
         status='planned'
    )
    event1.category.set([category1])

    event2 = Event.objects.create(
         title='Music Concert',
         description='Live performances by top artists.',
         date='2024-07-20T19:00:00Z',
         venue=venue2,
         organizer=organizer2,
         max_participants=200,
         price=49.99,
         status='planned'
    )
    event2.category.set([category3])

    # Create Participants
    participant1 = Participant.objects.create(user=participant_user1, event=event1, special_requirements='Vegetarian meal')
    participant2 = Participant.objects.create(user=participant_user2, event=event1)
    participant3 = Participant.objects.create(user=participant_user1, event=event2)

    # Create Ratings
    rating1 = Rating.objects.create(event=event1, user=participant_user1, score=5, comment='Great conference!')
    rating2 = Rating.objects.create(event=event1, user=participant_user2, score=4, comment='Very informative.')
    rating3 = Rating.objects.create(event=event2, user=participant_user1, score=5, comment='Amazing concert!')

    # Create Subscriptions
    subscription1 = Subscription.objects.create(user=participant_user1, event=event1)
    subscription2 = Subscription.objects.create(user=participant_user2, event=event1)

    exit()
    ```

8. **Run the Development Server**

    ```sh
    python manage.py runserver
    ```

    Access the API at `http://localhost:8000/api/` and the admin panel at `http://localhost:8000/admin/`.

## API Endpoints

The API provides the following endpoints:

- **Events**
  - `GET /api/events/` - List all events
  - `POST /api/events/` - Create a new event
  - `GET /api/events/{id}/` - Retrieve event details
  - `PUT /api/events/{id}/` - Update an event
  - `DELETE /api/events/{id}/` - Delete an event
  - `POST /api/events/{id}/add_to_favorites/` - Add event to favorites
  - `POST /api/events/{id}/remove_from_favorites/` - Remove event from favorites
  - `POST /api/events/{id}/subscribe/` - Subscribe to event notifications

- **Participants**
  - `GET /api/participants/` - List all participants
  - `POST /api/participants/` - Register as a participant for an event
  - `GET /api/participants/{id}/` - Retrieve participant details
  - `PUT /api/participants/{id}/` - Update participant information
  - `DELETE /api/participants/{id}/` - Remove participant from an event

- **Organizers**
  - `GET /api/organizers/` - List all organizers (Admin only)
  - `POST /api/organizers/` - Create a new organizer (Admin only)
  - `GET /api/organizers/{id}/` - Retrieve organizer details
  - `PUT /api/organizers/{id}/` - Update organizer information (Admin only)
  - `DELETE /api/organizers/{id}/` - Delete an organizer (Admin only)

- **Venues**
  - `GET /api/venues/` - List all venues (Admin only)
  - `POST /api/venues/` - Create a new venue (Admin only)
  - `GET /api/venues/{id}/` - Retrieve venue details (Admin only)
  - `PUT /api/venues/{id}/` - Update venue information (Admin only)
  - `DELETE /api/venues/{id}/` - Delete a venue (Admin only)

- **Ratings**
  - `GET /api/ratings/` - List all ratings
  - `POST /api/ratings/` - Create a new rating
  - `GET /api/ratings/{id}/` - Retrieve rating details
  - `PUT /api/ratings/{id}/` - Update a rating
  - `DELETE /api/ratings/{id}/` - Delete a rating

- **Subscriptions**
  - `GET /api/subscriptions/` - List all subscriptions for the authenticated user
  - `POST /api/subscriptions/` - Subscribe to an event
  - `GET /api/subscriptions/{id}/` - Retrieve subscription details
  - `PUT /api/subscriptions/{id}/` - Update subscription information
  - `DELETE /api/subscriptions/{id}/` - Unsubscribe from an event

- **Statistics**
  - `GET /api/statistics/` - Retrieve event statistics (Admin only)

- **Organizer Events**
  - `GET /api/organizer-events/` - List events for the authenticated organizer
  - `POST /api/organizer-events/` - Create a new event for the organizer
  - `GET /api/organizer-events/{id}/` - Retrieve organizer's event details
  - `PUT /api/organizer-events/{id}/` - Update organizer's event
  - `DELETE /api/organizer-events/{id}/` - Delete organizer's event

- **Categories**
  - `GET /api/categories/` - List all event categories
  - `POST /api/categories/` - Create a new event category (Authenticated users)
  - `GET /api/categories/{id}/` - Retrieve category details
  - `PUT /api/categories/{id}/` - Update a category (Authenticated users)
  - `DELETE /api/categories/{id}/` - Delete a category (Authenticated users)

## Authentication

The API uses Django's built-in authentication system. To perform actions that require authentication:

1. **Obtain Authentication Credentials**

    - Access the Django admin panel at `http://localhost:8000/admin/` and log in with your superuser account.
    - Alternatively, create users via the API endpoints.

2. **Authenticate Requests**

    - Include the user's credentials in the request headers to access protected endpoints.
    - Example using HTTP Basic Auth in `curl`:

      ```sh
      curl -u username:password http://localhost:8000/api/events/
      ```

## Running Tests

To run the project's tests, execute:

```sh
python manage.py test
```

Ensure that you have written tests for your models, serializers, and views to maintain code quality and functionality.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create a Feature Branch**

    ```sh
    git checkout -b feature/YourFeatureName
    ```

3. **Commit Your Changes**

    ```sh
    git commit -m "Add some feature"
    ```

4. **Push to the Branch**

    ```sh
    git push origin feature/YourFeatureName
    ```

5. **Open a Pull Request**

## License

This project is licensed under the MIT License.

## Contact

For any inquiries or support, please contact [info@garten.dev](mailto:info@garten.dev).
