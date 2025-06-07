# README.md

# Wamama Chama System

## Overview
Wamama Chama System is a Django web application designed to facilitate the management of meetings, user registrations, and articles related to community groups (Chamas). The application integrates with various payment methods, including MPESA and Pesapal, to streamline contributions and transactions.

## Features
- User registration and authentication
- Meeting management (create, view, delete)
- Article management (create, view)
- Payment integration with MPESA and Pesapal
- Admin dashboard for managing users and meetings

## Technologies Used
- Django: A high-level Python web framework for rapid development.
- Firebase Firestore: A NoSQL cloud database for storing application data.
- HTML/CSS: For front-end development.
- Bootstrap: For responsive design.

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd Wamama-Chama-System
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up Firebase:
   - Create a Firebase project and enable Firestore.
   - Obtain the service account key and configure it in your project.

4. Run the application:
   ```
   python manage.py runserver
   ```

5. Access the application at `http://127.0.0.1:8000/`.

## Usage
- Navigate to the sign-up page to create a new account.
- Log in to access the admin dashboard and manage meetings and articles.
- Use the payment methods to make contributions.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.