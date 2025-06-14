#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from voiceboard.crew import Voiceboard

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information



def run():
    """
    Run the full Voiceboard crew workflow for startup idea evaluation.
    """
    # Example startup idea - in production, this would come from user input
    startup_idea = "An AI-powered personal finance app that analyzes spending patterns and provides automated investment recommendations"
    
    inputs = {
        'startup_idea': startup_idea,
        'current_year': str(datetime.now().year)
    }
    
    try:
        print("🚀 Starting Voiceboard crew for startup idea evaluation...")
        print(f"💡 Startup Idea: {startup_idea}")
        print("\n" + "="*80 + "\n")
        
        # Run the initial setup (persona identification + voice research)
        voiceboard = Voiceboard()
        result = voiceboard.run_initial_setup(startup_idea)
        
        print("✅ Voiceboard crew execution completed!")
        print("\n📋 Results:")
        print(result)
        
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def interactive():
    """
    Run an interactive session where users can have conversations with selected personas.
    """
    try:
        print("🎯 Welcome to Voiceboard - Interactive Startup Evaluation!")
        print("="*60)
        
        # Get startup idea from user
        startup_idea = input("\n💡 Describe your startup idea: ")
        
        if not startup_idea.strip():
            print("❌ Please provide a startup idea to continue.")
            return
            
        print(f"\n🔍 Analyzing your idea: {startup_idea}")
        print("⏳ Finding relevant critical personas and researching their voices...")
        
        # Initialize Voiceboard and run setup
        voiceboard = Voiceboard()
        setup_result = voiceboard.run_initial_setup(startup_idea)
        
        print("\n✅ Research complete! Here are the critical personas who can evaluate your idea:")
        
        # In a real implementation, you'd parse the JSON result to show persona options
        # For now, we'll simulate the selection process
        print("\n👥 Available Personas:")
        print("1. Kevin O'Leary - Direct investor feedback")
        print("2. Barbara Corcoran - Market reality check") 
        print("3. Mark Cuban - Scalability challenges")
        
        # Get persona selection
        persona_choice = input("\n🎯 Select a persona (1-3): ")
        persona_map = {
            "1": "Kevin O'Leary",
            "2": "Barbara Corcoran", 
            "3": "Mark Cuban"
        }
        
        selected_persona = persona_map.get(persona_choice, "Kevin O'Leary")
        print(f"\n🗣️  You'll be talking to: {selected_persona}")
        
        # Start conversation loop
        conversation_history = ""
        
        while True:
            user_message = input(f"\n💬 Your message to {selected_persona} (or 'quit' to exit): ")
            
            if user_message.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thanks for using Voiceboard! Good luck with your startup!")
                break
                
            if not user_message.strip():
                continue
                
            print(f"\n⏳ {selected_persona} is thinking...")
            
            # Run conversation
            if not conversation_history:
                response = voiceboard.run_conversation(selected_persona, user_message)
            else:
                response = voiceboard.run_followup(selected_persona, user_message, conversation_history)
            
            print(f"\n🎙️  {selected_persona}: {response.raw}")
            
            # Update conversation history
            conversation_history += f"User: {user_message}\n{selected_persona}: {response.raw}\n"
            
    except Exception as e:
        raise Exception(f"An error occurred during interactive session: {e}")


def demo():
    """
    Run a demo conversation with preset messages.
    """
    startup_idea = "An AI-powered meal planning app that creates personalized recipes based on dietary restrictions and local ingredient availability"
    
    try:
        print("🎬 Running Voiceboard Demo...")
        print(f"💡 Demo Startup: {startup_idea}")
        print("\n" + "="*80 + "\n")
        
        voiceboard = Voiceboard()
        
        # Setup phase
        print("🔍 Phase 1: Finding critical personas...")
        setup_result = voiceboard.run_initial_setup(startup_idea)
        print("✅ Setup complete!\n")
        
        # Demo conversation
        selected_persona = "Kevin O'Leary"  # Simulated selection
        user_message = "I think this app could make millions by solving meal planning for busy families"
        
        print(f"🗣️  Demo conversation with {selected_persona}")
        print(f"👤 User: {user_message}")
        
        response = voiceboard.run_conversation(selected_persona, user_message)
        print(f"🎙️  {selected_persona}: {response.raw}")
        
        # Follow-up
        user_followup = "But I have a strong business model with subscription revenue and partnerships with grocery stores"
        print(f"\n👤 User: {user_followup}")
        
        conversation_history = f"User: {user_message}\n{selected_persona}: {response.raw}"
        followup_response = voiceboard.run_followup(selected_persona, user_followup, conversation_history)
        print(f"🎙️  {selected_persona}: {followup_response.raw}")
        
        print("\n🎬 Demo completed!")
        
    except Exception as e:
        raise Exception(f"An error occurred while running the demo: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    startup_idea = "An AI-powered productivity app that automatically schedules tasks based on priority and energy levels"
    
    inputs = {
        "startup_idea": startup_idea,
        'current_year': str(datetime.now().year)
    }
    
    try:
        n_iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 2
        filename = sys.argv[2] if len(sys.argv) > 2 else "voiceboard_training"
        
        print(f"🎓 Training Voiceboard crew for {n_iterations} iterations...")
        print(f"💾 Saving training data to: {filename}")
        
        Voiceboard().crew().train(n_iterations=n_iterations, filename=filename, inputs=inputs)
        
        print("✅ Training completed!")

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        task_id = sys.argv[1] if len(sys.argv) > 1 else None
        
        if not task_id:
            print("❌ Please provide a task ID to replay")
            print("Usage: python main.py replay <task_id>")
            return
            
        print(f"🔄 Replaying Voiceboard crew from task: {task_id}")
        
        Voiceboard().crew().replay(task_id=task_id)
        
        print("✅ Replay completed!")

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    startup_idea = "A blockchain-based social media platform that rewards users with cryptocurrency for quality content"
    
    inputs = {
        "startup_idea": startup_idea,
        "current_year": str(datetime.now().year)
    }
    
    try:
        n_iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 1
        eval_llm = sys.argv[2] if len(sys.argv) > 2 else "gpt-4"
        
        print(f"🧪 Testing Voiceboard crew with {n_iterations} iterations...")
        print(f"🤖 Using evaluation LLM: {eval_llm}")
        print(f"💡 Test Startup: {startup_idea}")
        
        Voiceboard().crew().test(n_iterations=n_iterations, eval_llm=eval_llm, inputs=inputs)
        
        print("✅ Testing completed!")

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "interactive":
            interactive()
        elif command == "demo":
            demo()
        elif command == "train":
            train()
        elif command == "replay":
            replay()
        elif command == "test":
            test()
        elif command == "run":
            run()
        else:
            print("❌ Unknown command. Available commands:")
            print("  python main.py run          - Run basic crew workflow")
            print("  python main.py interactive  - Interactive conversation session")
            print("  python main.py demo         - Run demonstration")
            print("  python main.py train <n> <filename> - Train the crew")
            print("  python main.py replay <task_id> - Replay from specific task")
            print("  python main.py test <n> <llm> - Test the crew")
    else:
        # Default to interactive mode
        interactive()