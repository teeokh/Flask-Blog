from flaskblog import create_app # This will import from the __init__.py file

app = create_app()

if __name__== '__main__':
    app.run(debug=True)