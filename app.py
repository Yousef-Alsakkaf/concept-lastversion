from flask import Flask, request, jsonify, render_template, send_from_directory, url_for, redirect, g, session
from flask_cors import CORS
from stripe import stripe, error
# import stripe
import openai
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased
from werkzeug.utils import secure_filename
from celery import Celery
from flask_apscheduler import APScheduler
from datetime import datetime, timezone, timedelta
from sqlalchemy.sql import text
import smtplib, ssl, random
from email.message import EmailMessage
from sqlalchemy import desc

from dotenv import load_dotenv
import os


#Load Environment Variables from .env file
load_dotenv()

# Configure API Keys
openai.api_key = os.getenv('openaikey')
# stripe.api_key = os.getenv('stripeprivatekey')
# stripepublickkey = os.getenv('stripepublickey')
zeptokey = os.getenv('zeptomailkey')

# openai.api_key = os.environ.get('openaikey')
# stripe.api_key = os.environ.get('stripeprivatekey')
# stripepublickkey = os.environ.get('stripepublickey')
# zeptokey = os.environ.get('zeptomailkey')

#print(zeptokey)


# Flask app initialization
app = Flask(__name__)
CORS(app)

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback_secret_key')

# from models import ChatSession
# from models import Login ChatInteraction, TblAgent, Transaction, tbl_prompt # Import Models

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nehar:GwyPfbcWtpCFwCg2WNOc6YjNMxM0nZ77@dpg-ct8o3jd6l47c73d5grgg-a/aibot_3bis'  ##Onrender Internal
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nehar:GwyPfbcWtpCFwCg2WNOc6YjNMxM0nZ77@dpg-ct8o3jd6l47c73d5grgg-a.oregon-postgres.render.com/aibot_3bis' ##OnRender External
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost/aibot'  ##Local
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     "postgresql+psycopg2://postgreadmin:Lkj@321@50ad903e3875:5432/aibot1"
# )

# Local PostgreSQL connection URL
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
# print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# TEST
# Celery configuration
app.config['broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'
# app.config['broker_url'] = 'rediss://red-ctckvrrtq21c73frunm0:wO6u9NWJfOoGud3X9jCoRKw2nB5n1kZc@oregon-redis.render.com:6379'
# app.config['result_backend'] = 'rediss://red-ctckvrrtq21c73frunm0:wO6u9NWJfOoGud3X9jCoRKw2nB5n1kZc@oregon-redis.render.com:6379'

db = SQLAlchemy(app)


def sendfollowmail(mailid):
    port = 587
    smtp_server = "smtp.zeptomail.com"
    username="emailapikey"
    password = zeptokey
    message = "test mail for retention function"
    msg = EmailMessage()
    msg['Subject'] = "Conceptiv AI - Callback"
    msg['From'] = "noreply@conceptiv.ai"
    msg['To'] = mailid
    msg.set_content(message)
    try:
        if port == 465:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(username, password)
                server.send_message(msg)
        elif port == 587:
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
        else:
            print ("use 465 / 587 as port value")
            return False
        print ("Follow Up Email Successfully Sent")
        return True
    except Exception as e:
        print (e)
        return False

app.config.update(
    #broker_url='rediss://red-ctckvrrtq21c73frunm0:wO6u9NWJfOoGud3X9jCoRKw2nB5n1kZc@oregon-redis.render.com:6379',
    #result_backend='rediss://red-ctckvrrtq21c73frunm0:wO6u9NWJfOoGud3X9jCoRKw2nB5n1kZc@oregon-redis.render.com:6379',
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    # broker_transport_options={
    #     'ssl': {
    #         'ssl_cert_reqs': ssl.CERT_REQUIRED  # Change to ssl.CERT_REQUIRED if you have a valid certificate
    #     }
    # },
    # redis_backend_transport_options={
    #     'ssl': {
    #         'ssl_cert_reqs': ssl.CERT_REQUIRED  # Same here
    #     }
    # }
)

# Celery setup
def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['broker_url'],
        backend=app.config['result_backend']
    )
    celery.conf.update(app.config)
    celery.conf.update(
        broker_url='redis://localhost:6379/0',  # Local Redis broker
        result_backend='redis://localhost:6379/0',  # Local Redis backend
        # broker_use_ssl={
        #     'ssl_cert_reqs': 'CERT_REQUIRED'
        # },
        # redis_backend_use_ssl={
        #     'ssl_cert_reqs': 'CERT_REQUIRED'
        # }
    )
    return celery

celery = make_celery(app)

# Celery task
@celery.task
def check_and_send_email():
    sendfollowmail("conceptivai@gmail.com")

