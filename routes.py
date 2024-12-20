from flask import render_template, request, jsonify, send_from_directory, url_for, redirect
from __main__ import app 

@app.route("/test")
def test_connection():
    try:
        # Run a lightweight query to test the connection
        db.session.execute(text('SELECT 1'))
        return "Database connected successfully!"
    except Exception as e:
        return f"Database connection failed: {e}"

        # # Routes
# UI_DIRECTORY = os.path.join(os.getcwd(), 'Code', 'UI')


@app.route('/', methods=['GET'])
def serve_login_page():
    print("Home route accessed")
    return render_template('LoginPage.html')


@app.route('/agent')

def serve_agent_page():

    agents = TblAgent.query.all()

    print(agents)

    return render_template('Agent.html', agents=agents)

@app.route('/dashboard', methods=['GET'])
def serve_dashboard_page():
    return render_template('Dashboard.html')

@app.route('/company-detail', methods=['GET'])
def serve_company_page():
    return render_template('CompanyDetails.html')

@app.route('/home', methods=['GET'])
def serve_home_page():
    return render_template('index.html', key=os.environ.get('stripepublickkey'))

@app.route('/product-detail', methods=['GET'])
def serve_product_page():
    return render_template('ProductDetails.html')

@app.route('/service-detail', methods=['GET'])
def serve_service_page():
    return render_template('ServiceDetails.html')

@app.route('/terms', methods=['GET'])
def serve_terms_page():
    return render_template('TermsPolicies.html')

@app.route('/knowledge', methods=['GET'])
def serve_knowledge_page():
    return render_template('KnowledgeBase.html')

@app.route('/portal', methods=['GET'])
def serve_portal_page():
    return render_template('portal.html')

@app.route('/UserLogin', methods=['GET'])
def serve_userlogin_page():
    return render_template('UserLogin.html')

@app.route('/create-agent', methods=['GET'])
def serve_create_agent():
    return render_template('create-agent.html')

#================================================

@app.route('/generateotp', methods=['POST'])
def generateotp():
    data = request.json
    email = data.get('email')
    otp = str(random.randint(100000, 999999))  # OTP must be a string to include in the email

    # Send the OTP email
    otp_sent = sendOTP(otp, email)  # Use a different variable name to avoid conflict

    if otp_sent:

        return jsonify({
            "status": "success",
            "message": "OTP sent successfully!",
            "user": {
                "otp": otp,
            }
        })
    else:
        return jsonify({"status": "failure", "message": "Failed to generate OTP"}), 401

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Conceptiv AI - 30 minute Premium',
                    },
                    'unit_amount': 999,  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/UserLogin',
            cancel_url='http://127.0.0.1:8000/home',
        #     success_url='https://conceptiv.onrender.com/UserLogin',
        #     cancel_url='https://conceptiv.onrender.com/home',
        )
        print(checkout_session.id)
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/loginuser', methods=['POST'])
def loginuser():
    data = request.json
   
    email = data.get('email')
    password = data.get('password')

    user = Login.query.filter_by(email=email, password=password).first()
    if user:
        return jsonify({
            "status": "success",
            "message": "Login successful!",
            "redirect": "/agent",
            "user": {
                "user_id": user.user_id,
                "fname": user.fname,
                "lname": user.lname,
                "email": user.email
            }
        })
    else:
        return jsonify({"status": "failure", "message": "Invalid email or password!"}), 401

@app.route('/signupuser', methods=['POST'])
def signupuser():
    data = request.json
    fname = data.get('fname')
    lname = data.get('lname')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    existing_user = Login.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"status": "failure", "message": "Email already registered!"}), 400

    new_user = Login(fname=fname, lname=lname, email=email, phone=phone, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "Signup successful! You may login"})

