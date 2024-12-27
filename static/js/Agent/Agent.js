document.addEventListener("DOMContentLoaded", () => {
  const agentCards = document.querySelectorAll(
    ".agent-card input[type='radio']"
  );
  // const fields = [
  //   "name",
  //   "persona",
  //   "purpose",
  //   "attitude",
  //   "uniquetraits",
  //   "limitations",
  //   "agent-profile-picture",
  //   "agent-profile-name",
  //   "agent-profile-description",
  //   "agent-profile-reviews",
  // ];

  const fields = Array.from(document.querySelectorAll("#custom-fields-container label"))
    .map(label => label.getAttribute("for"));
   function redirectToAgentPage(agentId) {
      const agentPageUrl = `/agent-prom?agentId=${encodeURIComponent(
        agentId
      )}`;

      window.location.href = agentPageUrl;
    }
  const savedcustompropt = "customPromptKey";

  const agentData = {
    Josephine: {
      name: "Josephine",
      persona: "Expert Healthcare Advisor",
      purpose: "Health Guidance",
      attitude: "Empathetic",
      uniquetraits: "Warm, Friendly",
      limitations: "Be Polite",
      "agent-profile-picture": "static/Assets/Josephine DP.png",
      "agent-profile-name": "Josephine",
      "agent-profile-description":
        "An expert healthcare advisor here to help you!",
      "agent-profile-reviews":
        "⭐ Excellent service!,⭐ Very professional,⭐ Highly recommended.",
      "agent-ui-color": "#673ab7",
    },
    Jasmine: {
      name: "Jasmine",
      persona: "Tech Support Specialist",
      purpose: "Tech Support",
      attitude: "Professional",
      uniquetraits: "Detail-oriented",
      limitations: "Be Polite",
      "agent-profile-picture": "static/Assets/Jasmine DP.png",
      "agent-profile-name": "Jasmine",
      "agent-profile-description": "Solving your tech needs always",
      "agent-profile-reviews":
        "⭐ Excellent service!,⭐ Very professional,⭐ Highly recommended.",
      "agent-ui-color": "#eb6534",
    },
    Tony: {
      name: "Tony",
      persona: "Marketing Expert",
      purpose: "Business Growth",
      attitude: "Charismatic",
      uniquetraits: "Strategic Thinker",
      limitations: "Be Polite",
      "agent-profile-picture": "static/Assets/Tony DP.png",
      "agent-profile-name": "Tony",
      "agent-profile-description": "Your own expert business guru",
      "agent-profile-reviews":
        "⭐ Excellent service!,⭐ Very professional,⭐ Highly recommended.",
      "agent-ui-color": "#8c7116",
    },
    agent4: {
      name: "Agent 4",
      persona: "",
      purpose: "",
      attitude: "",
      uniquetraits: "coming soon",
    },
    agent5: {
      name: "Agent 5",
      persona: "",
      purpose: "",
      attitude: "",
      uniquetraits: "coming soon",
    },
  };

  // document.getElementById("create-new-agent").addEventListener("click", () => {
  //   // Select all input fields and labels under #promptarea
  //   const promptArea = document.getElementById("promptarea");
  //   const inputs = Array.from(promptArea.querySelectorAll("textarea, input"));
  //   const labels = Array.from(promptArea.querySelectorAll("label"));
  //   const infoIcons = Array.from(promptArea.querySelectorAll(".info-icon"));

  //   // Clear input fields and disable placeholders, skipping the first field
  //   inputs.slice(1).forEach(input => {
  //     input.value = "";
  //     input.placeholder = ""; // Clear the placeholder
  //   });

  //   // Make labels editable, skipping the first label
  //   labels.slice(1).forEach(label => {
  //     label.contentEditable = true;
  //     label.style.border = "1px dashed #673ab7"; // Optional visual cue
  //     label.style.padding = "2px";

  //     // Remove 'for' attribute to prevent focusing on input
  //     label.removeAttribute("for");
  //   });

  //   // Disable info icons, skipping the first icon
  //   infoIcons.slice(1).forEach(icon => {
  //     icon.style.pointerEvents = "none"; // Disable interaction
  //     icon.style.opacity = "0.5"; // Visual feedback for disabled state
  //   });

  //   localStorage.setItem("customPromptName", "Conceptive");

  //   alert("You can now edit labels and start creating a new agent!");
  // });

  // function resetCustomization() {
  //   const promptArea = document.getElementById("promptarea");
  //   const inputs = promptArea.querySelectorAll("textarea, input");
  //   const labels = promptArea.querySelectorAll("label");
  //   const infoIcons = promptArea.querySelectorAll(".info-icon");
/*
    // Reset placeholders
    inputs.forEach(input => {
      const label = promptArea.querySelector(`label[for='${input.id}']`);
      if (label) {
        input.placeholder = `Enter ${label.textContent.trim()}`; // Restore placeholder dynamically
      }
    });

    // Reset labels to non-editable state
    labels.forEach(label => {
      const fieldId = label.textContent.trim().toLowerCase().replace(/\s+/g, "-");
      const input = document.querySelector(`#${fieldId}`);
      if (input) {
        label.setAttribute("for", fieldId);
      }
      label.contentEditable = false;
      label.style.border = ""; // Remove visual cue
      label.style.padding = "";
    });

    // Re-enable info icons
    infoIcons.forEach(icon => {
      icon.style.pointerEvents = ""; // Enable interaction
      icon.style.opacity = "1"; // Restore visibility
    });
  }

  document.querySelectorAll('.info-icon').forEach((icon) => {
    icon.addEventListener('mouseenter', () => {
      // Get the title attribute value
      const titleText = icon.getAttribute('title');

      if (!titleText) return;

      // Remove the title attribute to disable the default tooltip
      icon.setAttribute('data-title', titleText);
      icon.removeAttribute('title');

      // Create and display the custom tooltip
      const tooltip = document.createElement('div');
      tooltip.className = 'tooltip';
      tooltip.textContent = titleText;
      document.body.appendChild(tooltip);

      // Calculate dimensions and position
      const iconRect = icon.getBoundingClientRect();
      const tooltipRect = tooltip.getBoundingClientRect();

      let top = iconRect.top + (iconRect.height - tooltipRect.height) / 2;
      let left = iconRect.right + 10;

      // Adjust for viewport boundaries
      if (left + tooltipRect.width > window.innerWidth) {
        left = iconRect.left - tooltipRect.width - 10;
      }

      if (top < 0) {
        top = 10;
      } else if (top + tooltipRect.height > window.innerHeight) {
        top = window.innerHeight - tooltipRect.height - 10;
      }

      tooltip.style.top = `${top}px`;
      tooltip.style.left = `${left}px`;

      // Allow the tooltip to resize based on content
      tooltip.style.width = 'auto';
      tooltip.style.height = 'auto';
    });

    icon.addEventListener('mouseleave', () => {
      // Restore the title attribute
      const titleText = icon.getAttribute('data-title');
      if (titleText) {
        icon.setAttribute('title', titleText);
        icon.removeAttribute('data-title');
      }

      // Remove the custom tooltip
      const tooltip = document.querySelector('.tooltip');
      if (tooltip) tooltip.remove();
    });
  });
*/

  // const updateChatboxTitle = () => {
  //     const botName = localStorage.getItem("customPromptName") || "Bot";
  //     document.getElementById("chat-title").textContent = botName;
  // };

  // Populate saved fields from localStorage on page load
  fields.forEach((field) => {
    const input = document.getElementById(field);
    input.value = localStorage.getItem(field) || "";
    input.addEventListener("input", () => {
      localStorage.setItem(field, input.value);

      // Update bot name dynamically if the "name" field changes
      if (field === "name") {
        localStorage.setItem("customPromptName", input.value || "Bot");
        // updateChatboxTitle();
      }
    });
  });

  // Update fields and store selected bot name when an agent is selected
  agentCards.forEach((card) => {
    card.addEventListener("change", () => {
      const selectedAgent = card.value;
      const data = agentData[selectedAgent] || {};

      // Save the bot name for use in the chat interface
      localStorage.setItem("customPromptName", data.name || "Bot");
      // updateChatboxTitle();
      // resetCustomization();

      fields.forEach((field) => {
        const input = document.getElementById(field);
        input.value = data[field] || "";
        localStorage.setItem(field, data[field] || "");
      });
    });
  });

  document.querySelectorAll('input[type="radio"]').forEach((radio) => {
    radio.addEventListener("click", () => {
      const button = document.querySelector(".save-button");
      button.scrollIntoView({
        behavior: "smooth", // Smooth scrolling effect
        block: "center", // Align the button to the center of the viewport
      });
    });
  });

  // Submit handler
  document
    .getElementById("agent-selection-form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      const userId = localStorage.getItem("user_id");
      if (!userId) {
        alert("User not logged in. Please log in again.");
        window.location.href = "/";
        return;
      }

      const profilePicture =
        document.getElementById("agent-profile-picture").value ||
        "https://via.placeholder.com/150";
      const profileName =
        document.getElementById("agent-profile-name").value ||
        localStorage.getItem("name") ||
        "Agent Name";
      const profileDescription =
        document.getElementById("agent-profile-description").value ||
        localStorage.getItem("persona") ||
        "Title";
      const profileReviewsInput =
        document.getElementById("agent-profile-reviews").value ||
        "Excellent service!,Very professional.,Highly recommended.";
      const profileReviews = profileReviewsInput
        .split(",")
        .map((review) => review.trim());
      const uicolor =
        document.getElementById("agent-ui-color").value ||
        "#673ab7";

      // Save to localStorage
      localStorage.setItem("profilePicture", profilePicture);
      localStorage.setItem("profileTitle", profileName);
      localStorage.setItem("profileDescription", profileDescription);
      localStorage.setItem("customerReviews", JSON.stringify(profileReviews));
      localStorage.setItem("uicolor", uicolor);

      // // Create a custom prompt string for submission
      // const customPrompt = fields
      //     .map(field => {
      //         const value = document.getElementById(field).value;
      //         return value ? `Your ${field} is ${value}.` : null;
      //     })
      //     .filter(Boolean) // Remove null or undefined values
      //     .join(" ");

      // Create a custom prompt string for submission
      const customPrompt = fields
            .slice(0, 6) // Take only the first 6 fields
            .map((field) => {
              const value = document.getElementById(field).value;
              return value ? `Your ${field} is ${value}.` : null;  // Return a string or null
            })
            .filter(Boolean) // Remove null or undefined values
            .join(" "); // Join the non-null values with a space


      if (!customPrompt) {
        alert("Please fill at least one field to create a custom prompt.");
        return;
      }

      const prevsavedcustompropt =
        localStorage.getItem(savedcustompropt) || null;
      const payload = {
        user_id: userId,
        localprompt: prevsavedcustompropt,
        customprompt: customPrompt,
      };

      try {
        const response = await fetch("/prompt", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (response.ok) {
          alert("Prompt updated successfully!");
          localStorage.setItem(savedcustompropt, customPrompt);
          window.location.href = "/home";
        } else {
          const errorData = await response.json();
          // alert("Error: " + errorData.error);
          console.log("Error: " + errorData.error);
        }
      } catch (error) {
        console.error("Error:", error);
        alert("Failed to update the prompt.");
      }
    });
});
