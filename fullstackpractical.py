mkdir student-api
cd student-api
npm init -y
npm install express


Create server.js and paste this code.

const express = require("express");
const app = express();

app.use(express.json());

let students = [];
let nextId = 1;

// POST: Create student
app.post("/students", (req, res) => {
  const { name, email, age } = req.body || {};

  if (
    typeof name !== "string" ||
    !name.trim() ||
    typeof email !== "string" ||
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim()) ||
    !Number.isInteger(age) ||
    age <= 0
  ) {
    return res.status(400).json({ error: "Invalid input" });
  }

  if (
    students.some(
      s => s.email.toLowerCase() === email.trim().toLowerCase()
    )
  ) {
    return res.status(409).json({
      error: "Email already exists"
    });
  }

  const student = {
    id: nextId++,
    name: name.trim(),
    email: email.trim(),
    age
  };

  students.push(student);
  res.status(201).json(student);
});

// GET: List all students or filter by minAge
app.get("/students", (req, res) => {
  const { minAge } = req.query;

  if (
    minAge !== undefined &&
    (minAge.trim() === "" ||
      !Number.isFinite(Number(minAge)) ||
      Number(minAge) < 0)
  ) {
    return res.status(400).json({ error: "Invalid input" });
  }

  const result =
    minAge === undefined
      ? students
      : students.filter(s => s.age >= Number(minAge));

  res.status(200).json(result);
});

// GET: Fetch student by ID
app.get("/students/:id", (req, res) => {
  const id = Number(req.params.id);
  const student = students.find(s => s.id === id);

  if (!Number.isSafeInteger(id) || id < 1 || !student) {
    return res.status(404).json({
      error: "Student not found"
    });
  }

  res.status(200).json(student);
});

// DELETE: Delete student by ID
app.delete("/students/:id", (req, res) => {
  const id = Number(req.params.id);
  const index = students.findIndex(s => s.id === id);

  if (!Number.isSafeInteger(id) || id < 1 || index === -1) {
    return res.status(404).json({
      error: "Student not found"
    });
  }

  students.splice(index, 1);
  res.status(204).end();
});

// Invalid JSON handler
app.use((err, req, res, next) => {
  if (err instanceof SyntaxError && err.status === 400) {
    return res.status(400).json({ error: "Invalid input" });
  }
  next(err);
});

app.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});



Run the server:
node server.js


Example POST request body:
{
  "name": "Rahul",
  "email": "rahul@example.com",
  "age": 20
}


Expected response: 201 Created
{
  "id": 1,
  "name": "Rahul",
  "email": "rahul@example.com",
  "age": 20
}


Practical A2: React Feedback Form with Validation
Create a React project:
npm create vite@latest feedback-app -- --template react
cd feedback-app
npm install
npm run dev


Create src/FeedbackForm.jsx and paste this code.

import React, { useState } from "react";

export default function FeedbackForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [rating, setRating] = useState("");
  const [comment, setComment] = useState("");
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();

    const newErrors = {};

    if (!name.trim()) {
      newErrors.name = "Name is required";
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      newErrors.email = "Enter a valid email";
    }

    if (!["1", "2", "3", "4", "5"].includes(rating)) {
      newErrors.rating = "Please select a rating";
    }

    if (!comment.trim()) {
      newErrors.comment = "Comment is required";
    }

    setErrors(newErrors);
    setSuccess(false);

    if (Object.keys(newErrors).length === 0) {
      setSuccess(true);
    }
  }

  return (
    <div>
      <h2>Course Feedback Form</h2>

      {success && (
        <p role="status" data-testid="success-message">
          Thank you! Your feedback has been submitted successfully.
        </p>
      )}

      <form onSubmit={handleSubmit} noValidate>
        <label htmlFor="name">Name:</label>
        <input
          id="name"
          type="text"
          data-testid="name-input"
          value={name}
          onChange={e => setName(e.target.value)}
        />
        {errors.name && <p role="alert">{errors.name}</p>}

        <label htmlFor="email">Email:</label>
        <input
          id="email"
          type="email"
          data-testid="email-input"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        {errors.email && <p role="alert">{errors.email}</p>}

        <label htmlFor="rating">Rating:</label>
        <select
          id="rating"
          data-testid="rating-select"
          value={rating}
          onChange={e => setRating(e.target.value)}
        >
          <option value="">Select rating</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
        {errors.rating && <p role="alert">{errors.rating}</p>}

        <label htmlFor="comment">Comment:</label>
        <textarea
          id="comment"
          data-testid="comment-input"
          value={comment}
          onChange={e => setComment(e.target.value)}
        />
        {errors.comment && <p role="alert">{errors.comment}</p>}

        <button type="submit">Submit Feedback</button>
      </form>
    </div>
  );
}



In src/App.jsx, use the component:

import FeedbackForm from "./FeedbackForm";

export default function App() {
  return <FeedbackForm />;
}