@app.route('/fetch_latest_users', methods=['GET'])
def fetch_latest_users():
    try:
        query = text("""
            SELECT 
                u.user_id, u.fname, u.lname, u.email, MAX(c.timestamp) as latest_timestamp
            FROM tbl_login u
            JOIN tbl_chat_interaction c ON u.user_id = c.user_id
            GROUP BY u.user_id, u.fname, u.lname, u.email
            ORDER BY latest_timestamp DESC
        """)
        results = db.session.execute(query).fetchall()

        # Convert result to dictionary
        data = []
        for r in results:
            data.append({
                "user_id": r.user_id,
                "fname": r.fname,
                "lname": r.lname,
                "email": r.email,
                "timestamp": r.latest_timestamp
            })
        return jsonify(data), 200
    except Exception as e:
        print("Error in /fetch_latest_users:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/fetch_messages', methods=['GET'])
def fetch_messages():
    email = request.args.get('email')
    try:
        # Base query
        base_query = """
            SELECT 
                u.user_id, u.email, u.fname, u.lname, 
                c.user_question as user_message, c.ai_response as bot_reply, c.timestamp
            FROM tbl_login u
            JOIN tbl_chat_interaction c ON u.user_id = c.user_id
        """
        
        if email and email != "everything":
            # Query for specific email
            query = text(base_query + " WHERE u.email = :email ORDER BY c.timestamp DESC")
            results = db.session.execute(query, {"email": email}).fetchall()
        else:
            # Query for all messages
            query = text(base_query + " ORDER BY c.timestamp DESC")
            results = db.session.execute(query).fetchall()

        # Convert results to a dictionary
        data = []
        for r in results:
            data.append({
                "user_id": r.user_id,
                "email": r.email,
                "fname": r.fname,
                "lname": r.lname,
                "user_message": r.user_message,
                "bot_reply": r.bot_reply,
                "timestamp": r.timestamp
            })
        return jsonify(data), 200
    except Exception as e:
        print("Error in /fetch_messages:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/prompt', methods=['POST'])
def modify_prompt():
    global custom_prompt
    try:
        data = request.json
        user_id = data.get('user_id')
        previousprompt = data.get('localprompt')
        custom_prompt = data.get('customprompt', '').strip()
        company_id = data.get('company_id', None)

        if not user_id or not custom_prompt:
            return jsonify({"error": "User ID and custom prompt are required"}), 400

        session = db.session.query(ChatSession).filter_by(user_id=user_id).first()
        if not session:
            session = ChatSession(user_id=user_id, custom_prompt=custom_prompt, history=[])
            db.session.add(session)
        else:
            if previousprompt != custom_prompt:
                session.history = []
            session.custom_prompt = custom_prompt
            session.updated_at = datetime.now(timezone.utc)

        prompt_entry = db.session.query(tbl_prompt).filter_by(user_id=user_id).first()
        if not prompt_entry:
            new_prompt = tbl_prompt(
                role='admin',  # Assuming role is 'user'
                prompt=custom_prompt,
                user_id=user_id,
                company_id=company_id,
            )
            db.session.add(new_prompt)
        else:
            prompt_entry.prompt = custom_prompt
            prompt_entry.updated_at = datetime.now(timezone.utc)

        
        db.session.commit()

        return jsonify({"message": "Prompt loaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        data = request.json
        print("Received data:", data)

        user_message = data.get('message', '').strip()
        user_id = data.get('user_id')
        company_id = data.get('company_id',None)  # Include company_id if available
        context = data.get('context', None)  # Optional field for additional context
        
        if not user_message or not user_id:
            print("Missing message or user_id")
            return jsonify({"error": "Message and User ID are required"}), 400

         # Retrieve or create session
        session = db.session.query(ChatSession).filter_by(user_id=user_id).first()
        if not session:
            print("Session not initialized")
            return jsonify({"error": "Session not initialized. Please set up a custom prompt first."}), 400

        # Prepare history for OpenAI API
        # constraints=" Whenever responding to user saying hi, introduce yourself and speak. Keep your responses consize unless it is demanded by the situation of conversation for it to be long, else try to keep it within the amount how a person might in a clear text based conversation. Keep your conversations interactive by asking questions when required instead of just answering with a statement always."
        # constrained_prompt=[{"role": "user", "content": constraints}]
        history = session.history + [{"role": "user", "content": user_message}]
        session_history = [{"role": "system", "content": session.custom_prompt}] + history #+ constrained_prompt
        print("Session history:", session_history)

        # Correct usage of openai.chat.completions.create
        response =  openai.chat.completions.create(
            model="gpt-4o-mini",  # Use the desired model
            messages=session_history
        )
        ai_response = response.choices[0].message.content.strip()
        print(type(ai_response),"<==type of ai_response")
        print("AI Response:", ai_response)

        # Update session history
        history.append({"role": "assistant", "content": ai_response})
        session.history = history
        session.updated_at = datetime.now(timezone.utc)
        db.session.commit()


        new_interaction = ChatInteraction(
            company_id=company_id,
            user_question=user_message,
            ai_response=ai_response,
            context=context,
            user_id=user_id
        )
        db.session.add(new_interaction)
        db.session.commit()

        return jsonify({"reply": ai_response}), 200

    except Exception as e:
        print("Error in /chat:", str(e))
        return jsonify({"error": str(e)}), 500

#=================================================

# Route to Create Payment Intent and Store Transaction
@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    data = request.json
    payment_method_id = data.get('payment_method')
    customer_email = data.get('cust_email')

    print(customer_email)

    

    try:
        # Create Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=2000,  # Example: $20 in cents
            currency="usd",
            payment_method=payment_method_id,
            receipt_email=customer_email,
            confirm=True,
            automatic_payment_methods={
                "enabled": True, 
                "allow_redirects": "never"
            },
        )

        # Store Transaction in Database
        transaction = Transaction(
            payment_method_id=payment_method_id,
            receipt_email=customer_email,
            amount=payment_intent.amount,
            currency=payment_intent.currency,
            status=payment_intent.status
        )
        db.session.add(transaction)
        db.session.commit()

        return jsonify({"success": True, "client_secret": payment_intent.client_secret})

    except stripe.error.StripeError as e:
        return jsonify({"success": False, "message": str(e)}), 400
