# BlogNest

## Description

**BlogNest** is a simple yet powerful blogging platform built using Django. It allows users to create, view, and manage blog posts with ease. The platform supports user authentication, categories, tags, and comments, making it a comprehensive solution for anyone looking to start a blog.

With a focus on simplicity and expandability, BlogNest is perfect for those who want to build a personal blog or a more complex multi-author platform. The project also includes responsive design, making it accessible on various devices.

## Features

- **User Registration and Authentication**: Secure user sign-up, login, and logout functionality.
- **Create, Edit, and Delete Posts**: Users can easily manage their blog posts.
- **Categories and Tags**: Posts can be organized by categories and tagged for easy navigation.
- **Comments**: Readers can engage with posts by leaving comments.
- **Responsive Design**: The platform is designed to look great on both desktop and mobile devices.
- **Image Uploads**: Supports uploading images for posts, including thumbnail and main images.
- **Search Functionality**: Easily find posts by keywords, categories, or tags.
- **Post Slugs**: Clean URLs with post slugs for SEO-friendly links.

## Project URL

You can view the live project here: [BlogNest](https://simple-blog-kd6o.onrender.com)

## Installation

To run BlogNest locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/BlogNest.git
   cd BlogNest
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows, use `env\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**:
   Open your web browser and go to `http://127.0.0.1:8000/`.

## Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file:

- `SECRET_KEY`: Your Django secret key.
- `DEBUG`: Set to `True` for development.
- `DATABASE_URL`: The URL for your PostgreSQL database.
- `ALLOWED_HOSTS`: A comma-separated list of allowed hosts.

## Database Setup

BlogNest uses PostgreSQL as the database backend. You can set up the database with the following command:

```bash
python manage.py migrate
```

## Contributing

Contributions are welcome! Please fork this repository, create a new branch, and submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request



## Contact

If you have any questions or feedback, feel free to reach out:

- **Yakubu Abraham**
- [LinkedIn](https://www.linkedin.com/in/yourprofile/)
- [GitHub](https://github.com/Abraham-s-yakubu)

---

Thank you for checking out BlogNest! Happy blogging!
```
