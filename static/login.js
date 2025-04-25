    import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-app.js";
    import { getAuth, signOut } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-auth.js";

    const firebaseConfig = {
      apiKey: "AIzaSyDXAxuf8tgTOQEFXviWPImkoWvhUczVBm0",
      authDomain: "jobassistant-8b080.firebaseapp.com",
      projectId: "jobassistant-8b080",
      storageBucket: "jobassistant-8b080.appspot.com",
      messagingSenderId: "307661761493",
      appId: "1:307661761493:web:882130080b36325feb2b5c"
    };

    const app = initializeApp(firebaseConfig);
    const auth = getAuth(app);

    window.logoutUser = function () {
      signOut(auth).then(() => {
        alert("Successfully logged out!");
        window.location.href = "/";
      }).catch((error) => {
        alert("Error logging out: " + error.message);
      });
    };