#!/usr/bin/env python
import sys
import os
from datetime import datetime
from voiceboard.crew import Voiceboard


def interactive():
    """
    Interactive startup evaluation session with critical business personas.
    """
    try:
        print("🎯 Welcome to Voiceboard - Get Critical Feedback on Your Startup!")
        print("="*65)
        
        # Get startup idea from user
        startup_idea = input("\n💡 Describe your startup idea: ")
        
        if not startup_idea.strip():
            print("❌ Please provide a startup idea to continue.")
            return
            
        print(f"\n🔍 Analyzing your idea: {startup_idea}")
        print("⏳ Finding critical personas and researching their voices...")
        
        # Initialize Voiceboard and run setup
        voiceboard = Voiceboard()
        setup_result = voiceboard.run_initial_setup(startup_idea)
        
        print("\n✅ Research complete! Here are critical personas who can evaluate your idea:")
        
        # Show available personas (in production, you'd parse the actual JSON results)
        print("\n👥 Available Critical Personas:")
        print("1. Kevin O'Leary - Direct, money-focused investor feedback")
        print("2. Barbara Corcoran - Market reality and execution challenges") 
        print("3. Mark Cuban - Scalability and competitive analysis")
        print("4. Reid Hoffman - Network effects and platform strategy")
        print("5. Sara Blakely - Customer validation and bootstrapping")
        
        # Get persona selection
        persona_choice = input("\n🎯 Select a persona (1-5): ")
        persona_map = {
            "1": "Kevin O'Leary",
            "2": "Barbara Corcoran", 
            "3": "Mark Cuban",
            "4": "Reid Hoffman",
            "5": "Sara Blakely"
        }
        
        selected_persona = persona_map.get(persona_choice, "Kevin O'Leary")
        print(f"\n🗣️  You're now talking to: {selected_persona}")
        print("💡 Tip: They will give you honest, critical feedback - not validation!")
        
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
            
            try:
                # Run conversation
                if not conversation_history:
                    response = voiceboard.run_conversation(
                        selected_persona_name=selected_persona, 
                        user_message=user_message,
                        startup_idea=startup_idea
                    )
                else:
                    response = voiceboard.run_followup(
                        selected_persona_name=selected_persona, 
                        user_response=user_message, 
                        conversation_history=conversation_history
                    )
                
                print(f"\n🎙️  {selected_persona}: {response.raw}")
                
                # Update conversation history
                conversation_history += f"User: {user_message}\n{selected_persona}: {response.raw}\n"
                
            except Exception as e:
                print(f"❌ Error during conversation: {e}")
                print("Let's try again...")
                continue
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        print("Please check your API keys and try again.")


def simple_test():
    """
    Test basic crew setup without running full workflow.
    """
    try:
        print("🧪 Testing Voiceboard setup...")
        
        # Check API key
        if not os.getenv('SERPER_API_KEY'):
            print("⚠️  Warning: SERPER_API_KEY not found in environment")
            print("   Set it in .env file or environment variables for full functionality")
        else:
            print("✅ SERPER_API_KEY found")
        
        # Test crew initialization
        voiceboard = Voiceboard()
        print("✅ Voiceboard crew initialized successfully!")
        
        # Test agent creation
        persona_agent = voiceboard.persona_identifier()
        print("✅ Persona identifier agent created!")
        
        voice_agent = voiceboard.voice_researcher()
        print("✅ Voice researcher agent created!")
        
        conversation_agent = voiceboard.persona_conversation_agent()
        print("✅ Conversation agent created!")
        
        print("\n🎉 All systems ready! Run 'python main.py' to start interactive session.")
        
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        import traceback
        traceback.print_exc()


def help_info():
    """
    Show help information about Voiceboard.
    """
    print("🎯 Voiceboard - Critical Startup Feedback Tool")
    print("="*50)
    print("\nVoiceboard helps entrepreneurs get honest, critical feedback on their")
    print("startup ideas by simulating conversations with tough business personas.")
    print("\nUsage:")
    print("  python main.py              - Start interactive session")
    print("  python main.py test          - Test system setup")
    print("  python main.py help          - Show this help")
    print("\nSetup:")
    print("  1. Get API key from serper.dev")
    print("  2. Add SERPER_API_KEY to .env file")
    print("  3. Run interactive session")
    print("\nFeatures:")
    print("  • Research critical business personas")
    print("  • Simulate authentic tough conversations")
    print("  • Get realistic feedback (not validation)")
    print("  • Challenge your assumptions")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ["test", "check"]:
            simple_test()
        elif command in ["help", "-h", "--help"]:
            help_info()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: test, help")
            print("Run without arguments for interactive session.")
    else:
        # Default to interactive mode
        interactive()