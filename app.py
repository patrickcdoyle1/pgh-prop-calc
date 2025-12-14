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
    
    # Initialize homestead_status to hold the selected value for persistence
    homestead_status = request.form.get('homestead', 'no') 

    if request.method == 'POST':
        try:
            # 1. Get the Assessed Value
            num1 = float(request.form['num1'])
            
            # 2. GET the Homestead Selection from the form
            homestead = request.form['homestead'] 
            
            # Save the status for template persistence
            homestead_status = homestead 

            # --- Property Tax Calculation Logic ---
            taxable_value = num1
            
            if homestead == 'yes':
                # Apply $18,000 exemption
                if num1 <= 18000:
                    taxable_value = 0 # No tax if property value is less than exemption
                else:
                    taxable_value = num1 - 18000
            
            # Calculate final result using the tax rate (8.06 per $1000)
            # (taxable_value / 1000) * 8.06
            result = (taxable_value / 1000) * 8.06
            
            # Check for negative result (though logic above mostly prevents this)
            if result < 0:
                result = 0

        except ValueError:
            error = "Error: Invalid input. Please enter a valid number for the assessed value."
        except Exception as e:
            error = f"An unexpected error occurred: {e}"

    # Render the HTML template, passing the result, error, and the last selected homestead status
    return render_template('calculator.html', 
                           result=result, 
                           error=error,
                           homestead_status=homestead_status)

# To run the application
if __name__ == '__main__':
    app.run(debug=True)