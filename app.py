# app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# This middleware adds the X-Frame-Options header to allow embedding.
@app.after_request
def add_security_headers(response):
    # This header controls whether your site can be embedded.

    # (Optional, but more secure) CSP header for framing:
    # frame-ancestors *; allows embedding by any domain
    # frame-ancestors 'self' https://yourdomain.com; is more restrictive
    # TURN THIS BACK ON FOR IFRAME
    # response.headers['Content-Security-Policy'] = "frame-ancestors *;"
    return response

# Main route for the calculator

# app.py (Modified for Checkbox)
@app.route('/', methods=['GET', 'POST'])
def calculator():
    city = None
    parks = None
    library = None
    schools = None
    total = None
    city_new = None
    schools_new = None
    total_new = None
    increase = None
    city_increase = None
    schools_increase = None
    num1 = None
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

            # --- Property Tax Calculation Logic: City, Schools, Library ---
            
            # 1. Initialize total deduction amount
            total_deduction = 0
            school_deduction = 0
        
            # 2. Calculate Homestead Exemption (Act 50) $15,000 deduction
            if homestead_applied == 'yes':
                total_deduction += 15000
                school_deduction = 43750
                
            # 3. Calculate Senior Tax Relief (Act 77): 40% reduction 
            #    Applied to the ORIGINAL Assessed Value (num1)
            if senior_applied == 'yes':
                senior_deduction = num1 * 0.40
                total_deduction += senior_deduction

            # 4. Calculate Taxable Value
            taxable_value = max(0, num1 - total_deduction)
            school_value = max(0, num1 - school_deduction)
            
            # Ensure the taxable value is never negative
            if taxable_value < 0:
                taxable_value = 0   
            
            if school_value < 0:
                school_value = 0
            
            # 5. Calculate final result using the tax rate 
            city = taxable_value * 0.00806
            parks = taxable_value * 0.0005
            library = taxable_value * 0.00025
            schools = school_value * 0.01025
            total = city + parks + library + schools

            city_new = taxable_value * 0.01048
            schools_new = school_value * 0.010457
            city_increase = city_new - city
            schools_increase = schools_new - schools
            total_new = city_new + parks + library + schools_new
            increase = total_new - total 
    

        except ValueError:
            error = "Error: Invalid input. Please enter a valid number for the assessed value."
        except Exception as e:
            error = f"An unexpected error occurred: {e}"

    # Pass the last status to the template (None if unchecked, 'yes' if checked)
    return render_template('calculator.html', 
                           num1=num1,
                           city=city,
                           parks=parks,
                           library=library, 
                           schools = schools,
                           total=total,
                           city_new=city_new,
                           schools_new=schools_new,
                           total_new=total_new,
                           increase=increase,
                           city_increase=city_increase,
                           schools_increase=schools_increase,
                           error=error,
                           homestead_status=homestead_status,
                           senior_status=senior_status)
# To run the application
if __name__ == '__main__':
    # use 501 to bypass MacOS conflict
    app.run(debug=True, port=5001)