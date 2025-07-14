"""
This is a basic example of how to use the CUA model along with the Responses API.
The code will run a loop taking screenshots and perform actions suggested by the model.
Make sure to install the required packages before running the script.
"""

import argparse
import asyncio
import logging
import os
import sys

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import cua
import local_computer
import openai


async def main():

    # Parse args first to check debug flag
    parser = argparse.ArgumentParser()
    parser.add_argument("--instructions", dest="instructions",
        default="Open web browser and go to microsoft.com.",
        help="Instructions to follow")
    parser.add_argument("--model", dest="model",
        default="computer-use-preview")
    parser.add_argument("--endpoint", default="azure",
        help="The endpoint to use, either OpenAI or Azure OpenAI")
    parser.add_argument("--autoplay", dest="autoplay", action="store_true",
        default=True, help="Autoplay actions without confirmation")
    parser.add_argument("--environment", dest="environment", default="linux")
    parser.add_argument("--no-safety", dest="no_safety", action="store_true",
        default=False, help="Disable safety checks")
    parser.add_argument("--log-tokens", dest="log_tokens", action="store_true",
        default=False, help="Log token usage statistics")
    parser.add_argument("--debug", dest="debug", action="store_true",
        default=False, help="Enable debug logging")
    parser.add_argument("--resolution", dest="resolution", 
        default="1024x768", help="Screen resolution for AI model (e.g., 1024x768, 1280x1024, 1920x1080)")
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.WARNING, format="%(message)s")
    logger = logging.getLogger(__name__)
    
    # Set debug level if requested
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if args.endpoint == "azure":
        # Check for required environment variables
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        
        if not endpoint or not api_key:
            logger.error("Error: Missing Azure OpenAI credentials!")
            logger.error("")
            logger.error("Please set environment variables:")
            logger.error("  AZURE_OPENAI_ENDPOINT")
            logger.error("  AZURE_OPENAI_API_KEY")
            logger.error("")
            logger.error("You can:")
            logger.error("1. Set them in PowerShell:")
            logger.error('   $env:AZURE_OPENAI_ENDPOINT = "your-endpoint"')
            logger.error('   $env:AZURE_OPENAI_API_KEY = "your-api-key"')
            logger.error("")
            logger.error("2. Or create a .env file in this directory with:")
            logger.error("   AZURE_OPENAI_ENDPOINT=your-endpoint")
            logger.error("   AZURE_OPENAI_API_KEY=your-api-key")
            sys.exit(1)
        
        client = openai.AsyncAzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version="2025-03-01-preview",
        )
    else:
        if not os.environ.get("OPENAI_API_KEY"):
            logger.error("Error: Missing OPENAI_API_KEY environment variable!")
            sys.exit(1)
        client = openai.AsyncOpenAI()

    model = args.model

    # Computer is used to take screenshots and send keystrokes or mouse clicks
    computer = local_computer.LocalComputer()

    # Parse resolution
    try:
        width, height = map(int, args.resolution.split('x'))
        logger.info(f"Using resolution: {width}x{height}")
    except ValueError:
        logger.warning(f"Invalid resolution format: {args.resolution}. Using default 1024x768")
        width, height = 1024, 768

    # Scaler is used to resize the screen to a smaller size
    computer = cua.Scaler(computer, (width, height))

    # Agent to run the CUA model and keep track of state
    agent = cua.Agent(client, model, computer)

    # Get the user request
    if args.instructions:
        user_input = args.instructions
    else:
        user_input = input("Please enter the initial task: ")

    logger.info(f"User: {user_input}")
    agent.start_task()
    
    # Token usage tracking
    total_tokens = 0
    prompt_tokens = 0
    completion_tokens = 0
    
    while True:
        if not user_input and agent.requires_user_input:
            logger.info("")
            user_input = input("User: ")
        await agent.continue_task(user_input)
        user_input = ""
        
        # Token usage tracking
        if args.log_tokens:
            try:
                if hasattr(agent.response, 'usage') and agent.response.usage:
                    usage = agent.response.usage
                    
                    # Try to extract token count from various possible formats
                    current_tokens = 0
                    
                    # Check for tokens attribute (Azure OpenAI Responses API format)
                    if hasattr(usage, 'tokens'):
                        current_tokens = usage.tokens
                    # Check for total_tokens (standard OpenAI format)
                    elif hasattr(usage, 'total_tokens'):
                        current_tokens = usage.total_tokens
                    # Check if it's a dict-like object
                    elif hasattr(usage, '__dict__'):
                        usage_dict = usage.__dict__
                        current_tokens = usage_dict.get('tokens', 0) or usage_dict.get('total_tokens', 0)
                    
                    if current_tokens > 0:
                        total_tokens += current_tokens
                        logger.info(f"\n[Tokens] Current: {current_tokens} | Total session: {total_tokens}")
                    else:
                        # Log the usage object for debugging
                        logger.debug(f"Usage object: {usage}")
                        logger.debug(f"Usage type: {type(usage)}")
                        if hasattr(usage, '__dict__'):
                            logger.debug(f"Usage attributes: {usage.__dict__}")
                        # Also log the entire response for debugging
                        if args.debug and hasattr(agent.response, '__dict__'):
                            logger.debug(f"Full response attributes: {list(agent.response.__dict__.keys())}")
            except Exception as e:
                logger.debug(f"Error tracking tokens: {e}")
        
        # Safety checks handling
        if not args.no_safety:
            if agent.requires_consent and not args.autoplay:
                input("Press Enter to run computer tool...")
            elif agent.pending_safety_checks and not args.autoplay:
                logger.info(f"Safety checks: {agent.pending_safety_checks}")
                input("Press Enter to acknowledge and continue...")
        else:
            # Auto-acknowledge safety checks when --no-safety is used
            if agent.pending_safety_checks:
                logger.debug(f"Auto-acknowledging safety checks: {agent.pending_safety_checks}")
        if agent.reasoning_summary:
            logger.info("")
            logger.info(f"Action: {agent.reasoning_summary}")
        for action, action_args in agent.actions:
            logger.info(f"  {action} {action_args}")
        if agent.messages:
            logger.info("")
            logger.info(f"Agent: {"".join(agent.messages)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTask interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
