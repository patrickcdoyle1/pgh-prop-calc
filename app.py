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

# app.py (Modified for Checkbox)
@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    error = None
    
    # Initialize homestead_status to hold the selected value for template persistence
    # Default to 'no' (False/None) if not submitted or first load
    homestead_status = request.form.get('homestead', 'no') 
    senior_status = request.form.get('senior', 'no')

    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            
            # --- CHECKBOX LOGIC CHANGE HERE ---
            # If the checkbox is checked, request.form.get('homestead') will return 'yes'.
            # If the checkbox is UNCHECKED, it returns None.
            homestead_applied = request.form.get('homestead')
            senior_applied = request.form.get('senior')
            
            # Save the status for template persistence
            homestead_status = homestead_applied 
            senior_status = senior_applied

            # --- Property Tax Calculation Logic ---
            taxable_value = num1
            
          #  if homestead_applied == 'yes' & senior_applied == 'yes': # Only applies if both boxes checked
            if senior_applied == 'yes':
                taxable_value = num1 * .6

                if homestead_applied == 'yes':
                    taxable_value = taxable_value - 15000

            elif senior_applied == 'no' & homestead_applied == 'yes':
                taxable_value = num1 - 15000
            
            else: taxable_value = num1
            
            # If not checked, taxable_value remains num1
            
            # Calculate final result using the tax rate (8.06 per $1000)
            result = (taxable_value / 1000) * 8.06
            
            # Ensure the result is not negative
            if result < 0:
                result = 0

        except ValueError:
            error = "Error: Invalid input. Please enter a valid number for the assessed value."
        except Exception as e:
            error = f"An unexpected error occurred: {e}"

    # Pass the last status to the template (None if unchecked, 'yes' if checked)
    return render_template('calculator.html', 
                           result=result, 
                           error=error,
                           homestead_status=homestead_status)
# To run the application
if __name__ == '__main__':
    app.run(debug=True)