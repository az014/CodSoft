# Basic rule-based chatbot using Python

def chatbot_response(user_input):
    # Convert the input to lowercase for case insensitivity
    user_input = user_input.lower()

    # Dictionary to handle greetings
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    greeting_responses = ["Hey!", "Hello there!", "Hi, how can I help you?", "Good to see you!"]

    # Responses for basic queries
    basic_knowledge = {
        "what's your name?": "I'm your chatbot assistant.",
        "how are you?": "I'm just a bot, but I'm here to help you!",
        "what can you do?": "I can help with basic queries, calculations, weather, and more."
    }

    # Math calculations
    if "calculate" in user_input:
        try:
            result = eval(user_input.replace("calculate", ""))
            return f"The result is {result}."
        except:
            return "Sorry, I couldn't calculate that. Please try again."

    # Weather response (static for rule-based chatbot, dynamic in real scenario)
    if "weather" in user_input:
        return "The weather today is sunny with a high of 25°C."

    # Handling greetings
    if user_input in greetings:
        return greeting_responses[greetings.index(user_input) % len(greeting_responses)]

    # Basic knowledge responses
    for question, answer in basic_knowledge.items():
        if question in user_input:
            return answer

    # Default response if no rule matches
    return "I'm not sure about that, but I'm learning!"

# Simulating a conversation
while True:
    user_message = input("You: ")
    if user_message.lower() == "exit":
        print("Goodbye!")
        break
    print("Chatbot:", chatbot_response(user_message))
