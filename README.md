# Dimension Studio - Virtual Try-On System

## 🎯 Project Description
**Dimension Studio** is an AI-powered platform that allows users to try on virtual clothing on their photos. The project focuses on improving online shopping experience and reducing return rates.

## 🛠️ Technologies Used

### Backend:
- **Django 5.2.3** (Python web framework)
- **SQLite** database
- **Gunicorn** (WSGI server for production)
- **Cloudinary** (cloud image storage)

### Frontend:
- **HTML5, CSS3, JavaScript**
- **Bootstrap** (responsive design)
- **Font Awesome** (icons)

### AI/ML:
- **Fashn.ai API** (fashion try-on service)
- **Cloudinary API** (image processing and storage)
- **PyTorch** (deep learning framework)
- **OpenCV** (image processing)

### Deployment:
- **Render** (cloud hosting)
- **Cloudflare** (CDN and tunnel)

## 📦 Installation and Setup

### System Requirements
- **Python 3.8+**
- **pip** (Python package manager)
- **Git** (version control)
- **4GB+ RAM** (recommended for AI processing)
- **2GB+ free disk space** (for media files)

### 🚀 Quick Start

1. **Clone repository:**
```bash
git clone https://github.com/your-username/Dimension_Studio.git
cd Dimension_Studio
```

2. **Create virtual environment:**
```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Download Media Files:**
```bash
# Create media directory if it doesn't exist
mkdir -p media

# Download media files from Google Drive
# Use wget or curl to download zip file
wget "https://drive.google.com/file/d/1e_4q7riOZlP8JLLh0MzpwVph2Fq5IabV/view?usp=sharing" -O media_files.zip

# Extract to media directory
unzip media_files.zip -d media/
rm media_files.zip  # Remove zip file after extraction
```

5. **Environment Configuration:**
```bash
# Create .env file and add necessary environment variables
```

**Required environment variables:**
```env
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# Cloudinary Configuration
CLOUDINARY_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret

# Fashion API
FASHN_API_KEY=your-fashion-api-key
```

6. **Database Setup:**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

7. **Create superuser:**
```bash
python manage.py createsuperuser
```

8. **Run development server:**
```bash
python manage.py runserver
```

9. **Access application:**
- **Main site:** http://localhost:8000
- **Admin panel:** http://localhost:8000/admin
- **Admin site:** http://localhost:8000/admin_site/

## 📁 Project Structure
```
Dimension_Studio/
├── VTON/                    # Django settings and configuration
├── home/                    # Main application (homepage, try-on)
│   ├── templates/           # HTML templates
│   ├── static/             # CSS, JS files
│   ├── views.py            # View functions
│   └── urls.py             # URL routing
├── user/                    # User management (auth, profile, payment)
│   ├── models.py           # User, Profile, Subscription models
│   ├── views.py            # Authentication views
│   ├── middleware.py       # Custom middleware
│   └── templates/          # User templates
├── admin_site/              # Admin dashboard
│   ├── views.py            # Admin views
│   └── templates/          # Admin templates
├── AI/                      # AI integration
│   └── api_client.py       # Fashn.ai API client
├── media/                   # Media files (images, avatars, demos)
│   ├── avatar/             # User profile pictures
│   ├── demo/               # Demo images
│   ├── payment_image/      # Payment screenshots
│   └── QR_code/            # QR code images
├── staticfiles/             # Static files (CSS, JS, images)
├── log/                     # Application logs
├── requirements.txt         # Python dependencies
└── manage.py               # Django management script
```

## ✨ Main Features

### 🔐 User Management
- **Email-based authentication** (no username required)
- **Email verification** system with token
- **Password reset** functionality
- **Profile management** with avatar upload
- **Account security** settings
- **Custom User model** with email as username

### 👗 Virtual Try-On
- **AI-powered try-on** using Fashn.ai API
- **Real-time processing** with Cloudinary storage
- **Image upload** for person and clothing
- **High-quality results** in seconds
- **Try-on history** tracking
- **Attempt-based system** (Free: 20 attempts, Premium: unlimited)

### 💳 Subscription System
- **Free plan** with 20 attempts
- **Premium plan** with unlimited access
- **Payment integration** with screenshot upload
- **Purchase history** tracking
- **Auto-downgrade** after 30 days
- **Transaction queue** for admin

### 🛠️ Admin Features
- **User management** dashboard with filters
- **Subscription monitoring** and management
- **Transaction queue** management
- **Analytics** and reporting (revenue, users)
- **System configuration**
- **Role-based access** (Admin, Staff, User)

### 🎨 User Interface
- **Responsive design** (mobile-friendly)
- **Modern UI/UX** with Bootstrap
- **Interactive elements** with JavaScript
- **Multi-language support** (Vietnamese/English)
- **Accessibility** features

### 🔧 System Features
- **Custom middleware** for auto-cleanup
- **Email notifications** for verification
- **Cloudinary integration** for image storage
- **Logging system** for monitoring
- **Environment-based configuration**

## 🚀 How to Use

### For Users:
1. **Register** account with email
2. **Verify email** through sent link
3. **Login** and upload profile image
4. **Try-on** virtual clothing:
   - Upload person image
   - Upload outfit image
   - Get results in seconds
5. **Purchase subscription** for unlimited access

### For Admins:
1. **Access admin panel** at `/admin_site/`
2. **Manage users** and subscriptions
3. **Process payments** in transaction queue
4. **Monitor analytics** and revenue
5. **Configure system** settings

## 📊 Database Models

### User Model:
- Email-based authentication
- Email verification status
- Custom user manager

### Profile Model:
- Avatar upload
- Phone number
- Subscription plan
- Expiry date
- Attempts counter (0-20)

### Subscription Model:
- Plan name and price
- Description
- Popular plan flag

### PurchaseHistory Model:
- Transaction tracking
- Payment status (processing/success/failed)
- Payment image upload
- Auto-update profile on success

### TryOnHistory Model:
- User try-on records
- Image URLs (person, outfit, result)
- Timestamp tracking

## 🔧 Configuration

### Environment Variables:
All configuration is managed through `.env` file:
- Django settings (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- Email configuration (SMTP settings)
- Cloudinary API credentials
- Fashn.ai API key

### Middleware:
- **CleanUnverifiedUsersMiddleware**: Delete unverified accounts after 20 minutes
- **AutoDowngradeMiddleware**: Auto-downgrade after 30 days
- **ResetFreePlanMiddleware**: Reset attempts for Free plan after 30 days

## 📝 API Integration

### Fashn.ai API:
- Model: `tryon-v1.6`
- Input: Person image + Garment image
- Output: Generated try-on result
- Authentication: Bearer token

### Cloudinary API:
- Image upload and storage
- Automatic optimization
- CDN delivery
- Secure URLs

## 🐛 Troubleshooting

### Common Issues:
1. **Media files not loading**: Ensure media files are downloaded from Google Drive
2. **API errors**: Check API keys in `.env`
3. **Email not sending**: Configure SMTP settings
4. **Database errors**: Run `python manage.py migrate`

### Logs:
- Application logs: `log/` directory
- Django logs: Console output
- Error tracking: Admin panel

## 👥 Author
**EXE201 Team** - FPT University AI Project - Tran Le Duy 

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📞 Support
If you encounter any issues, please create an issue on GitHub or contact the team via email.