# Vendor-Mangement-System
 Backend for vendor management system using django and django rest framework. 

 Setup instructions
    1. Clone the repository into your local machine.
    2. Install latest version of python (3.8.10 preffered to run the project without any conflicts) in your machine.
    3. Create virtual environment and install all the packages in the 'requirements.txt' to run the project.
    4. Ensure, the variables that has 'os.getenv()' in the settings should be replace with correct values.
    5. Run 'python manage.py runserver' to start the server (listening port : 'localhost:8000' or '127.0.0.1:8000').

Instructions on how to run the test suite
    1. After successfully complete the setup instructions, visit 'http://localhost:8000/api/schema/swagger-ui/' to test the API endpoints.
    2. Visit '/api/user/' to create an user.
    3. After create the user, visit '/api-token-auth/' or run the command 'python manage.py drf_create_token 'username'' to obtain token. To get token send 'username' and 'password' as input incase of using swagger-ui.
    4. After that, click Authorize on the top right and paste the token value. format : (Token XXXXXXXXXXXXXXXXXXX) 
    5. /api/vendors/ --> used to create a vendor and list all vendors. (name,contact details and address) fields are enough to create a vendor.
    6. /api/vendors/{vendor_code}/ --> used to get particular vendor, update a vendor and delete a vendor.
    7. /api/purchase_orders/ --> used to create purchase order and list all purchase orders. (order date,items,quantity,status,expected delivery date,vendor) fields enough to create a purchase order.
    8. /api/purchase_orders/{po_number}/ --> used to update, get selected po order, delete po order using po number.
    9. /api/purchase_orders/{po_number}/acknowledge/ --> used to update the acknowledge and status of the po order.
    10. /api/vendors/{vendor_code}/performance/ --> used to get individual performance of the vendor using vendor code.   
