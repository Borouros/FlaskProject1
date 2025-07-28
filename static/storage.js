document.addEventListener("DOMContentLoaded", () => {
  const sortedKeys = [];

  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key.startsWith("userData_")) {
      sortedKeys.push(key);
    }
  }

  sortedKeys.sort();

  let entryCount = 1;
  for (const key of sortedKeys) {
    const entry = JSON.parse(localStorage.getItem(key));
    console.log(`Restored entry ${entryCount}:`, entry);
    entryCount++;
  }

  const form = document.getElementById("contactForm");
  const emailInput = document.getElementById("userEmail");
  const emailMessage = document.getElementById("message");
  const phoneInput = document.getElementById("userPhone");
  const phoneError = document.getElementById("phoneError");
  const saveBtn = document.getElementById("saveBtn");
  const clearBtn = document.getElementById("clearStorageBtn");

  const emailPattern = /^(?!.*\.\.)(?!\.)(?!.*\.$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/i;
  const phonePattern = /^(?=(?:\D*\d){6,17}\D*$)\+?\d{1,3}?[-.\s]?\(?\d{2,4}?\)?[-.\s]?\d{1,4}(?:[-.\s]?\d{1,4})*$/;


  if (emailInput && emailMessage) {
    emailInput.addEventListener("input", () => {
      const email = emailInput.value.trim();
      emailMessage.textContent = email === "" || emailPattern.test(email) ? "" : "Please enter a valid email address";
      emailMessage.style.color = "red";
    });

    emailInput.addEventListener("keydown", (e) => {
      const allowedEmailKeys = [
        "Backspace", "ArrowLeft", "ArrowRight", "Delete", "Tab",
        ".", "@", "_", "-", "+", "Home", "End"
      ];
      if (!allowedEmailKeys.includes(e.key) && !/[a-zA-Z0-9]/.test(e.key)) {
        e.preventDefault();
      }
    });
  }

  if (phoneInput && phoneError) {
    phoneInput.addEventListener("input", () => {
      const phone = phoneInput.value.trim();
      phoneError.textContent = phone === "" || phonePattern.test(phone) ? "" : "Please enter a valid phone number";
      phoneError.style.color = "red";
    });
  }

  if (phoneInput && phoneError) {
    phoneError.style.color = "red";

    phoneInput.addEventListener("keydown", (e) => {
      const allowedKeys = [
        "Backspace", "ArrowLeft", "ArrowRight", "Delete", "Tab",
        "+", "-", "(", ")", " ", "Home", "End"
      ];
      if (!allowedKeys.includes(e.key) && !(e.key >= "0" && e.key <= "9")) {
        e.preventDefault();
      }
    });

    phoneInput.addEventListener("input", function () {
      const isValid = phonePattern.test(this.value);
      phoneError.style.display = this.value === "" || isValid ? "none" : "block";
    });
  }

  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();

      const userName = document.getElementById("userName")?.value || "";
      const userEmail = emailInput?.value.trim() || "";
      const userPhone = phoneInput?.value.trim() || "";
      const userMessage = document.getElementById("userMessage")?.value || "";

      const isValidName = userName !== "";
      const isValidEmail = userEmail !== "" && emailPattern.test(userEmail);
      const isValidPhone = userPhone === "" || phonePattern.test(userPhone);
      const isValidMessage = userMessage !== "";


      if (!isValidName || !isValidEmail || !isValidMessage || !isValidPhone) {
        return;
      }

      const userData = {
        name: userName,
        email: userEmail,
        phone: userPhone,
        message: userMessage
      };

      const timestamp = Date.now();
      localStorage.setItem(`userData_${timestamp}`, JSON.stringify(userData));

      const successBox = document.createElement("div");
      successBox.textContent = "Thank you! Form submitted.";
      successBox.style.color = "green";
      successBox.style.fontWeight = "bold";
      successBox.style.margin = "1em 0";
      successBox.style.textAlign = "center";

      form.style.display = "none";
      form.after(successBox);

      setTimeout(() => {
        form.reset();
        successBox.remove();
        form.style.display = "block";
      }, 3000);
    });
  }

  if (saveBtn) {
    saveBtn.addEventListener("click", () => {
      const userName = document.getElementById("userName")?.value || "";
      const userEmail = emailInput?.value.trim() || "";
      const userPhone = phoneInput?.value.trim() || "";
      const userMessage = document.getElementById("userMessage")?.value || "";

      localStorage.setItem("hiddenName", userName);
      localStorage.setItem("hiddenEmail", userEmail);
      localStorage.setItem("hiddenPhone", userPhone);
      localStorage.setItem("hiddenMessage", userMessage);

      console.log(`Submission Summary:
      Name: ${userName}
      Email: ${userEmail}
      Phone: ${userPhone}
      Message: ${userMessage}`);
    });
  }

  window.enterDebugMode = (password) => {
    const correctPassword = "PortNewsThe";
    const clearBtn = document.getElementById("clearStorageBtn");

    if (password === correctPassword) {
      if (clearBtn) {
        clearBtn.style.display = "inline-block";
        sessionStorage.setItem("debugActive", "true");
        console.log("Debug mode activated. Clear button revealed.");
      }
    } else {
      console.warn("Incorrect password. Access denied.");
    }
  };

  window.leaveDebugMode = () => {
    const clearBtn = document.getElementById("clearStorageBtn");
    if (clearBtn) {
      clearBtn.style.display = "none";
      sessionStorage.removeItem("debugActive");
      console.log("Debug mode exited. Clear button hidden.");
    }
  };
  if (clearBtn) {
  clearBtn.addEventListener("click", () => {
    const debugToken = sessionStorage.getItem("debugActive");

    if (debugToken === "true") {
      const keysToRemove = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key.startsWith("userData_") || key.startsWith("hidden")) {
          keysToRemove.push(key);
        }
      }
      keysToRemove.forEach((key) => localStorage.removeItem(key));
      alert("All stored data has been cleared.");
    } else {
      console.warn("Access denied: Debug mode not enabled.");
    }
  });
}
});
