import kagglehub

# Download latest version
path = kagglehub.dataset_download("bitext/bitext-gen-ai-chatbot-customer-support-dataset")

print("Path to dataset files:", path)