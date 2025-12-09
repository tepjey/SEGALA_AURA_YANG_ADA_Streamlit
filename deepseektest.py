from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load DeepSeek model in 4-bit mode for CPU
model_name = "deepseek-ai/deepseek-chat-1.3b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # Use float16 for better performance
    device_map="cpu",           # Run on CPU
    load_in_4bit=True           # Enable 4-bit quantization
)

# Store chat history (keeps last 5 messages)
chat_history = []

def chat_with_aura(user_input):
    global chat_history

    # System instruction for AURA
    system_message = (
        "You are AURA, an intelligent assistant designed to help users manage their studies, "
        "plan schedules, and improve productivity. You provide polite, concise, and accurate "
        "responses. Your tasks include creating study timetables, offering real-time feedback based "
        "on user emotions, assisting with event scheduling and offers personalized advice based on users mood. " 
        "Use user-provided context to generate specific and actionable suggestions. Adhere strictly to these guidelines:\n"
        "- Focus on students and academic success.\n"
        "- Be empathetic, understanding, and professional but casual.\n"
        "- Ensure responses are simple and easy to understand, avoiding technical jargon unless necessary.\n"
        "- Prioritize halal and ethical practices in any recommendations.\n"
        "Your goal is to act as a dedicated and helpful academic companion."
    )

    # Add user input to history
    chat_history.append(f"<|user|>{user_input}")

    # Limit memory to last 5 messages
    if len(chat_history) > 5:
        chat_history.pop(0)

    # Format conversation history
    conversation = f"<|system|>{system_message}" + "".join(chat_history) + "<|assistant|>"

    # Tokenize input
    inputs = tokenizer(conversation, return_tensors="pt").to("cpu")
    
    # Generate response
    output = model.generate(**inputs, max_length=200)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Add AURA's response to history
    chat_history.append(f"<|assistant|>{response}")

    return response

# Example chat
print(chat_with_aura("Hello AURA, can you help me study?"))
print(chat_with_aura("What did I ask earlier?"))  # AURA should remember!
