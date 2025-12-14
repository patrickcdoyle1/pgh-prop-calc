# app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# This middleware adds the X-Frame-Options header to allow embedding.
@app.after_request
def add_security_headers(response):
    # This header controls whether your site can be embedded.
    # Set it to ALLOWALL to allow embedding on any site.
    # OR set to ALLOW-FROM https://yourdomain.com if you know the exact domain.
    response.headers['X-Frame-Options'] = 'ALLOWALL'

    # (Optional, but more secure) CSP header for framing:
    # frame-ancestors *; allows embedding by any domain
    # frame-ancestors 'self' https://yourdomain.com; is more restrictive
    response.headers['Content-Security-Policy'] = "frame-ancestors *;"
    return response

# Main route for the calculator
@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    error = None

    if request.method == 'POST':
        try:
            # Get numbers and operation from the submitted form
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            operation = request.form['operation']

            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                if num2 == 0:
                    error = "Error: Cannot divide by zero!"
                else:
                    result = num1 / num2
            else:
                error = "Error: Invalid operation."

        except ValueError:
            error = "Error: Invalid input. Please enter valid numbers."
        except Exception as e:
            error = f"An unexpected error occurred: {e}"

    # Render the HTML template, passing the result or error message
    return render_template('calculator.html', result=result, error=error)

# To run the application
if __name__ == '__main__':
    # Setting debug=True allows for automatic restarts when you save changes
    app.run(debug=True)