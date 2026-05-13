#!/bin/bash
# 1. Copy the structure from the example
cp .env.example .env

# 2. Ask for the Groq Key
echo "Please enter your GROQ_API_KEY:"
read -s GROQ_KEY

# 3. Inject the key into the live .env
sed -i "s/GROQ_API_KEY=.*/GROQ_API_KEY=$GROQ_KEY/" .env

echo ".env has been successfully generated for this session!"
