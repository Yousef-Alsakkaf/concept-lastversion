document.addEventListener("DOMContentLoaded", () => {
  const userInput = document.getElementById("user-input");
  const chatMessages = document.getElementById("messages");
  const sendButton = document.getElementById("send-btn");
  const countdownElement = document.getElementById("countdown");
  const modal = document.getElementById("paymentModal");
  const emailModal = document.getElementById("email-modal");
  const emailSubmit = document.getElementById("extra-submit");
  const getOTP = document.getElementById("extra-get-otp");
  const extraEmail = document.getElementById("extra-email");
  const extraOtp = document.getElementById("login-otp");
  // const buyPremiumBtn = document.getElementById("buy-premium-btn");
  const chatWindow = document.getElementById("chat-window");
  const profilePicture =
    localStorage.getItem("profilePicture") || "default-avatar.png";
  const profileTitle = localStorage.getItem("profileTitle") || "Your Title";
  const profileDescription =
    localStorage.getItem("profileDescription") ||
    "Short description goes here...";
  const reviews = JSON.parse(localStorage.getItem("customerReviews") || "[]");

  let currentModal = emailModal; // Email Modal is Passing

  let isNewPremiumUser = localStorage.getItem("premiumUser") || false;
  let initialisedtimer = localStorage.getItem("initialisedtimer") || false;

  const FREE_USAGE_DURATION = 20 * 1000; // 10 minutes in milliseconds
  const EXTRA_TIME_DURATION = 20 * 1000; // 5 minutes in milliseconds
  const TIMER_KEY = "chat_start_time";

  const user_email = sessionStorage.getItem("userEmail");

  let countdownInterval = null;

  let receivedOTP = ""; // Variable to store the OTP from the response


  if((localStorage.getItem("initialisedtimer") || false)=='false'){
    currentModal = emailModal;
    localStorage.setItem("initialisedtimer",true);
  }

  // Disable OTP button initially
  getOTP.disabled = true;

  // Disable Submit button initially
  emailSubmit.disabled = true;

    // Enable the OTP button if an email ID is entered
    extraEmail.addEventListener("input", () => {
      getOTP.disabled = !extraEmail.value.trim(); // Disable if email field is empty
    });

    // Handle OTP generation
    getOTP.addEventListener("click", async () => {
      const email = extraEmail.value.trim();
      localStorage.setItem("usermail", email);

      if (email) {
        try {
          const response = await fetch("/generateotp", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: email }),
          });

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const data = await response.json();

          if (data.status === "success") {
            alert(data.message); // Notify user that OTP was sent
            receivedOTP = data.user.otp; // Save OTP from the response
            console.log(receivedOTP);    // DEBUGGING PURPOSE
          } else {
            alert("Failed to send OTP. Please try again.");
          }
        } catch (error) {
          console.error("Error sending OTP:", error);
          alert("An error occurred while sending OTP.");
        }
      } else {
        alert("Please enter a valid email ID.");
      }
    });

    // Enable the Submit button only if 6 digits are entered in the OTP field
    extraOtp.addEventListener("input", () => {
      const otpValue = extraOtp.value.trim();
      emailSubmit.disabled = otpValue.length !== 6; // Enable button if OTP length is 6
    });

    // Handle Submit button click
    emailSubmit.addEventListener("click", () => {
      const enteredOTP = extraOtp.value.trim();

      if (enteredOTP === receivedOTP) {
        alert("Email verified successfully!");
        hideemailModal();
      } else {
        alert("Incorrect OTP. Please try again.");
      }
    });
    


  // Initialize Timer
    function initializeTimer() {
      const now = Date.now();
      let startTime = localStorage.getItem(TIMER_KEY);

      if (!startTime) {
        startTime = now;
        localStorage.setItem(TIMER_KEY, startTime);
      }

      const elapsed = now - startTime;
      const remainingTime = Math.max(FREE_USAGE_DURATION - elapsed, 0);

      if (remainingTime <= 0) {
        showemailModal();
        console.log("Show Email Modal");
      } else {
        startCountdown(remainingTime);
      }
    }

    // Start Countdown
    function startCountdown(remainingTime) {
      clearInterval(countdownInterval); // Clear any previous intervals
      countdownInterval = setInterval(() => {
        if (remainingTime <= 0) {
          clearInterval(countdownInterval);
          localStorage.removeItem(TIMER_KEY); // Reset timer
          // console.log(currentModal); // Show what is it in currentModal
          if (currentModal === emailModal) {
            showemailModal();
          } else if (currentModal === modal) {
            showPremiumModal();
          }
        } else {
          remainingTime -= 1000;
          updateCountdownDisplay(remainingTime);
        }
      }, 1000);
    }


  // Update Countdown Display
  function updateCountdownDisplay(remainingTime) {
    const minutes = Math.floor(remainingTime / 60000);
    const seconds = Math.floor((remainingTime % 60000) / 1000);
    countdownElement.textContent = `${minutes}:${seconds
      .toString()
      .padStart(2, "0")}`;
  }

  // Reset Timer and Hide Modal
  function resetTimer(newduration) {
    console.log("Timer Value is: " + newduration);
    const now = Date.now();
    localStorage.setItem(TIMER_KEY, now); // Reset timer to the current time
    // hidePremiumModal();
    // startCountdown(FREE_USAGE_DURATION); // Restart countdown
    startCountdown(newduration * 10 * 1000);
    alert("Thanks for Signup, Enjoy your Free Credits");
  }
    // Show Email Modal
    function showemailModal() {
      emailModal.style.display = "flex";
      document.body.style.overflow = "hidden"; // Prevent scrolling
    }
  
    // Hide Email Modal and Add Extra Time
    function hideemailModal() {
      emailModal.style.display = "none";
      document.body.style.overflow = "auto"; // Restore scrolling
  
      // Add extra time to the timer
      const now = Date.now();
      localStorage.setItem(TIMER_KEY, now); // Reset timer
      startCountdown(EXTRA_TIME_DURATION);
      
      if (currentModal == emailModal) {
        resetTimer(5); 
        currentModal = modal;
      }
    }

  // Show Premium Modal
  function showPremiumModal() {
    currentModal.style.display = "flex";
    document.body.style.overflow = "hidden"; // Prevent scrolling
  }

  // Hide Premium Modal
  function hidePremiumModal() {
    currentModal.style.display = "none";
    document.body.style.overflow = "auto"; // Restore scrolling
    if (currentModal == emailModal) {
      resetTimer(20);
      currentModal = modal;
    }
    if((localStorage.getItem("premiumremaining")||false)=='true'){
      localStorage.setItem("premiumremaining",false);
    }
    console.log('Hide Premium Modal is triggered');
  }

  // Update DOM elements
  document.getElementById("profile-picture").src = profilePicture;
  document.getElementById("profile-title").textContent = profileTitle;
  document.getElementById("profile-description").textContent =
    profileDescription;

  // Add reviews to the list
  const reviewsList = document.getElementById("reviews-list");
  reviews.forEach((review) => {
    const listItem = document.createElement("li");
    listItem.textContent = review;
    reviewsList.appendChild(listItem);
  });

  // **********************************
  // Split long messages into chunks
  //***********************************
  function splitMessage(message) {
    const MAX_LENGTH = 120; // Maximum allowed length per chunk

    // Split by sentence boundaries or start of numbered list items
    const sentences = message.split(/(?<=\.\s)|(?=\d\.\s)/);

    let chunks = [];
    let currentChunk = "";

    sentences.forEach((sentence, index) => {
      sentence = sentence.trim(); // Remove leading and trailing spaces

      if (/^\d\.\s/.test(sentence)) {
        // If it's a numbered list item, finalize the current chunk
        if (currentChunk.length > 0) {
          chunks.push(currentChunk.trim());
        }
        currentChunk = sentence; // Start a new chunk with the numbered item
      } else if (currentChunk.match(/^\d\.\s/)) {
        // Append content to the current numbered list item
        currentChunk += " " + sentence;
      } else if (currentChunk.length + sentence.length > MAX_LENGTH) {
        // If the chunk exceeds the max length, finalize it
        chunks.push(currentChunk.trim());
        currentChunk = sentence; // Start a new chunk
      } else {
        // Otherwise, append the sentence to the current chunk
        currentChunk += (currentChunk ? " " : "") + sentence;
      }

      // Finalize the last chunk
      if (index === sentences.length - 1 && currentChunk) {
        chunks.push(currentChunk.trim());
      }
    });

    return chunks;
  }

  // Update Chatbot Title
  const updateChatboxTitle = () => {
    const botName = localStorage.getItem("customPromptName") || "Bot";
    document.getElementById("chat-title").textContent = botName;
    // document.getElementById("chat-title").textContent = "Conceptive";
  };

  // Function to append a message with the chatbot's custom name
  function appendMessage(text, sender, isFirstMessage = false) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);

    if (sender === "bot" && isFirstMessage) {
      const nameSpan = document.createElement("span");
      nameSpan.classList.add("name");
      // Dynamically set the bot's name from localStorage
      nameSpan.textContent = localStorage.getItem("customPromptName") || "Bot";
      // nameSpan.textContent = "Conceptive";
      messageDiv.appendChild(nameSpan);
    }

    //Create Bubble Div
    const bubbleDiv = document.createElement("div");
    bubbleDiv.classList.add("bubble");
    bubbleDiv.textContent = text;

    messageDiv.appendChild(bubbleDiv);
    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTo({
      top: chatMessages.scrollHeight,
      behavior: "smooth",
    });

    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  // Add Typing Indicator
  function addTypingIndicator() {
    const typingDiv = document.createElement("div");
    typingDiv.classList.add("message", "bot", "typing-indicator");
    typingDiv.innerHTML = `
            <div class="bubble">
                <span class="dots"><span>.</span><span>.</span><span>.</span></span>
            </div>
        `;
    chatMessages.appendChild(typingDiv);

    const chatWindow = document.getElementById("chat-window");
    chatWindow.scrollTop = chatWindow.scrollHeight;
    // console.log("Wroking")
  }

  // Remove Typing Indicator
  function removeTypingIndicator() {
    const typingDiv = document.querySelector(".typing-indicator");
    if (typingDiv) typingDiv.remove();
  }

  // Append Message with Delay
  function appendMessageWithDelay(
    text,
    sender,
    typingDelay = 0,
    showTitle = false
  ) {
    const messageChunks = splitMessage(text); // Split the message into chunks
    let totalDelay = 0;

    // Ensure only one typing indicator is visible
    const manageTypingIndicator = (action) => {
      if (action === "add") {
        if (!document.querySelector(".typing-indicator")) {
          addTypingIndicator();
        }
      } else if (action === "remove") {
        removeTypingIndicator();
      }
    };

    messageChunks.forEach((chunk, index) => {
      // chatWindow.scrollTop = chatWindow.scrollHeight;
      // Show typing indicator for the duration proportional to the chunk length
      setTimeout(() => {
        manageTypingIndicator("add");
        const chatWindow = document.getElementById("chat-window");
        chatWindow.scrollTop = chatWindow.scrollHeight;
      }, totalDelay);

      // Remove typing indicator and show the message
      setTimeout(() => {
        manageTypingIndicator("remove");
        if (chunk.length > 0) {
          if (index === 0 && sender === "bot" && showTitle) {
            appendMessage(chunk, sender, true); // Show title for the first chunk if required
            const chatWindow = document.getElementById("chat-window");
            chatWindow.scrollTop = chatWindow.scrollHeight;
          } else {
            appendMessage(chunk, sender);
            const chatWindow = document.getElementById("chat-window");
            chatWindow.scrollTop = chatWindow.scrollHeight;
          }
        }
      }, totalDelay + 30 * chunk.length);

      // Increment delay to handle the next chunk
      totalDelay += 30 * chunk.length + typingDelay;
    });

    // Clean up the last typing indicator
    setTimeout(() => {
      manageTypingIndicator("remove");
    }, totalDelay);
  }

  // Function to send user messages to the bot
  function sendMessage() {
    const userText = userInput.value.trim();
    if (!userText) return; // Do nothing if the input is empty

    appendMessage(userText, "user");
    userInput.value = ""; // Clear the input field
    addTypingIndicator();
    const chatWindow = document.getElementById("chat-window");
    chatWindow.scrollTop = chatWindow.scrollHeight;

    fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: userText,
        user_id: localStorage.getItem("user_id"),
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(
            `Failed to fetch response. Status: ${response.status}`
          );
        }
        return response.json();
      })
      .then((data) => {
        removeTypingIndicator();
        appendMessageWithDelay(data.reply, "bot", 300, true);
      })
      .catch((error) => {
        removeTypingIndicator();
        appendMessage(
          "Sorry, something went wrong. Please try again later.",
          "bot"
        );
      });
  }

  // Event listeners
  sendButton.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });


  

  // buyPremiumBtn.addEventListener("click", function () {
  //   fetch("/create-checkout-session", {
  //     method: "POST",
  //   })
  //     .then(function (response) {
  //       return response.json();
  //     })
  //     .then(function (sessionId) {
  //       return stripe.redirectToCheckout({ sessionId: sessionId.id });
  //     })
  //     .then(function (result) {
  //       if (result.error) {
  //         alert(result.error.message);
  //       }
  //     })
  //     .catch(function (error) {
  //       console.error("Error:", error);
  //     });
  //   resetTimer(30);
  // });

  
  
  // Fetch the initial bot message on page load
  function fetchInitialMessage() {
    addTypingIndicator();

    fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: "hi",
        user_id: localStorage.getItem("user_id"),
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(
            `Failed to fetch initial message. Status: ${response.status}`
          );
        }
        return response.json();
      })
      .then((data) => {
        removeTypingIndicator();
        appendMessageWithDelay(data.reply, "bot", 0, true);
      })
      .catch((error) => {
        removeTypingIndicator();
        appendMessage(
          "Sorry, something went wrong. Please try again later.",
          "bot"
        );
      });
  }

  updateChatboxTitle();
  fetchInitialMessage();
  initializeTimer();

  isNewPremiumUser = localStorage.getItem("premiumUser")||false;


  if(localStorage.getItem("premiumUser")=='true'){
    if((localStorage.getItem("premiumremaining")||false)=='true'){
      hidePremiumModal();
      resetTimer(20);
    }
    localStorage.setItem("premiumUser",false);
  }


      /***************************************** 
                CUSTOMIZATION OPTIONS
      ******************************************/

      function updateColorScheme(newColor) {
        // Replace all occurrences of #673ab7 with the new color
        document.querySelectorAll('*').forEach(element => {
            const computedStyle = window.getComputedStyle(element);

            // Update background color
            if (computedStyle.backgroundColor === 'rgb(103, 58, 183)') {
                element.style.backgroundColor = newColor;
            }

            // Update border color
            if (computedStyle.borderColor === 'rgb(103, 58, 183)') {
                element.style.borderColor = newColor;
            }

            // Update text color
            if (computedStyle.color === 'rgb(103, 58, 183)') {
                element.style.color = newColor;
            }
        });

        // Adjust other complementary colors for better matching
        const complementaryColor = adjustColorBrightness(newColor, 0.5); // Slightly brighter
        const darkerColor = adjustColorBrightness(newColor, -0.5); // Slightly darker

        document.querySelectorAll('.nav-item').forEach(item => {
            item.style.backgroundColor = complementaryColor;
            item.style.color = darkerColor;
        });

        document.querySelectorAll('.bubble').forEach(bubble => {
            bubble.style.backgroundColor = complementaryColor;
            bubble.style.color = darkerColor;
        });
    }

    // Helper function to adjust brightness of a hex color
    function adjustColorBrightness(hex, factor) {
        const [r, g, b] = hexToRgb(hex);
        const newR = Math.min(255, Math.max(0, r + Math.round(255 * factor)));
        const newG = Math.min(255, Math.max(0, g + Math.round(255 * factor)));
        const newB = Math.min(255, Math.max(0, b + Math.round(255 * factor)));
        return rgbToHex(newR, newG, newB);
    }

    // Convert hex to RGB
    function hexToRgb(hex) {
        const bigint = parseInt(hex.replace('#', ''), 16);
        return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255];
    }

    // Convert RGB to hex
    function rgbToHex(r, g, b) {
        return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
    }
      
    // Pass the Value to the "UpdateColorScheme" function
    updateColorScheme(localStorage.getItem("uicolor")||"#673ab7");

      /***************************************** 
              CUSTOMIZATION OPTIONS END
      ******************************************/

   
});


