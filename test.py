# Retrieve the system prompt from tbl_agent
def get_system_prompt(agent_id):
    prompt = db_session.query(tbl_agent).filter_by(agent_id=agent_id).first().prompt
    return prompt

# Retrieve conversation history from tbl_chatinteraction
def get_conversation_history(user_id, agent_id):
    history = db_session.query(tbl_chatinteraction).filter_by(user_id=user_id, agent_id=agent_id).all()
    return [{'role': 'user', 'content': record.user_question} for record in history] + \
           [{'role': 'assistant', 'content': record.ai_response} for record in history]

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
        session = (
                    db.session.query(tbl_prompt)
                    .filter((tbl_prompt.user_id == user_id) & (tbl_prompt.agent_id == agent_id))
                    .order_by(desc(tbl_prompt.created_at))
                    .first()
                  )
        
        if session:
            # Access specific fields
            print("User ID:", session.user_id)                # DEBUGGING PURPOSE
            print("Agent ID:", session.agent_id)              # DEBUGGING PURPOSE
            print("Created At:", session.created_at)          # DEBUGGING PURPOSE
            print("Prompt Is:", session.prompt)                # DEBUGGING PURPOSE
        else:   
            print("No record found.")                               # DEBUGGING PURPOSE

        my_agent_prompt = session.prompt if session else None  
                              
        if not session:
            print("Session not initialized")
            return jsonify({"error": "Session not initialized. Please set up a custom prompt first."}), 400

        
        session_history = [
            {"role": "system", "content":session.prompt},
            {"role": "user", "content":user_message}
        ] 
        print("Session history:", session_history)

        # Correct usage of openai.chat.completions.create
        response =  openai.chat.completions.create(
            model="gpt-4o-mini",  # Use the desired model
            messages=session_history
        )
        ai_response = response.choices[0].message.content.strip()
        # print(type(ai_response),"<==type of ai_response")                    # DEBUGGING PURPOSE
        # print("AI Response:", ai_response)                                   # DEBUGGING PURPOSE

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


        return jsonify({"reply": ai_response }), 200

    except Exception as e:
        print("Error in /chat:", str(e))
        return jsonify({"error": str(e)}), 500
