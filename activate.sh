cd ..

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment 'env' not found!"
    echo "Creating  environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created successfully!"
fi

# activate the virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate


# go to the lms_ai directory
cd NotifyHub

# check the python version
echo "🐍 Python version check:"
python --version

# Check pip version
echo "📦 Pip version check:"
pip --version


python manage.py runserver