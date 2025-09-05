// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

// Your Firebase Configuration
const firebaseConfig = {
  apiKey: "AIzaSyDW5m3f-LcgTotUEBG4-z2aLr9Ri2JNJZ0",
  authDomain: "edss-f657a.firebaseapp.com",
  projectId: "edss-f657a",
  storageBucket: "edss-f657a.appspot.com",
  messagingSenderId: "247327625316",
  appId: "1:247327625316:web:d07d720f958ee189664f71",
  measurementId: "G-2HZ2QL6HGW"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app); // Initialize Firestore

export { db };