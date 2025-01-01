# User Interaction Service

The **User Interaction Service** acts as the user-facing entry point to the weather system. It accepts user input (e.g., city name), forwards the request to the **Weather Analysis Service**, and returns weather insights.

---

## Features

- Accepts user requests with city names.
- Forwards requests to the **Weather Analysis Service**.
- Returns weather data and actionable insights.
- Health check endpoint for monitoring service status.

---

## Endpoints

### **Interact**
- **URL**: `/interact`
- **Method**: `POST`
- **Description**: Accepts a city name and returns weather insights.
- **Request Body**:
  ```json
  {
    "city": "chicago"
  }