# Flask-APScheduler setup for periodic tasks
scheduler = APScheduler()

@scheduler.task('interval', id='check_and_send_email', seconds=60)
def periodic_task():
    check_and_send_email.delay()  # Trigger the Celery task

scheduler.init_app(app)
scheduler.start()

@app.route("/test")
def test_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return "Database connected successfully!"
    except Exception as e:
        return f"Database connection failed: {e}"



@app.route('/', methods=['GET'])
def serve_login_page():
    print("Home route accessed")
    return render_template('LoginPage.html')

@app.route('/agent-prom', methods=['GET'])
def server_prompts_page():
    agent_id = request.args.get('agentId', default=None, type=str)
    
    all_prompts = tbl_customer_prompt.query.all()
    
#     agentdata = (
#     db.session.query(tbl_prompt)
#     .filter((tbl_prompt.user_id == user_id) & (tbl_prompt.agent_id == agent_id))
#     .order_by(desc(tbl_prompt.created_at))
#     .first()
# )


#     my_agent_prompt = agentdata.prompt if session else None  
        
    agent_details = TblAgent.query.filter_by(agent_id=agent_id).first()

    if not agent_details:
        return f"Agent with ID {agent_id} not found.", 404

    print('this is the image url:', agent_details.image_url)
    return render_template(
        'agent-prompt.html',
        agent_id=agent_id,
        agent_name=agent_details.agent_name,
        agent_image_url=agent_details.image_url,
        agent_role=agent_details.agent_role 
    )

@app.route('/agent', methods=['GET'])
def serve_agent_page():
    user_id = session.get('user_id')

    # Create an alias for TblPrompt
    prompt_alias = aliased(tbl_prompt)

    # Subquery to get the latest TblPrompt per user_id
    latest_prompt_subquery = db.session.query(
        tbl_prompt.user_id, 
        tbl_prompt.prompt_id
    ).filter(
        tbl_prompt.user_id == TblAgent.user_id  # Ensure we're filtering by the same user_id
    ).order_by(
        desc(tbl_prompt.prompt_id)  # Order by id (desc) to get the latest one
    ).limit(1).subquery()  # Wrap it as a subquery   # Get only the latest prompt

    # Query agents and join with the latest prompt (from the subquery)
    agents_and_prompts = db.session.query(TblAgent, tbl_prompt) \
        .join(latest_prompt_subquery, TblAgent.user_id == latest_prompt_subquery.c.user_id) \
        .join(tbl_prompt, tbl_prompt.prompt_id == latest_prompt_subquery.c.prompt_id) \
        .filter(TblAgent.user_id == user_id) \
        .all()

    print('Agents and prompts:', agents_and_prompts)

    return render_template('Agent.html', agents_and_prompts=agents_and_prompts)


@app.route('/stripe-settings', methods=['GET'])
def serve_stripe_settings():
    stripe_keys = tbl_stripe.query.all()
    print("Stripe Keys ", stripe_keys)
    return render_template('stripe-settings.html', stripe_keys = stripe_keys)

@app.route('/edit-stripe-settings', methods=['POST'])
def edit_stripe_settings():
    data = request.get_json() 
    f
    stripe_id = data.get('stripe_id')
    stripe_public_key = data.get('stripe_public_key')
    stripe_secret_key = data.get('stripe_secret_key')
    
    if not stripe_id or not stripe_public_key or not stripe_secret_key:
        return jsonify({'message': 'Missing required fields'}), 400

    stripe_record = tbl_stripe.query.filter_by(stripe_id=stripe_id).first()
    
    if not stripe_record:
        return jsonify({'message': 'Stripe record not found'}), 404
    
    stripe_record.stripe_public_key = stripe_public_key
    stripe_record.stripe_secret_key = stripe_secret_key
    stripe_record.updated_at = datetime.utcnow() 

    try:
        db.session.commit()  
        return jsonify({'message': 'Stripe settings updated successfully'}), 200
    except Exception as e:
        db.session.rollback() 
        return jsonify({'message': str(e)}), 500



@app.route('/dashboard', methods=['GET'])
def serve_dashboard_page():
    return render_template('Dashboard.html')

@app.route('/company-detail', methods=['GET'])
def serve_company_page():
    return render_template('CompanyDetails.html')

