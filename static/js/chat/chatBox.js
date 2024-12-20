const stripePublishableKey = "{{ key }}";
const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const messagesContainer = document.getElementById('messages');
const userId = Number(localStorage.getItem('user_id'));
let companyId;
let context;
let agentIdNumber;

function appendMessage(content, sender = 'user') {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'agent-message');
  messageDiv.textContent = content;
  messagesContainer.appendChild(messageDiv);
  const chatWindow = document.getElementById('chat-window');
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

const agentId = document.getElementById('agent-id').getAttribute('data-agent-id');

function sendMessageToServer(message) {
  agentIdNumber = parseInt(agentId, 10);

  if (isNaN(agentIdNumber)) {
    console.error("Invalid agent_id:", agentId);
    return;
  }

  const agentRole = "{{ agent_role }}";

  fetch('/save-prompt', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      role: agentRole,
      prompt: message,
      agent_id: agentIdNumber,
    }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
        console.log(data.message);
        // After saving the prompt, send the message to /chat
        sendChatRequest(message);
      } else {
        console.error('Error:', data.error);
      }
    })
    .catch(error => {
      console.error('Error sending prompt:', error);
    });
}

function sendChatRequest(userMessage) {

  console.log('entered the send request chat function')
  fetch('/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: userMessage,
      user_id: userId,
      company_id: companyId,
      context: context,
      agent_id: agentIdNumber
    }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.reply) {
        console.log('AI Reply:', data.reply);
        appendMessage(data.reply, 'agent');
      } else {
        console.error('Error:', data.error);
      }
    })
    .catch(error => {
      console.error('Error sending chat request:', error);
    });
}

sendBtn.addEventListener('click', () => {
  const message = userInput.value.trim();
  if (message) {
    appendMessage(message, 'user');
    sendMessageToServer(message);
    userInput.value = '';
  }
});

userInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    sendBtn.click();
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const agentIdElement = document.getElementById('agent-id');
  const agentId = agentIdElement ? agentIdElement.dataset.agentId : null;

  console.log('this is the agen id ', agentId)
  if (agentId) {
    fetch('/getAdminContext', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ agent_id: 1 }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((result) => {
        context = result.data.prompt;
        companyId = result.data.company_id;
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  } else {
    console.warn('Agent ID not found in the DOM.');
  }
});
