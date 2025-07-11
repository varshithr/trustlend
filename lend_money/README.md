# Lend Money App

This is the `lend_money` Django app, designed to facilitate lending transactions between users. 

## Overview

The `lend_money` app allows users to lend and borrow money through a simple interface. It includes features for managing loans, tracking repayments, and viewing transaction history.

## Installation

To install the `lend_money` app, follow these steps:

1. Ensure you have Django installed in your environment. You can install it using pip:

   ```
   pip install django
   ```

2. Add `lend_money` to your `INSTALLED_APPS` in the Django settings:

   ```python
   INSTALLED_APPS = [
       ...
       'lend_money',
   ]
   ```

3. Run the migrations to set up the database:

   ```
   python manage.py migrate
   ```

4. Start the development server:

   ```
   python manage.py runserver
   ```

## Usage

After setting up the app, you can access the lending features through the provided views. You can also manage the app through the Django admin interface by registering your models in `admin.py`.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.