@app.route('/home', methods=['GET'])
def serve_home_page():
    # Fetch the most recent Stripe settings from the database
    stripe_settings = tbl_stripe.query.order_by(tbl_stripe.stripe_id.desc()).first()

    if stripe_settings:
        # Set the Stripe API keys
        stripe.api_key = stripe_settings.stripe_secret_key  # Private key for Stripe API
        app.config['STRIPE_PUBLIC_KEY'] = stripe_settings.stripe_public_key  # Public key for frontend usage
        
        # print("Stripe Secret Key has been set.")                      # DEBUGGING PURPOSE
        # print("Stripe Public Key:", app.config['STRIPE_PUBLIC_KEY'])  # DEBUGGING PURPOSE
    else:
        # Handle the case where no keys are found in the database
        print("Stripe keys not found in the database.")
        
    # Return the rendered template with the Stripe public key passed to JavaScript
    return render_template('index.html', stripepublickkey=app.config['STRIPE_PUBLIC_KEY'])

    # if hasattr(g, 'stripepublickkey'):
    #     return render_template('index.html', stripepublickkey=app.config['STRIPE_PUBLIC_KEY'])
    # else:
    #     # Handle case where stripepublickkey is not set
    #     return "Stripe key not set", 500

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
    # otp_sent = sendOTP(otp, email)  # Use a different variable name to avoid conflict
    otp_sent = otp;                            # DEBUGGING PURPOSE

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
        # print(checkout_session.id)                                  #DEBUGGING PURPOSE
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
        session['user_id'] = user.user_id

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

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()

        if not data.get('agent_name') or not data.get('image_url') or not data.get('agent_prompt') or not data.get('agent_role'):
            return jsonify({'error': 'Missing required fields'}), 400

        print('This is the user id:', data.get("userId"))

        new_agent = TblAgent(
            agent_name=data['agent_name'],
            gender=data.get('gender'), 
            image_url=data['image_url'],
            agent_prompt=data['agent_prompt'],
            agent_role=data['agent_role'],
            user_id=data.get('userId'), 
            updated_at=datetime.now(timezone.utc)
        )

        print(new_agent)            # DEBUGGING PURPOSE

        db.session.add(new_agent)
        db.session.commit()

        new_prompt = tbl_prompt(
            role=data['agent_role'],  
            prompt=data['agent_prompt'], 
            user_id=data.get('userId'),  
            company_id=1,
            agent_id=new_agent.agent_id,  
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        print(new_prompt)            # DEBUGGING PURPOSE

        db.session.add(new_prompt)
        db.session.commit()

        new_chat_session = ChatSession(
            user_id=data.get('userId'),  
            custom_prompt=data.get('agent_prompt'), 
            history=[], 
            updated_at=datetime.now(timezone.utc) 
        )

        db.session.add(new_chat_session)
        db.session.commit()

        return jsonify({'message': 'Agent, prompt, and chat session added successfully', 'agent_id': new_agent.agent_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/edit_user', methods=['POST'])
def edit_user():

    data = request.get_json()
    agent_id = data['agent_id']
    agent_name = data['agent_name']
    gender = data['gender']
    agent_prompt = data['agent_prompt']
    agent_role = data['agent_role']

    agent = TblAgent.query.filter_by(agent_id=agent_id).first()

    # TABLE PROMPT
    if agent:
        new_prompt = tbl_prompt(
            role=agent_role,
            prompt=agent_prompt,
            user_id=session.get('user_id'),
            company_id=1,
            agent_id = agent_id
        )
        db.session.add(new_prompt)
    
    try:
        db.session.commit()
        print('Agent Prompt Created')
    except Exception as e:
        print(e)

    # TABLE AGENT
    if not agent:
        return jsonify({'message': 'Agent not found'}), 404

    if agent_name:
        agent.agent_name = agent_name
    if gender:
        agent.gender = gender
    if agent_prompt:
        agent.agent_prompt = agent_prompt
    if agent_role:
        agent.agent_role = agent_role

    agent.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        return jsonify({'message': 'Agent updated successfully'}), 200
        print('Agent updated')
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
        


@app.route('/fetch_messages', methods=['GET'])
def fetch_messages():
    email = request.args.get('email')
    try:
        base_query = """
            SELECT 
                u.user_id, u.email, u.fname, u.lname, 
                c.user_question as user_message, c.ai_response as bot_reply, c.timestamp
            FROM tbl_login u
            JOIN tbl_chat_interaction c ON u.user_id = c.user_id
        """
        
        if email and email != "everything":
            query = text(base_query + " WHERE u.email = :email ORDER BY c.timestamp DESC")
            results = db.session.execute(query, {"email": email}).fetchall()
        else:
            query = text(base_query + " ORDER BY c.timestamp DESC")
            results = db.session.execute(query).fetchall()

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
                role='admin',
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

@app.route('/save-prompt', methods=['POST'])
def save_prompt():
    try:
        data = request.get_json()

        if not data or 'role' not in data or 'prompt' not in data or 'agent_id' not in data:
            return jsonify({"error": "Missing required fields: 'role', 'prompt', or 'agent_id'"}), 400

        role = data['role']
        prompt = data['prompt']
        agent_id = int(data['agent_id'])  # Convert agent_id to an integer

        new_prompt = tbl_customer_prompt(
            role=role,
            prompt=prompt,
            agent_id=agent_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        db.session.add(new_prompt)
        db.session.commit()

        return jsonify({"message": "Prompt saved successfully.", "prompt_id": new_prompt.prompt_id}), 201
    except Exception as e:
        print('This is the error:', str(e))
        return jsonify({"error": "An error occurred while saving the prompt.", "details": str(e)}), 500

@app.route('/getAdminContext', methods=['POST'])
def getAdminContext():
    try:
        data = request.get_json()
        if not data or 'agent_id' not in data:
            return jsonify({"error": "Missing 'agent_id' in request data"}), 400
        
        agent_id = data['agent_id']
        
        prompt = db.session.query(tbl_prompt).filter(tbl_prompt.agent_id == agent_id).first()

        if not prompt:
            return jsonify({"message": "No prompt found for this agent_id"}), 404
        
        result = {
            "company_id": prompt.company_id,
            "prompt": prompt.prompt,
        }

        return jsonify({"data": result}), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving the prompt.", "details": str(e)}), 500


# Retrieve the system prompt from tbl_agent
def get_system_prompt(agent_id):
    prompt = db.session.query(TblAgent).filter_by(agent_id=agent_id).first().agent_prompt
    return prompt

# Retrieve conversation history from tbl_chatinteraction
def get_conversation_history(user_id, agent_id):
    history = db.session.query(ChatInteraction).filter_by(user_id=user_id, agent_id=agent_id).all()
    return [{'role': 'user', 'content': record.user_question} for record in history] + \
           [{'role': 'assistant', 'content': record.ai_response} for record in history]

# Save new user and assistant interaction to the database
def save_conversation(user_id, agent_id, user_question, ai_response):
    new_interaction = ChatInteraction(
        user_id=user_id,
        agent_id=agent_id,
        user_question=user_question,
        ai_response=ai_response
    )
    db.session.add(new_interaction)
    db.session.commit()

# Function to interact with OpenAI API
def interact_with_openai(user_id, agent_id, user_message):
    system_prompt = get_system_prompt(agent_id)
    conversation_history = get_conversation_history(user_id, agent_id)

    # Prepare the request to OpenAI API
    messages = [
        {"role": "system", "content": system_prompt}
    ] + conversation_history + [{"role": "user", "content": user_message}]
    
@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        data = request.get_json()
        # print("Received data from Script JS: ", data)       # DEBUGGING PURPOSE
        # need to get the context_id and company_id 
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id')
        company_id = data.get('company_id',None)  # Include company_id if available
        context = data.get('context', None)  # Optional field for additional context
        agent_id=data.get('agent_id', None)
        # print("User ID = ", user_id)            # DEBUGGING PURPOSE
        # print("Agent ID = ", agent_id)          # DEBUGGING PURPOSE
        if not user_message or not user_id:
            print("Missing message or user_id")
            return jsonify({"error": "Message and User ID are required"}), 400
            
            
         # Retrieve or create session
        agent_prompt = (
                    db.session.query(tbl_prompt)
                    .filter((tbl_prompt.user_id == user_id) & (tbl_prompt.agent_id == agent_id))
                    .order_by(desc(tbl_prompt.created_at))
                    .first()
                  )
        
        if agent_prompt:
            # Access specific fields
            print("User ID:", agent_prompt.user_id)                # DEBUGGING PURPOSE
            print("Agent ID:", agent_prompt.agent_id)              # DEBUGGING PURPOSE
            print("Created At:", agent_prompt.created_at)          # DEBUGGING PURPOSE
            print("Prompt Is:", agent_prompt.prompt)   # DEBUGGING PURPOSE
        else:   
            print("No record found.")                               # DEBUGGING PURPOSE

        system_prompt = get_system_prompt(agent_id)

        conversation_history = get_conversation_history(user_id, agent_id)

        # Prepare the request to OpenAI API
        messages = [
            {"role": "system", "content": system_prompt}
        ] + conversation_history + [{"role": "user", "content": user_message}]
    
        print(messages)
        # Correct usage of openai.chat.completions.create
        response =  openai.chat.completions.create(
            model="gpt-4o-mini",  # Use the desired model
            messages=messages
        )
        ai_response = response.choices[0].message.content.strip()
        # print(type(ai_response),"<==type of ai_response")                    # DEBUGGING PURPOSE
        # print("AI Response:", ai_response)                                   # DEBUGGING PURPOSE
        # Update session history
        # history.append({"role": "assistant", "content": ai_response})
        # session.history = history
        session.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        new_interaction = ChatInteraction(
            company_id=1,
            user_question=user_message,
            ai_response=ai_response,
            context=context,
            user_id=user_id,
            agent_id=agent_id
        )
        db.session.add(new_interaction)
        db.session.commit()
        return jsonify({"reply": ai_response }), 200
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


# Chat session model ================
class ChatSession(db.Model):
    __tablename__ = 'tbl_chat_session'

    session_id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    custom_prompt = db.Column(db.Text)
    history = db.Column(db.JSON, default=[])
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)



# Login model =======================
class Login(db.Model):
    __tablename__ = 'tbl_login'

    user_id = db.Column(db.BigInteger, primary_key=True)
    fname = db.Column(db.Text, nullable=False)
    lname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    phone = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

class ChatInteraction(db.Model): #===================
    __tablename__ = 'tbl_chat_interaction'

    interaction_id = db.Column(db.BigInteger, primary_key=True)
    company_id = db.Column(db.BigInteger, nullable=True)
    user_question = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    context = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    user_id = db.Column(db.BigInteger, nullable=False)
    agent_id = db.Column(db.BigInteger, nullable=False)

class tbl_prompt(db.Model): #================
    __tablename__ = 'tbl_prompt'
    # we need to put role:
    # defalt
    # prompt: from the add_user route
    # user_id from the add_user route after getting it from the html page
    # company id will be harded coded as 1
    # agent_id I will be getting it from the route add_user
    prompt_id = db.Column(db.BigInteger, primary_key=True,  autoincrement=True)
    role = db.Column(db.String(255), nullable=True)
    prompt = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    user_id = db.Column(db.BigInteger, nullable=True)
    company_id = db.Column(db.BigInteger, nullable=True)
    agent_id = db.Column(db.BigInteger, nullable=True)



class tbl_customer_prompt(db.Model):
    __tablename__ = 'tbl_customer_prompt'

    prompt_id = db.Column(db.BigInteger, primary_key=True,  autoincrement=True)
    role = db.Column(db.String(255), nullable=True)
    prompt = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    agent_id = db.Column(db.BigInteger, nullable=True)

class TblAgent(db.Model):
    __tablename__ = 'tbl_agent'

    agent_id_seq = db.Sequence('agent_id_seq', start=5) 
    agent_id = db.Column(db.BigInteger, primary_key=True,  autoincrement=True)
    agent_name = db.Column(db.String(255), nullable=False) 
    gender = db.Column(db.String(10)) 
    image_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)  
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  
    agent_prompt = db.Column(db.Text, nullable=False) 
    agent_role = db.Column(db.String(255), nullable=False) 
    user_id = db.Column(db.BigInteger, nullable=False)

class tbl_stripe(db.Model):
    __tablename__ = 'tbl_stripe'

    stripe_id = db.Column(db.BigInteger, primary_key=True)  # Primary key column
    stripe_public_key = db.Column(db.Text, nullable=False)  # Not null
    stripe_secret_key = db.Column(db.Text, nullable=False )  # Not null
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)  # Default timestamp
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  # Updated timestamp


class Transaction(db.Model):
    __tablename__ = 'transaction' 
    
    id = db.Column(db.Integer, primary_key=True)
    payment_method_id = db.Column(db.String(255), nullable=False)
    receipt_email = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), default="usd")
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


def sendOTP(OTP,mailid):
    port = 587
    smtp_server = "smtp.zeptomail.com"
    username="emailapikey"
    password = zeptokey
    message = "Your OTP for Concceptive AI is "+ OTP +" . This is only for your private. Never share your OTP to unknown people over the phone or internet."
    msg = EmailMessage()
    msg['Subject'] = "Conceptiv AI - OTP"
    msg['From'] = "noreply@conceptiv.ai"
    msg['To'] = mailid
    msg.set_content(message)
    try:
        if port == 465:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(username, password)
                server.send_message(msg)
        elif port == 587:
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
        else:
            print ("use 465 / 587 as port value")
            return False
        print ("OTP Successfully Sent")
        return True
    except Exception as e:
        print (e)
        return False

# agent = TblAgent.query.first()
# print(agent)

  
with app.app_context(): 
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)