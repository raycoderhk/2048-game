#!/usr/bin/env python3
"""
Hello World Program
Created by: Coding Agent (via Jarvis)
Date: 2026-02-26
Task: Test sub-agent functionality
"""

def greet_user():
    """Greet the user with a personalized message"""
    print("=" * 50)
    print("👋 Hello World Program!")
    print("=" * 50)
    print()
    
    # Get user's name
    name = input("What's your name? ").strip()
    
    if name:
        print()
        print(f"🌟 Welcome, {name}!")
        print()
        print("This is a simple Python program that demonstrates:")
        print("  ✓ Basic input/output")
        print("  ✓ String formatting")
        print("  ✓ Functions")
        print()
        print(f"Nice to meet you, {name}! Have a great day! 🎉")
    else:
        print()
        print("🌍 Hello, World!")
        print()
        print("No name provided, but that's okay!")
        print("The classic Hello World still works! 😊")
    
    print()
    print("=" * 50)

if __name__ == "__main__":
    greet_user()
